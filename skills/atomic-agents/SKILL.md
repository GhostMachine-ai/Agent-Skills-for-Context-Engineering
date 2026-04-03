---
name: atomic-agents
description: This skill should be used when the user asks to "build an agent with atomic-agents", "use Instructor for agent I/O", "create a BaseAgent", "design typed agent schemas", "chain agents together", or mentions atomic-agents, BrainBlend-AI, BaseIOSchema, system prompt context providers, or Pydantic-validated agent pipelines.
---

# Atomic Agents Framework

Atomic Agents is a Python framework for building modular, composable AI agents with type-safe, validated input/output schemas. Built on Instructor and Pydantic, it enforces explicit contracts between every component while remaining agnostic to LLM provider. The framework's core philosophy is small, single-purpose components — "atoms" — that compose into larger systems without hidden magic, monolithic base classes, or implicit state.

Unlike AutoGen or CrewAI, atomic-agents does not anthropomorphize agents or manage conversation topology for you. You define every schema, every prompt, every connection. This makes the framework verbose for simple cases but highly predictable and debuggable for production systems.

## When to Activate

Activate this skill when:
- Building new agents with the atomic-agents library
- Designing BaseIOSchema input/output contracts for agents
- Configuring system prompt context providers
- Connecting multiple agents into processing pipelines
- Choosing between atomic-agents, AutoGen, CrewAI, or custom implementations
- Debugging schema validation errors in Instructor-backed agents
- Integrating atomic-agents with OpenAI, Anthropic, Groq, Ollama, or Gemini

## Core Concepts

Every agent in atomic-agents is a `BaseAgent` instance with three explicit contracts: an `input_schema` (what it accepts), an `output_schema` (what it returns), and a `system_prompt_generator` (how it is instructed). Both schemas are Pydantic models, so validation and serialization are guaranteed by the runtime. Instructor handles the LLM call and enforces that the model's response parses into the output schema — retrying on failure.

The framework distinguishes between **agents** (stateful, have memory, make LLM calls) and **tools** (stateless, deterministic Python functions registered on an agent). This separation maps cleanly onto the tool-design skill's consolidation principle.

## Detailed Topics

### BaseAgent and BaseIOSchema

`BaseAgent` is the fundamental unit. Every subclass must define `input_schema` and `output_schema` as `BaseIOSchema` subclasses. `BaseIOSchema` extends Pydantic's `BaseModel` with a required `chat_message` field that serializes to the conversation turn passed to the LLM.

```python
from atomic_agents import BaseAgent, BaseIOSchema
from pydantic import Field

class ResearchInput(BaseIOSchema):
    """Input for the research agent."""
    chat_message: str = Field(..., description="Topic to research")
    max_sources: int = Field(5, description="Maximum sources to consult")

class ResearchOutput(BaseIOSchema):
    """Output from the research agent."""
    chat_message: str = Field(..., description="Research summary")
    sources: list[str] = Field(..., description="URLs or references used")
    confidence: float = Field(..., ge=0.0, le=1.0)
```

The `chat_message` field convention is load-bearing: Instructor uses it to populate the final message turn. All other fields are structured data extracted alongside it.

### System Prompt Context Providers

A `SystemPromptContextProvider` is a class with a `get_info_section()` method that returns a string injected into the system prompt at call time. Providers are registered on the agent's `system_prompt_generator`, making dynamic context (current date, user profile, retrieved documents) first-class citizens.

```python
from atomic_agents.system_prompt_generator import SystemPromptContextProvider

class DateContextProvider(SystemPromptContextProvider):
    title = "Current Date"

    def get_info_section(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

agent = ResearchAgent(
    client=instructor_client,
    system_prompt_generator=SystemPromptGenerator(
        background=["You are a research assistant."],
        context_providers={"date": DateContextProvider()},
    )
)
```

Context providers are the right place to inject memory retrievals, tool inventories, or external state — keeping the system prompt deterministic in structure while dynamic in content. This pattern maps directly to context-fundamentals: treat context injection as a first-class engineering problem, not an afterthought.

### Multi-Provider Setup

atomic-agents uses Instructor as the LLM adapter layer. Any provider Instructor supports works with zero changes to agent code.

