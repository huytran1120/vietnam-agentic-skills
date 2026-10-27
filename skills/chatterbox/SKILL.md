---
name: chatterbox
description: "Open-source neural voiceover and voice cloning synthesis by Resemble AI. Covers Chatterbox local TTS pipelines, zero-shot voice cloning from reference audio clips, emotional expressiveness conditioning, phoneme timestamp alignment, audio chunk streaming, batch narration generation, and seamless audio track export for AI video creation pipelines (Remotion, FFmpeg)."
category: voice-agents
risk: safe
source: community
source_repo: "resemble-ai/chatterbox"
author: "resemble-ai"
tags: ["chatterbox", "voiceover", "text-to-speech", "voice-cloning", "tts", "neural-audio", "audio-generation", "voice-agents", "resemble-ai"]
date_added: "2026-10-27"
---

# Chatterbox — Neural Voiceover & Voice Cloning Engine

Chatterbox is Resemble AI's open-source neural text-to-speech (TTS) and voice cloning toolkit. It enables AI agents to generate high-fidelity spoken voiceovers, clone voices from short reference audio samples, inject emotional conditioning, and export time-aligned narration tracks for programmatic video rendering.

---

## 1. Quickstart: Python Inference Pipeline

```python
import torch
import torchaudio
from chatterbox import ChatterboxTTS

def generate_voiceover(text: str, speaker_wav_path: str, output_path: str):
    """
    Synthesize natural voiceover cloned from a reference speaker audio clip.
    """
    device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Loading Chatterbox model on {device}...")

    model = ChatterboxTTS.from_pretrained("resemble-ai/chatterbox-base").to(device)

    # 1. Extract speaker voice embedding from reference audio (3-10 seconds clean sample)
    speaker_embedding = model.extract_speaker_embedding(speaker_wav_path)

    # 2. Synthesize speech with prosody control
    wav, sample_rate, word_timestamps = model.synthesize(
        text=text,
        speaker_embedding=speaker_embedding,
        temperature=0.7,        # Prosody variation (0.5 = robotic/stable, 0.9 = expressive)
        speed=1.0,              # Speech tempo rate
        return_timestamps=True  # Enables automatic subtitle / caption sync
    )

    # 3. Save output WAV
    torchaudio.save(output_path, wav.cpu(), sample_rate)
    print(f"✓ Voiceover rendered to: {output_path} ({len(word_timestamps)} words mapped)")

    return {
        "audio_path": output_path,
        "sample_rate": sample_rate,
        "timestamps": word_timestamps
    }
```

---

## 2. CLI Batch Voiceover Generation

```bash
# Basic voice synthesis with reference voice
python -m chatterbox.cli \
  --text "Welcome to Vietnam Agentic Skills, the universal catalog for AI coding agents." \
  --voice-reference ./voices/narrator_studio.wav \
  --output ./build/audio/intro_voiceover.wav

# Synthesis with JSON subtitle timing dump
python -m chatterbox.cli \
  --script-file ./narration_script.txt \
  --voice-reference ./voices/narrator_studio.wav \
  --export-subtitles ./build/audio/subtitles.json \
  --output ./build/audio/full_narration.wav
```

---

## 3. Integration with Remotion & FFmpeg Pipelines

Once Chatterbox generates the `.wav` file and word timestamps, ingest it into Remotion or combine via FFmpeg:

```bash
# Mux voiceover audio with video, ducking background music
ffmpeg -i video_without_audio.mp4 -i voiceover.wav \
  -c:v copy -c:a aac -b:a 192k \
  -shortest output_with_voice.mp4
```

```tsx
// Inside Remotion composition:
import { Audio, staticFile } from 'remotion';

export const VideoVoiceoverTrack: React.FC = () => {
  return (
    <Audio
      src={staticFile('audio/intro_voiceover.wav')}
      volume={1.0}
    />
  );
};
```

---

## 4. Best Practices & Audio Quality Checklist

- **Reference Audio Quality**: For best cloning fidelity, supply 5 to 15 seconds of clean, dry vocal audio with zero background music, zero reverb, and 24kHz or 48kHz sample rate.
- **Normalize Audio Levels**: Run output files through EBU R128 loudness normalization (`-14 LUFS` to `-16 LUFS`) for modern web and mobile playback.
- **Phoneme Alignment**: Use the returned `word_timestamps` to trigger animated captions or on-screen kinetic typography perfectly synced with the voice.
