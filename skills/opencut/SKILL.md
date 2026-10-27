---
name: opencut
description: "Open-source programmatic video editing and timeline composition with OpenCut. Covers timeline data models (tracks, clips, transitions, keyframes, effects, audio waveforms), WebCodecs hardware-accelerated video decoding/encoding, non-destructive editing, timeline serialization (JSON EDL / OpenTimelineIO), project file parsing, asset management, and browser-based rendering pipelines."
category: video
risk: safe
source: community
source_repo: "OpenCut-app/OpenCut"
author: "OpenCut-app"
tags: ["opencut", "video-editor", "timeline-editing", "webcodecs", "video-pipeline", "clip-composition", "video"]
date_added: "2026-10-27"
---

# OpenCut — Programmatic Timeline Video Editing Engine

OpenCut is an open-source, web-based video editing engine designed for timeline-driven video manipulation. It provides a non-destructive editing architecture powered by WebCodecs, WebGL/WebGPU compositing, and programmatic JSON Edit Decision Lists (EDL).

---

## 1. Timeline Data Model & Architecture

```
+-----------------------------------------------------------+
|                      OpenCut Project                      |
| (Resolution: 1920x1080, FPS: 30/60, Timebase: Microseconds) |
+-----------------------------------------------------------+
                              |
             +----------------+----------------+
             |                                 |
     [Video Track Layer]               [Audio Track Layer]
             |                                 |
     +-------+-------+                 +-------+-------+
     |               |                 |               |
 [Clip A]        [Clip B]          [Voiceover]     [Music Track]
 (Start, Trim,   (Keyframes,       (Gain, Fade,    (Looping, Duck)
  Transform)      Transition)       Pan)
```

---

## 2. Programmatic Timeline Definition (JSON EDL)

AI agents can construct and serialize complete video compositions programmatically:

```typescript
export interface TimelineTrack {
  id: string;
  type: 'video' | 'audio' | 'overlay';
  clips: TimelineClip[];
}

export interface TimelineClip {
  id: string;
  sourceUrl: string;
  startInTimeline: number; // in seconds
  duration: number;        // in seconds
  sourceTrimStart: number; // in seconds
  volume?: number;
  transform?: {
    x: number;
    y: number;
    scale: number;
    opacity: number;
  };
  transitions?: {
    in?: { type: 'crossfade' | 'slide' | 'wipe'; duration: number };
    out?: { type: 'crossfade' | 'slide' | 'wipe'; duration: number };
  };
}

export const sampleProjectManifest = {
  version: '1.0',
  canvas: { width: 1920, height: 1080, fps: 30 },
  tracks: [
    {
      id: 'track-v1',
      type: 'video',
      clips: [
        {
          id: 'clip-intro',
          sourceUrl: '/assets/footage/intro.mp4',
          startInTimeline: 0,
          duration: 4.5,
          sourceTrimStart: 0,
        },
        {
          id: 'clip-demo',
          sourceUrl: '/assets/footage/demo_screen.mp4',
          startInTimeline: 4.5,
          duration: 12.0,
          sourceTrimStart: 2.0,
        },
      ],
    },
    {
      id: 'track-a1',
      type: 'audio',
      clips: [
        {
          id: 'clip-voice',
          sourceUrl: '/assets/audio/voiceover.wav',
          startInTimeline: 0.5,
          duration: 15.0,
          sourceTrimStart: 0,
          volume: 1.0,
        },
      ],
    },
  ],
};
```

---

## 3. WebCodecs Hardware-Accelerated Video Rendering Pipeline

OpenCut leverages modern browser WebCodecs (`VideoDecoder` and `VideoEncoder`) for zero-lag frame extraction:

```typescript
export class FrameExtractor {
  private decoder: VideoDecoder;

  constructor(onFrame: (frame: VideoFrame) => void) {
    this.decoder = new VideoDecoder({
      output: (frame) => onFrame(frame),
      error: (e) => console.error('WebCodecs Decoder Error:', e),
    });
  }

  configure(codec = 'avc1.42E01E', width = 1920, height = 1080) {
    this.decoder.configure({
      codec,
      codedWidth: width,
      codedHeight: height,
      hardwareAcceleration: 'prefer-hardware',
    });
  }
}
```

---

## 4. Integration Recipes

- **With FFmpeg**: Export project timeline manifests as EDL / FCPXML / OTIO and render with FFmpeg for server-side exports.
- **With Remotion**: Convert OpenCut timeline clips into Remotion `<Series>` and `<Sequence>` components.
- **With faster-whisper & Chatterbox**: Align generated transcriptions and voiceovers directly into audio and subtitle tracks on the timeline.

---

## 5. Critical Rules & Performance Checklist

- **Non-Destructive Trimming**: Never truncate source assets; maintain separate `startInTimeline` and `sourceTrimStart` timestamps.
- **Always Close `VideoFrame` Objects**: WebCodecs `VideoFrame` allocations live in GPU memory. Call `frame.close()` as soon as the frame is drawn to canvas to prevent browser OOM crashes.
- **Prefer Standard Timebases**: Store internal timestamps in integer microseconds (or exact frame numbers) to prevent floating-point precision drift across long multi-hour timelines.
