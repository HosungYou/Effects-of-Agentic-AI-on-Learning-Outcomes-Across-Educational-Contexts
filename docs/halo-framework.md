# HALO Framework: Human-AI Learning Orchestration

## 1. Overview

The **HALO (Human-AI Learning Orchestration) Framework** is a 3-layer architecture for designing, implementing, and evaluating AI agent-based learning support systems. It integrates:

- **MCP (Model Context Protocol)**: Multi-agent communication and state tracking
- **Diverga**: Human oversight checkpoints and mode collapse prevention
- **Meta-analytic evidence**: Empirically-grounded design principles

The framework addresses the fundamental question: **"How should AI agents and human instructors collaborate to optimize learning outcomes?"**

---

## 2. Design Philosophy

### 2.1 Evidence-Based Design

Every design principle in HALO is mapped to meta-analytic findings:

```
Meta-analysis finding (Hedges' g, moderator effect)
        |
        v
Design Principle (what the system should do)
        |
        v
Implementation Guideline (how to build it)
        |
        v
Evaluation Criteria (how to assess it)
```

### 2.2 Core Assumptions

1. **Neither full autonomy nor full human control is optimal** -- the question is finding the right balance
2. **Context matters** -- optimal design varies by learning context, outcome level, and learner characteristics
3. **Multi-agent architectures require explicit coordination** -- orchestration is not optional
4. **Human oversight should be strategic, not constant** -- checkpoints at critical moments, not continuous monitoring

---

## 3. The 3-Layer Architecture

```
+================================================================+
||                                                                ||
||  Layer 3: ORCHESTRATION                                        ||
||  "HOW should AI agents interact with learners?"                ||
||                                                                ||
||  +------------------+ +------------------+ +------------------+||
||  | Human Oversight   | | Agent Role       | | Mode Collapse    |||
||  | Calibration       | | Assignment       | | Prevention       |||
||  |                   | |                  | |                  |||
||  | - Checkpoint      | | - Role-affordance| | - VS Methodology |||
||  |   frequency       | |   mapping        | | - Response       |||
||  | - Trigger         | | - Context-based  | |   diversity      |||
||  |   conditions      | |   role selection | | - Anti-pattern   |||
||  | - Override        | | - Dynamic role   | |   detection      |||
||  |   protocols       | |   switching      | |                  |||
||  +------------------+ +------------------+ +------------------+||
||                                                                ||
+================================================================+
||                                                                ||
||  Layer 2: PROTOCOL                                             ||
||  "WHAT should the system track and communicate?"               ||
||                                                                ||
||  +------------------+ +------------------+ +------------------+||
||  | Dynamic Learner   | | Multi-Agent      | | Adaptivity       |||
||  | State Tracking    | | Communication    | | Engine           |||
||  |                   | |                  | |                  |||
||  | - Mastery level   | | - MCP protocol   | | - Performance-   |||
||  | - Confidence      | | - Agent registry | |   based          |||
||  | - Context vars    | | - Message routing| | - Behavior-based |||
||  | - Decay modeling  | | - State sharing  | | - Affect-based   |||
||  +------------------+ +------------------+ +------------------+||
||                                                                ||
+================================================================+
||                                                                ||
||  Layer 1: FOUNDATION                                           ||
||  "FOR WHOM and IN WHAT CONTEXT?"                               ||
||                                                                ||
||  +------------------+ +------------------+ +------------------+||
||  | Agency Level      | | Context-Specific | | Outcome-Specific |||
||  | Calibration       | | Rules            | | Rules            |||
||  |                   | |                  | |                  |||
||  | - APCP 4 stages   | | - K-12 config    | | - Lower-order:   |||
||  | - Evidence-based  | | - HE config      | |   AI-led OK      |||
||  |   level selection | | - Workplace      | | - Higher-order:  |||
||  | - Progression     | |   config         | |   human-led      |||
||  |   pathways        | | - Domain-specific| |   preferred      |||
||  +------------------+ +------------------+ +------------------+||
||                                                                ||
+================================================================+
```

---

## 4. Layer 1: Foundation

### Purpose
Establishes the foundational parameters: who the learner is, what context they are in, and what outcomes are targeted. This layer determines the baseline configuration before any orchestration occurs.

### 4.1 Agency Level Calibration

Based on Yan (2025) APCP Framework, calibrated by meta-analytic evidence:

