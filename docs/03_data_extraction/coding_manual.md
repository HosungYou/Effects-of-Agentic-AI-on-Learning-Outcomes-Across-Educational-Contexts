# Comprehensive Coding Manual

## Overview

This coding manual provides complete operational definitions, coding procedures, and decision rules for all variables in the meta-analysis of Agentic AI effects on learning outcomes. This document complements the Excel-based coding template. Both coders must use this manual during independent coding. Target intercoder reliability: Cohen's kappa ≥ 0.80 for all categorical variables; ICC ≥ 0.85 for continuous variables.

---

## Part A: Study Identification Variables

### A1. Study ID (`study_id`)
- **Type**: Numeric, auto-assigned
- **Format**: Sequential integer (001, 002, ...)
- **Rule**: Assigned by primary coder (Coder 1) before independent coding begins

### A2. Effect Size ID (`es_id`)
- **Type**: Numeric
- **Format**: [study_id].[es_sequence] (e.g., 001.1, 001.2, 001.3)
- **Rule**: Multiple effect sizes from the same study share the study_id prefix

### A3. First Author (`author`)
- **Type**: Text
- **Format**: Last name only (e.g., "Smith")
- **Rule**: If two authors with same last name and year, add first initial (e.g., "Smith_J")

### A4. Publication Year (`year`)
- **Type**: Numeric (4 digits)
- **Format**: YYYY
- **Rule**: Year of publication, not year of data collection

### A5. Journal/Conference (`journal`)
- **Type**: Text (full name, no abbreviations)
- **Example**: "Computers & Education" not "C&E"

### A6. Country (`country`)
- **Type**: Text (country name where study was conducted)
- **Rule**: If multinational study, list all countries separated by semicolon
- **If unclear**: Code country of first author's institution

### A7. Publication Type (`pub_type`)
- **Type**: Categorical
- **Codes**:
  - 1 = Peer-reviewed journal article
  - 2 = Conference proceedings (peer-reviewed)
  - 3 = Dissertation
  - 4 = Other (specify in notes)

---

## Part B: Study Design Variables

### B1. Research Design (`design`)
- **Type**: Categorical
- **Codes**:
  - 1 = Randomized Controlled Trial (RCT): Random assignment to conditions
  - 2 = Quasi-experimental: Non-random assignment with comparison group
  - 3 = Pre-post within-subjects: Same participants; pre-test and post-test; no concurrent control
  - 4 = Cross-over: Participants experience both conditions in sequence

**Decision Rules**:
- If random assignment is described explicitly ("participants were randomly assigned"), code 1
- If classes or schools are assigned (not individuals), code 2 (cluster assignment, not individual random)
- If the study says "randomly selected" for participation but not randomly assigned to conditions, code 2
- If only one group and both pre- and post-test data exist, code 3

### B2. Random Assignment (`random_assignment`)
- **Type**: Binary
- **Codes**: 0 = No, 1 = Yes
- **Rule**: Only code 1 if individual-level randomization is explicitly described

### B3. Control Condition Type (`control_type`)
- **Type**: Categorical
- **Codes**:
  - 1 = No AI (traditional instruction, lecture, textbook, human tutor only)
  - 2 = Non-agentic AI (static content, simple FAQ bot, non-adaptive software)
  - 3 = Different AI agency level (e.g., lower autonomy AI as control)
  - 4 = Waitlist control (no instruction during study period)
  - 5 = Active comparison (different type of AI agent, not agency level)

### B4. Intervention Duration (`duration_weeks`)
- **Type**: Numeric (decimal allowed)
- **Format**: Total weeks of intervention (convert days: 1 week = 7 days; convert months: 1 month = 4.3 weeks)
- **If unclear**: Code 999 (missing) and note source of uncertainty

### B5. Treatment Group N (`n_treatment`)
- **Type**: Numeric (integer)
- **Rule**: Post-attrition N if reported; pre-attrition N if post-attrition not available
- **Note**: Record which N was used in the `notes` field

### B6. Control Group N (`n_control`)
- **Type**: Numeric (integer)
- **Rule**: Same as B5; use post-attrition if available

### B7. Attrition Rate (`attrition_rate`)
- **Type**: Numeric (proportion: 0.00-1.00)
- **Formula**: (Initial N - Final N) / Initial N
- **If not reported**: Code 999 (missing)

---

## Part C: AI Agent Characteristics

### C1. Human Oversight Level (`oversight_level`) — PRIMARY MODERATOR (RQ2)

This is the most critical coding variable. Code based on WHO primarily makes pedagogical decisions during the learning session.

