# Getting Started: Running Agents with Local Models

## Overview

The Google Antigravity SDK supports running agents entirely on-device using local
models. No API key or cloud connectivity is required.

There are two primary local execution paths:

- **LiteRT** — Google's optimized, high-performance runtime for running local
  models directly on-device with native GPU/NPU acceleration.
- **OpenAI-Compatible Servers** — for connecting to external local model servers
  such as [Ollama](https://ollama.com) or [LM Studio](https://lmstudio.ai).

---

## Path 1: LiteRT (On-Device Runtime)

### Setup Steps

#### 1. Create a virtual environment

Using a virtual environment avoids PATH issues and dependency conflicts:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

*(Optional: If your virtual environment lacks `pip`, run
`python3 -m ensurepip --default-pip`)*.

#### 2. Install the SDK and LiteRT dependencies

```bash
pip install google-antigravity litert-lm
```

#### 3. Download and import the Gemma 4 26B model checkpoint

Use the `litert-lm` CLI utility to download and register the 26B Gemma 4
checkpoint:

```bash
litert-lm import \
  --from-huggingface-repo=litert-community/gemma-4-26B-A4B-it-litert-lm \
  gemma-4-26B-A4B-it-web.litertlm \
  gemma4-26b
```

> [!NOTE]
> This downloads approximately **16.8 GB** and registers the checkpoint at
> `~/.litert-lm/models/gemma4-26b/model.litertlm`. A device with **24 GB+ VRAM
> or unified memory** is recommended for running the 26B model.

> [!TIP]
> On macOS, if `litert-lm import` fails with an SSL certificate verification
> error, run:
> 
> ```bash
> pip install certifi
> export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")
> ```
> Then re-run the `litert-lm import` command.

### Minimal Example

```python
import asyncio
import os

from google.antigravity import Agent, LiteRTAgentConfig


async def main():
    config = LiteRTAgentConfig(
        model_path=os.path.expanduser(
            "~/.litert-lm/models/gemma4-26b/model.litertlm"
        ),
    )

    async with Agent(config) as agent:
        response = await agent.chat("Explain Python generators.")
        async for token in response:
            print(token, end="", flush=True)
        print()


if __name__ == "__main__":
    asyncio.run(main())
```

> [!IMPORTANT]
> `model_path` must be an absolute path. Use `os.path.expanduser()` to expand
> `~`.

> [!TIP]
> `LiteRTAgentConfig` supports all standard `AgentConfig` options. Custom tools,
> safety policies, system instructions, hooks, and workspaces configure
> identically to `LocalAgentConfig` — refer to [custom_tool.md](custom_tool.md)
> or [persona_config.md](persona_config.md) to customize your agent further.

### Full Autonomous Local Agent Example (File Editing & Shell)

For complete software development workflows, configure a workspace directory
and enable autonomous tool permissions:

```python
import asyncio
import os

from google.antigravity import Agent, LiteRTAgentConfig
from google.antigravity.hooks import policy


async def main():
    workspace = os.path.expanduser("~/my-local-project")
    os.makedirs(workspace, exist_ok=True)

    config = LiteRTAgentConfig(
        model_path=os.path.expanduser(
            "~/.litert-lm/models/gemma4-26b/model.litertlm"
        ),
        workspaces=[workspace],
        # Auto-allows shell commands (run_command) without interactive confirmation:
        policies=[policy.allow_all()],
    )

    async with Agent(config) as agent:
        response = await agent.chat(
            "Create a simple static webpage index.html with a dark-mode toggle."
        )
        async for token in response:
            print(token, end="", flush=True)
        print()


if __name__ == "__main__":
    asyncio.run(main())
```

### Key Configuration Notes

| Setting | Detail |
| --- | --- |
| **Lightweight defaults (auto-applied)** | `LiteRTAgentConfig` automatically applies the lightweight preset upon instantiation: configures the minimal tool set (`BuiltinTools.minimal()`: view, edit, write, bash, list_dir, grep), prunes verbose prompt sections (`AgentBehavior.MINIMAL`), disables subagent delegation, and sets context compaction. No explicit `.lightweight()` call is needed. |
| **Context compaction (`token_threshold`)** | `LiteRTAgentConfig` automatically configures a derived context compaction threshold (`token_threshold=40960`) tailored for the LiteRT engine's 64k KV-cache capacity (`65536` tokens), enabling multi-turn file inspection without manual configuration. |
| **Hardware acceleration** | Automatically detected: **Metal** on Apple Silicon (macOS), **CUDA** on Linux/Windows, and **WebGPU**. On Apple Silicon, the initial launch compiles GPU graph shaders for Metal (1–2 minutes); subsequent runs use cached binaries and start in seconds. |

---

## Path 2: OpenAI-Compatible Server (Ollama, LM Studio)

If you already run a local model server that exposes an OpenAI-compatible API,
point the SDK at it with `LocalOpenAIAgentConfig(...).lightweight()`:

```python
import asyncio
from google.antigravity import Agent, LocalOpenAIAgentConfig


async def main():
    config = LocalOpenAIAgentConfig(
        model="gemma4:26b",
        base_url="http://localhost:11434/v1",  # Ollama default
    ).lightweight()

    async with Agent(config) as agent:
        response = await agent.chat("Hello!")
        async for token in response:
            print(token, end="", flush=True)
        print()


if __name__ == "__main__":
    asyncio.run(main())
```

> [!TIP]
> For **Ollama**, start the server with `ollama serve` and pull a model
> (`ollama pull gemma4:26b`) before running your agent. For **LM Studio**,
> enable the local server in the app settings and note the port it binds to.

> [!WARNING]
> Do **not** use `LocalOpenAIAgentConfig` to connect to `litert-lm serve`.
> Use `LiteRTAgentConfig` instead — it manages the LiteRT server lifecycle
> automatically. `LocalOpenAIAgentConfig` is for external servers like Ollama
> or LM Studio that you start and manage independently.

For the full comparison table and detailed configuration reference, see
`references/local_models.md`.
