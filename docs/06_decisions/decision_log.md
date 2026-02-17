# Methodological Decision Log

## Overview

This document records all methodological decisions made during the meta-analysis. Every deviation from the pre-registered protocol, every borderline coding decision that required consensus, and every analysis choice must be logged here with date, rationale, and authors involved. This log ensures transparency and reproducibility.

---

## How to Use This Log

**When to add an entry**:
- Protocol deviation from pre-registered PROSPERO plan
- Clarification added to coding manual after pilot
- Decision about a borderline case that sets a precedent
- Analysis choice not fully specified in pre-registration
- Handling of a novel situation not covered by existing procedures

**Entry format**:
```
## [DEC-XXX] [Short Title]
**Date**: YYYY-MM-DD
**Phase**: [Search / Screening / Coding / Analysis / Writing]
**Decision makers**: [Names]
**Issue**: Brief description of the situation
**Options considered**:
  - Option A: ...
  - Option B: ...
**Decision**: Which option was chosen and why
**Impact**: Which studies/variables are affected
**Protocol status**: [Pre-registered / Deviation from protocol / Addition to protocol]
```

---

## Phase 1: Protocol and Search Decisions

### [DEC-001] Template Entry
**Date**: [To be completed]
**Phase**: Protocol
**Decision makers**: [Names]
**Issue**: [Description]
**Options considered**:
- Option A: [Description]
- Option B: [Description]
**Decision**: [Choice and rationale]
**Impact**: [Scope of impact]
**Protocol status**: [Classification]

---

## Phase 2: Screening Decisions

*Entries to be added during screening phase (Months 1-3)*

### Common Screening Precedents Template

When a borderline study is encountered and a decision is made, add an entry here to ensure consistent future decisions:

```
## [DEC-XXX] Screening Precedent: [Study Type]
**Date**: YYYY-MM-DD
**Study**: [Author, Year]
**Phase**: Screening (Phase 1 or 2)
**Decision makers**: [Names]
**Issue**: Why was this study borderline?
**Relevant criterion**: [IC1-IC8 or EC1-EC8]
**Decision**: Include / Exclude
**Rationale**: [Specific text from paper and criteria that applies]
**Future rule**: [How to handle similar cases going forward]
```

---

## Phase 3: Coding Decisions

*Entries to be added during coding phase (Month 3-4)*

### Anticipated Coding Decision Areas

The following are areas where decisions are likely to be needed based on existing literature:

#### Oversight Level (C1) — Anticipated Issues

| Scenario | Anticipated Decision | Rationale |
|----------|---------------------|-----------|
| Study describes instructor "monitoring" via dashboard but no explicit intervention described | Code 1 (Fully Autonomous) | Monitoring without intervention mechanism = autonomous |
| Study uses "human-in-the-loop" language but mechanism is unclear | Code based on closest described behavior; document uncertainty | Apply conservative coding |
| AI tutoring system used within a teacher-directed class with AI as supplement | Code 3 (Human-Led with AI Support) | Teacher primary pedagogical decision-maker |

#### Agency Level (C3) — Anticipated Issues

| Scenario | Anticipated Decision |
|----------|---------------------|
| System described as "proactive" but only reacts to explicit requests | Code 1 (Adaptive) — label does not determine code |
| LLM chatbot that can be used in many ways | Code based on documented use in the study, not LLM capability |
| System initiates reminder emails | Code 2 (Proactive) — initiates unprompted interaction |

---

## Phase 4: Analysis Decisions

*Entries to be added during analysis phase (Month 4-5)*

### Analysis Decision Template

```
## [DEC-XXX] Analysis: [Decision Title]
**Date**: YYYY-MM-DD
**Phase**: Analysis
**Decision makers**: [Names]
**Issue**: [Statistical or methodological choice]
**Options**:
  - Option A: [Statistical approach 1]
  - Option B: [Statistical approach 2]
**Decision**: [Chosen approach]
**Rationale**: [Statistical and methodological justification]
**Reference**: [Citation supporting the choice]
**Impact on results**: [How results would differ under Option A vs B]
**Reporting**: [Will both approaches be reported? Which is primary?]
```

### Pre-Anticipated Analysis Decisions

#### ANA-001: Primary Model for Dependent Effect Sizes

**Pre-decision**: If the majority of studies (>50%) report multiple effect sizes, use 3-level meta-analysis as the primary model and RVE as the robustness check. If <50% of studies report multiple effect sizes, use standard RE model with one effect size per study as primary and 3-level model as sensitivity.

**Rationale**: Align model complexity with data structure.

#### ANA-002: Minimum Subgroup Size

**Pre-decision**: For any subgroup or moderator analysis, require k ≥ 4 independent studies per cell. Report cells with k < 4 as "insufficient data."

**Rationale**: Effect size estimates are unstable with very small k; avoid spurious moderation claims.

#### ANA-003: Publication Bias Correction Reporting

**Pre-decision**: Report original estimate and trim-and-fill adjusted estimate side by side. Use original estimate as primary (trim-and-fill is known to over-correct). If PET-PEESE suggests true effect near zero, flag as potential bias concern.

#### ANA-004: Assumed Pre-Post Correlation

**Pre-decision**: Use r = 0.70 as the primary assumption for pre-post correlation. Report sensitivity analyses with r = 0.50 and r = 0.90 as supplementary.

**Rationale**: r = 0.70 is consistent with prior educational meta-analyses (Morris & DeShon, 2002).

---

## Phase 5: Writing Decisions

*Entries to be added during writing phase (Month 5-7)*

### Writing Decision Template

```
## [DEC-XXX] Writing: [Decision Title]
**Date**: YYYY-MM-DD
**Phase**: Writing
**Decision makers**: [Names]
**Issue**: [Framing, reporting, or presentation choice]
**Decision**: [Choice made]
**Rationale**: [Justification]
**Impact**: [Which section/claim is affected]
```

---

## Decision Summary Table

*To be completed as decisions are made*

| ID | Date | Phase | Category | Summary | Status |
|----|------|-------|----------|---------|--------|
| DEC-001 | [TBD] | Protocol | [Type] | [Summary] | [Open/Closed] |
| ... | | | | | |

---

## Deviation Register

Any deviation from the pre-registered PROSPERO protocol must be flagged here with additional detail:

| Deviation ID | PROSPERO Item | Original Plan | Actual Approach | Reason | Date |
|:---:|---|---|---|---|---|
| DEV-001 | [Item] | [What was planned] | [What was done] | [Why] | [Date] |

---

## Audit Trail

All entries must be timestamped and attributed. This document should be treated as an immutable log — previous entries should never be edited. Corrections should be added as new entries referencing the original.

**Document version**: 1.0
**Created**: 2026-02-16
**Last updated**: 2026-02-16
**Maintained by**: Hosung You (Coder 1)
**Co-maintained by**: Dr. Yang (Coder 2)
