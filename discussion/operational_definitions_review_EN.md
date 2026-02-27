# Operational Definition Challenges of Core Constructs: An Evidence-Based Critical Review

**Document Type**: Internal Discussion Document
**Date**: 2026-02-27
**Project**: Effects of Agentic AI on Learning Outcomes Across Educational Contexts
**Purpose**: Critical review of operational definitions for key RQ constructs and alternative proposals

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Operational Definition of "Agentic AI"](#2-operational-definition-of-agentic-ai)
3. [Human Oversight Levels and Checkpoints](#3-human-oversight-levels-and-checkpoints)
4. [Single-Agent vs. Multi-Agent Systems](#4-single-agent-vs-multi-agent-operational-distinction)
5. [Synthesis and Recommendations](#5-synthesis-fundamental-challenges-and-solutions)
6. [References](#6-references)

---

## 1. Problem Statement

Three critical questions were raised regarding the core constructs of this meta-analysis:

1. **What exactly is "Agentic AI"?** Does a consensus operational definition exist in the literature?
2. **How can "checkpoints" in RQ2 be operationally specified?** Is "fully autonomous education" realistically possible?
3. **What is the real difference between single-agent and multi-agent systems in educational practice**, and how can this distinction be operationally recognized?

**Core hypothesis**: Substantial research exists in related areas, but the constructs lack established operational definitions, making meta-analytic synthesis problematic.

This document examines this hypothesis through systematic review of the academic literature and proposes alternatives.

---

## 2. Operational Definition of "Agentic AI"

### 2.1 Key Finding: No Consensus Operational Definition Exists

"Agentic AI" is widely used but poorly operationalized. Every major source reviewed acknowledges this explicitly or implicitly.

#### Comparison of Definitions Across Sources

| Source | Definition Approach | Limitation |
|---|---|---|
| **OpenAI** (Shavit et al., 2023) | "The degree to which a system can adaptably achieve complex goals in complex environments with limited direct supervision" | Defined as a **continuum** -- no clear boundary for "agentic" |
| **Anthropic** (2024) | Workflows (predefined code paths) vs. Agents (LLM dynamically directs own processes) | Practical architectural distinction, not a measurement criterion |
| **MIT AI Agent Index** (2025) | Autonomy + Goal complexity + Environmental interaction + Generality; "3+ autonomous tool calls" | Most concrete attempt, but designed for classifying commercial products |
| **Yan et al. (2025) APCP** | Adaptive -> Proactive -> Co-Learner -> Peer (4 levels) | Best education-specific framework, but still conceptual; no empirical validation |
| **Russell & Norvig** (1995/2021) | "Anything that can perceive its environment and act upon it" | Under this definition, a thermostat qualifies as an agent |
| **Suri et al. (2025)** | Attempted distinction between "AI Agents" and "Agentic AI" | The paper itself was written to address "lack of consensus" |
| **Bandi et al. (2025)** | Reviewed 143 studies; concluded "no universally agreed upon definition" | Meta-level confirmation of definitional chaos |

#### Shared Attributes Across Definitions (Family Resemblance)

```
Autonomy                      <- Present in nearly all definitions
Goal-directedness             <- Present in most definitions
Tool use                      <- Emphasized in CS/AI definitions
Planning                      <- Emphasized in LLM-era definitions
Minimal human supervision     <- Present in most definitions
Adaptability                  <- Emphasized in education definitions
Multi-agent coordination      <- Present in some definitions only
```

> **Core problem**: No definition specifies *how much* of each attribute is required for a system to qualify as "agentic."

### 2.2 Assessment of the Current Study's Operational Definition

The current protocol classifies a system as Agentic AI if it demonstrates "at least one of six autonomous capabilities":

| Capability | Assessment |
|---|---|
| Adaptive Response | **Overly broad** -- includes most ITS from the 2000s; any CAI with difficulty adjustment qualifies |
| Proactive Intervention | Relatively clear, but "without explicit learner request" criterion is ambiguous |
| Automated Assessment | **Overly broad** -- includes most automated grading systems |
| Recommendation Generation | Boundary unclear -- does Netflix-style recommendation qualify? |
| Dialogue Management | Relatively clear |
| Multi-Agent Coordination | Relatively clear |

**Conclusion**: The current operational definition effectively includes "AI-enhanced Educational Technology in general" rather than "Agentic AI" specifically. Adaptive ITS (2000s), automated scoring (2010s), and LLM tutors (2020s) are all grouped together despite fundamentally different technical mechanisms and pedagogical affordances.

### 2.3 Critical Review of Yan (2025) APCP Framework

The protocol claims APCP resolves this issue, but:

1. It remains an empirically unvalidated conceptual framework
2. Published as an arXiv preprint (peer review incomplete)
3. Intercoder reliability for the 4-level coding is untested
4. No application cases in educational field settings exist

### 2.4 Proposal: Two-Stage Operational Definition Strategy

| Stage | Content | Rationale |
|---|---|---|
| **Broad inclusion** (Search/Screening) | Retain current 6 criteria -> secure 40-80 studies | Ensure statistical power |
| **"Agenticity" continuous variable coding** (Analysis) | Code each study on MIT Index 4 dimensions (0-4): Autonomy, Goal complexity, Environmental interaction, Generality | Reflects OpenAI's "continuum" perspective |

Advantages of this strategy:
- Avoids the arbitrariness of binary classification ("agentic/non-agentic")
- Enables meta-regression with "Agenticity" score as a continuous moderator
- Testing whether higher agenticity predicts larger effects is itself a novel contribution

```
[Figure 1] Agenticity Continuum Model

    Non-Agentic                                              Highly Agentic
    |----|----|----|----|----|----|----|----|----|----|
    0    1    2    3    4    5    6    7    8    9    10
    |         |              |              |         |
    Static    Adaptive ITS   Conversational Proactive  Autonomous
    content   (include,      tutors         agents     multi-agent
    (exclude) low score)     (mid score)    (high)     (highest)

    <- Current criterion: include all scoring >= 1 ->
    <- Proposed: include, then meta-regress on continuous score ->
```

---

## 3. Human Oversight Levels and Checkpoints

### 3.1 Academic Status of "Checkpoint" Definitions

**Key finding**: The term "checkpoint" has no standardized operational definition in the AIED literature. Related frameworks exist, but none has been applied in an educational meta-analysis.

#### Related Frameworks

| Framework | Content | Applied in Education Meta-Analysis? |
|---|---|---|
| **Parasuraman et al. (2000)** | 10-level automation across 4 functions | **No** |
| **Molenaar (2022)** | SAE-inspired 6-level educational automation | **No** (conceptual proposal only) |
| **EU AI Act Art.14** | HITL / HOTL / HIC distinction | Rarely used in education research |
| **Jia et al. (2024)** | Entity-Relationship analysis of 28 HITL-AIED studies | Most studies described only 2-3 entities |
| **Cheng et al. (2026)** | Teacher-directed vs. self-directed (binary) | **Only instance in a meta-analysis** |

#### Oversight Coding in Existing Meta-Analyses

| Meta-Analysis | What Was Coded | Oversight Level Coded? |
|---|---|---|
| Ma et al. (2014) ITS | "Instructional context" (4 categories) | Instructional context, not oversight |
| Kulik & Fletcher (2016) | ITS type, comparison treatment | Not coded |
| Dai et al. (2024) | Agent role, AI technology, modality | Not coded |
| Cheng et al. (2026) | Teacher-directed vs. self-directed | **Binary level only** |
| Wang et al. (2024) | Adaptive sources, adaptive targets | Not coded |
| Vaccaro et al. (2024) | Human+AI vs. human/AI alone | Presence/absence only |

> **Conclusion**: No precedent exists for coding a graduated oversight scale in any AI/education meta-analysis.

### 3.2 Is "Fully Autonomous Education" Realistic?

#### It exists as a research construct but is not pedagogically endorsed

Real systems operating without a teacher present:

| System | What It Does Autonomously | What It Cannot Do |
|---|---|---|
| **Duolingo** | Lessons, feedback, difficulty adaptation, pronunciation evaluation | Social-emotional support, curriculum alignment, motivation crisis response |
| **Khan Academy** (self-paced) | Videos, practice problems, mastery tracking | Designed for teacher dashboard integration; teacher-free use is not the design intent |
| **AutoTutor** (Graesser) | ~100 turns of natural language tutoring dialogue | Research settings; d = 0.80 but rarely deployed in real classrooms without teachers |

#### Decisive Empirical Evidence: Bastani et al. (2025, PNAS)

Approximately 1,000 high school math students randomized to 3 groups:
- **Unrestricted ChatGPT** (no guardrails, no teacher involvement): 48% improvement during practice, **17% decline on exams**
- **Teacher-designed guardrail ChatGPT**: No harmful effect
- **Control group**: Baseline

> **This is direct evidence that unsupervised autonomous AI education can actively harm learning.**

#### Regulatory Reality

- **EU AI Act**: Education classified as high-risk (Annex III). Art.14 mandates human oversight -> Fully autonomous AI education violates EU law
- **UNESCO** (2023, 2024): Consistent position that AI is a support tool, not a teacher replacement

### 3.3 Reporting Quality of Teacher Involvement in Primary Studies

Reporting quality is extremely poor:

- **Topali et al. (2025)**: Half of K-12 AIED papers lacked pedagogical foundation and course contextualization, without describing teacher roles
- **Jia et al. (2024)**: Most of 28 HITL-AIED studies described only one-sided relationships
- **Stains & Vickrey (2017)**: Evidence-based instruction studies "typically do not characterize instructors' adherence to the practice"

> **Implication**: Even if we attempt to code oversight levels, most primary studies do not report what teachers actually did during AI use, forcing coders to rely on inference.

### 3.4 Proposed Taxonomy: Five Types of Checkpoints

Based on literature synthesis:

```
[Figure 2] Temporal Placement of Checkpoint Types

    ──────────────── AI-Learner Interaction Timeline ────────────────
    |                    |                              |             |
    Pre-deployment       Real-time dashboard            Post-hoc
    gate (Type 1)        (Type 2)                       review (Type 4)
                              |           |
                         AI-triggered    Co-orchestration
                         alert (Type 3)  decision point (Type 5)
```

| Type | Definition | Real Example | Timing |
|---|---|---|---|
| **Type 1: Pre-deployment gate** | Teacher approves AI system configuration, content scope, and parameters before student interaction | Khanmigo parameter setup; ChatGPT guardrail design (Bastani et al., 2025) | **Before** AI interaction |
| **Type 2: Real-time dashboard** | Teacher monitors learner state in real-time during AI use | Holstein et al. (2019) Lumilo smart glasses | **During** |
| **Type 3: AI-triggered alert** | AI flags a condition and notifies a human for intervention | Early warning systems; student performance decline flags | **Event-based** |
| **Type 4: Post-hoc review gate** | Teacher reviews AI-generated outputs after generation | Eedi/DeepMind LearnLM teacher approval (2025) | **After** AI interaction |
| **Type 5: Co-orchestration decision point** | AI recommends an action and waits for teacher approval | Lawrence et al. (2024) Pair-Up co-orchestration tool | **At decision point** |

### 3.5 Critique of the Current 3-Level Coding Scheme

Current protocol classification:

```
Level 1: Fully autonomous -- AI acts without human review
Level 2: AI-led with checkpoints -- human reviews at defined intervals
Level 3: Human-led with AI support -- human retains primary control
```

**Problem 1: Level 1 codes "absence = autonomous."** The decision rule states that if no oversight mechanism is described, the study is coded as fully autonomous. This systematically encodes **reporting bias** into the moderator variable. Older studies, word-limited conference papers, and CS-venue publications that do not describe pedagogical context are more likely to omit oversight descriptions, biasing Level 1 toward these papers.

**Problem 2: Level 2's "defined intervals" are unverifiable.** Most primary studies do not report when, how frequently, or under what conditions teachers intervene. If the existence of "checkpoints" cannot be confirmed, Level 1 and Level 2 are indistinguishable.

**Problem 3: The Level 2 / Level 3 boundary is ambiguous.** The difference between "AI-led with checkpoints" and "human-led with AI support" is a continuum, not a discrete category.

### 3.6 Alternative Proposal: Hierarchical Coding Strategy

Given that Cheng et al. (2026) detected significant moderation effects using only binary coding:

| Strategy | Content |
|---|---|
| **Primary analysis: Binary coding** | "Teacher involvement reported" vs. "No teacher involvement / not reported" -- following Cheng et al. (2026) precedent |
| **Secondary analysis: 3-level (exploratory)** | Apply 3-level coding only to the codeable subset; report if k is sufficient |
| **Separate "not reported" category** | Maintain "not reported" as distinct from "fully autonomous" to separate reporting bias from actual autonomy |

```
[Figure 3] Proposed Hierarchical Coding Strategy

                    Full Study Pool (k = 40-80)
                           |
              +------------+------------+
              |                         |
    Teacher involvement           Teacher involvement
    REPORTED                      NOT REPORTED
    (Primary: "present")          (Primary: "absent/unreported")
              |                         |
    +---------+---------+        Kept as separate category
    |         |         |        (distinguished from "autonomous")
  Level 3  Level 2   Level 1
  Human-   AI-led    Autonomous
  led      + CP      (explicit)
  (Secondary analysis: exploratory, only when k is sufficient)
```

---

## 4. Single-Agent vs. Multi-Agent: Operational Distinction

### 4.1 Key Finding: Three Coexisting, Incompatible Definitions

The distinction is real but means entirely different things depending on who defines it.

| Perspective | What "Multi-Agent" Means | Criterion |
|---|---|---|
| **Computer Science** (Wooldridge & Jennings, 1995) | 2+ autonomous decision-making entities with private state interacting | Architectural: private state + communication protocol |
| **Educational Technology** (Lippert/Graesser et al., 2020) | Learner interacts with 2+ distinguishable characters | Phenomenological: learner's perceptual experience |
| **LLM Era** (AutoGen, CrewAI) | Multiple LLM invocations with different system prompts/tools | Functional: role separation |

### 4.2 Cases Where the Three Definitions Diverge Completely

```
[Figure 4] Divergence of Three Definitions

Case A: Single LLM alternating between "tutor" and "peer" personas
+--------------------------------------------------+
|  Architectural:   SINGLE agent   <- one model     |
|  Phenomenological: MULTI agent   <- learner sees 2|
|  Functional:      MULTI role     <- two roles     |
+--------------------------------------------------+

Case B: 5 LLMs processing curriculum/assessment/strategy/reflection/memory in backend
+--------------------------------------------------+
|  Architectural:   MULTI agent    <- 5 models      |
|  Phenomenological: SINGLE agent  <- learner sees 1|
|  Functional:      MULTI role     <- five roles    |
+--------------------------------------------------+

Case C: AutoTutor trialogue (tutor agent + peer student agent + human)
+--------------------------------------------------+
|  Architectural:   MULTI agent    <- 2 agents      |
|  Phenomenological: MULTI agent   <- learner sees 2|
|  Functional:      MULTI role     <- two roles     |
+--------------------------------------------------+
```

### 4.3 What Matters Educationally?

Graesser's research group found that in trialogues, when two agents **disagree**, this triggers **productive confusion** leading to deeper learning. The mechanisms:

- **Cognitive disequilibrium**
- **Vicarious learning** (observing agent-to-agent dialogue)
- **Social role modeling**

This is a **phenomenological** multi-agent effect -- what matters is that learners perceive multiple characters and experience the social dynamics between them.

In contrast, 5 LLMs coordinating in the backend (**architectural** multi-agent) are invisible to the learner, so the mechanism for affecting learning is entirely different (e.g., better content quality, more accurate assessment).

### 4.4 Decisive Counter-Evidence from Recent Research

Two 2026 papers provide strong evidence:

**"Rethinking the Value of Multi-Agent Workflow" (arXiv, 2026)**
- Across 7 benchmarks, single-agent (performing multiple roles sequentially) matched or exceeded multi-agent performance, at ~23% lower cost
- Mathematical proof: Homogeneous multi-agent systems = single-agent (when tool side-effects are deterministic and routing depends only on visible history)

**"When Single-Agent with Skills Replace Multi-Agent Systems" (arXiv, 2026)**
- Multi-agent overhead: 58%-515% increase in token usage, 30-50% increase in cloud costs
- Truly necessary only when: (a) complex interdependencies, (b) non-consolidatable domain expertise, (c) parallel processing needed, (d) emergent consensus required

### 4.5 Current Empirical Evidence

Direct comparison studies are extremely scarce:

| Category | Studies Found (k) |
|---|---|
| Multi-agent vs. **single** agent, with learning outcomes | **k = 2** (possibly 3) |
| Multi-agent vs. **no** agent/traditional, with learning outcomes | **k = 7-9** |
| Multi-agent vs. **any** control, with learning outcomes | **k ~ 9-11** |

> **Conclusion**: The single vs. multi-agent subgroup comparison does not meet k >= 4.

### 4.6 Proposal: Reoperationalize RQ3

| Current RQ3 | Proposed Alternative |
|---|---|
| "What is the difference in effect sizes between single-agent and multi-agent systems?" | **"Does the number of agents perceived by the learner (1 vs. 2+) moderate learning outcomes?"** |

Advantages of this reformulation:
1. Adopts **phenomenological definition** -> dramatically improves coding reliability
2. Focuses on educationally meaningful mechanisms (social dynamics, vicarious learning)
3. Expands the codeable study pool (k = 7-9 becomes feasible)
4. Theoretically sound distinction between architecture and learner experience

```
[Figure 5] Proposed RQ3 Reoperationalization

Current: Architecture-based distinction
+--------------+     +--------------+
| Single agent | vs  | Multi-agent  |  -> k = 2-3 (insufficient)
| (1 backend)  |     | (2+ backend) |
+--------------+     +--------------+

Proposed: Learner experience-based distinction
+-------------------+     +-------------------+
| Single character   | vs  | Multiple characters|  -> k = 7-9 (feasible)
| perceived          |     | perceived          |
| (learner sees 1)   |     | (learner sees 2+)  |
+-------------------+     +-------------------+
```

---

## 5. Synthesis: Fundamental Challenges and Solutions

### 5.1 Common Problem Across All Three Constructs

| Construct | Status of Academic Definition | Coding Feasibility |
|---|---|---|
| Agentic AI | No consensus -- continuum, not category | Binary inclusion/exclusion possible but arbitrary |
| Human oversight level | Frameworks exist but **0** meta-analytic applications | Binary feasible; 3-level risky |
| Single/multi-agent | Three incompatible definitions coexist | Only phenomenological definition reliably codeable |

> **Core diagnosis**: This is a **construct validity** problem. When what is being measured is unclear, even the most sophisticated meta-analysis produces ambiguous results.

### 5.2 Integrated Recommendations for Meta-Analysis Redesign

This is not a call to abandon the current design, but to adjust operationalization to be realistic.

| Element | Current | Proposed |
|---|---|---|
| **Inclusion criteria** | Binary "Agentic AI" classification | Retain, but add Agenticity continuous score (0-4) -> meta-regression |
| **RQ2 (Oversight)** | 3-level categorical (primary moderator) | Primary: Binary (teacher involvement yes/no) + Secondary: 3-level (exploratory) |
| **RQ3 (Architecture)** | Single vs. multi-agent (primary moderator) | Reoperationalize as "learner-perceived agent count" + downgrade to exploratory |
| **"Not reported" handling** | Absence = fully autonomous | "Not reported" as independent category -- separate reporting bias from actual autonomy |
| **Theoretical basis** | Parasuraman 10->3 collapse | Add Molenaar (2022) 6-level model as primary reference -- education-specific framework |

### 5.3 Advantages of This Redesign

1. **Enhanced transparency of operational definitions** -> preemptive response to reviewer criticism
2. **Improved coding reliability** -> binary coding achieves higher kappa than 3-level
3. **Honest acknowledgment of evidence gaps** -> frames gaps as contributions
4. **The operational definition proposal itself becomes a contribution** -> organizing what the literature lacks

> **Key insight**: The greatest contribution of this meta-analysis may not be a single effect size, but the **methodological framework for how to code human oversight in educational AI**. Establishing a lineage from Parasuraman (2000) -> Molenaar (2022) -> this study's education-meta-analysis-specific coding system would constitute an independent contribution.

---

## 6. References

### Agentic AI Definitions

- Bandi, A., et al. (2025). The Rise of Agentic AI: A Review of Definitions, Frameworks, Architectures, Applications, Evaluation Metrics, and Challenges. *Future Internet*, 17(9), 404.
- Huyen, C. (2025). Agents. Blog post, January 2025.
- MIT (2025). The 2025 AI Agent Index. aiagentindex.mit.edu.
- OpenAI / Shavit, Y., et al. (2023). Practices for Governing Agentic AI Systems. OpenAI whitepaper.
- Anthropic (2024). Building Effective Agents. Blog post, December 2024.
- Russell, S. & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
- Suri, M., et al. (2025). AI Agents vs. Agentic AI: A Conceptual Taxonomy. *Information Fusion*.
- Yan, L. (2025). From Passive Tool to Socio-cognitive Teammate: APCP Framework. arXiv:2508.14825.

### Human Oversight and Automation Levels

- Bastani, H., et al. (2025). Generative AI without guardrails can harm learning. *PNAS*.
- Cheng, L., et al. (2026). Do GenAI-powered pedagogical agents improve academic performance? *JCER*.
- EU AI Act (2024). Article 14: Human Oversight.
- Holstein, K., et al. (2019). Co-Designing a Real-Time Classroom Orchestration Tool. *Journal of Learning Analytics*, 6(2), 27-52.
- Jia, F., et al. (2024). Human-in-the-loop in AIED: A review and ER analysis. *CEAI*, 6.
- Lawrence, L., et al. (2024). How teachers conceptualise shared control with an AI co-orchestration tool. *BJET*.
- Molenaar, I. (2022). Towards hybrid human-AI learning technologies. *European Journal of Education*, 57(4), 632-645.
- Parasuraman, R., et al. (2000). A model for types and levels of human interaction with automation. *IEEE Trans. SMC*, 30(3), 286-297.
- Topali, P., et al. (2025). Pedagogical considerations in the automation era. *BERJ*.
- UNESCO (2023). Guidance for generative AI in education and research.
- UNESCO (2024). AI Competency Framework for Teachers.

### Single/Multi-Agent Systems

- Botti, V. (2025). Agentic AI and Multiagentic: Are We Reinventing the Wheel? arXiv:2506.01463.
- Goldberg, Y. (2024). What makes multi-agent LLM systems multi-agent? GitHub Gist.
- Lippert, A., et al. (2020). Multiple Agent Designs in Conversational ITS. *Technology, Knowledge and Learning*, 25, 443-463.
- Rethinking the Value of Multi-Agent Workflow (2026). arXiv:2601.12307.
- When Single-Agent with Skills Replace Multi-Agent Systems (2026). arXiv:2601.04748.
- Wooldridge, M. & Jennings, N.R. (1995). Intelligent Agents: Theory and Practice. *Knowledge Engineering Review*, 10(2), 115-152.

### Meta-Analysis Methodology

- Dai, C.-P., et al. (2024). Effects of AI-Powered Virtual Agents. *Educational Psychology Review*, 36, 31.
- Ma, W., et al. (2014). Intelligent Tutoring Systems and Learning Outcomes. *JEP*, 106(4), 901-918.
- Vaccaro, M., et al. (2024). When combinations of humans and AI are useful. *Nature Human Behaviour*, 8(12), 2293-2303.
- Wang, X., et al. (2024). The efficacy of AI-enabled adaptive learning systems. *JCER*.

---

*This document is for internal discussion purposes. Co-author review is recommended prior to final methodological decisions.*
