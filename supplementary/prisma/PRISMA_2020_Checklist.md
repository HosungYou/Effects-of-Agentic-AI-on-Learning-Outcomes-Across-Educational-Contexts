# PRISMA 2020 Checklist

## Preferred Reporting Items for Systematic Reviews and Meta-Analyses

**Study**: Effects of Agentic AI on Learning Outcomes Across Educational Contexts: A Meta-Analysis with Implications for Human-AI Learning Orchestration

**Authors**: Hosung You & Dr. Yang

**Target Journal**: Educational Research Review / Computers & Education

**Reference**: Page et al. (2021). The PRISMA 2020 statement. *BMJ*, 372, n71.

---

## TITLE

### Item 1: Title
**Guideline**: Identify the report as a systematic review.

**Status**: [ ] Completed
**Manuscript location**: Title page
**Draft title**: "Effects of Agentic AI on Learning Outcomes Across Educational Contexts: A Meta-Analysis with Implications for Human-AI Learning Orchestration (HALO Framework)"
**Notes**: Title identifies as meta-analysis; includes scope (educational contexts) and framework output (HALO).

---

## ABSTRACT

### Item 2: Abstract
**Guideline**: See the PRISMA 2020 for Abstracts checklist.

**Status**: [ ] Completed
**Manuscript location**: Abstract section
**Required elements**:
- [ ] Background/Objectives
- [ ] Eligibility criteria
- [ ] Information sources
- [ ] Risk of bias
- [ ] Synthesis methods
- [ ] Results (studies included, overall effect, moderator results)
- [ ] Limitations
- [ ] Conclusions
- [ ] Registration information (PROSPERO number)

---

## INTRODUCTION

### Item 3: Rationale
**Guideline**: Describe the rationale for the review in the context of existing knowledge.

**Status**: [ ] Completed
**Manuscript location**: Introduction section
**Content to include**:
- [ ] Rapid proliferation of AI agents in education (problem context)
- [ ] Three core research gaps (no meta-analysis on oversight level, architecture, or cross-context comparison)
- [ ] Comparison with existing meta-analyses (Dai et al., 2024; Ma et al., 2014; Kulik & Fletcher, 2016)
- [ ] Why these gaps matter (theory and practice)
- [ ] Coherence logic: meta-analysis → HALO Framework

### Item 4: Objectives
**Guideline**: Provide an explicit statement of the objectives or questions the review addresses.

**Status**: [ ] Completed
**Manuscript location**: End of Introduction
**Research Questions to state**:
- [ ] RQ1: Overall effect of Agentic AI on learning outcomes
- [ ] RQ2: Human oversight level as moderator
- [ ] RQ3: Agent architecture (single vs. multi-agent) as moderator
- [ ] RQ4: Learning context as moderator
- [ ] RQ5: Design principles for HALO Framework

---

## METHODS

### Item 5: Protocol and Registration
**Guideline**: Indicate if a review protocol exists, and if and where it can be accessed (e.g., a web address); and, if available, provide registration information including the registration number.

