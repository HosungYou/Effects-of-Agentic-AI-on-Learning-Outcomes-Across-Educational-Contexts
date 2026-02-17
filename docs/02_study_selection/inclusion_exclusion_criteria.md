# Inclusion and Exclusion Criteria

## Overview

This document defines the complete inclusion and exclusion criteria for study selection in the meta-analysis of Agentic AI effects on learning outcomes. Criteria follow the PICOS framework (Population, Intervention, Comparison, Outcome, Study design) adapted for educational meta-analysis.

---

## 1. PICOS Framework

| PICOS Element | Include | Exclude |
|---------------|---------|---------|
| **Population** | Learners in K-12, higher education, workplace, professional, or continuing education settings | Non-learner populations (e.g., patients without learning objective, general public using AI for non-educational purposes) |
| **Intervention** | AI agent system with autonomous action capability | Simple search tools, static content, passive AI, non-agentic software |
| **Comparison** | No AI, non-agentic AI, traditional instruction, or different AI agency level | No comparison group (descriptive use only) |
| **Outcome** | At least one quantitative learning outcome | Satisfaction/usability only, system performance metrics only |
| **Study Design** | Experimental, quasi-experimental, pre-post comparison | Purely qualitative, case study, survey-only, design-based research without quantitative outcomes |

---

## 2. Detailed Inclusion Criteria

### IC1: Study Design

**Include** if the study uses:
- **Randomized Controlled Trial (RCT)**: Random assignment to AI agent condition vs. comparison
- **Quasi-experimental design**: Non-random assignment with a control or comparison group (e.g., matched groups, classroom-level assignment)
- **Pre-post within-subjects design**: Same participants measured before and after AI agent intervention (requires pre-test and post-test data)
- **Cross-over design**: Participants experience both conditions with washout period (extract data for each period separately)

**Borderline cases**:
- Single-group pre-post designs with no comparison are **included if** they provide sufficient data for pre-post effect size calculation (d = (M_post - M_pre) / SD_pre or SD_pooled)
- Regression discontinuity designs: **Include** if effect size is calculable

### IC2: Intervention Specification

**Include** if the AI system demonstrates at least ONE of the following autonomous capabilities:

| Capability | Operational Definition | Examples |
|-----------|----------------------|----------|
| **Adaptive Response** | System adjusts content, difficulty, pacing, or feedback automatically based on learner input | ITS difficulty adjustment; adaptive quiz systems; personalized content sequencing |
| **Proactive Intervention** | System initiates interactions without explicit learner request | Alert system detecting confusion; unsolicited hint generation; proactive encouragement messages |
| **Automated Assessment** | System independently evaluates learner work and generates substantive feedback | Automated essay scoring with feedback; intelligent code review; automated problem-set grading |
| **Recommendation Generation** | System suggests learning paths, resources, or strategies without human instructor approval | Next-step recommenders; resource suggestion engines; learning path planners |
| **Dialogue Management** | System maintains contextually aware multi-turn conversation about learning content | Socratic dialogue tutors; conversational ITS; pedagogical chatbots with knowledge state tracking |
| **Multi-Agent Coordination** | Multiple AI agents collaborate to support learning with different specialized roles | Tutor agent + assessor agent; coach agent + facilitator agent combinations |

### IC3: Comparison Condition

**Include** if the study compares AI agent condition to at least one of:
- No AI agent (traditional instruction only)
- Non-agentic AI (e.g., static content delivery, simple keyword FAQ)
- Different AI agency level (e.g., fully autonomous vs. human-supervised)
- Waitlist control
- Business-as-usual instruction

**Borderline cases**:
- Studies comparing two different AI agents: **Include** and code both conditions; treat as moderator comparison
- Studies with historical controls: **Include** with high risk of bias rating

### IC4: Learning Outcome

**Include** if the study reports at least one of:

| Outcome Type | Examples |
|-------------|---------|
| **Cognitive (Knowledge)** | Factual recall, conceptual understanding, comprehension tests, knowledge assessments |
| **Skill-based** | Procedural skill performance, problem-solving tasks, writing skills, coding skills |
| **Affective** | Motivation, self-efficacy, academic engagement, attitude toward learning, persistence |
| **Performance** | Job performance tasks, transfer tests, real-world application measures, simulation performance |

**Exclude** if outcomes are ONLY:
- User satisfaction or usability ratings
- System performance (AI accuracy, response time)
- Learner perceptions of AI without linking to performance
- Teacher/instructor evaluations of AI (not linked to learning outcome)

### IC5: Educational Context

**Include** any of:
- **K-12 Education**: Kindergarten through grade 12 (ages ~5-18); formal schooling
- **Higher Education**: Undergraduate, graduate, professional degree programs at accredited institutions
- **Workplace Training**: Employer-sponsored training; organizational training programs; on-the-job training
- **Professional Education**: Continuing education for licensed professionals (medical, legal, engineering, teaching); certification programs
- **Continuing Education**: Adult education programs, lifelong learning, non-degree seeking education