| Code | Level | Definition | Indicators |
|------|-------|------------|-----------|
| 1 | **Fully Autonomous** | AI independently determines learning path, content, pacing, and feedback without instructor involvement during learning | No instructor monitoring described; AI makes all decisions; "fully automated"; no human intervention loop |
| 2 | **AI-Led with Checkpoints** | AI primarily directs experience; human reviews/intervenes at defined checkpoints or triggered conditions | Instructor dashboard described; alert system for struggling learners; "human-in-the-loop at key moments"; periodic human check-ins |
| 3 | **Human-Led with AI Support** | Human instructor primarily directs; AI provides tools/recommendations that human may use or ignore | AI described as "assistant"; instructor decides which AI suggestions to use; AI generates options for instructor review |

**Critical Decision Rules**:

| Scenario | Code | Rationale |
|----------|:----:|-----------|
| ITS operates without described instructor monitoring | 1 | Default absence of oversight = fully autonomous |
| System emails instructor when learner fails 3 consecutive items | 2 | Failure-triggered checkpoint = AI-led with checkpoint |
| Instructor uses AI dashboard to monitor and intervenes when they choose | 2 | Periodic optional human check-in = AI-led with checkpoint |
| AI grades essays; instructor reviews grades before release | 3 | Human reviews all AI output = human-led |
| AI provides suggested next resources; instructor selects which to assign | 3 | Human makes final content decisions = human-led |
| Instructor monitoring described but no actual intervention mechanism | 1 | Monitoring without intervention = fully autonomous |

**Anchor Examples**:
- Code 1: AutoTutor, MetaTutor, fully automated adaptive learning platforms without instructor dashboards
- Code 2: AI systems with learning analytics dashboards + instructor alert features; AI tutors with "check-in" protocols
- Code 3: AI writing feedback tools used within instructor-directed lessons; AI recommendation systems where instructor decides

### C2. Agent Architecture (`architecture`) — PRIMARY MODERATOR (RQ3)

| Code | Level | Definition | Decision Rule |
|------|-------|------------|---------------|
| 1 | **Single Agent** | One AI agent handles all functions (tutoring, assessment, feedback) | Default if multiple modules but no distinct agent identities |
| 2 | **Multi-Agent System** | 2+ AI agents with distinct roles and identities collaborating | Must have distinct named/described agents with different roles |

**Decision Rules**:
- If paper describes "modules" or "components" of a single system → Code 1
- If paper describes distinct agents (e.g., "TutorBot and AssessBot work together") → Code 2
- If MCP or similar inter-agent protocol is mentioned → Code 2
- If unsure → Code 1 (conservative; document uncertainty in notes)

### C3. Agency Level (`agency_level`) — APCP Framework (Yan, 2025)

| Code | Level | Definition | Behavioral Indicators |
|------|-------|------------|----------------------|
| 1 | **Adaptive** | AI reacts to inputs; adjusts difficulty/content based on performance | Adjusts quiz difficulty; changes explanation based on prior answer; performance-based content selection |
| 2 | **Proactive** | AI anticipates needs; initiates unsolicited interactions | Detects confusion and offers help without request; proactively sends reminders; initiates encouragement |
| 3 | **Co-Learner** | AI engages as learning partner; models learning behaviors | Collaborates on tasks; shows its own "thinking process"; explores problems alongside learner |
| 4 | **Peer** | AI functions as social peer; reciprocal interaction; social co-regulation | Engages in social conversation about learning; celebrates achievements mutually; peer-like collaborative problem-solving |

**Decision Rules**:
- Code the **highest** level demonstrated consistently throughout the intervention
- If agency level varies, code the **predominant** level (>50% of interactions)
- Adaptive is the default/minimum (all agentic AI must be at least adaptive by inclusion criteria)
- Peer-level coding requires explicit description of reciprocal social interaction, not just friendly language

### C4. Agent Role (`agent_role`)

| Code | Role | Definition | Examples |
|------|------|------------|---------|
| 1 | **Tutor** | Provides instruction, explanation, guided practice | AutoTutor; ITS with explanation capability; conversational tutoring |
| 2 | **Coach** | Motivational support, learning strategy guidance, metacognitive scaffolding | Goal-setting agents; reflection prompt systems; motivational dialogue agents |
| 3 | **Assessor** | Evaluates work; provides assessment feedback; scores/grades | Automated essay scoring; intelligent homework graders; performance diagnostics |
| 4 | **Collaborator** | Works alongside learner on shared tasks; co-creates | Collaborative writing agents; pair programming AI; co-design AI systems |
| 5 | **Facilitator** | Moderates discussion; manages resources; orchestrates activities | Discussion board AI moderators; group learning orchestrators |
| 6 | **Multiple Roles** | Agent performs 2+ distinct roles | Note all roles in coding notes (e.g., "Tutor + Assessor") |