| APCP Level | Description | When to Use (Hypothesized) | Theoretical Basis |
|-----------|-------------|---------------------------|-------------------|
| **Adaptive** | AI reacts to learner inputs | Novice learners; well-structured domains; lower-order outcomes | SDT: High structure supports competence |
| **Proactive** | AI anticipates needs | Intermediate learners; semi-structured domains | EST: Proactive intervention at critical events |
| **Co-Learner** | AI as learning partner | Advanced learners; ill-structured domains; workplace contexts | SDT: Supports autonomy and relatedness |
| **Peer** | AI as equal peer | Expert learners; creative/evaluative tasks | AAT: Full affordance actualization |

**Meta-analysis input**: RQ4 results will validate or modify these assignments based on effect sizes across contexts.

### 4.2 Context-Specific Rules

| Context | Expected Configuration | Basis |
|---------|----------------------|-------|
| **K-12** | Higher structure, more adaptive, more checkpoints | Developmental stage; regulatory requirements |
| **Higher Education** | Moderate structure, proactive agency, balanced checkpoints | SDT: Growing autonomy needs |
| **Workplace Training** | Lower structure, co-learner/peer agency, strategic checkpoints | Adult learning principles; SDT: High autonomy |
| **Professional Education** | Domain-dependent; high adaptivity to performance | Domain expertise; high-stakes outcomes |

**Meta-analysis input**: RQ4 moderator analysis will provide effect size differences across contexts, informing specific configuration parameters.

### 4.3 Outcome-Specific Rules

