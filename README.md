# Effects of Agentic AI on Learning Outcomes Across Educational Contexts

## A Meta-Analysis with Implications for Human-AI Learning Orchestration

[![PRISMA 2020](https://img.shields.io/badge/Protocol-PRISMA%202020-blue)](https://www.prisma-statement.org/)
[![Pre-registration](https://img.shields.io/badge/Pre--registration-PROSPERO-green)](#)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## Overview

This repository contains the research protocol, coding materials, and documentation for a **systematic meta-analysis** examining the effects of Agentic AI on learning outcomes across educational contexts, culminating in the development of the **HALO (Human-AI Learning Orchestration) Framework**.

### Research Questions

1. **RQ1 (Overall Effect)**: What is the overall effect of Agentic AI interventions on learning outcomes in educational contexts?
2. **RQ2 (Human Oversight)**: How does the level of human oversight (fully autonomous / AI-led with checkpoints / human-led with AI support) moderate the effect of Agentic AI on learning?
3. **RQ3 (Agent Architecture)**: What is the difference in learning effect sizes between single-agent and multi-agent systems?
4. **RQ4 (Learning Context)**: How do learning contexts (K-12 / Higher Education / Workplace Training) moderate the effectiveness of Agentic AI?
5. **RQ5 (Framework Derivation)**: What design principles for AI-agent-based learning support systems (HALO) are implied by the meta-analysis results?

---

## HALO Framework Summary

The **Human-AI Learning Orchestration (HALO) Framework** integrates MCP (Model Context Protocol) and Diverga principles into a 3-layer architecture, with each layer grounded in meta-analytic evidence:

```
+-------------------------------------------------------------+
|  Layer 3: ORCHESTRATION                                      |
|  "HOW should AI agents interact with learners?"              |
|  - Human Oversight Calibration (RQ2 findings)                |
|  - Agent Role Assignment (moderator-based)                   |
|  - Mode Collapse Prevention (VS Methodology / Diverga)       |
+-------------------------------------------------------------+
|  Layer 2: PROTOCOL                                           |
|  "WHAT should the system track and communicate?"             |
|  - Dynamic Learner State Tracking (Yang, 2025)               |
|  - Multi-Agent Communication (RQ3 findings / MCP)            |
|  - Adaptivity Engine (moderator-based)                       |
+-------------------------------------------------------------+
|  Layer 1: FOUNDATION                                         |
|  "FOR WHOM and IN WHAT CONTEXT?"                             |
|  - Agency Level Calibration (Yan, 2025 APCP)                 |
|  - Context-Specific Rules (RQ4 findings)                     |
|  - Outcome-Specific Rules (Bloom's taxonomy-based)           |
+-------------------------------------------------------------+
```

---

## Theoretical Foundations

| Theory | Role in Meta-Analysis | HALO Framework Integration |
|--------|----------------------|---------------------------|
| **Affordance Actualization Theory (AAT)** | Explains differential effects by AI agent type | Layer 3: Agent role-affordance mapping |
| **Event System Theory (EST)** | Optimal AI intervention based on event characteristics | Layer 3: Checkpoint trigger conditions |
| **Dynamic Learner State (Yang, 2025)** | Dimensions of learner state AI should track | Layer 2: MCP-based state tracking |
| **Self-Determination Theory (SDT)** | Impact of oversight level on autonomy/competence | Layer 1: Autonomy-supervision balance |
| **APCP Framework (Yan, 2025)** | 4-stage AI agency classification | Coding scheme: Agent agency level |

---

## Repository Structure

```
.
+-- README.md                          # This file
+-- docs/
|   +-- research-proposal.md           # Full research proposal
|   +-- coding-scheme.md               # Meta-analysis coding scheme
|   +-- search-strategy.md             # Search strategy & inclusion/exclusion criteria
|   +-- halo-framework.md              # HALO Framework detailed description
|   +-- pitch-for-collaborator.md      # 1-page pitch for Dr. Yang
|   +-- timeline.md                    # Project timeline
|   +-- references.md                  # Key references
```

---

## Methodology

- **Protocol**: PRISMA 2020
- **Pre-registration**: PROSPERO or OSF
- **Effect Size**: Hedges' g (standardized mean difference)
- **Databases**: Web of Science, Scopus, ERIC, PsycINFO, IEEE Xplore, ACM Digital Library
- **Publication Period**: 2018-2025
- **Expected Studies**: 40-80 studies, 100-200 effect sizes
- **Software**: R (`metafor`, `robumeta`, `clubSandwich`)
- **Intercoder Reliability**: Cohen's kappa (2 independent coders)

---

## Key Differentiators

| Dimension | Existing Meta-Analyses | This Study |
|-----------|----------------------|------------|
| **Focus** | AI tools in general or specific types | "Agentic AI" -- AI with autonomous action capabilities |
| **Key Moderator** | AI type, subject, learner level | **Human oversight level** (first of its kind) |
| **Context** | K-12 or higher education only | All educational contexts including workplace learning |
| **Framework** | Report results only | Meta-analysis results directly mapped to HALO design principles |
| **Theory** | Single learning theory | AAT + EST + SDT + DLS + APCP integration |

---

## Target Journals

- **Educational Research Review** (IF 11.8)
- **Computers & Education** (IF 11.5)
- **Educational Psychology Review** (IF 10.1)

---

## Authors

- Hosung You
- Dr. Yang (Collaboration TBD)

---

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
