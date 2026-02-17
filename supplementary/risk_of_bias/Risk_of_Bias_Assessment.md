# Risk of Bias Assessment Tool

## Adapted for Educational AI Intervention Studies

**Based on**: Cochrane Risk of Bias Tool 2.0 (RoB 2; Sterne et al., 2019)
**Adaptations**: Modified for educational intervention research where blinding is typically not feasible

---

## Overview

This tool assesses the risk of bias in each included study across 7 domains. Each domain is rated on a 3-point scale:

| Rating | Code | Meaning |
|--------|:----:|---------|
| Low risk | 2 | Bias is unlikely to affect the results |
| Some concerns | 1 | Bias may affect results; uncertainty about bias presence |
| High risk | 0 | Bias is very likely to affect the results |

**Two independent coders** assess each study. Disagreements are resolved through discussion.

---

## Domain 1: Randomization Process (`rob_random_seq`)

**Question**: Was the sequence used to assign participants to groups generated appropriately and was allocation concealed until assignment?

### Signaling Questions

| # | Question | Answers |
|---|----------|---------|
| 1.1 | Was the allocation sequence random? | Y / PY / PN / N / NI |
| 1.2 | Was the allocation sequence concealed until participants were enrolled and assigned to interventions? | Y / PY / PN / N / NI |

*Y=Yes, PY=Probably Yes, PN=Probably No, N=No, NI=No Information*

### Rating Algorithm

| Conditions | Rating |
|------------|--------|
| 1.1=Y or PY AND 1.2=Y or PY | **Low risk (2)** |
| 1.1=Y or PY AND 1.2=PN, N, or NI | **Some concerns (1)** |
| 1.1=PN or N; OR no randomization described | **High risk (0)** |

### Educational Context Notes

- **RCT with individual randomization**: Most rigorous; code based on signaling questions
- **Cluster randomization** (classes/schools assigned): Valid design; note as cluster randomization; assess sequence at cluster level
- **Quasi-experimental** (not randomized): Automatically code 0 (high risk) for this domain
- **Pre-post within-subjects** (no control group): Code 0 (not applicable; note NA in notes)

### Evidence to Look For

- "Random number generator"
- "Computer-based randomization"
- "Randomized lottery"
- Sealed envelopes (allocation concealment)
- "Stratified randomization by [variable]"

---

## Domain 2: Allocation Concealment (`rob_allocation`)

**Question**: Were participants, investigators, or outcome assessors aware of the intervention assignment?

*Note: This domain primarily applies to RCTs. For quasi-experimental studies, code based on whether groups were comparable at baseline.*

### Signaling Questions

| # | Question | Answers |
|---|----------|---------|
| 2.1 | Were participants aware of their assigned intervention? | Y / PY / PN / N / NI |
| 2.2 | Were outcome assessors aware of intervention assignment? | Y / PY / PN / N / NI |

### Rating for Educational AI Studies

| Conditions | Rating | Educational Context |
|------------|--------|---------------------|
| Participants blinded AND assessors blinded | **Low risk (2)** | Rare in ed research |
| Participants not blinded but objective outcomes used | **Some concerns (1)** | Common; acceptable |
| Participants not blinded AND self-report outcomes used | **Some concerns (1)** | Demand characteristics possible |
| No baseline equivalence check in quasi-experimental study | **High risk (0)** | Groups may not be comparable |
| Baseline equivalence confirmed (quasi-experimental) | **Some concerns (1)** | Improved but still not randomized |

---

## Domain 3: Blinding of Participants (`rob_blind_part`)

**Question**: Were participants blinded to the intervention they received?

### Educational Research Note

In educational AI research, true participant blinding is nearly impossible — participants know whether they are using an AI system. This domain should therefore be interpreted as assessing whether knowledge of condition assignment could have biased outcomes.

### Rating Guidelines for Educational AI

| Situation | Rating | Rationale |
|-----------|--------|-----------|
| Objective tests scored by computer or blinded assessors | **Some concerns (1)** | Participants unblinded but outcomes objective |
| Self-report outcomes (motivation, self-efficacy) | **Some concerns (1)** | Demand characteristics possible; note this |
| Participants in control condition received attention control (active comparison) | **Some concerns (1)** | Reduces Hawthorne effect |
| Control group received no-treatment / business-as-usual | **Some concerns (1)** | Standard educational quasi-experiment |
| Researchers clearly favored AI condition; study outcome is self-report | **High risk (0)** | Social desirability bias likely |

**Default for educational AI studies**: Code 1 (Some concerns) unless specific evidence of bias from unblinding.