**Status**: [ ] Completed
**Manuscript location**: Methods — Protocol subsection
**Content**:
- [ ] PROSPERO registration number: [CRD#TBD]
- [ ] Registration date: [Month 1, TBD]
- [ ] Protocol URL: https://www.crd.york.ac.uk/prospero/display_record.php?ID=CRD#TBD
- [ ] Any deviations from protocol: documented in `06_decisions/decision_log.md`

### Item 6: Eligibility Criteria
**Guideline**: Specify the inclusion and exclusion criteria for the review and how studies were grouped for the syntheses.

**Status**: [ ] Completed
**Manuscript location**: Methods — Eligibility Criteria subsection
**Content**:
- [ ] PICOS framework table (Population, Intervention, Comparison, Outcome, Study design)
- [ ] All 8 inclusion criteria (IC1-IC8) summarized
- [ ] All 8 exclusion criteria (EC1-EC8) summarized
- [ ] Definition of "Agentic AI" (6 autonomous capabilities)
- [ ] Grouping rationale for subgroup analyses

### Item 7: Information Sources
**Guideline**: Describe all information sources (e.g., databases with date of last search, contact with study authors to identify additional studies) and date last searched.

**Status**: [ ] Completed
**Manuscript location**: Methods — Search Strategy subsection
**Content**:
- [ ] All 6 databases listed: Web of Science, Scopus, ERIC, PsycINFO, IEEE Xplore, ACM Digital Library
- [ ] Date of each database search
- [ ] Citation tracking (backward + forward)
- [ ] Hand search of key journals
- [ ] Grey literature sources
- [ ] Author contact for missing data

### Item 8: Search Strategy
**Guideline**: Present the full search strategies for all databases, including any filters that were applied.

**Status**: [ ] Completed
**Manuscript location**: Methods (summary) + Supplementary Appendix (full strings)
**Content**:
- [ ] Full Boolean search string for each database (Supplementary Appendix A)
- [ ] Date ranges applied (2018-2025)
- [ ] Language filter (English)
- [ ] Publication type filters
- [ ] See `supplementary/Search_Strategy_Appendix.md`

### Item 9: Selection Process
**Guideline**: Specify the methods used to select studies for inclusion, including how many reviewers screened each record and each report retrieved, whether they worked independently, and if applicable, details of automation tools used in the process.

**Status**: [ ] Completed
**Manuscript location**: Methods — Study Selection subsection
**Content**:
- [ ] Two independent reviewers (named)
- [ ] Phase 1: Title/abstract screening; blinded in Covidence
- [ ] Phase 2: Full-text screening
- [ ] Conflict resolution procedure
- [ ] Pilot screening (50 records) before independent screening
- [ ] Cohen's kappa for screening agreement

### Item 10: Data Collection Process
**Guideline**: Describe the methods used to collect data from reports, including how many reviewers collected data from each report, whether they worked independently, any processes for obtaining or confirming data from study investigators, and if applicable, details of automation tools used in the process.

**Status**: [ ] Completed
**Manuscript location**: Methods — Data Extraction subsection
**Content**:
- [ ] Two independent coders
- [ ] Standardized coding template (Excel/Google Sheets)
- [ ] Pilot coding (5 studies) before independent coding
- [ ] 20% reliability sample for ICR
- [ ] Author contact protocol for missing data

### Item 11: Data Items
**Guideline**: List and define all outcomes for which data were sought. Specify whether all results that were compatible with each outcome domain in each study were sought (e.g., for all measures, time points, and analyses reported), and if not, the methods used to decide which results to collect.

**Status**: [ ] Completed
**Manuscript location**: Methods — Coding Scheme subsection
**Content**:
- [ ] A: Study identification variables
- [ ] B: Study design variables
- [ ] C: AI agent characteristic variables (7 variables)
- [ ] D: Learning context variables (4 variables)
- [ ] E: Learning outcome variables (4 variables)
- [ ] F: Effect size data
- [ ] G: Risk of bias variables
- [ ] Reference: `03_data_extraction/coding_manual.md`

### Item 12: Study Risk of Bias Assessment
**Guideline**: Describe the methods used to assess risk of bias in the included studies, including details of the tool(s) used, how many reviewers assessed each study, and whether they worked independently.

**Status**: [ ] Completed
**Manuscript location**: Methods — Quality Assessment subsection
**Content**:
- [ ] Cochrane Risk of Bias 2.0 adapted for educational research
- [ ] 7 domains assessed (randomization, allocation, blinding participants, blinding outcome, incomplete data, selective reporting, other)
- [ ] Both coders independently assess
- [ ] Overall risk judgment per study

### Item 13: Effect Measures
**Guideline**: Specify the effect measure(s) used in the synthesis (e.g., risk ratio, mean difference).

**Status**: [ ] Completed
**Manuscript location**: Methods — Effect Size subsection
**Content**:
- [ ] Primary effect measure: Hedges' g (bias-corrected SMD)
- [ ] Rationale: Hedges' g appropriate for comparing groups on continuous outcomes with correction for small-sample bias
- [ ] Direction convention: positive g = AI agent outperforms comparison
- [ ] Variance formula for Hedges' g

### Item 14: Synthesis Methods
**Guideline**: Describe the methods used to synthesize results and provide a rationale for the choice(s).

**Status**: [ ] Completed
**Manuscript location**: Methods — Analysis subsection
**Content**:
- [ ] Random-effects model (REML estimator); rationale for RE over FE
- [ ] 3-level meta-analysis for dependent effect sizes
- [ ] Robust Variance Estimation (RVE) with clubSandwich corrections
- [ ] Subgroup analysis for categorical moderators
- [ ] Meta-regression for continuous moderators
- [ ] Assumed within-study correlation (ρ = 0.80 for RVE)
- [ ] Software: R (metafor, robumeta, clubSandwich)

### Item 15: Reporting Bias Assessment
**Guideline**: Describe any methods used to assess risk of bias due to missing results in a synthesis.

**Status**: [ ] Completed
**Manuscript location**: Methods — Publication Bias subsection
**Content**:
- [ ] Funnel plot visual inspection
- [ ] Egger's test for funnel plot asymmetry
- [ ] Trim-and-fill method (Duval & Tweedie)
- [ ] PET-PEESE correction
- [ ] Step function selection models

### Item 16: Certainty Assessment
**Guideline**: Describe any methods used to assess certainty (or confidence) in the body of evidence for an outcome.

**Status**: [ ] Completed (if required by journal)
**Manuscript location**: Methods or Discussion
**Content**:
- [ ] GRADE assessment (if required by target journal)
- [ ] Domains: Risk of bias, inconsistency, indirectness, imprecision, publication bias

---

## RESULTS

### Item 17: Study Selection
**Guideline**: Describe the results of the search and selection process, from the number of records identified to the number of studies included in the review, ideally using a flow diagram.

**Status**: [ ] To be completed after search
**Manuscript location**: Results — Study Selection
**Content**:
- [ ] PRISMA 2020 flow diagram (Figure 1)
- [ ] Records identified per database
- [ ] Duplicates removed
- [ ] Title/abstract screened and excluded
- [ ] Full texts assessed and excluded (with reasons and counts)
- [ ] Studies included in synthesis

### Item 18: Study Characteristics
**Guideline**: Cite each included study and present its characteristics.

**Status**: [ ] To be completed after coding
**Manuscript location**: Results — Study Characteristics (Table 1)
**Content**:
- [ ] Summary table of all included studies
- [ ] Authors, year, country, design, N, AI type, context, outcome, Hedges' g

### Item 19: Risk of Bias in Studies
**Guideline**: Present assessments of risk of bias for each included study.

**Status**: [ ] To be completed after coding
**Manuscript location**: Results or Supplementary
**Content**:
- [ ] Risk of bias summary figure or table
- [ ] Percentage of studies at low/moderate/high risk per domain

### Item 20: Results of Individual Studies
**Guideline**: For all outcomes, present, for each study: (a) summary statistics for each group (where appropriate) and (b) an effect estimate and its precision, ideally using structured tables or plots.

**Status**: [ ] To be completed after analysis
**Manuscript location**: Results + Supplementary
**Content**:
- [ ] Forest plot with individual study effect sizes (Figure 2)
- [ ] Complete effect size table in supplementary materials

### Item 21: Results of Syntheses
**Guideline**: For each synthesis, present the main results, including the strength of evidence.

**Status**: [ ] To be completed after analysis
**Manuscript location**: Results section (Tables 2-6)
**Content**:
- [ ] Overall pooled effect (RQ1): g, 95% CI, PI, Q, I², τ²
- [ ] Oversight level subgroups (RQ2): g per level, Q_between, p
- [ ] Architecture subgroups (RQ3): single vs. multi-agent comparison
- [ ] Context subgroups (RQ4): g per context, Q_between, p
- [ ] Additional moderator results

### Item 22: Reporting Biases
**Guideline**: Present assessments of reporting biases for included studies.

**Status**: [ ] To be completed after analysis
**Manuscript location**: Results — Publication Bias
**Content**:
- [ ] Funnel plot (Figure 3)
- [ ] Egger's test result
- [ ] Trim-and-fill result
- [ ] PET-PEESE result

### Item 23: Certainty of Evidence
**Guideline**: Present assessments of certainty (or confidence) in the body of evidence for each outcome.

**Status**: [ ] To be completed if GRADE applied
**Manuscript location**: Results or Discussion

---

## DISCUSSION

### Item 24: Discussion
**Guideline**: Provide a general interpretation of the results in the context of other evidence.

**Status**: [ ] To be completed during writing phase
**Manuscript location**: Discussion section
**Subsections**:
- [ ] Summary of main findings linked to RQs
- [ ] Theoretical implications (AAT, EST, SDT, DLS, APCP)
- [ ] Practical implications for HRD and EdTech
- [ ] HALO Framework design principles (RQ5)
- [ ] Limitations
- [ ] Future research directions

### Item 25: Limitations
**Guideline**: Discuss limitations of the evidence included in the review, and of the review process.

**Status**: [ ] To be completed during writing phase
**Manuscript location**: Discussion — Limitations subsection
**Anticipated limitations**:
- [ ] English-language only (linguistic bias)
- [ ] Publication bias (favoring positive results)
- [ ] Heterogeneity in AI system operationalization
- [ ] Limited pre-2018 coverage (design choice; acknowledged)
- [ ] Inability to obtain unpublished data
- [ ] Rater judgment required for oversight level coding

### Item 26: Conclusions
**Guideline**: Provide a general interpretation of the results in the context of other evidence, and implications for future research.

**Status**: [ ] To be completed during writing phase
**Manuscript location**: Conclusions section

---

## OTHER INFORMATION

### Item 27: Registration and Protocol
**Guideline**: Provide registration information for the review, including register name and registration number, or state that the review was not registered.

**Status**: [ ] To be completed in Month 1
**Manuscript location**: Methods and Abstract
**Content**: PROSPERO registration number and date

### Item 28: Support
**Guideline**: Describe sources of financial or other support for the review, and the role of the funders or sponsors in the review.

**Status**: [ ] To be completed
**Manuscript location**: Acknowledgments section

### Item 29: Competing Interests
**Guideline**: Declare any competing interests of review authors.

**Status**: [ ] To be completed
**Manuscript location**: Declaration of competing interests

### Item 30: Availability of Data, Code, and Other Materials
**Guideline**: Report which of the following are publicly available and where they can be found: template data collection forms; data extracted from included studies; data used for all analyses; analytic code; any other materials used in the review.

**Status**: [ ] To be completed
**Manuscript location**: Data availability statement
**Planned availability**:
- [ ] Coding template: OSF or Zenodo
- [ ] Extracted data: OSF or Zenodo (anonymized if needed)
- [ ] R analysis scripts: GitHub repository
- [ ] Pre-registration: PROSPERO

---

## Checklist Completion Status

| Section | Items | Completed | Remaining |
|---------|:-----:|:---------:|:---------:|
| Title | 1 | 0 | 1 |
| Abstract | 1 | 0 | 1 |
| Introduction | 2 | 0 | 2 |
| Methods | 12 | 0 | 12 |
| Results | 7 | 0 | 7 |
| Discussion | 3 | 0 | 3 |
| Other | 4 | 0 | 4 |
| **Total** | **30** | **0** | **30** |

*Update this table as manuscript sections are completed.*

---

*Reference: Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., ... & Moher, D. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. BMJ, 372, n71. https://doi.org/10.1136/bmj.n71*
