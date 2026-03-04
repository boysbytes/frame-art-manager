---
title: "Samsung Frame TV Art Manager"
description: "Lightweight web app for preparing and uploading images to a Samsung Frame TV over its websocket API."
target_audience: "Frame TV owners who want a simple tool to manage their art collection without needing a server or complex setup."
---

# Frame TV Art Manager

This folder contains the source for a simple, client‑side web app that helps you prepare and upload images to a Samsung Frame TV. The app runs entirely in the browser.

Use it to:

- drag & drop photos, crop/scale them to 3840×2160 canvas size
- pair portrait shots side‑by‑side automatically or manually
- download processed images as a ZIP archive
- upload images directly to your Frame TV with optional matte/style settings
- inspect and delete items already stored on the television
- adjust slideshow interval and auto‑activate Art Mode after uploads

Everything is stored locally (settings, pairing token, upload history) so nothing leaves your machine.

---

## Getting started

1. Open `frame-art-manager.html` in a modern browser on the same network as your Frame TV.
2. If this is your first time connecting, follow the one‑time setup below to trust the TV's certificate and pair the app.
3. Drag images onto the **Source Images** area or click to browse.
4. When ready, click **Process Images**, then either download them or upload to the TV (after connecting).

> ℹ️ The app works offline except for TV communication. You can prepare files anywhere and upload later once you have network access.

### One‑time setup

The TV uses a self‑signed SSL certificate so browsers block the WebSocket unless you manually trust it:

1. Enter the TV IP in the **TV IP Address** field and click **① Trust
   certificate**. A new tab opens at `https://<TV_IP>:8002`.
2. Choose **Advanced → Proceed** to accept the warning.
3. Return to the original tab and click **Connect**. Authorise the pairing
   prompt on the TV. A token is stored for future sessions.

---

## Features

- **Image processing** – scales and crops images to fit the Frame's 16:9 canvas. Portraits can be paired side‑by‑side.
- **Batch upload** with progress logging, matte selection, and optional auto‑enable Art Mode.
- **Library view** – list current content on the TV, filter by yours vs. Samsung's, and delete selected items.
- **Settings** – control matte style/colour, slideshow timing, and clear stored data or remote images.
- **Local storage** – settings and upload history persist between sessions.

### Deleting remote images

Use the **Delete from TV** button in the Settings tab. It requires an active
connection and will remove all your `MY-` content IDs from the TV. A separate
button wipes all local app data (settings + token).

---

## Development notes

The entire application is a single HTML file (`frame-art-manager.html`) with embedded CSS and JavaScript. It was built for ease of use rather than modularity – feel free to extract modules if you spin it into a larger project.

A sequence diagram (`communication-flow.excalidraw`) illustrates the communication between the web client and the TV. Open it using [Excalidraw] by dragging the file onto the canvas.

> 🛠 This code is stored in personal notes; adapt freely but be mindful that the
> TV protocol is not officially supported and may change with firmware updates.

> 📌 **Note:** The core art‑upload and management logic was inspired by the
> [samsung-tv-ws-api](https://github.com/NickWaterton/samsung-tv-ws-api) Python
> library, which implements the same `com.samsung.art-app` protocol for Frame
> TVs.
---

## Troubleshooting

- **WebSocket errors** usually mean the certificate isn't trusted or the IP is
  wrong. Re‑visit the **Trust certificate** step.
- **Uploads fail** if the TV disconnects or you hit throttling; retry after a
  short delay.
- **Images look cropped** – the app maintains the 16:9 ratio by cropping the
  longer dimension. Pair portraits for a better fit.

---

## File overview

| File | Purpose |
|------|---------|
| `frame-art-manager.html` | The working web application |
| `communication-flow.excalidraw` | Visual sequence diagram of the app–TV
|  | interaction |


[Excalidraw]: https://excalidraw.com

[api]: https://github.com/NickWaterton/samsung-tv-ws-api