**Exclude**:
- Pure laboratory experiments without realistic learning context
- AI agent used for entertainment/gaming without explicit learning objectives
- AI used for clinical decision support without educational component

### IC6: Quantitative Data Sufficiency

**Include** if the study provides sufficient statistical data for effect size calculation:

| Data Type | Sufficient for ES? |
|-----------|:-:|
| Means + SDs + sample sizes (treatment and control) | Yes |
| t-statistic + sample sizes | Yes |
| F-statistic (df = 1 for treatment) + sample sizes | Yes |
| Correlation coefficient (r) + sample size | Yes |
| Odds ratio + sample sizes | Yes |
| Chi-square + sample sizes (for binary outcomes) | Yes (limited) |
| p-value only (without test statistic) | Borderline - attempt estimation |
| Effect size reported by authors (d, g, eta-squared) | Yes |
| "Significant" or "not significant" without statistics | No |

**Protocol for insufficient data**:
1. Attempt to extract from tables, figures, or supplementary materials
2. Contact corresponding author (one email; 2-week response window)
3. If still insufficient after contact attempt, exclude with reason documented

### IC7: Language

**Include**: English-language publications only

**Rationale**: Consistent with most prior educational meta-analyses; ensures coding reliability; feasible with current research team

### IC8: Publication Type

**Include**:
- Peer-reviewed journal articles (all disciplines)
- Conference papers with full-text peer review (proceedings)
- Published dissertations (if peer-reviewed or defended)

**Exclude**:
- Editorials, commentaries, opinion pieces
- Book reviews, book chapters (unless specific empirical chapter)
- Conference abstracts without full text
- Non-peer-reviewed reports, white papers
- Unpublished manuscripts (unless available as pre-print with sufficient peer indication)

---

## 3. Exclusion Criteria

### EC1: Study Design Exclusions

**Exclude** if:
- Purely qualitative study (interviews, observation, content analysis without quantitative outcomes)
- Single-group study with no pre-test (post-test only, no comparison)
- Survey study measuring perceptions only (no behavioral outcome)
- Design-based research/development study without comparative experimental component
- N-of-1 or single-subject design (too small for meta-analytic inclusion)

### EC2: Intervention Exclusions

**Exclude** if the AI system is:
- Simple FAQ or keyword-based chatbot with scripted responses and no adaptation
- Static content delivery system (PDFs, videos with no interaction)
- Calculator or formula tool without pedagogical intelligence
- Search engine (Google, etc.) used in educational context
- Generic recommendation system not designed for learning (Netflix-style)
- Human tutor or human teaching assistant (even if using AI tools)
- Automated grading without feedback (grading-only, no instructional component)

### EC3: Comparison Exclusions

**Exclude** if:
- No comparison condition (descriptive use study, satisfaction survey only)
- Comparison is inadequately described to determine condition type
- Pre-post within the AI agent condition only with no baseline comparison

### EC4: Outcome Exclusions

**Exclude** if outcomes are ONLY:
- Satisfaction/usability/user experience ratings
- AI system performance metrics (accuracy, F1 score, BLEU score)
- Engagement metrics without cognitive outcome (time-on-task only)
- Technology acceptance (TAM measures only)
- Instructor perceptions without learner outcome data

### EC5: Context Exclusions

**Exclude** if:
- Pure laboratory experiment without ecological validity (no actual learners; undergraduate convenience sample in non-educational AI study)
- AI agent used for non-educational purposes (medical diagnosis, route planning, retail)
- Simulation study without human learners (agent simulation only)

### EC6: Data Exclusions

**Exclude** if:
- Insufficient statistical data even after author contact
- Authors declined to provide data
- Data reported only graphically with no way to extract numerical values

### EC7: Language Exclusion

**Exclude**: Non-English publications

### EC8: Publication Type Exclusion

**Exclude**:
- Editorials, commentaries, letters to editor
- Book reviews
- Conference abstracts only (no full paper)
- Non-peer-reviewed sources (blog posts, newspaper articles)

---

## 4. Definition of "Agentic AI"

A core operationalization challenge is defining what constitutes "Agentic AI" for this review.

### 4.1 Operational Definition

An AI system qualifies as **Agentic AI** if it satisfies BOTH conditions:
1. **Autonomy**: The system makes decisions and takes actions without explicit human instruction for each action
2. **Goal-directedness**: The system's autonomous actions are oriented toward a learning objective

### 4.2 Minimum Agenticity Threshold

Systems qualify if they demonstrate at least one of the six capabilities in IC2. This threshold is:
- **Conservative enough** to exclude simple, passive AI tools
- **Broad enough** to include the full spectrum from adaptive ITS to LLM-based agents

### 4.3 Non-Agentic Examples (Excluded)

