# Running Agents with Local Models

This guide covers running Google Antigravity agents entirely on-device using
local models. Local execution does not require an API key or cloud connectivity.

There are two configuration classes for local model execution:

| Config Class | Backend | Auth Required | Execution Mode | Use Case |
|---|---|---|---|---|
| `LiteRTAgentConfig` | Local LiteRT-LM | None | Managed On-Device | High-performance on-device execution via LiteRT runtime (e.g., Gemma 4 26B) |
| `LocalOpenAIAgentConfig` | External OpenAI-compat server | None | External Server | Connecting to external local servers (Ollama, LM Studio, etc.) |

## LiteRTAgentConfig

`LiteRTAgentConfig` runs local models using Google's LiteRT runtime. When
the agent starts, it spins up a local OpenAI-compatible loopback HTTP server
backed by the model checkpoint. All inference and tool execution happen
on-device with zero cloud network latency and zero cost.

### Quick Setup: Installing Gemma 4 26B

Install the dependencies and import the 26B Gemma 4 checkpoint using the
`litert-lm` CLI:

```bash
pip install google-antigravity litert-lm
litert-lm import \
  --from-huggingface-repo=litert-community/gemma-4-26B-A4B-it-litert-lm \
  gemma-4-26B-A4B-it-web.litertlm \
  gemma4-26b
```

This downloads approximately **16.8 GB** and registers the checkpoint at
`~/.litert-lm/models/gemma4-26b/model.litertlm`. A device with **24 GB+ VRAM
or unified memory** is recommended for running the 26B model.

*(Tip: On macOS, if the import fails with an SSL verification error, install `certifi` and run `export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")` before retrying).*

### Import

```python
from google.antigravity import Agent, LiteRTAgentConfig, LiteRTBackend
```

### Key Parameters

- `model_path` (str, **required**): Absolute path to a `.litertlm` model file.
  Tilde (`~`) is **not** expanded automatically — use `os.path.expanduser()` in
  Python or pass the full absolute path.
- `backend` (`'gpu'` | `'npu'`, default `'gpu'`): Hardware backend for
  inference. Use `LiteRTBackend.GPU` or `LiteRTBackend.NPU`.
- `compaction_config` (`CompactionConfig` | None, default None): Configure
  context compaction. By default, `LiteRTAgentConfig` automatically configures
  a derived compaction threshold (`token_threshold=40960`) tailored for the
  LiteRT engine's 64k KV-cache capacity (`65536` tokens).
- `capabilities` (`CapabilitiesConfig` | None, default None): Configure agent
  capabilities (subagents, tool allowlists, behavior mode).
- `enable_speculative_decoding` (bool, default False): Enable multi-token
  prediction for faster generation.
- `cache_dir` (str | None): Directory for compilation caching. Speeds up
  subsequent launches.
- `audio_backend` / `vision_backend`: Override the hardware backend for
  multimodal (audio / vision) processing.
- `port` (int, default 0): Port for the local loopback server. `0` selects a
  random available port.
- `download_if_missing` (bool, default False): Automatically download model
  weights if the `model_path` does not exist.

All standard `AgentConfig` parameters are also supported: `system_instructions`,
`capabilities`, `tools`, `policies`, `hooks`, `triggers`, `mcp_servers`,
`subagents`, `workspaces`, etc.

### Canonical Example

`LiteRTAgentConfig` automatically applies the lightweight preset upon
instantiation—minimizing prompt overhead, restricting tools to core coding
capabilities, disabling subagents, and configuring context compaction:

```python
import asyncio
import os

from google.antigravity import Agent, LiteRTAgentConfig
from google.antigravity.hooks import policy


async def main():
    model_path = os.path.expanduser(
        "~/.litert-lm/models/gemma4-26b/model.litertlm"
    )

    config = LiteRTAgentConfig(
        model_path=model_path,
        # Auto-allows shell commands (run_command) without interactive confirmation:
        policies=[policy.allow_all()],
    )

    async with Agent(config=config) as agent:
        response = await agent.chat("Explain Python generators.")
        async for token in response:
            print(token, end="", flush=True)
        print()


if __name__ == "__main__":
    asyncio.run(main())
```