---

## Domain 4: Blinding of Outcome Assessment (`rob_blind_outcome`)

**Question**: Were outcome assessors blinded to the intervention received?

### Signaling Questions

| # | Question | Answers |
|---|----------|---------|
| 4.1 | Were outcome assessors aware of the intervention received by study participants? | Y / PY / PN / N / NI |
| 4.2 | Could non-blinded assessment of outcomes have introduced bias? | Y / PY / PN / N / NI |

### Rating Algorithm

| Conditions | Rating |
|------------|--------|
| Computerized/automated scoring (no human assessor) | **Low risk (2)** |
| Human assessors blinded to condition | **Low risk (2)** |
| Self-report measures (no assessor) | **Some concerns (1)** |
| Human assessors not blinded; subjective outcomes (e.g., essay rubric) | **High risk (0)** |
| Human assessors not blinded; objective outcomes (machine-scored test) | **Some concerns (1)** |

### Common Scenarios

| Scenario | Code | Notes |
|----------|:----:|-------|
| Multiple-choice test scored by computer | 2 | Objective; no human assessment needed |
| Automated essay scoring system | 2 | AI scores; no human bias |
| Human raters use rubric; told which group | 0 | Bias likely |
| Human raters use rubric; blinded to condition | 2 | Proper blinding |
| Likert scale self-report | 1 | No assessor; demand characteristics possible |

---

## Domain 5: Incomplete Outcome Data (`rob_incomplete`)

**Question**: Were incomplete outcome data adequately addressed?

### Signaling Questions

| # | Question | Answers |
|---|----------|---------|
| 5.1 | Were data for this outcome available for all, or nearly all, participants? | Y / PY / PN / N / NI |
| 5.2 | If not, is there evidence that results were not biased by missing data? | Y / PY / PN / N / NI |
| 5.3 | If not, could missingness in outcomes have been induced by the true outcome? | Y / PY / PN / N / NI |

### Rating Algorithm

| Conditions | Rating |
|------------|--------|
| Attrition ≤ 5% OR intent-to-treat analysis used OR missing completely at random confirmed | **Low risk (2)** |
| Attrition 6-20% AND no differential attrition by group AND no plausible bias mechanism | **Some concerns (1)** |
| Attrition > 20% OR differential attrition by group (more dropouts in control) | **High risk (0)** |
| Attrition not reported | **Some concerns (1)** |

### Attrition Assessment Table

| Study | Initial N (T) | Final N (T) | Initial N (C) | Final N (C) | Attrition Rate | Differential? | Rating |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [Study 1] | | | | | | | |
| ... | | | | | | | |

---

## Domain 6: Selective Reporting (`rob_selective`)

**Question**: Are results free of selective outcome reporting?

### Signaling Questions

| # | Question | Answers |
|---|----------|---------|
| 6.1 | Were the trial's pre-specified primary and secondary outcomes reported? | Y / PY / PN / N / NI |
| 6.2 | Was the trial registered with a pre-specified protocol that matches the reported outcomes? | Y / PY / PN / N / NI |

### Rating Algorithm

| Conditions | Rating |
|------------|--------|
| Pre-registered AND all outcomes reported | **Low risk (2)** |
| Not pre-registered BUT all plausible outcomes reported; no evidence of selective reporting | **Some concerns (1)** |
| Pre-registered AND some outcomes not reported | **High risk (0)** |
| Evidence of selective reporting (e.g., only significant outcomes reported) | **High risk (0)** |
| Cannot assess (no registration; no way to verify all outcomes) | **Some concerns (1)** |

### Detection Strategies

- Search PROSPERO, ClinicalTrials.gov, OSF for pre-registration
- Compare methods section outcomes with results section
- Check if any stated outcomes lack results
- Look for phrases like "additional analyses are available from the author" without reporting them

---

## Domain 7: Other Sources of Bias (`rob_other`)

**Question**: Does the study appear to be free of other problems that could put it at high risk of bias?

### Educational AI-Specific Bias Threats

| Bias Type | Description | When to Flag |
|-----------|-------------|--------------|
| **Hawthorne Effect** | Participants change behavior because they know they are being studied | When control group has no equivalent attention/novelty |
| **Novelty Effect** | AI system appears effective simply because it is new and engaging | When intervention is novel AI technology used for first time |
| **Teacher/Instructor Enthusiasm Bias** | Instructors more enthusiastic about AI condition | When single instructor delivers both conditions |
| **Contamination** | Control group participants access AI intervention | When classes share resources or communicate |
| **Differential Expertise** | AI condition users receive implicit technical training | When technical operation of AI requires training that control doesn't receive |
| **Expectancy Bias** | Researchers expect AI to outperform; subtly communicate this | When researchers directly interact with participants and are not blinded |
| **Researcher-Developed AI** | AI system developed by the researchers conducting the study | Common in ed tech; creates conflict of interest |
| **Publication Bias** | Study may not have been published if AI did not outperform | Cannot assess per study; addressed at meta-analytic level |