| System Type | Why Excluded |
|-------------|-------------|
| YouTube educational videos | No adaptation, no interaction |
| Google Classroom (without AI features) | No autonomous AI action |
| Static quiz platform (no adaptive features) | No adaptation |
| Turnitin plagiarism checker | No learning feedback |
| Google Translate used for language learning | No pedagogical intelligence |
| Pre-programmed linear tutorial | No adaptation to learner state |

---

## 5. Borderline Case Decision Trees

### 5.1 Decision Tree: Is This an "Agentic AI" Intervention?

```
START: Does the system use any AI/ML algorithm?
    |
    NO ---> EXCLUDE (not AI)
    |
    YES
    |
    v
Does the system respond differently to different learners?
    |
    NO ---> EXCLUDE (static AI, not agentic)
    |
    YES
    |
    v
Does the system make any autonomous decisions about learning content,
sequencing, feedback, or interaction timing?
    |
    NO ---> EXCLUDE (AI tool, not agent)
    |
    YES
    |
    v
Is the AI the primary intervention (not just a minor tool)?
    |
    NO ---> BORDERLINE: Code as primary intervention if
    |       AI component is explicitly tested
    |
    YES
    |
    v
INCLUDE as Agentic AI
```

### 5.2 Decision Tree: Is There a Valid Comparison Condition?

```
START: Does the study have more than one condition?
    |
    NO ---> Is there a pre-test and post-test?
    |           |
    |           NO ---> EXCLUDE
    |           |
    |           YES ---> INCLUDE as pre-post design (single group)
    |
    YES
    |
    v
Is the comparison condition explicitly described?
    |
    NO ---> BORDERLINE: Include if control can be inferred from context
    |
    YES
    |
    v
Is the comparison free from AI agent intervention?
(or different AI agency level)
    |
    NO ---> INCLUDE if comparing AI agent levels (code appropriately)
    |
    YES
    |
    v
INCLUDE
```

### 5.3 Decision Tree: Is There a Valid Learning Outcome?

```
START: What does the study measure?
    |
    |---> Cognitive test (knowledge, comprehension) ---> INCLUDE
    |
    |---> Skill assessment (procedural, problem-solving) ---> INCLUDE
    |
    |---> Affective measure (motivation, self-efficacy) ---> INCLUDE
    |
    |---> Performance measure (job performance, transfer) ---> INCLUDE
    |
    |---> Satisfaction/usability ONLY ---> EXCLUDE
    |
    |---> System performance (AI accuracy) ONLY ---> EXCLUDE
    |
    |---> Combination: Learning outcome + satisfaction ---> INCLUDE
                       (extract learning outcome only)
```

---

## 6. Pilot Screening Calibration

### 6.1 Pre-Screening Agreement Exercise

Before independent screening, both reviewers independently code 20 articles (10 clear include, 5 clear exclude, 5 borderline). Calculate agreement and resolve disagreements.

**Target**: >80% agreement before proceeding to independent screening.

### 6.2 Calibration Studies (Pre-identified)

The following studies are pre-coded as calibration examples:

| Study | Decision | Rationale |
|-------|----------|-----------|
| Dai et al. (2024) - Primary seed | INCLUDE | AI virtual agent meta-analysis; relevant to our review |
| [Studies identified during pilot search] | [To be determined] | |

### 6.3 Grey-Area Resolution

When both reviewers disagree and cannot resolve through discussion:
1. Re-read relevant sections of inclusion/exclusion criteria together
2. Code the specific criterion in question (which criterion applies?)
3. If still unresolved, consult third reviewer (project advisor)
4. Document decision with rationale

---

## 7. Reporting and Documentation

### 7.1 Exclusion Reason Documentation

For each excluded study at full-text stage, document the primary exclusion reason using codes:

| Code | Reason |
|------|--------|
| EC1 | Wrong study design |
| EC2 | Intervention not agentic AI |
| EC3 | No valid comparison condition |
| EC4 | No learning outcome reported |
| EC5 | Wrong population/context |
| EC6 | Insufficient quantitative data |
| EC7 | Non-English |
| EC8 | Wrong publication type |
| EC9 | Duplicate (retained in primary database) |

**One primary reason only** — use the first applicable code in the list above.

### 7.2 PRISMA Flow Counts

Track at each stage:
- Total records identified per database
- Duplicates removed
- Records screened (title/abstract)
- Records excluded with reasons at T/A stage
- Full texts assessed
- Full texts excluded with reasons (documented per study)
- Studies included in quantitative synthesis

---

## 8. Updates to Criteria

Any changes to inclusion/exclusion criteria after protocol registration must be:
1. Documented in the decision log (`06_decisions/decision_log.md`)
2. Applied consistently to all studies (retroactive if applicable)
3. Reported as a deviation from pre-registered protocol in the manuscript

---

*These criteria were developed following PRISMA 2020 guidelines and adapted from Dai et al. (2024) and Pigott & Polanin (2020) best practices for educational meta-analyses.*