| Outcome Level (Bloom's) | Expected Optimal Design | Basis |
|-------------------------|------------------------|-------|
| **Remember-Understand** | AI-led with minimal checkpoints; drill-based; high automation | Lower cognitive load; efficiency matters |
| **Apply-Analyze** | AI-led with regular checkpoints; scaffolded practice | Moderate complexity; structured support |
| **Evaluate-Create** | Human-led with AI support; collaborative; frequent checkpoints | High cognitive complexity; human judgment critical |

**Meta-analysis input**: Moderator analysis of outcome level will validate this gradient.

---

## 5. Layer 2: Protocol

### Purpose
Defines what the system tracks and how agents communicate. This is the infrastructure layer that enables intelligent orchestration.

### 5.1 Dynamic Learner State Tracking

Based on Yang (2025), the system tracks four key dimensions:

| Dimension | What It Tracks | How It's Used |
|-----------|---------------|---------------|
| **Mastery** | Current knowledge/skill level per learning objective | Triggers content adaptation; informs checkpoint urgency |
| **Confidence** | Learner's self-assessed vs. actual confidence (calibration) | Detects overconfidence (reduce scaffolding) or underconfidence (increase support) |
| **Context** | Environmental variables (time, prior activities, social setting) | Adjusts agent behavior based on situational factors |
| **Decay** | Predicted knowledge decay since last interaction | Triggers review/retrieval practice at optimal intervals |

**Implementation via MCP**:
- Each dimension is a structured data field in the MCP state object
- Agents read/write these fields through the protocol
- State updates trigger re-evaluation of orchestration rules

### 5.2 Multi-Agent Communication

Based on MCP principles:

```
+-------------------+
| Orchestrator      |  <-- Manages agent coordination
| (HALO Controller) |
+--------+----------+
         |
    MCP Protocol
         |
    +----+----+----+----+
    |    |    |    |    |
    v    v    v    v    v
  Tutor Coach Assessor Facilitator Recommender
  Agent Agent  Agent    Agent      Agent
```

**Key Protocols**:

| Protocol | Description |
|----------|-------------|
| **Agent Registration** | Each agent registers its capabilities, constraints, and state requirements |
| **State Sharing** | Agents share learner state updates through MCP; single source of truth |
| **Handoff Protocol** | Structured handoff when switching from one agent to another (e.g., tutor to assessor) |
| **Conflict Resolution** | When agents disagree (e.g., tutor says "continue" but assessor says "review"), orchestrator decides based on Layer 3 rules |
| **Checkpoint Trigger** | Any agent can trigger a human checkpoint based on predefined conditions |

**Meta-analysis input**: RQ3 results will determine whether multi-agent architectures actually produce better outcomes than single-agent, informing whether this complexity is warranted.

### 5.3 Adaptivity Engine

| Adaptivity Level | Data Required | Complexity | Effect (Hypothesized) |
|-----------------|---------------|------------|----------------------|
| **Performance-Adaptive** | Scores, correct/incorrect | Low | Baseline effective |
| **Behavior-Adaptive** | Time-on-task, navigation, engagement | Medium | Incrementally better |
| **Affect-Adaptive** | Emotion detection, frustration, flow | High | Best for engagement/motivation outcomes |
| **Multi-Dimensional** | All of the above | Highest | Optimal for complex learning goals |

**Meta-analysis input**: Moderator analysis of adaptivity level will provide effect sizes for each level, informing cost-benefit recommendations.

---

## 6. Layer 3: Orchestration

### Purpose
Defines how AI agents interact with learners in real-time. This is the "intelligence" layer that makes context-sensitive decisions about agent behavior.

### 6.1 Human Oversight Calibration

The central innovation of HALO, grounded in Diverga checkpoint principles:

#### Checkpoint Types

| Type | Symbol | Trigger Condition | Action |
|------|--------|------------------|--------|
| **Critical** | Red | High-stakes decision; significant learner confusion; ethical concerns | Mandatory human review before proceeding |
| **Advisory** | Orange | Moderate uncertainty; learner performance decline; complex domain transition | Human notified; can intervene or approve AI continuation |
| **Informational** | Yellow | Routine update; periodic summary; milestone reached | Human informed; AI continues unless human intervenes |

#### Trigger Conditions (EST-Based)

Based on Event System Theory (Morgeson et al., 2015):

| Event Characteristic | Low | Medium | High |
|---------------------|-----|--------|------|
| **Novelty** | Yellow | Orange | Red |
| **Disruption** | Yellow | Orange | Red |
| **Criticality** | Yellow | Orange | Red |

Examples:
- Learner encounters a completely new concept (high novelty) = Red checkpoint
- Learner shows gradual performance decline (medium disruption) = Orange checkpoint
- Learner completes a routine practice set (low all) = Yellow checkpoint

#### Calibration by Context

| Context | Default Checkpoint Frequency | Rationale |
|---------|----------------------------|-----------|
| K-12 | High (more Red/Orange) | Developmental protection; regulatory compliance |
| Higher Education | Moderate (balanced) | Growing autonomy with safety net |
| Workplace Training | Low (more Yellow) | Adult autonomy; self-regulation expected |
| High-Stakes Professional | High (more Red/Orange) | Consequence severity (medical, legal) |

**Meta-analysis input**: RQ2 results are the primary evidence for this component. If checkpoint-based AI shows significantly larger effect sizes than fully autonomous AI, this validates the HALO approach.

### 6.2 Agent Role Assignment

Based on moderator analysis of agent role:

| Learning Phase | Primary Agent | Support Agent | Rationale |
|---------------|--------------|---------------|-----------|
| Introduction | Tutor Agent | Coach Agent | Knowledge delivery + motivation |
| Practice | Tutor Agent | Assessor Agent | Guided practice + formative feedback |
| Application | Facilitator Agent | Collaborator Agent | Transfer + contextual application |
| Assessment | Assessor Agent | Coach Agent | Evaluation + metacognitive reflection |
| Review | Tutor Agent | Recommender Agent | Consolidation + personalized next steps |

**Dynamic Role Switching**: The orchestrator switches active agents based on learner state and learning phase, using MCP for seamless handoffs.

### 6.3 Mode Collapse Prevention

Adapted from Diverga's VS (Verbalized Sampling) Methodology:

| Risk | Detection | Prevention |
|------|-----------|-----------|
| **Repetitive Responses** | Monitor agent response diversity over time | Force exploration of alternative explanations/approaches |
| **Feedback Loops** | Detect when learner and AI are stuck in unproductive cycles | Trigger checkpoint; switch agent; change approach |
| **Overreliance** | Track learner's independent vs. AI-supported performance gap | Gradually reduce scaffolding; increase autonomous practice |
| **Domain Narrowing** | Monitor breadth of topics/skills covered | Ensure coverage of all learning objectives |

---

## 7. Meta-Analysis to Design Principle Mapping

### Mapping Logic

Each meta-analytic finding maps to specific HALO design principles:

| Meta-Analysis Finding (Hypothetical) | HALO Design Principle | Layer |
|--------------------------------------|----------------------|-------|
| Checkpoint-based AI > fully autonomous (g difference significant) | Human checkpoints as default; Red/Orange/Yellow system | Layer 3 |
| Multi-agent > single agent (g difference significant) | Multi-agent orchestration recommended; MCP protocol required | Layer 2 |
| Workplace: Co-Learner/Peer > Adaptive (g difference significant) | Higher agency levels for adult learners | Layer 1 |
| Multi-dimensional adaptivity > static (g difference significant) | Multi-dimensional state tracking justified despite cost | Layer 2 |
| Higher-order outcomes: Human-led > AI-led (g difference significant) | Human-led mode for Evaluate/Create tasks | Layer 3 |
| Context effect significant (K-12 vs HE vs Workplace) | Context-specific configuration rules required | Layer 1 |

### What If Findings Differ from Hypotheses?

| Unexpected Finding | Framework Adjustment |
|-------------------|---------------------|
| Fully autonomous = checkpoint-based | Recommend context-specific checkpoint deployment; checkpoints optional |
| Single agent = multi-agent | Simplify Layer 2; MCP optional for simple implementations |
| No context differences | Simplify Layer 1; universal configuration |
| Technology type matters more than oversight | Add technology layer; reweight design priorities |

The framework is designed to be **falsifiable and adaptable** -- meta-analytic evidence can both support and challenge the initial architecture.

---

## 8. Implementation Guidelines

### 8.1 Minimum Viable HALO Implementation

For practitioners who want to adopt HALO with minimal infrastructure:

1. **Layer 1**: Choose agency level based on learner context (use lookup table)
2. **Layer 2**: Implement performance-adaptive tracking (scores + correct/incorrect)
3. **Layer 3**: Implement Yellow checkpoints (periodic human review of AI recommendations)

### 8.2 Full HALO Implementation

For organizations with technical capacity:

1. **Layer 1**: Full APCP calibration with progression pathways
2. **Layer 2**: MCP-based multi-agent communication with multi-dimensional state tracking
3. **Layer 3**: Full Red/Orange/Yellow checkpoint system with EST-based triggers; VS-based mode collapse prevention

### 8.3 Evaluation Checklist

| Component | Question | Evidence |
|-----------|----------|----------|
| Layer 1 | Is the agency level appropriate for the context? | Context-effect size mapping from meta-analysis |
| Layer 2 | Is learner state being tracked adequately? | Adaptivity level effect sizes |
| Layer 2 | Is multi-agent coordination functioning? | Architecture effect size comparison |
| Layer 3 | Are checkpoints triggered at appropriate times? | Human oversight effect sizes |
| Layer 3 | Is mode collapse being prevented? | Response diversity metrics |
| Overall | Are learning outcomes improving? | Pre-post comparison against meta-analytic benchmarks |

---

## 9. Theoretical Integration

| Theory | HALO Integration Point | Mechanism |
|--------|----------------------|-----------|
| **AAT** | Agent affordances are matched to learning contexts and outcomes | Layer 3: Role assignment ensures affordance-context fit |
| **EST** | Event characteristics trigger appropriate checkpoint levels | Layer 3: Novelty/disruption/criticality assessment |
| **SDT** | Oversight level calibrated to preserve autonomy while ensuring competence | Layer 1 + Layer 3: Balance autonomy support with structured guidance |
| **DLS** | Multi-dimensional state tracking captures dynamic learner changes | Layer 2: Mastery/confidence/context/decay tracking |
| **APCP** | Progressive agency levels match learner developmental stage | Layer 1: Evidence-based level selection |

---

## 10. Limitations and Future Directions

### Known Limitations
1. Framework assumes technology infrastructure for MCP implementation
2. Checkpoint system requires trained human overseers
3. Agency level calibration may not account for individual differences within contexts
4. Mode collapse prevention metrics need empirical validation

### Future Research Directions
1. Empirical validation of HALO through controlled experiments
2. Development of automated checkpoint triggering algorithms
3. Longitudinal studies of agency level progression
4. Cross-cultural validation of context-specific rules
5. Cost-benefit analysis of implementation levels (minimum vs. full)

---

*Note: This is the initial (pre-meta-analysis) version of the HALO Framework. The refined version will incorporate actual meta-analytic findings in place of the hypothetical examples used here.*