**Decision Rule**: If the primary role is instruction/explanation → Code 1 (Tutor) even if some coaching occurs

### C5. Agent Modality (`modality`)

| Code | Modality | Indicators |
|------|----------|-----------|
| 1 | **Text-only** | Chat interface; written feedback; no audio or visual avatar |
| 2 | **Voice** | Text-to-speech output; speech recognition input; spoken dialogue |
| 3 | **Embodied/Avatar** | Animated character; virtual human; 2D or 3D visual representation |
| 4 | **Mixed** | Combination of 2+ modalities (e.g., text + avatar; voice + avatar) |

### C6. AI Technology Base (`technology`)

| Code | Technology | Indicators |
|------|-----------|-----------|
| 1 | **Rule-based** | Expert systems; decision trees; IF-THEN rules; scripted responses |
| 2 | **Machine Learning (non-NLP)** | Supervised learning; clustering; recommendation algorithms |
| 3 | **NLP (Pre-LLM)** | Natural language processing; BERT; earlier transformer models; NLU/NLG systems |
| 4 | **Large Language Model (LLM)** | GPT-3/4; ChatGPT; LLaMA; Claude; Gemini; described as "generative AI" or "foundation model" |
| 5 | **Reinforcement Learning** | RL-based adaptive systems; policy learning; reward-based optimization |
| 6 | **Hybrid** | Combines 2+ technologies (specify in notes, e.g., "Rule-based + ML") |

**Decision Rules**:
- If paper mentions "ChatGPT," "GPT," or any LLM → Code 4
- If paper says "adaptive system" without specifying algorithm → Code 2 (conservative)
- If published before 2020 and uses NLP → Code 3 (pre-LLM era by default)

### C7. Adaptivity Level (`adaptivity`)

| Code | Level | Definition | Minimum Data Requirements |
|------|-------|------------|--------------------------|
| 1 | **Static** | Same behavior for all learners; no personalization | No learner data required |
| 2 | **Performance-Adaptive** | Adapts based on scores, accuracy, test results | Performance/score data |
| 3 | **Behavior-Adaptive** | Adapts based on time-on-task, navigation, clickstream | Behavioral log data |
| 4 | **Affect-Adaptive** | Adapts based on emotion detection, physiological data, affect self-report | Affect/physiological data |
| 5 | **Multi-Dimensional** | Adapts based on 2+ data types simultaneously | Multiple data streams |

---

## Part D: Learning Context Variables

### D1. Learning Context (`context`) — PRIMARY MODERATOR (RQ4)

| Code | Context | Operational Definition | Age/Level |
|------|---------|----------------------|-----------|
| 1 | **K-12** | Primary and secondary school (formal schooling before university) | Ages ~5-18; grades K-12 |
| 2 | **Higher Education** | Degree-granting post-secondary education | Undergraduate, graduate, professional degree students |
| 3 | **Workplace Training** | Employer-provided, job-related training | Employed adults; organizational context |
| 4 | **Professional Education** | Continuing education for licensed professions | Medical, legal, nursing, teaching CEUs |
| 5 | **Continuing/Adult Education** | Non-degree adult learning outside formal programs | Adults; no employer mandate |

**Decision Rules**:
- If paper describes "university students" in a formal course → Code 2
- If paper describes nurses in hospital training → Code 4
- If paper describes corporate employees in mandatory training → Code 3
- If paper describes adults voluntarily learning a skill → Code 5

### D2. Subject Domain (`domain`)

| Code | Domain | Scope |
|------|--------|-------|
| 1 | **STEM** | Science, technology, engineering, mathematics |
| 2 | **Language** | L1/L2 reading, writing, grammar, composition |
| 3 | **Medical/Health Sciences** | Medicine, nursing, health professions |
| 4 | **Business/Management** | Business education, management, finance |
| 5 | **ICT/Computer Science** | Programming, data science, computing education |
| 6 | **Social Sciences/Humanities** | History, psychology, political science, philosophy |
| 7 | **Other** | Specify in notes |

### D3. Learning Mode (`mode`)

| Code | Mode | Definition |
|------|------|------------|
| 1 | **Formal** | Structured curriculum; defined objectives; graded assessment |
| 2 | **Informal** | Self-directed; unstructured; learner-chosen goals |
| 3 | **Blended** | Mix of formal structure and self-directed elements |

