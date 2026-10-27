---
name: tonejs
description: "Interactive Web Audio framework for audio synthesis, sound effects, music scheduling, and offline stem rendering with Tone.js. Covers Tone.Synth, Tone.PolySynth, Tone.Sampler, Tone.Transport (BPM, timeline ticks, loops), audio effects (Reverb, FeedbackDelay, Distortion, Filter, Limiter), signal routing (connect, chain, fan), user gesture audio context unlocking, and Tone.Offline export for video sound tracks."
category: media
risk: safe
source: community
source_repo: "Tonejs/Tone.js"
author: "Tonejs"
tags: ["tonejs", "web-audio", "synthesizer", "audio-synthesis", "sound-effects", "generative-audio", "music-computation", "media"]
date_added: "2026-10-27"
---

# Tone.js — Interactive Web Audio & Sound Design Engine

Tone.js is a Web Audio framework for making interactive music, generative soundscapes, dynamic sound effects, and synthesized audio in the browser and programmatic video engines.

---

## 1. Quickstart: Synths, Effects & User Gesture Unlocking

Modern browsers require a user gesture (click, tap, keypress) to start the Web Audio Context:

```typescript
import * as Tone from 'tone';

export async function playChime() {
  // Unlock audio context on initial interaction
  await Tone.start();

  // Create polyphonic synth with studio reverb
  const reverb = new Tone.Reverb({ decay: 2.5, preDelay: 0.05 }).toDestination();
  await reverb.generate();

  const synth = new Tone.PolySynth(Tone.Synth, {
    oscillator: { type: 'triangle' },
    envelope: { attack: 0.02, decay: 0.4, sustain: 0.2, release: 1.0 },
  }).connect(reverb);

  // Trigger a major 7th chord
  synth.triggerAttackRelease(['C4', 'E4', 'G4', 'B4'], '1n');
}
```

---

## 2. Musical Timeline Scheduling with `Tone.Transport`

`Tone.Transport` manages musical time (Bars:Beats:Sixteenths), tempo (BPM), and precise event scheduling:

```typescript
import * as Tone from 'tone';

export function startLoFiBeat() {
  Tone.Transport.bpm.value = 85;

  // Bass synth
  const bass = new Tone.MonoSynth({
    oscillator: { type: 'sawtooth' },
    filter: { Q: 2, type: 'lowpass', rolloff: -24 },
    filterEnvelope: { attack: 0.01, decay: 0.2, sustain: 0.1, release: 0.5, baseFrequency: 100, octaves: 2.5 },
  }).toDestination();

  // Schedule a repeating 2-bar bassline loop
  const loop = new Tone.Loop((time) => {
    bass.triggerAttackRelease('C2', '8n', time);
    bass.triggerAttackRelease('Eb2', '8n', time + Tone.Time('4n').toSeconds());
    bass.triggerAttackRelease('G2', '8n', time + Tone.Time('2n').toSeconds());
    bass.triggerAttackRelease('Bb1', '8n', time + Tone.Time('2n + 4n').toSeconds());
  }, '2m');

  loop.start(0);
  Tone.Transport.start();

  return () => {
    Tone.Transport.stop();
    loop.dispose();
    bass.dispose();
  };
}
```

---

## 3. UI Micro-Interactions & SFX (Clicks, Pops, Success)

```typescript
import * as Tone from 'tone';

export const SFX = {
  // Subtle click for buttons
  click: () => {
    const clickSynth = new Tone.MembraneSynth({
      pitchDecay: 0.008,
      octaves: 2,
      envelope: { attack: 0.001, decay: 0.05, sustain: 0 },
    }).toDestination();
    clickSynth.triggerAttackRelease('G5', '32n');
  },

  // Uplifting chime for success events
  success: () => {
    const chime = new Tone.Synth({
      oscillator: { type: 'sine' },
      envelope: { attack: 0.01, decay: 0.3, sustain: 0.1, release: 0.8 },
    }).toDestination();

    const now = Tone.now();
    chime.triggerAttackRelease('E5', '16n', now);
    chime.triggerAttackRelease('G#5', '16n', now + 0.1);
    chime.triggerAttackRelease('B5', '8n', now + 0.2);
  },
};
```

---

## 4. Offline Audio Stem Rendering (`Tone.Offline`)

Render synthesized audio tracks headlessly to a raw audio buffer without real-time playback (ideal for Remotion video export or saving `.wav` files):

```typescript
import * as Tone from 'tone';

export async function renderOfflineAudioTrack(durationSeconds: number): Promise<AudioBuffer> {
  const buffer = await Tone.Offline(({ transport }) => {
    const synth = new Tone.Synth().toDestination();
    synth.triggerAttackRelease('C4', '2n', 0.5);
    synth.triggerAttackRelease('G4', '2n', 1.5);
    synth.triggerAttackRelease('C5', '1n', 2.5);
  }, durationSeconds);

  return buffer; // Export to WAV or feed into WebCodecs/FFmpeg
}
```

---

## 5. Critical Rules & Audio Performance Checklist

- **Dispose Synths When Done**: Always call `.dispose()` on synths, effects, and loops when components unmount to avoid AudioNode memory leaks.
- **Never Run Multiple Unsynced Transports**: Keep `Tone.Transport` as the single source of truth for global tempo and musical time.
- **Limit Voices on PolySynth**: By default, `PolySynth` creates voices dynamically. For performance on mobile, set `maxPolyphony: 6`.
