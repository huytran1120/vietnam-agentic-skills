# Subagents Example

This example demonstrates how an agent can spawn and delegate tasks to
sub-agents using the Google Antigravity SDK.

## Spawning a Subagent

To allow an agent to spawn subagents, you need to enable them in the
`CapabilitiesConfig`. By default, subagents are enabled.

Here is a minimal example of an agent spawning a subagent to perform a specific
task.

```python
from google.antigravity import Agent, LocalAgentConfig, types

# Enable subagents in the config
config = LocalAgentConfig(
    capabilities=types.CapabilitiesConfig(
        enable_subagents=True,
    )
)

async with Agent(config) as agent:
    # Prompt the agent to use a subagent
    response = await agent.chat("Use a subagent to write a short poem about nature.")
    print(await response.text())
```

## Consuming Subagent Output

The result from the subagent is typically delivered back to the main agent,
which then presents it or uses it. The `await response.text()` call will return
the final aggregated response, including the output produced by the subagent.

## Configuring Subagent Capabilities and Behavior

Subagents default to `agent_behavior=AgentBehavior.AUTONOMOUS`. You can declare
custom subagents and customize their capabilities and execution behavior via
`SubagentConfig` and `SubagentCapabilities`:

```python
from google.antigravity import Agent, LocalAgentConfig, types

config = LocalAgentConfig(
    subagents=[
        types.SubagentConfig(
            name="researcher",
            description="Researches topics autonomously.",
            capabilities=types.SubagentCapabilities(
                agent_behavior=types.AgentBehavior.AUTONOMOUS,
            ),
        ),
    ],
)
```

## Hierarchical & Nested Subagents

You can create multi-tier subagent hierarchies where subagents delegate further
to other subagents. Configure the session-wide depth limit with
`max_subagent_depth` on `CapabilitiesConfig`, and scope which subagents each
tier can invoke with `allowed_subagents`:

```python
from google.antigravity import Agent, LocalAgentConfig, types

# Leaf tier: Can read files but cannot spawn further subagents.
fact_checker = types.SubagentConfig(
    name="fact_checker",
    description="Fact checks claims by verifying data.",
    capabilities=types.SubagentCapabilities(
        enabled_tools=[types.BuiltinTools.VIEW_FILE],
    ),
)

# Middle tier: Can read files and delegate to fact_checker.
lead_researcher = types.SubagentConfig(
    name="lead_researcher",
    description="Researches a topic and delegates verification to fact_checker.",
    capabilities=types.SubagentCapabilities(
        enabled_tools=[
            types.BuiltinTools.VIEW_FILE,
            types.BuiltinTools.START_SUBAGENT,
        ],
        allowed_subagents=["fact_checker"],
    ),
)

# Root agent: Session depth ceiling of 3; initially allowed to invoke lead_researcher.
config = LocalAgentConfig(
    subagents=[lead_researcher, fact_checker],
    capabilities=types.CapabilitiesConfig(
        enable_subagents=True,
        max_subagent_depth=3,
        allowed_subagents=["lead_researcher"],
    ),
)

async with Agent(config) as agent:
    response = await agent.chat(
        "Use 'lead_researcher' to analyze the report and have 'fact_checker' verify figures."
    )
    print(await response.text())
```