### D4. Delivery Format (`format`)

| Code | Format | Definition |
|------|--------|------------|
| 1 | **Face-to-face with AI** | In-person classroom/lab; AI used during face-to-face instruction |
| 2 | **Fully Online** | All instruction and AI interaction via internet; no in-person component |
| 3 | **Hybrid/Blended** | Combination of in-person and online with AI |

---

## Part E: Learning Outcome Variables

### E1. Outcome Type (`outcome_type`)

| Code | Type | Definition | Examples |
|------|------|------------|---------|
| 1 | **Cognitive (Knowledge)** | Declarative knowledge; comprehension; conceptual understanding | Knowledge tests; comprehension assessments; recall measures |
| 2 | **Skill-based** | Procedural skills; problem-solving; technical performance | Programming skill tests; essay quality; math problem-solving |
| 3 | **Affective** | Motivation; engagement; self-efficacy; attitudes | Intrinsic motivation scales; academic self-efficacy; engagement surveys |
| 4 | **Performance** | Transfer; job performance; real-world application | Work simulation tasks; transfer tests; on-the-job performance |

**Decision Rule**: If a study reports multiple outcome types, extract a separate effect size for each. Code this variable for each effect size independently.

### E2. Bloom's Taxonomy Level (`blooms_level`)

| Code | Level | Bloom's Verbs | Examples |
|------|-------|--------------|---------|
| 1 | **Remember-Understand** | Recall, recognize, list, describe, explain, summarize | Factual knowledge tests; vocabulary assessments; concept definitions |
| 2 | **Apply-Analyze** | Use, implement, solve, compare, differentiate, organize | Problem-solving tests; application exercises; case analysis |
| 3 | **Evaluate-Create** | Judge, critique, design, create, produce, argue | Essays requiring argument; design projects; creative problem-solving |

**Decision Rule**: Code the primary cognitive demand of the outcome measure, not the highest level touched

### E3. Measurement Type (`measurement_type`)

| Code | Measurement |
|------|-------------|
| 1 | Standardized test (validated, normed instrument) |
| 2 | Researcher-developed test (created for study) |
| 3 | Performance assessment (rubric-scored product) |
| 4 | Self-report measure (Likert scales; surveys) |
| 5 | System-logged performance data (accuracy rates; completion) |
| 6 | Mixed (combination; specify in notes) |

### E4. Measurement Timing (`timing`)

| Code | Timing | Definition |
|------|--------|------------|
| 1 | **Immediate post-test** | Within 1 week of intervention completion |
| 2 | **Delayed post-test** | More than 1 week after intervention completion (specify weeks in notes) |
| 3 | **Transfer test** | Assessment in novel context/domain (not just delayed) |

---

## Part F: Effect Size Data Extraction

### F1. Effect Size Identifier (`es_id`)
- Unique per effect size: format [study_id].[sequential number]

### F2. Effect Size Type (`es_type`)
Indicates the statistical information available:

| Code | Type | Formula Path |
|------|------|-------------|
| 1 | M + SD (treatment & control) | Direct computation |
| 2 | t-statistic + n | Convert t → d → Hedges' g |
| 3 | F-statistic (df numerator=1) + n | Convert F → d → Hedges' g |
| 4 | Correlation r + n | Convert r → d → Hedges' g |
| 5 | Chi-square + n | Convert χ² → Phi → d → Hedges' g |
| 6 | Odds ratio + n | Convert OR → d → Hedges' g |
| 7 | Pre-post design (M_pre, M_post, SD, n) | Morris & DeShon (2002) |
| 8 | Author-reported d or g | Apply J correction if d; verify if g |
| 9 | Other (specify in notes) | Manual conversion |

### F3. Data Fields

| Variable | Description | Units |
|----------|-------------|-------|
| `mean_treatment` | Treatment group post-test mean | Original scale units |
| `sd_treatment` | Treatment group post-test SD | Original scale units |
| `mean_control` | Control group post-test mean | Original scale units |
| `sd_control` | Control group post-test SD | Original scale units |
| `n_treatment_es` | Treatment n for this effect size | Integer |
| `n_control_es` | Control n for this effect size | Integer |
| `mean_pre_treatment` | Pre-test mean (treatment, if applicable) | Original scale |
| `sd_pre_treatment` | Pre-test SD (treatment, if applicable) | Original scale |
| `mean_pre_control` | Pre-test mean (control, if applicable) | Original scale |
| `sd_pre_control` | Pre-test SD (control, if applicable) | Original scale |
| `t_value` | t-statistic if reported | t |
| `f_value` | F-statistic if reported | F |
| `r_value` | Correlation coefficient if reported | r |
| `p_value` | p-value if reported | p |
| `hedges_g` | Calculated Hedges' g (positive = AI > control) | g |
| `se_g` | Standard error of Hedges' g | SE |
| `var_g` | Variance of Hedges' g | Var |
| `ci_lower` | 95% CI lower bound | g |
| `ci_upper` | 95% CI upper bound | g |
| `pre_post` | 0 = post-test design; 1 = gain score design | Binary |

