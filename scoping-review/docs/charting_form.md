# Data Charting Form — Trust in Educational AI Scoping Review

## Overview

This charting form follows JBI scoping review methodology (Peters et al., 2020). Data is extracted in a single pass during full-text assessment. Variables are designed to map onto the two-level trust-calibrated oversight framework.

---

## Charting Variables

### A. Study Identification

| Variable | Type | Options/Format |
|----------|------|----------------|
| `study_id` | Auto | SCR_0001, SCR_0002, ... |
| `first_author` | Text | Last name |
| `year` | Numeric | 2015-2026 |
| `title` | Text | Full title |
| `journal` | Text | Journal/conference name |
| `country` | Text | Country of data collection (or first author affiliation if multi-country) |
| `doi` | Text | DOI string |

### B. Study Design

| Variable | Type | Options |
|----------|------|---------|
| `study_type` | Categorical | Quantitative / Qualitative / Mixed Methods / Conceptual / Review / Design-based |
| `study_design_detail` | Text | e.g., "Cross-sectional survey", "Experimental RCT", "Phenomenological interview", "SEM" |
| `sample_size` | Numeric | Total N (0 for conceptual/review papers) |
| `population` | Text | e.g., "undergraduate students", "K-12 teachers", "medical residents" |
| `educational_level` | Categorical | K-12 / Undergraduate / Graduate / Professional / Adult/Continuing / Mixed / Not specified |

### C. AI System

| Variable | Type | Options |
|----------|------|---------|
| `ai_system_type` | Categorical | ITS / Chatbot / Generative AI (ChatGPT, etc.) / AI Writing Assistant / AI Tutoring Agent / Agentic AI / Recommendation System / AI Assessment / Other |
| `ai_system_name` | Text | Specific name if given (e.g., "ChatGPT", "AutoTutor", "Khanmigo") |
| `ai_system_description` | Text | Brief description of the system |
| `ai_autonomy_level` | Categorical | Fully autonomous / AI-led with checkpoints / Human-led with AI support / Advisory only / Not specified |

### D. Trust Construct (Core Variables)

| Variable | Type | Options |
|----------|------|---------|
| `trust_construct` | Categorical | Trust in AI / Reliance / Resistance / Overtrust / Distrust / Calibrated trust / Trustworthiness / General trust / Multiple |
| `trust_definition_provided` | Categorical | Yes (explicit definition) / No / Implicit (trust discussed but not defined) |
| `trust_definition_text` | Text | Verbatim definition if provided (quote with page number) |
| `trust_theoretical_framework` | Categorical | Lee & See (2004) / Mayer et al. (1995) / TAM / UTAUT / S-O-R / Hoff & Bashir (2015) / McKnight et al. (2011) / None explicit / Other |
| `trust_framework_other` | Text | If Other, specify |

### E. Trust Measurement

| Variable | Type | Options |
|----------|------|---------|
| `trust_measurement` | Categorical | Survey/Scale / Behavioral measure / Interview / Observation / Mixed / Not measured (conceptual) |
| `trust_scale_name` | Text | Name of scale if survey (e.g., "Trust in Automation scale", "Jian et al., 2000") |
| `trust_scale_items` | Numeric | Number of items |
| `trust_reliability` | Text | Reported reliability (e.g., "Cronbach's alpha = .89") |

### F. Trust in the Model

| Variable | Type | Options |
|----------|------|---------|
| `trust_role_in_model` | Categorical | DV (outcome) / IV (predictor) / Mediator / Moderator / Not modeled / Descriptive only |
| `trust_antecedents` | Text | What predicts trust? (list variables) |
| `trust_outcomes` | Text | What does trust predict? (list variables) |
| `trust_key_finding` | Text | 1-2 sentence summary of main trust-related finding |

### G. Trust Calibration (Key Gap Variables)

| Variable | Type | Options |
|----------|------|---------|
| `calibration_discussed` | Boolean | Yes / No |
| `calibration_definition` | Text | How calibration is defined/described (if discussed) |
| `calibration_mechanism` | Categorical | Internal (self-directed learning, metacognition) / External (teacher/system checkpoint) / Both / N/A |
| `overtrust_discussed` | Boolean | Yes / No |
| `overtrust_evidence` | Text | Evidence/findings related to overtrust |
| `distrust_discussed` | Boolean | Yes / No |
| `distrust_evidence` | Text | Evidence/findings related to distrust |

### H. Oversight and Design (Level 2 Variables)

