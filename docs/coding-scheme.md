# Meta-Analysis Coding Scheme

## Overview

This document details the coding scheme for the meta-analysis of Agentic AI effects on learning outcomes. Two independent coders will apply this scheme to all included studies. Target intercoder reliability: Cohen's kappa >= 0.80.

---

## A. Study Identification

| Variable | Code | Description |
|----------|------|-------------|
| `study_id` | Numeric | Unique study identifier |
| `author` | Text | First author last name |
| `year` | Numeric | Publication year (2018-2025) |
| `journal` | Text | Journal or conference name |
| `country` | Text | Country where study was conducted |
| `publication_type` | 1 = Journal article, 2 = Conference paper | Type of publication |

---

## B. Study Design Characteristics

| Variable | Code | Description |
|----------|------|-------------|
| `design` | 1 = RCT, 2 = Quasi-experimental, 3 = Pre-post within-subjects | Research design type |
| `random_assignment` | 0 = No, 1 = Yes | Whether participants were randomly assigned |
| `control_type` | 1 = No AI, 2 = Non-agentic AI, 3 = Different agency level, 4 = Traditional instruction | Type of comparison condition |
| `duration_weeks` | Numeric | Duration of intervention in weeks |
| `n_treatment` | Numeric | Sample size in treatment group |
| `n_control` | Numeric | Sample size in control group |
| `n_total` | Numeric | Total sample size |
| `attrition_rate` | Numeric (0-1) | Proportion of participants lost |

---

## C. AI Agent Characteristics (Key Moderator Variables)

### C1. Human Oversight Level (RQ2)

This is the **primary novel moderator** of this meta-analysis.

**Theoretical basis**: This three-level taxonomy is grounded in Parasuraman, Sheridan, and Wickens' (2000) foundational model of types and levels of human interaction with automation. Their 10-level framework is collapsed into three meta-analytically tractable categories to ensure coding reliability (target Cohen's kappa >= 0.80) and adequate cell sizes (k >= 4 per level). This approach aligns with Molenaar's (2022) conceptualization of hybrid human-AI regulation in education and responds to the EU AI Act (2024, Article 14), which mandates human oversight for high-risk AI systems in educational contexts.

| Code | Level | Operational Definition | Examples |
|------|-------|----------------------|----------|
| 1 | **Fully Autonomous** | AI agent independently determines learning path, content, pacing, and feedback without human instructor involvement during the learning process | Fully autonomous ITS; AI tutor operating without instructor monitoring; self-directed AI learning companion |
| 2 | **AI-Led with Checkpoints** | AI agent primarily directs the learning experience, but human instructor reviews/intervenes at predetermined checkpoints or when triggered by specific conditions | AI tutor with instructor dashboard review; system that alerts instructor when learner struggles; AI-led with periodic human check-ins |
| 3 | **Human-Led with AI Support** | Human instructor primarily directs the learning experience, using AI agent as a tool/assistant; AI provides recommendations but human makes final decisions | AI teaching assistant; instructor uses AI for grading/feedback that they review; AI recommends resources that instructor selects |

**Decision Rules:**
- If unclear, code based on who makes the primary pedagogical decisions during the learning session
- If the study describes instructor monitoring without intervention, code as 1 (Fully Autonomous)
- If checkpoint frequency is described, code as 2 regardless of checkpoint content
- If the AI only provides suggestions that a human must approve, code as 3

### C2. Agent Architecture (RQ3)

| Code | Level | Operational Definition |
|------|-------|----------------------|
| 1 | **Single Agent** | One AI agent handles all functions (tutoring, assessment, feedback, etc.) |
| 2 | **Multi-Agent System** | Two or more AI agents with distinct roles collaborating to support learning |

**Decision Rules:**
- If a system has multiple "modules" but is presented as a single integrated system without distinct agent identities, code as 1
- If distinct agents are described with different roles (e.g., tutor agent + assessment agent), code as 2
- If unclear, code as 1 (conservative)

### C3. Agent Agency Level (Yan, 2025 APCP Framework)

| Code | Level | Operational Definition |
|------|-------|----------------------|
| 1 | **Adaptive** | AI reacts to learner inputs; adjusts difficulty/content based on performance; responsive but not proactive |
| 2 | **Proactive** | AI anticipates learner needs; initiates interactions; provides unsolicited scaffolding or guidance |
| 3 | **Co-Learner** | AI engages as a learning partner; shares the learning process; models learning behaviors |
| 4 | **Peer** | AI functions as a peer; engages in reciprocal interaction; capable of social and cognitive co-regulation |