### F4. Sign Convention

**Positive Hedges' g** = AI agent condition outperforms comparison
**Negative Hedges' g** = Comparison condition outperforms AI agent

Always code so that positive g = AI benefit. If the paper reports the comparison group mean first, reverse the sign.

---

## Part G: Study Quality (Risk of Bias)

Adapted from Cochrane Risk of Bias 2.0 for educational intervention research:

### G1-G7 Variables

| Variable | Code | Criteria |
|----------|:----:|---------|
| `rob_randomization` | 0/1/2 | 0=High risk, 1=Some concerns, 2=Low risk |
| `rob_allocation` | 0/1/2 | Concealment of group assignment |
| `rob_blinding_participants` | 0/1/2 | Participants unaware of condition (2=blinded; often N/A in ed research) |
| `rob_blinding_outcome` | 0/1/2 | Outcome assessors unaware of condition |
| `rob_incomplete_data` | 0/1/2 | Attrition handled appropriately (LOCF, intent-to-treat) |
| `rob_selective_reporting` | 0/1/2 | All pre-registered outcomes reported |
| `rob_other` | 0/1/2 | Contamination; expectancy effects; design threats |
| `rob_overall` | 0/1/2 | Overall risk of bias judgment |

**Educational Research Note**: Blinding of participants (G3) is typically not feasible in educational AI studies. Code 1 (some concerns) as default unless there is specific reason to code otherwise.

---

## Part H: Coding Procedures

### H1. Coder Training Sequence

1. Both coders read this manual independently
2. Meet to discuss all variables; clarify questions
3. Pilot code 5 studies independently
4. Compare all decisions; calculate initial kappa
5. Discuss each discrepancy citing specific text from the paper
6. Update decision rules if needed (document in `06_decisions/decision_log.md`)
7. Repeat pilot if kappa < 0.80

### H2. Independent Coding Phase

1. Each coder codes all included studies independently
2. Use the Excel/Google Sheets coding template (one row per effect size)
3. Document evidence for each subjective decision in the `notes` column
4. **Do not discuss coding decisions** during independent phase
5. Complete coding within 2 weeks (both coders)

### H3. Kappa Calculation Schedule

Calculate Cohen's kappa after:
- 5-study pilot (calibration)
- 20% of studies coded (interim check)
- All studies coded (final reliability)

Variables requiring kappa calculation: `oversight_level`, `architecture`, `agency_level`, `agent_role`, `modality`, `technology`, `adaptivity`, `context`, `domain`, `outcome_type`, `blooms_level`, `measurement_type`, `timing`, `design`, `control_type`

### H4. Ambiguity Documentation

When uncertain about a coding decision:
1. Note the uncertainty in the `notes` column
2. Record what information led to the uncertainty
3. Do NOT leave the field blank — make a best judgment and flag it
4. During conflict resolution, flagged cases receive priority discussion

---

## Part I: Decision Trees for Ambiguous Cases

### I1. Is This Study in Scope?

See `02_study_selection/inclusion_exclusion_criteria.md` Section 5 for decision trees.

### I2. Oversight Level When Both AI and Human Are Active

```
Who makes the primary pedagogical decisions during the session?

AI only → Code 1 (Fully Autonomous)
AI primarily, with human override capability → Is override triggered automatically?
    YES, at defined conditions → Code 2 (AI-Led with Checkpoints)
    NO, only if instructor chooses → Code 2 (still AI-led)
Human primarily, using AI tools → Code 3 (Human-Led with AI Support)
```

### I3. Multiple Outcomes in One Study

```
Study reports N distinct outcomes → Extract N separate effect sizes
Each effect size gets same study-level codes (B, C, D)
Each effect size gets its own outcome codes (E1-E4)
Each effect size gets its own statistical data (F)
```

---

*Version 1.0. This manual will be updated based on pilot coding experience. All updates logged in `06_decisions/decision_log.md`.*
