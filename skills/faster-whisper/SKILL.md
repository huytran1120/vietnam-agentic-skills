---
name: faster-whisper
description: "High-performance speech-to-text transcription and subtitle generation using faster-whisper (CTranslate2). Up to 4x faster than OpenAI Whisper with lower VRAM consumption. Covers model selection (tiny, base, small, medium, large-v3), Silero VAD speech filtering, word-level timestamps (word_timestamps=True), automated SRT/VTT subtitle export, multi-language translation, and batch audio/video transcription pipelines."
category: voice-agents
risk: safe
source: community
source_repo: "SYSTRAN/faster-whisper"
author: "SYSTRAN"
tags: ["faster-whisper", "whisper", "speech-to-text", "transcription", "ctranslate2", "subtitles", "captions", "srt", "vtt", "voice-agents"]
date_added: "2026-10-27"
---

# faster-whisper — High-Speed Speech Transcription & Subtitles

`faster-whisper` is a reimplementation of OpenAI's Whisper model using CTranslate2, a fast inference engine for Transformer models. It delivers up to **4x faster transcription speed** with significant reductions in memory and VRAM usage on both GPU and CPU.

---

## 1. Quickstart: Python Transcription Script

```python
from faster_whisper import WhisperModel
import json

def transcribe_media(audio_file_path: str, model_size="small", device="auto", compute_type="auto"):
    """
    Transcribe audio/video file with word-level timestamps and Silero VAD filtering.
    """
    # Initialize model (auto detects CUDA, Apple Silicon MPS or CPU with int8 quantization)
    model = WhisperModel(model_size, device=device, compute_type=compute_type)

    segments, info = model.transcribe(
        audio_file_path,
        beam_size=5,
        vad_filter=True,                # Filter out silence and background noise
        vad_parameters=dict(min_silence_duration_ms=500),
        word_timestamps=True            # Capture start and end time for every single word
    )

    print(f"Detected language: '{info.language}' with probability {info.language_probability:.2f}")

    results = []
    for segment in segments:
        segment_data = {
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip(),
            "words": [
                {"word": w.word, "start": w.start, "end": w.end, "probability": w.probability}
                for w in (segment.words or [])
            ]
        }
        results.append(segment_data)
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

    return results
```

---

## 2. Generating Standard Subtitle Formats (SRT & VTT)

```python
def format_timestamp_srt(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

def export_srt(segments, srt_output_path: str):
    with open(srt_output_path, "w", encoding="utf-8") as f:
        for idx, segment in enumerate(segments, start=1):
            start = format_timestamp_srt(segment["start"])
            end = format_timestamp_srt(segment["end"])
            f.write(f"{idx}\n{start} --> {end}\n{segment['text']}\n\n")
    print(f"✓ SRT subtitles exported to: {srt_output_path}")
```

---

## 3. CLI Command-Line Usage

```bash
# Transcribe video directly and produce SRT
python -m faster_whisper.cli \
  --model small \
  --device auto \
  --output_format srt \
  --output_dir ./subtitles \
  ./video_clip.mp4

# Translate foreign speech directly into English subtitles
python -m faster_whisper.cli \
  --model medium \
  --task translate \
  --output_format vtt \
  ./vietnamese_speech.mp3
```

---

## 4. Model Selection & Hardware Matrix

| Model | Memory (VRAM / RAM) | Speed Multiplier | Typical Accuracy / Use Case |
| :--- | :---: | :---: | :--- |
| **`tiny`** | ~500 MB | ~15x | Fast draft, command parsing, noisy environments |
| **`base`** | ~1 GB | ~10x | Real-time voice commands, UI dictation |
| **`small`** | ~2 GB | ~6x | **Recommended default**: High accuracy, fast speed |
| **`medium`** | ~5 GB | ~3x | Multi-speaker podcasts, technical jargon |
| **`large-v3`** | ~10 GB | ~1x | Broadcast publishing, multilingual dialect nuance |

---

## 5. Critical Rules & Audio Pipeline Tips

- **Always Enable `vad_filter=True`**: Silero VAD prevents Whisper from hallucinating phantom loops during prolonged silences or background music segments.
- **Set `compute_type="int8"` on CPU**: On machines without NVIDIA GPUs (including Apple Silicon CPU fallback), `int8` quantization delivers a 2x-3x speedup with almost zero perceptible accuracy loss.
- **Direct Video Ingestion**: You do not need to extract audio separately with FFmpeg first; `faster-whisper` decodes MP4, MOV, MKV, WAV, and MP3 files directly via PyAV.