| Variable | Type | Options |
|----------|------|---------|
| `oversight_discussed` | Boolean | Yes / No |
| `oversight_level` | Categorical | Fully autonomous / AI-led with checkpoints / Human-led with AI support / Full human control / Not specified |
| `oversight_recommendation` | Text | Any recommendations for human oversight design |
| `design_implications` | Text | Any implications for educational AI design mentioned |
| `checkpoint_mechanism` | Text | Any checkpoint or intervention mechanism described |

### I. Framework Mapping

| Variable | Type | Options |
|----------|------|---------|
| `maps_to_level1` | Boolean | Does this study address Level 1 (Learner --> Trust --> Reliance/Resistance --> Use)? |
| `maps_to_level2` | Boolean | Does this study address Level 2 (Designer --> Checkpoint --> Trust Calibration --> Level 1)? |
| `level1_evidence` | Text | Specific evidence for Level 1 mapping |
| `level2_evidence` | Text | Specific evidence for Level 2 mapping |
| `framework_gap_notes` | Text | What's missing from this study's perspective? |

### J. Quality Indicators (for context, not formal appraisal)

| Variable | Type | Options |
|----------|------|---------|
| `peer_reviewed` | Boolean | Yes / No |
| `citation_count` | Numeric | From Google Scholar or Semantic Scholar |
| `limitations_noted` | Text | Key limitations noted by authors |

---

## Charting Process

1. **Retrieve full text** via DOI + university library access
2. **Skim structure**: Read abstract, introduction conclusion, and methods
3. **Extract Section A-B**: Study identification and design (quick factual extraction)
4. **Extract Section C**: AI system details (usually in methods/intervention description)
5. **Extract Section D-F**: Trust construct details (the core of the charting -- read carefully)
6. **Extract Section G-H**: Trust calibration and oversight (read discussion section carefully)
7. **Map to framework (Section I)**: Researcher judgment based on full reading
8. **Note quality indicators (Section J)**: Quick factual extraction

**Estimated time**: 5-8 minutes per paper

---

## CSV Column Headers

For data entry, use these exact column headers:

```
study_id,first_author,year,title,journal,country,doi,study_type,study_design_detail,sample_size,population,educational_level,ai_system_type,ai_system_name,ai_system_description,ai_autonomy_level,trust_construct,trust_definition_provided,trust_definition_text,trust_theoretical_framework,trust_framework_other,trust_measurement,trust_scale_name,trust_scale_items,trust_reliability,trust_role_in_model,trust_antecedents,trust_outcomes,trust_key_finding,calibration_discussed,calibration_definition,calibration_mechanism,overtrust_discussed,overtrust_evidence,distrust_discussed,distrust_evidence,oversight_discussed,oversight_level,oversight_recommendation,design_implications,checkpoint_mechanism,maps_to_level1,maps_to_level2,level1_evidence,level2_evidence,framework_gap_notes,peer_reviewed,citation_count,limitations_noted
```

---

## RAG-Assisted Extraction Queries

When using RAG (diverga:i3) for batch extraction, use these prompts per variable:

```
Trust construct: "What trust-related construct does this paper study? (trust, reliance, resistance, overtrust, distrust, calibration)"
Trust definition: "Does this paper provide an explicit definition of trust? If so, quote it with page number."
Theoretical framework: "What theoretical framework guides the trust analysis? (Lee & See, Mayer, TAM, UTAUT, S-O-R, other)"
Trust measurement: "How is trust measured in this study? (survey, behavioral, interview, not measured)"
Trust role: "What role does trust play in the model? (DV, IV, mediator, moderator, not modeled)"
Calibration: "Does this paper discuss trust calibration, overtrust, undertrust, or appropriate trust? Quote relevant passages."
Oversight: "Does this paper discuss human oversight, checkpoints, or AI autonomy levels in educational contexts?"
```

---

## Template Row (Example)

| Variable | Example Value |
|----------|---------------|
| study_id | SCR_0001 |
| first_author | Wang |
| year | 2025 |
| title | Understanding trust and reliance... |
| trust_construct | Trust in AI, Reliance, Resistance |
| trust_definition_provided | Yes |
| trust_theoretical_framework | S-O-R |
| trust_measurement | Survey/Scale |
| trust_role_in_model | Mediator |
| calibration_discussed | No |
| oversight_discussed | No |
| maps_to_level1 | Yes |
| maps_to_level2 | No |
