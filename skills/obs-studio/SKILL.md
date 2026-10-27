---
name: obs-studio
description: "OBS Studio automation, programmatic screen capture, and recording pipelines via OBS WebSocket v5 and CLI. Covers obs-websocket-js API client, automated scene switching, source configuration (window capture, display capture, browser source, audio input/output), recording lifecycle (start/stop/pause recording, replay buffer), virtual camera streaming, headless video capture, and automated software walkthrough demos for AI coding agents."
category: media
risk: safe
source: community
source_repo: "obsproject/obs-studio"
author: "obsproject"
tags: ["obs-studio", "screen-capture", "obs-websocket", "video-recording", "streaming", "automation", "media"]
date_added: "2026-10-27"
---

# OBS Studio — Screen Capture & Recording Automation

OBS Studio is the premier open-source video recording and live streaming application. Through **OBS WebSocket v5** and headless CLI scripting, AI agents can programmatically control scenes, switch sources, trigger hardware-accelerated recordings, capture application windows, and automate software walkthrough demos.

---

## 1. OBS WebSocket v5 Connection Setup

OBS Studio 28+ ships with native WebSocket v5 support out-of-the-box (default port: `4455`).

```typescript
import { OBSWebSocket } from 'obs-websocket-js';

export async function connectToOBS(address = 'ws://127.0.0.1:4455', password?: string) {
  const obs = new OBSWebSocket();

  try {
    const { obsWebSocketVersion, negotiatedRpcVersion } = await obs.connect(address, password);
    console.log(`✓ Connected to OBS Studio (WebSocket v${obsWebSocketVersion}, RPC v${negotiatedRpcVersion})`);
    return obs;
  } catch (error) {
    console.error('Failed to connect to OBS WebSocket. Ensure OBS is running and WebSocket is enabled in Tools -> WebSocket Server Settings.', error);
    throw error;
  }
}
```

---

## 2. Automated Programmatic Recording Workflow

```typescript
import { OBSWebSocket } from 'obs-websocket-js';

export async function recordDemoSequence(obs: OBSWebSocket, sceneName: string, durationSeconds: number) {
  // 1. Verify target scene exists and switch to it
  await obs.call('SetCurrentProgramScene', { sceneName });

  // 2. Start hardware-accelerated video recording
  await obs.call('StartRecord');
  console.log(`🎬 Recording started on scene: ${sceneName}`);

  // 3. Wait for demo sequence duration
  await new Promise((resolve) => setTimeout(resolve, durationSeconds * 1000));

  // 4. Stop recording and retrieve output file path
  const response = await obs.call('StopRecord');
  console.log(`✓ Recording complete. Output video saved to: ${response.outputPath}`);

  return response.outputPath;
}
```

---

## 3. Dynamic Scene & Source Manipulation

```typescript
import { OBSWebSocket } from 'obs-websocket-js';

export async function configureBrowserSource(
  obs: OBSWebSocket,
  sceneName: string,
  sourceName: string,
  url: string,
  width = 1920,
  height = 1080
) {
  // Create or update Browser Source (e.g. for HTML-rendered overlays / Remotion previews)
  await obs.call('SetInputSettings', {
    inputName: sourceName,
    inputSettings: {
      url,
      width,
      height,
      reroute_audio: true,
      restart_when_active: true,
    },
  });

  // Take a real-time high-res screenshot of the scene
  const screenshot = await obs.call('GetSourceScreenshot', {
    sourceName: sceneName,
    imageFormat: 'png',
    imageWidth: 1920,
    imageHeight: 1080,
  });

  return screenshot.imageData; // Base64 encoded PNG
}
```

---

## 4. Headless OBS Launch via CLI

For unattended CI/CD test runners or automated agent demo production:

```bash
# macOS
/Applications/OBS.app/Contents/MacOS/OBS --startrecording --minimize-to-tray &

# Linux (with virtual frame buffer)
xvfb-run --auto-servernum obs --startrecording --minimize-to-tray &

# Windows (PowerShell)
Start-Process "C:\Program Files\obs-studio\bin\64bit\obs64.exe" -ArgumentList "--startrecording", "--minimize-to-tray"
```

---

## 5. Critical Rules & Automation Checklist

- **Use Atomic Async Calls**: Always `await` OBS WebSocket requests. Do not fire `StopRecord` immediately after `StartRecord` without confirming recording state; check `GetRecordStatus`.
- **Set Up Lossless / High-Bitrate Profiles**: Ensure OBS Settings -> Output is configured to NVENC / Apple Silicon hardware encoding with Constant Rate Factor (CRF 18-20) or CBR 15,000 kbps for crisp code text capture.
- **Always Disconnect on Process Exit**: Call `await obs.disconnect()` to cleanly unbind the WebSocket connection.
