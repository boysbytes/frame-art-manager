#!/usr/bin/env python3
"""
Samsung Frame TV TCP upload relay for frame-art-manager.html

The browser cannot open raw TCP sockets, so this relay bridges the gap.
It accepts a WebSocket connection from the browser, receives the target
{ip, port} and the binary image frame, then forwards the frame to the
TV over a raw TCP socket — exactly as the samsung-tv-ws-api library does.

Requirements:
    pip install websockets

Usage:
    python relay.py

Leave it running while you use frame-art-manager.html.  The app will
automatically detect and use the relay when uploading images.
"""

import asyncio
import json
import socket
import ssl
import sys

try:
    import websockets
except ImportError:
    sys.exit("websockets package not found. Run: pip install websockets")

RELAY_PORT = 8765
RELAY_HOST = "localhost"


async def handler(websocket):
    try:
        # First message: JSON object { ip, port, secured }
        target_str = await asyncio.wait_for(websocket.recv(), timeout=10)
        target = json.loads(target_str)
        ip = target["ip"]
        port = int(target["port"])
        secured = bool(target.get("secured", False))

        # Second message: raw binary frame
        frame = await asyncio.wait_for(websocket.recv(), timeout=30)
        if isinstance(frame, str):
            frame = frame.encode("latin-1")

        print(f"Relaying {len(frame):,} bytes → {ip}:{port} (TLS={secured})")

        # Forward over raw TCP (optionally TLS-wrapped)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _send_tcp, ip, port, secured, frame)

        await websocket.send("ok")
        print("  Done.")

    except Exception as exc:
        msg = f"error: {exc}"
        print(f"  {msg}")
        try:
            await websocket.send(msg)
        except Exception:
            pass


def _send_tcp(ip, port, secured, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(15)
    try:
        if secured:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            sock = ctx.wrap_socket(sock, server_hostname=ip)
        sock.connect((ip, port))
        sock.sendall(data)
    finally:
        sock.close()


async def main():
    print(f"Samsung Frame TV relay listening on ws://{RELAY_HOST}:{RELAY_PORT}")
    print("Keep this running while uploading from frame-art-manager.html")
    print("Press Ctrl+C to stop.\n")

    # Allow connections from the browser (same machine only).
    # max_size is raised well above the 3840×2160 JPEG worst-case (~8 MB).
    async with websockets.serve(handler, RELAY_HOST, RELAY_PORT, max_size=16 * 1024 * 1024):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nRelay stopped.")
