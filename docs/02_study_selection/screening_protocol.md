# Screening Protocol

## Overview

This document defines the two-phase screening protocol for study selection, including procedures for independent review, conflict resolution, intercoder reliability assessment, and pilot screening calibration. The protocol follows PRISMA 2020 guidelines for systematic reviews.

---

## 1. Screening Phases Overview

```
Phase 1: Title and Abstract Screening
    |
    Input: All deduplicated records (~4,000-8,000)
    Process: 2 independent reviewers; binary include/exclude decision
    Output: Records advancing to full-text review (~200-400)
    |
    v
Phase 2: Full-Text Screening
    |
    Input: Records from Phase 1 (~200-400)
    Process: 2 independent reviewers; systematic I/E criteria check
    Output: Included studies for data extraction (~40-80)
    |
    v
Data Extraction & Coding
```

---

## 2. Software and Tools

### 2.1 Primary Platform

**Covidence** (https://www.covidence.org)
- Web-based systematic review platform
- Supports duplicate detection, blinded screening, conflict tracking
- Generates PRISMA flow diagram
- Institutional license recommended

**Backup**: Rayyan (https://rayyan.ai) — free alternative with similar functionality

### 2.2 Reference Management

**Zotero** — for reference organization, PDF storage, and group library sharing between reviewers

### 2.3 Communication

- Shared Google Drive folder for notes and deliberation documents
- Agreed schedule for synchronous conflict resolution meetings

---

## 3. Phase 1: Title and Abstract Screening

### 3.1 Purpose

Rapidly identify records that are clearly relevant or clearly irrelevant based on title and abstract information alone. When in doubt, **include** (err on the side of inclusion at this stage).

### 3.2 Information Used

- Title
- Abstract
- Author(s) and year
- Journal/conference name
- Keywords (if available)

**Do NOT** retrieve full text during Phase 1.

### 3.3 Decision Rule

Apply the following binary decision for each record:

| Decision | Criteria |
|----------|---------|
| **INCLUDE** | Title/abstract suggests the study MAY meet all inclusion criteria; uncertain records (when in doubt, include) |
| **EXCLUDE** | Title/abstract clearly indicates the study does NOT meet at least one inclusion criterion |

**Conservative inclusion principle**: If there is any ambiguity about whether a study meets the criteria, **include** it for full-text review. The cost of a false exclude (missing a relevant study) is higher than a false include (reviewing an irrelevant full text).

### 3.4 Rapid Exclusion Signals

Exclude at title/abstract stage only if the record is **clearly** one of the following:

| Signal | Example |
|--------|---------|
| No AI component | "Teacher feedback on student writing" |
| No educational context | "AI agent for financial trading" |
| Not empirical | "Review of AI in education: A conceptual analysis" |
| Wrong language | Abstract in non-English language |
| Wrong time period | Published before 2018 |
| No learning outcome | "User experience of an AI chatbot system" |
| Clearly qualitative | "Teachers' perceptions of AI tools: A grounded theory study" |

### 3.5 Screening Procedure

1. Both reviewers independently screen records in Covidence
2. Covidence records each reviewer's decision (blinded)
3. After both reviewers complete each batch, Covidence reveals conflicts
4. Conflicts are resolved per Section 6 below

### 3.6 Screening Rate

Target: **>50 records per hour** during Phase 1 (approximately 5-10 days total for ~4,000-8,000 records at 2 reviewers)

---

## 4. Phase 2: Full-Text Screening

### 4.1 Purpose

Apply all inclusion/exclusion criteria systematically to the full text of each record to make a definitive include/exclude decision.

### 4.2 Full-Text Retrieval

**Retrieval procedure**:
1. Download PDFs for all records advancing from Phase 1
2. Use DOI lookup (Sci-Hub only as last resort for inaccessible papers)
3. If full text unavailable after 3 attempts: contact corresponding author via institutional email
4. If still unavailable after 1 week: record as "full text not available" and exclude with reason EC8

**Storage**: All PDFs stored in shared Zotero library (encrypted cloud storage)

### 4.3 Systematic Criteria Application

For each record, both reviewers independently assess all 8 inclusion criteria:

| Check | Criterion | Question to Answer |
|-------|-----------|-------------------|
| IC1 | Study design | Is the design experimental, quasi-experimental, or pre-post? |
| IC2 | Intervention | Is the AI system agentic (meets at least 1 of 6 capabilities)? |
| IC3 | Comparison | Is there a valid comparison condition? |
| IC4 | Outcome | Is at least one learning outcome quantitatively reported? |
| IC5 | Context | Is the context K-12, higher ed, workplace, professional, or continuing ed? |
| IC6 | Data | Are sufficient statistics available to compute Hedges' g? |
| IC7 | Language | Is the paper in English? |
| IC8 | Publication type | Is this a peer-reviewed article or conference paper? |

**Decision**: INCLUDE only if ALL 8 criteria are satisfied.

### 4.4 Exclusion Reason Documentation

For each excluded study, document the **primary** exclusion reason code (EC1-EC8) using the codes defined in `inclusion_exclusion_criteria.md`. Record the specific problematic criterion and the page/section of the paper that led to the decision.

**Format**:
```
Study ID: [Author, Year]
Decision: EXCLUDE
Primary Reason: EC2 (Intervention not agentic AI)
Relevant Text: "The AI system provided pre-written feedback templates..."
Section: Methods, p. 4
Coder: [Initials]
```

### 4.5 Screening Rate

Target: **~5-10 records per hour** during Phase 2 (requiring ~2-4 weeks for 200-400 records)

---

## 5. Pilot Screening Procedure

### 5.1 Purpose and Timing

The pilot screening occurs **before** independent screening begins to:
- Calibrate reviewer understanding of criteria
- Identify ambiguous criteria needing clarification
- Achieve acceptable inter-rater agreement (kappa ≥ 0.80) before proceeding

**Timing**: One week before independent screening begins

### 5.2 Pilot Set Composition

**Phase 1 Pilot** (Title/Abstract):
- 50 records randomly selected from deduplicated pool
- Stratified: ~30 clearly relevant, ~10 clearly irrelevant, ~10 borderline

**Phase 2 Pilot** (Full-Text):
- 10 full-text papers
- Stratified: ~5 include, ~3 exclude, ~2 borderline

### 5.3 Pilot Procedure

1. Both reviewers independently code pilot set
2. Calculate percent agreement and Cohen's kappa
3. Compare decisions on all records
4. Discuss each discrepancy with specific reference to criteria
5. Update coding guide with clarifications if needed
6. **If kappa < 0.70**: Revise criteria, conduct another pilot round
7. **If 0.70 ≤ kappa < 0.80**: Review specific problematic criteria; targeted retraining
8. **If kappa ≥ 0.80**: Proceed to independent screening

### 5.4 Kappa Target

| Phase | Minimum Acceptable | Target |
|-------|:-----------------:|:------:|
| Phase 1 (Title/Abstract) | κ ≥ 0.75 | κ ≥ 0.80 |
| Phase 2 (Full-Text) | κ ≥ 0.80 | κ ≥ 0.85 |

---

## 6. Conflict Resolution Procedure

### 6.1 Definition of Conflict

A conflict occurs when:
- Reviewer 1 codes INCLUDE; Reviewer 2 codes EXCLUDE (or vice versa)
- Reviewers agree to include but assign different primary reasons for uncertain decisions

### 6.2 Conflict Resolution Steps

**Step 1: Independent re-review**
- Each reviewer independently re-reads the abstract/full text
- Each writes a one-sentence rationale for their decision citing the specific criterion

**Step 2: Deliberation**
- Reviewers share written rationales (asynchronously via shared document)
- Both reviewers discuss discrepancy with reference to the inclusion/exclusion criteria document
- Discussion limited to factual content of the paper (not opinions about the field)

**Step 3: Consensus decision**
- If discussion resolves the conflict: record consensus decision with rationale
- Document which criterion was the basis for resolution

**Step 4: Third-party arbitration (if needed)**
- If reviewers cannot reach consensus after Step 2: escalate to project supervisor
- Project supervisor makes binding decision with written rationale
- Both reviewers acknowledge the decision

**Target**: Resolve >95% of conflicts through Steps 1-2 without arbitration

### 6.3 Conflict Rate Tracking

Track conflict rates across batches:
- High conflict rate in a batch (>30%) may indicate criteria need clarification
- Document systematic patterns in conflicts for protocol refinement

---

## 7. Inter-Rater Reliability Calculation

### 7.1 Agreement Statistics

**Phase 1 (Title/Abstract Screening)**:
- **Percent agreement**: (Number of agreements / Total records) × 100
- **Cohen's kappa**: κ = (Po - Pe) / (1 - Pe)
  - Po = observed agreement proportion
  - Pe = expected agreement by chance
- **Target**: κ ≥ 0.80

**Phase 2 (Full-Text Screening)**:
- Same statistics as Phase 1
- Additionally calculate kappa per criterion (IC1-IC8)
- This helps identify which criteria are most ambiguous
- **Target**: κ ≥ 0.80 overall; κ ≥ 0.75 per criterion

### 7.2 Kappa Interpretation

| Kappa Range | Interpretation | Action |
|-------------|----------------|--------|
| < 0.40 | Poor agreement | Stop; revise criteria; full retraining |
| 0.40-0.60 | Moderate agreement | Identify problematic criteria; targeted retraining |
| 0.61-0.80 | Substantial agreement | Proceed with monitoring; resolve conflicts carefully |
| > 0.80 | Almost perfect agreement | Proceed with full independent screening |

### 7.3 Kappa Reporting

Report the following in the manuscript:
- Kappa for Phase 1 title/abstract screening
- Kappa for Phase 2 full-text screening
- Number of conflicts and resolution method
- Percentage of studies requiring third-party arbitration

---

## 8. Screening Management and Workflow

### 8.1 Batch Scheduling

| Batch | Size | Reviewer 1 Deadline | Reviewer 2 Deadline | Conflict Resolution |
|-------|:----:|--------------------:|--------------------:|--------------------:|
| Batch 1 (Pilot) | 50 T/A | Day 1-2 | Day 1-2 | Day 3 |
| Batch 2 | 500 T/A | Week 1 | Week 1 | End Week 1 |
| Batch 3 | 500 T/A | Week 2 | Week 2 | End Week 2 |
| ... (continue) | ... | ... | ... | ... |
| Full-text pilot | 10 | Day 1 | Day 1 | Day 2 |
| Full-text Batch 1 | 50 | Week 1 | Week 1 | End Week 1 |
| ... (continue) | ... | ... | ... | ... |

### 8.2 Record-Keeping

Track in shared spreadsheet:
- Record ID (Covidence number)
- Reviewer 1 decision (I/E)
- Reviewer 2 decision (I/E)
- Agreement/conflict
- Resolution decision
- Exclusion reason (if excluded)
- Notes

### 8.3 Communication Protocol

- Weekly synchronous meeting to review conflicts and discuss borderline cases
- Asynchronous communication via shared document for non-urgent questions
- Any criteria clarification must be documented in `06_decisions/decision_log.md`

---

## 9. Handling Special Cases

### 9.1 Multiple Papers from Same Study

If multiple papers report results from the same study (same participants, same intervention):
- Include only one publication (prefer journal article over conference; most complete dataset)
- Document the companion papers as "duplicate publication"
- Merge data from both papers if they report different outcomes from the same sample

### 9.2 Papers with Multiple Studies

If one paper reports two or more distinct studies (different samples, different conditions):
- Treat each study as a separate unit of analysis
- Assign separate study IDs
- Code effect sizes independently

### 9.3 Review Papers and Meta-Analyses

If a review paper is encountered:
- Exclude from the current meta-analysis (wrong study design)
- Use its reference list for backward citation tracking
- Document as "secondary source — reference list checked"

### 9.4 Preprints

If a preprint is encountered (arXiv, EdArXiv, SSRN, OSF):
- Check if a published version exists
- If published version found: use published version (exclude preprint as duplicate)
- If no published version found: include preprint with note; apply stricter risk of bias assessment

---

## 10. Timeline

| Activity | Duration | Reviewer Hours (Each) |
|----------|:---------:|:--------------------:|
| Pilot T/A screening (50 records) | Day 1-2 | 2 hours |
| Pilot calibration meeting | Day 3 | 2 hours |
| Phase 1 independent screening (4,000-8,000 records) | Weeks 7-8 | 40-80 hours |
| Phase 1 conflict resolution | Ongoing | 5-10 hours |
| Full-text retrieval | Week 9 | 5-10 hours |
| Pilot full-text screening (10 records) | Week 9 Day 1 | 3 hours |
| Phase 2 independent screening (200-400 records) | Weeks 9-11 | 40-80 hours |
| Phase 2 conflict resolution | Ongoing | 10-15 hours |
| Final study list compilation | Week 12 | 2 hours |

---

*Protocol follows PRISMA 2020 guidelines. All deviations from this protocol will be documented in `06_decisions/decision_log.md` and reported in the manuscript.*