**Decision Rules:**
- Code based on the highest agency level demonstrated in the study
- If agency level varies across the intervention, code the predominant level
- Adaptive is the default if insufficient information to distinguish higher levels

### C4. Agent Role

| Code | Role | Operational Definition |
|------|------|----------------------|
| 1 | **Tutor** | Provides instruction, explanation, and guided practice |
| 2 | **Coach** | Provides motivational support, learning strategies, and metacognitive scaffolding |
| 3 | **Assessor** | Evaluates learner work, provides assessment feedback, grades |
| 4 | **Collaborator** | Works alongside the learner on shared tasks |
| 5 | **Facilitator** | Moderates discussion, manages learning resources, orchestrates activities |
| 6 | **Multiple Roles** | Agent performs 2+ roles; specify which in notes |

### C5. Agent Modality

| Code | Modality | Operational Definition |
|------|----------|----------------------|
| 1 | **Text-only** | Interacts through text (chat, written feedback) |
| 2 | **Voice** | Includes speech output (text-to-speech or voice interaction) |
| 3 | **Embodied (Avatar)** | Has a visual embodiment (animated character, virtual human) |
| 4 | **Mixed** | Combines 2+ modalities |

### C6. AI Technology Base

| Code | Technology | Operational Definition |
|------|-----------|----------------------|
| 1 | **Rule-based** | Expert systems, decision trees, scripted responses |
| 2 | **Machine Learning** | Supervised/unsupervised learning algorithms (non-NLP) |
| 3 | **NLP (Pre-LLM)** | Natural language processing without large language models |
| 4 | **Large Language Model (LLM)** | GPT, BERT, LLaMA-based or similar foundation models |
| 5 | **Reinforcement Learning** | RL-based adaptive systems |
| 6 | **Hybrid** | Combines 2+ technology types; specify in notes |

### C7. Adaptivity Level

| Code | Level | Operational Definition |
|------|-------|----------------------|
| 1 | **Static** | Same behavior for all learners; no adaptation |
| 2 | **Performance-Adaptive** | Adapts based on performance metrics (scores, correct/incorrect) |
| 3 | **Behavior-Adaptive** | Adapts based on behavioral data (time-on-task, navigation patterns, engagement) |
| 4 | **Affect-Adaptive** | Adapts based on emotional/affective state (detected via sensors, facial expression, self-report) |
| 5 | **Multi-Dimensional** | Adapts based on 2+ data types (performance + behavior + affect) |

---

## D. Learning Context Characteristics (RQ4)

### D1. Learning Context

| Code | Context | Operational Definition |
|------|---------|----------------------|
| 1 | **K-12** | Primary and secondary education (ages 5-18) |
| 2 | **Higher Education** | Undergraduate and graduate education in degree programs |
| 3 | **Workplace Training** | Employer-provided training and development programs |
| 4 | **Professional Education** | Licensed profession continuing education (medical, legal, etc.) |
| 5 | **Continuing Education** | Adult education, lifelong learning outside formal programs |

### D2. Subject Domain

| Code | Domain |
|------|--------|
| 1 | STEM (Science, Technology, Engineering, Math) |
| 2 | Language (L1 or L2, reading, writing) |
| 3 | Medical/Health Sciences |
| 4 | Business/Management |
| 5 | ICT/Computer Science |
| 6 | Social Sciences/Humanities |
| 7 | Other (specify in notes) |

### D3. Learning Mode

| Code | Mode | Operational Definition |
|------|------|----------------------|
| 1 | **Formal** | Structured curriculum with defined objectives and assessment |
| 2 | **Informal** | Self-directed, unstructured learning |
| 3 | **Blended** | Combination of formal and informal elements |

### D4. Delivery Format

| Code | Format | Operational Definition |
|------|--------|----------------------|
| 1 | **Face-to-face with AI** | In-person instruction augmented by AI agent |
| 2 | **Fully Online** | Entirely online/remote learning with AI agent |
| 3 | **Hybrid** | Combination of in-person and online with AI agent |

---

## E. Learning Outcome Characteristics

### E1. Outcome Type

| Code | Type | Operational Definition |
|------|------|----------------------|
| 1 | **Cognitive (Knowledge)** | Declarative knowledge, conceptual understanding, factual recall |
| 2 | **Skill-based** | Procedural skills, problem-solving, technical skills |
| 3 | **Affective** | Motivation, engagement, self-efficacy, attitudes toward learning |
| 4 | **Performance** | Job/task performance, transfer to real-world application |

