# Data Provenance Documentation

## Overview
This document describes the data flow, processing stages, and quality assurance steps for the Agentic AI Learning Outcomes meta-analysis.

## Data Flow Diagram

```
Raw Data (00_raw)
    ↓
Title/Abstract Screening (01_screened)
    ↓
Full-Text Extraction (02_extracted)
    ↓
Study Coding (03_coded)
    ↓
Final Dataset (04_final)
```

## Processing Stages

### Stage 1: Raw Data Collection (data/00_raw)
**Purpose**: Archive original search results from all databases
**Files**:
- `study_metadata.csv`: Master index of all retrieved studies
- `search_results/`: Database-specific search outputs
  - web_of_science_results.csv
  - scopus_results.csv
  - eric_results.csv
  - psycinfo_results.csv
  - ieee_xplore_results.csv
  - acm_digital_library_results.csv

**QA Steps**:
- Verify all database searches completed
- Check for duplicate entries across databases
- Record search query strings and result counts
- Archive original export files with timestamps

### Stage 2: Screening (data/01_screened)
**Purpose**: Remove irrelevant studies based on title/abstract
**Input**: Raw study metadata
**Output**: Screened studies with inclusion/exclusion decisions
**Files**:
- `screening_results.csv`: Study ID, screening decision, reason codes
- `screening_log.txt`: Timestamp, screener ID, number processed

**QA Steps**:
- Calculate inter-rater reliability (Cohen's kappa) for 20% sample
- Verify minimum kappa ≥ 0.70
- Document disagreement resolution process
- Calculate precision/recall against expert review sample

**AI Pipeline Provenance**:
- Record which model performed screening (Claude/GPT-4o/Llama)
- Track consensus decisions (if 2/3 models agreed)
- Document edge cases sent to human review
- Calculate model agreement rate

### Stage 3: Extraction (data/02_extracted)
**Purpose**: Extract study characteristics, design, and descriptive statistics
**Input**: Full texts of included studies
**Output**: Structured study data with raw effect size information
**Files**:
- `extraction_data.csv`: Study characteristics, sample sizes, outcomes
- `raw_effect_sizes.csv`: Means, SDs, t-values, correlations, etc.
- `extraction_log.csv`: Extractor ID, completion date, notes

**QA Steps**:
- Double-code 20% of studies for reliability
- Verify required fields populated (n, outcomes, design)
- Cross-check reported statistics (e.g., t-values vs effect sizes)
- Document missing data and imputation decisions
- Verify no duplicate or overlapping samples

**AI Pipeline Provenance**:
- Record extraction model and prompt version
- Document any model hallucinations/errors detected in human review
- Track confidence scores if available
- Log corrected vs. AI-generated values

### Stage 4: Coding (data/03_coded)
**Purpose**: Code moderator variables and intervention characteristics
**Input**: Extracted study data
**Output**: Full coded dataset ready for meta-analysis
**Files**:
- `coded_data.csv`: All moderators, intervention characteristics, outcome coding
- `coding_codebook.csv`: Variable names, codes, value labels
- `coding_log.csv`: Coder ID, date, number of studies
- `discrepancies.csv`: Inter-rater disagreements and resolutions

**QA Steps**:
- Calculate inter-rater reliability (Cohen's kappa or ICC) on 20% sample
- Verify minimum kappa ≥ 0.70 for categorical variables
- Check for out-of-range or invalid codes
- Verify logical consistency across variables
- Document any imputation or inference decisions

**AI Pipeline Provenance**:
- Record AI models used for coding (primary/secondary/tertiary)
- Track consensus vs. non-consensus decisions
- Document human override rate (times human disagreed with AI)
- Calculate per-variable agreement rates

**Moderators Coded**:
- Human oversight level (fully autonomous, AI-led checkpoints, human-led)
- Agent architecture (single vs. multi-agent)
- Agency level per APCP framework
- Agent role (tutor, coach, assessor, collaborator, facilitator)
- Learning context (K-12, higher ed, workplace, etc.)
- Outcome type (cognitive, skill-based, affective, performance)
- Bloom's taxonomy level of outcomes
- Domain (math, science, language, generic, etc.)
- Publication year
- Sample size per group
- Study quality indicators

### Stage 5: Final Dataset (data/04_final)
**Purpose**: Clean, validated dataset ready for meta-analysis
**Input**: Coded data with QA complete
**Output**: Final analysis dataset with no missing critical values
**Files**:
- `final_dataset.csv`: Complete analysis dataset
- `effect_sizes.csv`: Computed effect sizes (Hedges' g), variances, weights
- `study_summary.csv`: One row per study with summary statistics
- `DATA_QUALITY_REPORT.txt`: Summary of QA steps and decisions

**QA Steps**:
- Verify all critical fields populated
- Check distribution of effect sizes (identify outliers)
- Verify effect size calculations
- Confirm no duplicate studies
- Generate final quality report
- Document any decisions affecting analysis

## AI vs. Human Coding Provenance

### Screening Level (Title/Abstract)
- **Primary Method**: AI consensus voting (Claude, GPT-4o, Llama)
- **Arbitration**: Human review for non-consensus or low-confidence cases
- **Tracking**: Screen_ai_decision, Screen_ai_confidence, Screen_human_override
- **IRR Baseline**: All human baseline established on 100 studies

### Extraction Level (Full Text)
- **Primary Method**: AI extraction with human verification
- **High-Risk Fields**: Flagged for mandatory human review
- **Tracking**: Extract_ai_model, Extract_human_verified, Extract_corrections
- **IRR Baseline**: 20% sample double-coded by humans

### Coding Level (Moderators)
- **Primary Method**: AI coding with human review (consensus + random 20%)
- **Discrepancies**: Dual-coded to consensus
- **Tracking**: Code_ai_decision, Code_ai_confidence, Code_human_override, Code_final
- **IRR Baseline**: Cohen's kappa calculated on all disagreements

## Quality Assurance Summary

| Stage | Method | Sample | Threshold | Metric |
|-------|--------|--------|-----------|--------|
| Screening | AI + Human | 100% | κ ≥ 0.70 | Cohen's kappa |
| Extraction | Human + AI | 20% | κ ≥ 0.70 | Cohen's kappa |
| Coding | Human + AI | 100% consensus + 20% random | κ ≥ 0.70 | Cohen's kappa |
| Effect Size | Calculation verification | 100% | r = 0.99+ | Correlation check |

## Missing Data Handling

- **Screening**: Excluded if insufficient abstract information
- **Extraction**: Imputation using donor studies if <5% missing within variable
- **Coding**: Multiple imputation if >5% missing (documented in analysis)
- **Effect Sizes**: Studies excluded if cannot compute or estimate ES

## Conflict Resolution Process

1. **Identification**: Automated flagging of AI/human disagreements
2. **Documentation**: Log all discrepancies with context
3. **Discussion**: Third reviewer if disagreement persists
4. **Resolution**: Decision recorded with rationale
5. **Lessons Learned**: Feedback to improve AI prompts/training

## Data Versioning

- **Version Control**: All data files tracked in git
- **Timestamps**: Each processing stage includes processing date
- **Commits**: Atomic commits for each QA approval
- **Release Tags**: Semantic versioning for finalized datasets

## Limitations & Known Issues

Document any known limitations, data quality issues, or analytical decisions that affect interpretation of results.

---

**Last Updated**: [DATE]
**Data Manager**: [NAME]
**QA Approver**: [NAME]