### Speculative Decoding

Enable multi-token prediction for faster inference:

```python
config = LiteRTAgentConfig(
    model_path=os.path.expanduser(
        "~/.litert-lm/models/gemma4-26b/model.litertlm"
    ),
    enable_speculative_decoding=True,
)
```

---

## LocalOpenAIAgentConfig

`LocalOpenAIAgentConfig` connects to any locally running OpenAI-compatible API
server, such as [Ollama](https://ollama.com) or
[LM Studio](https://lmstudio.ai).

> [!WARNING]
> Do **not** use `LocalOpenAIAgentConfig` to connect to `litert-lm serve`.
> Use `LiteRTAgentConfig` instead — it manages the LiteRT server lifecycle
> automatically. `LocalOpenAIAgentConfig` is only for external servers like
> Ollama or LM Studio that you start and manage independently.

### Import

```python
from google.antigravity import Agent, LocalOpenAIAgentConfig
```

### Key Parameters

- `model` (str | ModelTarget | None): The model identifier as recognized by the
  local server (e.g., `"llama3"`, `"gemma:7b"`).
- `base_url` (str | None): URL of the local server's OpenAI-compatible endpoint
  (e.g., `"http://localhost:11434/v1"` for Ollama).

All standard `AgentConfig` parameters are also supported: `system_instructions`,
`capabilities`, `tools`, `policies`, `hooks`, `triggers`, `mcp_servers`,
`subagents`, `workspaces`, etc.

### Example with Ollama

Start Ollama and pull the model (e.g. `ollama pull gemma4:26b`), then create an
agent using `.lightweight()` for optimized prompt overhead and core coding
tools:

```python
import asyncio
from google.antigravity import Agent, LocalOpenAIAgentConfig


async def main():
  config = LocalOpenAIAgentConfig(
      model="gemma4:26b",
      base_url="http://localhost:11434/v1",
  ).lightweight()
  async with Agent(config=config) as agent:
    response = await agent.chat("What is the capital of France?")
    print(await response.text())


if __name__ == "__main__":
  asyncio.run(main())
```

### Example with LM Studio

```python
import asyncio
from google.antigravity import Agent, LocalOpenAIAgentConfig


async def main():
  config = LocalOpenAIAgentConfig(
      model="gemma-4-26B-A4B-it",
      base_url="http://localhost:1234/v1",
  ).lightweight()
  async with Agent(config=config) as agent:
    response = await agent.chat("Summarize this document.")
    print(await response.text())


if __name__ == "__main__":
  asyncio.run(main())
```

---

## Hardware & Platform Requirements

GPU detection is automatic. The SDK checks for available hardware acceleration
at startup and selects the appropriate backend. The detection logic is:

- **macOS**: Checks for Apple Silicon (`hw.optional.arm64`) → uses **Metal** via the `'gpu'` backend.
- **Linux**: Checks for `nvidia-smi` and CUDA libraries (`libcuda.so`) → uses **CUDA** via the `'gpu'` backend.
- **Windows**: Checks for `nvidia-smi` and CUDA libraries (`nvcuda.dll`). The LiteRT runtime also requires DirectX Shader Compiler components for GPU inference via WebGPU/Dawn.
- **NPU**: Available via `backend='npu'` where compatible hardware and drivers are present.

### Decision Table

| Your Environment | Suggested Config | Backend |
|---|---|---|
| macOS + Apple Silicon | `LiteRTAgentConfig` | `'gpu'` (Metal) |
| Linux + NVIDIA GPU | `LiteRTAgentConfig` | `'gpu'` (CUDA) |
| Windows + NVIDIA GPU | `LiteRTAgentConfig` | `'gpu'` (CUDA) |
| Ollama / LM Studio running | `LocalOpenAIAgentConfig` | N/A |
| NPU-equipped device | `LiteRTAgentConfig` | `'npu'` |

---

## Authentication

Local models do not require an API key or any external authentication.