```python
import instructor
import anthropic
import openai
from groq import Groq

# Anthropic
client = instructor.from_anthropic(anthropic.Anthropic())

# OpenAI
client = instructor.from_openai(openai.OpenAI())

# Groq (fast inference)
client = instructor.from_groq(Groq(), mode=instructor.Mode.JSON)

# Ollama (local)
client = instructor.from_openai(
    openai.OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
)
```

Pass the `client` and `model` string when constructing any agent. The agent code is identical across providers — only the constructor arguments change.

### Memory and State Management

`BaseAgent` maintains an `AgentMemory` instance that stores the conversation history as a list of message turns. By default, all turns accumulate, which is the context degradation problem described in context-degradation skill. Three patterns manage this:

**Bounded memory**: Set `max_messages` on `AgentMemory` to truncate history at a fixed count. Simple but loses early context.

**Summarization**: Before each call, run a dedicated summarizer agent over the full history and inject only the summary. Pairs with context-compression skill patterns.

**External memory**: Clear in-agent memory after each logical task boundary and use an external store (Mem0, filesystem, Graphiti) for long-horizon recall. The memory-systems skill covers architecture choices here.

```python
from atomic_agents import AgentMemory

# Bounded: keep last 20 messages
memory = AgentMemory(max_messages=20)
agent = ResearchAgent(client=client, memory=memory)

# Reset between tasks to prevent cross-task contamination
agent.memory.reset()
```

### Tool Integration

Tools in atomic-agents are Python callables registered via `agent.register_tool()`. The framework wraps them in Pydantic schemas for validation. Unlike tool-calling in raw OpenAI, the tool schema is derived from the function signature's type hints — there is no separate JSON schema to maintain.

```python
from atomic_agents import tool

@tool
def search_web(query: str, num_results: int = 5) -> list[dict]:
    """
    Search the web for information.
    Use when the agent needs current or external information.
    Returns a list of result dicts with 'title', 'url', 'snippet'.
    """
    return web_search_api(query, num_results)

agent = ResearchAgent(client=client, tools=[search_web])
```

Tool description quality follows all guidelines from the tool-design skill: write descriptions that answer what, when, and what returns. The docstring becomes the tool description seen by the LLM.

### Composition Patterns (Chaining Agents)

The primary composition pattern is **sequential chaining**: one agent's output schema becomes the next agent's input schema. Because both are Pydantic models, the handoff is type-validated at runtime.

```python
# Stage 1: Extract claims from a document
claims: ClaimsOutput = extractor_agent.run(
    ClaimsInput(chat_message=document_text)
)

# Stage 2: Verify each claim independently (parallelizable)
verified = [
    verifier_agent.run(VerifyInput(chat_message=claim))
    for claim in claims.claims
]

# Stage 3: Synthesize into final report
report: ReportOutput = writer_agent.run(
    ReportInput(
        chat_message="Write a report based on these verified claims.",
        verified_claims=verified,
    )
)
```

For parallel execution, wrap each agent call in `asyncio` using `agent.run_async()`. Each agent maintains its own memory, so parallel calls do not share state — this is the context isolation property described in multi-agent-patterns skill.

**Orchestrator pattern**: A dedicated orchestrator agent's output schema includes a `next_agent` field that routes control flow. This is explicit rather than framework-managed, keeping the execution path readable.

```python
class OrchestratorOutput(BaseIOSchema):
    chat_message: str
    next_step: Literal["research", "verify", "write", "done"]
    reasoning: str
```

## Practical Guidance

### When to Choose atomic-agents

| Situation | Recommendation |
|-----------|----------------|
| Need explicit, auditable schemas for every agent boundary | atomic-agents |
| Building on LangGraph with existing graph state | Stay on LangGraph |
| Rapid prototyping with role-based crews | CrewAI may be faster |
| Enterprise Python with strict type safety requirements | atomic-agents |
| Multi-framework team where some use AutoGen | Custom thin wrappers may be better |
| Need deep conversation management / GroupChat | AutoGen |

atomic-agents wins on legibility and debuggability. Every failure produces a Pydantic `ValidationError` with a specific field path. Every prompt is inspectable as a plain string. There is no hidden state machine.

### Anti-Patterns