### Rating Algorithm for Domain 7

| Conditions | Rating |
|------------|--------|
| No other bias threats identified | **Low risk (2)** |
| 1-2 minor bias threats present; unlikely to substantially affect results | **Some concerns (1)** |
| Major bias threat present (e.g., researcher-developed AI + researcher as instructor + self-report outcomes) | **High risk (0)** |

---

## Overall Risk of Bias Judgment (`rob_overall`)

### Algorithm

| Conditions | Overall Rating |
|------------|:---:|
| ALL domains rated Low risk | **Low (2)** |
| No domains rated High; ≥1 rated Some concerns | **Moderate (1)** |
| ≥1 domain rated High risk | **High (0)** |

### Expected Distribution for Educational AI Studies

Based on prior educational meta-analyses, expected distribution:
- Low risk: ~5-15% of studies
- Moderate risk: ~50-65% of studies
- High risk: ~25-40% of studies

This distribution reflects the typical difficulty of blinding in educational contexts.

---

## Risk of Bias Assessment Form

*Complete one form per included study*

```
STUDY RISK OF BIAS ASSESSMENT
==============================
Study ID: ___________
Author(s): ___________
Year: ___________
Design: [ ] RCT  [ ] Quasi-experimental  [ ] Pre-post

DOMAIN 1: Randomization
Rating: [ ] Low (2)  [ ] Some concerns (1)  [ ] High (0)  [ ] N/A
Evidence: ___________

DOMAIN 2: Allocation Concealment
Rating: [ ] Low (2)  [ ] Some concerns (1)  [ ] High (0)
Evidence: ___________

DOMAIN 3: Blinding of Participants
Rating: [ ] Low (2)  [ ] Some concerns (1)  [ ] High (0)
Evidence: ___________

DOMAIN 4: Blinding of Outcome Assessment
Rating: [ ] Low (2)  [ ] Some concerns (1)  [ ] High (0)
Evidence: ___________

DOMAIN 5: Incomplete Outcome Data
Attrition rate: _____ %  Differential: [ ] Yes  [ ] No  [ ] NR
Rating: [ ] Low (2)  [ ] Some concerns (1)  [ ] High (0)
Evidence: ___________

DOMAIN 6: Selective Reporting
Pre-registered: [ ] Yes  [ ] No
Rating: [ ] Low (2)  [ ] Some concerns (1)  [ ] High (0)
Evidence: ___________

DOMAIN 7: Other Bias
Bias types identified: ___________
Rating: [ ] Low (2)  [ ] Some concerns (1)  [ ] High (0)
Evidence: ___________

OVERALL RATING: [ ] Low (2)  [ ] Moderate (1)  [ ] High (0)
Rationale: ___________

Coder: ___________  Date: ___________
```

---

## Risk of Bias Summary Table Template

*Complete after all studies are assessed*

| Study | D1 | D2 | D3 | D4 | D5 | D6 | D7 | Overall |
|-------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:-------:|
| Author (Year) | | | | | | | | |
| ... | | | | | | | | |
| **% Low risk** | | | | | | | | |
| **% Some concerns** | | | | | | | | |
| **% High risk** | | | | | | | | |

*D1=Randomization, D2=Allocation, D3=Participant Blinding, D4=Outcome Blinding, D5=Incomplete Data, D6=Selective Reporting, D7=Other*

---

## Sensitivity Analysis Plan

Studies will be categorized for sensitivity analysis:

1. **Restrict to Low risk**: Include only studies with `rob_overall = 2`
2. **Restrict to Low + Moderate risk**: Include studies with `rob_overall ≥ 1`
3. **Full set**: Include all studies regardless of risk

Compare pooled effect sizes across these three subsets. If estimates differ substantially (>0.15 g units), discuss implications for evidence certainty.

---

*References: Sterne, J. A. C., et al. (2019). RoB 2: A revised tool for assessing risk of bias in randomised trials. BMJ, 366, l4898. Pigott, T. D., & Polanin, J. R. (2020). Methodological guidance paper: High-quality meta-analysis in a systematic review. Review of Educational Research, 90(1), 24-46.*