### E2. Outcome Level (Bloom's Taxonomy)

| Code | Level | Operational Definition |
|------|-------|----------------------|
| 1 | **Remember-Understand** | Recall, recognize, explain, describe (lower-order) |
| 2 | **Apply-Analyze** | Use, implement, compare, organize (middle-order) |
| 3 | **Evaluate-Create** | Judge, critique, design, produce (higher-order) |

### E3. Measurement Type

| Code | Measurement |
|------|-------------|
| 1 | Standardized test (validated instrument) |
| 2 | Researcher-developed test |
| 3 | Performance assessment (rubric-based) |
| 4 | Self-report measure |
| 5 | System-logged performance data |

### E4. Measurement Timing

| Code | Timing | Operational Definition |
|------|--------|----------------------|
| 1 | **Immediate Post-test** | Within 1 week of intervention completion |
| 2 | **Delayed Post-test** | More than 1 week after intervention completion |
| 3 | **Transfer Test** | Assessment in a different context/domain than training |

---

## F. Effect Size Data

| Variable | Description |
|----------|-------------|
| `es_id` | Unique effect size identifier (multiple per study possible) |
| `es_type` | Type of statistic reported (1=M+SD, 2=t-value, 3=F-value, 4=r/correlation, 5=Chi-square, 6=OR/RR, 7=Other) |
| `mean_treatment` | Treatment group mean (post-test or gain score) |
| `sd_treatment` | Treatment group standard deviation |
| `mean_control` | Control group mean (post-test or gain score) |
| `sd_control` | Control group standard deviation |
| `n_treatment_es` | Sample size for this specific effect size (treatment) |
| `n_control_es` | Sample size for this specific effect size (control) |
| `t_value` | t-statistic (if reported instead of M+SD) |
| `f_value` | F-statistic (if reported) |
| `p_value` | p-value (if reported) |
| `hedges_g` | Calculated Hedges' g |
| `se_g` | Standard error of Hedges' g |
| `var_g` | Variance of Hedges' g |
| `ci_lower` | 95% CI lower bound |
| `ci_upper` | 95% CI upper bound |
| `pre_post` | 0 = Post-test only, 1 = Gain scores (pre-post difference) |
| `notes` | Any relevant notes about data extraction decisions |

---

## G. Study Quality Assessment

Based on Cochrane Risk of Bias tool (adapted for educational research):

| Variable | Code | Description |
|----------|------|-------------|
| `rob_randomization` | 0 = High risk, 1 = Some concerns, 2 = Low risk | Random sequence generation |
| `rob_allocation` | 0 = High risk, 1 = Some concerns, 2 = Low risk | Allocation concealment |
| `rob_blinding_participants` | 0 = High risk, 1 = Some concerns, 2 = Low risk | Blinding of participants |
| `rob_blinding_outcome` | 0 = High risk, 1 = Some concerns, 2 = Low risk | Blinding of outcome assessment |
| `rob_incomplete_data` | 0 = High risk, 1 = Some concerns, 2 = Low risk | Incomplete outcome data |
| `rob_selective_reporting` | 0 = High risk, 1 = Some concerns, 2 = Low risk | Selective reporting |
| `rob_other` | 0 = High risk, 1 = Some concerns, 2 = Low risk | Other sources of bias |
| `rob_overall` | 0 = High, 1 = Some concerns, 2 = Low | Overall risk of bias judgment |

---

## H. Coding Procedures

### Coder Training
1. Both coders review coding manual together
2. Discuss each variable and decision rules
3. Pilot code 5 studies independently
4. Compare and discuss discrepancies
5. Refine coding definitions as needed
6. Repeat pilot if initial kappa < 0.80

### Independent Coding
1. Each coder codes all studies independently
2. Use standardized coding form (Excel/Google Sheets template)
3. Include notes/justifications for ambiguous decisions
4. Do not discuss coding decisions during independent phase

### Reliability Assessment
- Calculate Cohen's kappa for each categorical variable
- Calculate ICC (Intraclass Correlation Coefficient) for continuous variables
- Target: kappa >= 0.80, ICC >= 0.85
- Document all reliability statistics

### Conflict Resolution
1. Identify all discrepancies
2. Discuss each discrepancy with reference to original study text
3. Reach consensus through discussion
4. If no consensus, consult third reviewer
5. Document resolution decisions

---

*Note: This coding scheme will be pilot-tested and refined before full coding begins. All refinements will be documented with rationale.*