**Overloading `chat_message`**: Do not pack all structured data into the `chat_message` string. Use additional typed fields on the schema and let the LLM populate them through Instructor's structured extraction. This is the whole point of the framework.

**Sharing memory across agents**: Each agent should own its own `AgentMemory`. Cross-contaminating memory leads to the context poisoning failure mode described in context-degradation skill.

**Skipping field descriptions**: Pydantic `Field(description=...)` becomes part of the JSON schema Instructor passes to the model. Sparse descriptions degrade extraction accuracy the same way sparse tool descriptions degrade tool use.

**Monolithic output schemas**: Schemas with 15+ fields are hard for models to populate reliably. Decompose into smaller agents with focused outputs, then combine in an orchestrator.

## Examples

**Example 1: Minimal working agent**
```python
import instructor
import openai
from atomic_agents import BaseAgent, BaseIOSchema
from atomic_agents.system_prompt_generator import SystemPromptGenerator
from pydantic import Field

class QAInput(BaseIOSchema):
    """Question for the agent."""
    chat_message: str = Field(..., description="The question to answer")

class QAOutput(BaseIOSchema):
    """Answer from the agent."""
    chat_message: str = Field(..., description="Direct answer")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Answer confidence")

agent = BaseAgent(
    client=instructor.from_openai(openai.OpenAI()),
    model="gpt-4o-mini",
    system_prompt_generator=SystemPromptGenerator(
        background=["You are a concise Q&A assistant."]
    ),
    input_schema=QAInput,
    output_schema=QAOutput,
)

result = agent.run(QAInput(chat_message="What is the capital of France?"))
print(result.chat_message, result.confidence)
```

**Example 2: Two-stage pipeline with typed handoff**
```python
# Agent 1 extracts structured data
class ExtractionOutput(BaseIOSchema):
    chat_message: str
    entities: list[str]
    sentiment: Literal["positive", "negative", "neutral"]

# Agent 2 receives typed structured data as input
class ClassificationInput(BaseIOSchema):
    chat_message: str
    entities: list[str]  # typed handoff field

# Handoff — type-safe, validated at runtime
extracted = extractor.run(ExtractionInput(chat_message=raw_text))
classified = classifier.run(
    ClassificationInput(
        chat_message="Classify these entities.",
        entities=extracted.entities,
    )
)
```

## Guidelines

1. Every agent boundary must have explicit `BaseIOSchema` subclasses — no raw string passing between agents
2. Use `Field(description=...)` on every schema field; sparse descriptions degrade extraction quality
3. Keep output schemas focused: fewer than 8 fields per schema as a guideline
4. Inject dynamic context (dates, retrieved memory, user state) via `SystemPromptContextProvider`, not by mutating the system prompt string
5. Reset or bound agent memory at logical task boundaries to prevent cross-task context contamination
6. Use `run_async()` for independent parallel agent calls to avoid sequential bottlenecks
7. Write tool docstrings as if they are tool descriptions in the tool-design skill — answer what, when, and what returns
8. Validate pipeline correctness with typed assertions on output fields, not just on `chat_message` strings

## Integration

This skill connects to:
- context-fundamentals - Context injection via providers maps to context window management principles
- tool-design - Tool docstring conventions apply directly to atomic-agents `@tool` decorators
- multi-agent-patterns - Sequential and parallel composition patterns; context isolation per agent memory
- memory-systems - External memory architectures to use alongside `AgentMemory` for cross-session persistence
- evaluation - Schema-validated outputs enable deterministic evaluation rubrics; structured fields are directly assessable

## References

Related skills in this collection:
- tool-design - Tool description engineering applies to atomic-agents `@tool` docstrings
- multi-agent-patterns - Composition and context isolation patterns
- memory-systems - Long-horizon memory beyond in-agent history
- evaluation - Evaluating agents with typed, structured outputs

External resources:
- atomic-agents GitHub (github.com/BrainBlend-AI/atomic-agents)
- Instructor documentation (python.useinstructor.com)
- Pydantic v2 documentation (docs.pydantic.dev)

---

## Skill Metadata

**Created**: 2026-04-03
**Last Updated**: 2026-04-03
**Author**: Agent Skills for Context Engineering Contributors
**Version**: 1.0.0
