# 4. Method

This meta-analysis follows the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA 2020; Page et al., 2021) guidelines. The protocol was pre-registered on PROSPERO [registration number to be inserted upon completion].

## 4.1 Eligibility Criteria

Studies were included if they met five criteria organized by the PICOS framework (Population, Intervention, Comparison, Outcome, Study design):

**Population.** Learners in any formal or structured educational context, including K-12, higher education, workplace training, professional education, and continuing education settings. Studies involving non-learner populations (e.g., patients interacting with AI for non-educational purposes) were excluded.

**Intervention.** AI systems exhibiting at least one form of autonomous pedagogical action, operationally defined using the APCP framework (Yan, 2025) as AI systems that (a) adaptively respond to learner inputs by adjusting content, difficulty, or pacing; (b) proactively initiate interactions without explicit learner prompts; (c) engage as co-learners sharing the learning process; or (d) function as peers capable of reciprocal socio-cognitive interaction. Systems limited to static content delivery, simple keyword-based FAQ responses, or passive information retrieval tools without adaptive behavior were excluded.

**Comparison.** At least one comparison condition: no AI (traditional instruction, waitlist, or business-as-usual), non-agentic AI (static or passive AI tools), or a different AI agency level (e.g., fully autonomous vs. human-supervised conditions within the same study).

**Outcome.** At least one quantitative learning outcome in one of four categories: cognitive (factual recall, conceptual understanding), skill-based (procedural skills, problem-solving), affective (motivation, self-efficacy, engagement), or performance (job performance, transfer to real-world application). Studies reporting only satisfaction, usability, or system performance metrics were excluded.

**Study design.** Experimental (randomized controlled trials), quasi-experimental (non-random assignment with comparison group), or pre-post within-subjects designs providing sufficient data for effect size computation. Purely qualitative studies, case studies, and surveys without comparison conditions were excluded.

**Additional criteria.** Studies published between January 2018 and December 2025 in English-language peer-reviewed journals or conference proceedings were included. The 2018 lower bound reflects the emergence of agentic AI capabilities in educational contexts following advances in deep learning and natural language processing.

## 4.2 Information Sources and Search Strategy

Six electronic databases were searched: Web of Science (Core Collection), Scopus, ERIC, PsycINFO, IEEE Xplore, and ACM Digital Library. These databases were selected to ensure comprehensive coverage across education (ERIC, PsycINFO), interdisciplinary research (Web of Science, Scopus), and computer science and engineering (IEEE Xplore, ACM Digital Library).

The search strategy combined three concept blocks using Boolean AND operators: (a) AI agent terminology (e.g., "AI agent*," "intelligent tutoring system*," "pedagogical agent*," "agentic AI," "conversational agent*," "AI chatbot*," "multi-agent system*"), (b) learning outcome terminology (e.g., "learning outcome*," "academic achievement," "knowledge gain*," "skill acquisition," "test score*"), and (c) educational context terminology (e.g., "education*," "training," "instruction," "workplace," "professional development"). Database-specific syntax adaptations (field codes, truncation operators, proximity operators) were applied for each database. The complete search strings are reported in Supplementary Appendix A.

Supplementary searches included backward and forward citation tracking from five seed articles (Dai et al., 2024; Ma et al., 2014; Kulik & Fletcher, 2016; Yang, 2025; Yan, 2025), hand-searching of three key journals (*Computers & Education*, *International Journal of Artificial Intelligence in Education*, *Educational Technology Research and Development*), and screening of preprint servers (SSRN, EdArXiv) and dissertations (ProQuest).

## 4.3 Study Selection

Study selection followed a two-phase procedure with independent dual screening.

**Phase 1: Title and abstract screening.** After deduplication using automated tools, two reviewers independently screened titles and abstracts against the eligibility criteria. A pilot screening of 100 records was conducted first, with discrepancies discussed to calibrate inclusion thresholds. Target inter-rater agreement was Cohen's kappa >= 0.80. Records were retained if either reviewer judged them as potentially relevant (liberal inclusion strategy at this stage).

**Phase 2: Full-text screening.** Full texts of retained records were retrieved and independently assessed by both reviewers. Exclusion reasons were documented for each rejected study. Disagreements were resolved through discussion; unresolved cases were adjudicated by a third reviewer. The study selection process is documented in a PRISMA flow diagram (Figure 1).

## 4.4 Data Extraction and Coding

Data were extracted independently by two coders using a standardized coding form (see Supplementary Material B for the complete codebook). The coding scheme encompassed four domains:

**Study characteristics.** Publication year, journal, country, research design, sample sizes, attrition rate, and intervention duration.

**AI agent characteristics.** Six key moderator variables were coded: (a) *human oversight level* (1 = fully autonomous, 2 = AI-led with human checkpoints, 3 = human-led with AI support), coded from intervention descriptions using Parasuraman et al.'s (2000) automation level taxonomy collapsed into three meta-analytically tractable categories; (b) *agent architecture* (1 = single agent, 2 = multi-agent system); (c) *agent agency level* (1-4 on the APCP scale; Yan, 2025); (d) *agent role* (tutor, coach, assessor, collaborator, facilitator, or multiple); (e) *AI technology base* (rule-based, machine learning, NLP, large language model, reinforcement learning, or hybrid); and (f) *adaptivity level* (static, performance-adaptive, behavior-adaptive, affect-adaptive, or multi-dimensional).

