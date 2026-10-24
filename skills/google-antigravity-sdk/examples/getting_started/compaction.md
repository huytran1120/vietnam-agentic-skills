# Conversation Compaction & Context Limits

This guide demonstrates how to configure conversation history compaction thresholds using `CompactionConfig`.

---

## Overview

As an agent performs multi-turn tasks, its conversation trajectory grows. To prevent exceeding model token limits while retaining critical task history, Antigravity compacts older conversation history when the active trajectory exceeds `token_threshold`. Earlier turns are evicted and replaced with a cumulative summary, while recent turns are preserved verbatim with full fidelity.

---

## Code Example

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig, types

# Configure compaction parameters on LocalAgentConfig
config = LocalAgentConfig(
    compaction_config=types.CompactionConfig(
        token_threshold=50_000,
    ),
)

async def main():
    async with Agent(config=config) as agent:
        response = await agent.chat(
            "Perform a deep multi-step analysis of our code repository."
        )
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Key Concepts

* **`CompactionConfig`**: Attached to `LocalAgentConfig(compaction_config=...)`, `LiteRTAgentConfig`, `LocalOpenAIAgentConfig`, or `JetskiProdActorAgentConfig`.
* **`token_threshold`**: The token ceiling allowed for conversation history before older turns are compacted. When omitted or `None`, the backend's default threshold is used.