Human oversight level, the primary novel moderator, was coded using a structured decision protocol. Coders identified who made primary pedagogical decisions during the learning interaction and coded accordingly. When studies did not explicitly describe oversight arrangements, default coding rules were applied (e.g., "instructor monitoring without intervention mechanism" was coded as fully autonomous). All coding decisions were documented in a notes field with supporting textual evidence from the primary study.

**Learning context characteristics.** Context type (K-12, higher education, workplace training, professional education, continuing education), subject domain, learning mode, and delivery format.

**Learning outcome characteristics.** Outcome type (cognitive, skill-based, affective, performance), Bloom's taxonomy level (remember-understand, apply-analyze, evaluate-create), measurement type, and measurement timing (immediate, delayed, transfer).

**Intercoder reliability.** Following independent coding, Cohen's kappa was computed for each categorical variable and intraclass correlation coefficients (ICC) for continuous variables. Target thresholds were kappa >= 0.80 and ICC >= 0.85. Discrepancies were resolved through discussion; unresolved cases were adjudicated by a third coder.

## 4.5 Effect Size Computation

Hedges' *g* was computed as the primary effect size metric. For studies reporting means and standard deviations, *g* was calculated as:

*g* = *J* x (*M*_treatment - *M*_control) / *SD*_pooled

where *J* = 1 - 3 / (4(*df*) - 1) is the small-sample correction factor (Hedges, 1981). For studies reporting only test statistics (*t*, *F*, chi-square) or *p*-values, appropriate conversion formulas were applied (Borenstein et al., 2009). For pre-post within-subjects designs without a control group, effect sizes were computed following Morris and DeShon (2002). Positive values of *g* indicate that the agentic AI condition outperformed the comparison condition.

When studies reported insufficient data for effect size computation, corresponding authors were contacted with a standardized data request; a two-week response window was allowed before classifying the data as unavailable.

## 4.6 Statistical Analysis

**Overall effect size (RQ1).** A random-effects model with the restricted maximum likelihood (REML) estimator was fitted to estimate the overall mean effect of agentic AI on learning outcomes. Heterogeneity was assessed using the *Q*-statistic, *I*^2 (proportion of total variability due to true heterogeneity), tau^2 (between-study variance), and the 95% prediction interval.

**Dependent effect sizes.** Because many studies report multiple outcomes (e.g., knowledge test and motivation scale), a three-level meta-analytic model was employed as the primary approach, with effect sizes (Level 1) nested within studies (Level 2) and between-study heterogeneity at Level 3 (Van den Noortgate et al., 2013). Robust variance estimation (RVE) with cluster-robust standard errors (Hedges et al., 2010; Pustejovsky & Tipton, 2022) was employed as a complementary approach and for small-sample inference using the clubSandwich package in R.

**Moderator analyses (RQ2-RQ4).** Categorical moderators (human oversight level, agent architecture, learning context) were examined using mixed-effects subgroup analysis, with the between-group heterogeneity test (*Q*_between) assessing whether moderator levels differed significantly. For exploratory analyses with continuous moderators (publication year, intervention duration), meta-regression was employed. All moderator analyses used cluster-robust variance estimation to account for dependent effect sizes.

A minimum cell size of *k* >= 4 studies per moderator level was required for subgroup analysis. Moderator levels with fewer than four studies were either collapsed with conceptually adjacent levels or reported descriptively without formal testing.

**Publication bias (RQ1).** Publication bias was assessed using multiple complementary methods: visual inspection of funnel plots, Egger's regression test for funnel plot asymmetry, the trim-and-fill method (Duval & Tweedie, 2000), and the *p*-curve analysis. For the primary analysis, a fail-safe *N* (Rosenthal's method) was reported as a supplementary indicator.

**Sensitivity analyses.** Four pre-specified sensitivity analyses were conducted: (a) exclusion of studies with high overall risk of bias; (b) exclusion of pre-post within-subjects designs (retaining only between-group comparisons); (c) comparison of three-level model and RVE results; and (d) for the human oversight moderator, exclusion of studies coded with default rules due to insufficient intervention description (i.e., where oversight level was inferred rather than explicitly reported).

**Software.** All analyses were conducted in R (version >= 4.3.0) using the metafor (Viechtbauer, 2010), clubSandwich (Pustejovsky & Tipton, 2022), and robumeta packages. Analysis scripts are available in the project repository.

## 4.7 Risk of Bias Assessment

Risk of bias in individual studies was assessed using an adapted version of the Cochrane Risk of Bias tool (Sterne et al., 2019), modified for educational research contexts. Seven domains were evaluated: random sequence generation, allocation concealment, blinding of participants, blinding of outcome assessment, incomplete outcome data, selective outcome reporting, and other sources of bias. Each domain was rated as low risk, some concerns, or high risk. An overall risk of bias judgment was derived following Cochrane guidelines. Risk of bias ratings were used as a moderator in sensitivity analyses and as a quality indicator in the interpretation of results.
