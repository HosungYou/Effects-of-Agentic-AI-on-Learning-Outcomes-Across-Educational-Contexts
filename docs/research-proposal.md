# Research Proposal: Effects of Agentic AI on Learning Outcomes Across Educational Contexts

## A Meta-Analysis with Implications for Human-AI Learning Orchestration

---

## 1. Introduction and Problem Statement

The rapid proliferation of AI agents in education has outpaced the development of evidence-based design principles. While AI-powered tutoring systems, conversational agents, and pedagogical agents are increasingly deployed across K-12, higher education, and workplace training contexts, fundamental questions remain unanswered:

- **When should AI agents act autonomously, and when should humans intervene?**
- **Are multi-agent systems more effective than single-agent systems?**
- **Does the effectiveness of Agentic AI vary across educational contexts?**

This research addresses these questions through a systematic meta-analysis of Agentic AI interventions in education, followed by the development of the **HALO (Human-AI Learning Orchestration) Framework** -- an empirically-grounded architecture for designing AI agent-based learning support systems.

### Background

This study is inspired by Yang (2025), "Towards Dynamic Learner State: Orchestrating AI Agents and Workplace Performance via the Model Context Protocol" (*Education Sciences*), which introduced the concept of dynamic learner state tracking through the Model Context Protocol (MCP). We extend this work by providing meta-analytic evidence for the design principles that should govern AI agent deployment in learning contexts.

---

## 2. Coherence Logic: Why Meta-Analysis to Framework?

### The Coherence Problem

A direct meta-analysis of AI agent interventions provides a coherent pathway to framework development because each moderator variable maps directly to a specific design principle:

| Meta-Analysis Component | Framework Output |
|------------------------|-----------------|
| Human oversight moderator (RQ2) | Checkpoint calibration rules (Diverga principles) |
| Agent architecture moderator (RQ3) | Multi-agent orchestration guidelines (MCP principles) |
| Learning context moderator (RQ4) | Context-specific configuration rules (HRD relevance) |
| Overall effect + additional moderators | Comprehensive design principles |

This direct mapping ensures that the framework is grounded in empirical evidence rather than theoretical speculation alone.

---

## 3. Research Gap

### 3.1 Comparison with Existing Meta-Analyses

| Existing Meta-Analysis | Limitation | Our Differentiation |
|----------------------|-----------|-------------------|
| Dai et al. (2024): AI virtual agents in simulations | Simulation-only; human oversight not coded | All educational contexts; human oversight as key moderator |
| Ma et al. (2014): ITS meta-analysis | Pre-agentic AI era; over 10 years old | 2018-2025 Agentic AI era studies |
| Multiple 2024-2025 GenAI meta-analyses | Focus on GenAI tools (ChatGPT); do not distinguish agent autonomy | Focus on "agentic" characteristics (autonomous action capability) |
| Affective AI meta-analyses (2025) | Limited to affective AI | All AI agent types included |

### 3.2 Three Core Gaps

1. **No meta-analysis has applied established automation level frameworks (Parasuraman et al., 2000) to examine human oversight as a moderator of AI effectiveness in education** -- despite human oversight being a core requirement of emerging AI governance frameworks (EU AI Act, 2024).

2. **No meta-analysis has compared single vs. multi-agent architectures** -- The empirical basis for MCP-based multi-agent orchestration is absent.

3. **Cross-context comparison of Agentic AI effectiveness is unexplored** -- Whether AI agents work differently in K-12, higher education, and workplace training remains untested at the meta-analytic level.

---

## 4. Theoretical Foundations

### 4.1 Affordance Actualization Theory (AAT)

Bernhard et al. (2013) propose that technology affordances are not automatically realized but depend on contextual factors. In HALO, AAT explains why the same AI agent type may produce different effects across contexts -- the affordance-context fit determines actualization.

**Role in meta-analysis**: Explains heterogeneity in effect sizes across AI agent types and contexts.

**HALO mapping**: Layer 3 agent role-affordance mapping.

### 4.2 Event System Theory (EST)

Morgeson et al. (2015) characterize organizational events by novelty, disruption, and criticality. Applied to learning, EST provides a framework for determining when AI agents should yield control to human oversight.

**Role in meta-analysis**: Provides theoretical basis for the human oversight moderator coding.

**HALO mapping**: Layer 3 checkpoint trigger conditions.

### 4.3 Dynamic Learner State (Yang, 2025)

Yang proposes that effective AI-supported learning requires tracking dynamic learner states (mastery, confidence, context, decay) through the Model Context Protocol.

**Role in meta-analysis**: Informs coding of adaptivity level and state tracking capabilities.

**HALO mapping**: Layer 2 MCP-based state tracking variables.

### 4.4 Self-Determination Theory (SDT)

Ryan and Deci (2000, 2017) identify autonomy, competence, and relatedness as basic psychological needs. Human oversight level directly affects learner autonomy, making SDT essential for interpreting oversight moderator results.

**Role in meta-analysis**: Provides psychological explanation for why different oversight levels produce different effects.

**HALO mapping**: Layer 1 autonomy-supervision balance.

### 4.5 APCP Framework (Yan, 2025)

Yan classifies AI agency into four progressive levels: Adaptive, Proactive, Co-Learner, and Peer. This taxonomy provides the coding scheme for agent agency level.

**Role in meta-analysis**: Coding scheme for agent agency level variable.

**HALO mapping**: Layer 1 agency level calibration.

### 4.6 Automation Level Theory (Parasuraman et al., 2000)

Parasuraman, Sheridan, and Wickens (2000) established a foundational taxonomy of 10 levels of human-automation interaction, ranging from full human control to full automation. This framework has been widely applied in aviation, healthcare, and autonomous vehicles (e.g., SAE driving automation levels), but has not been systematically applied to educational AI.

**Role in meta-analysis**: Provides the theoretical grounding for the three-level human oversight coding taxonomy (RQ2). Our coding scheme collapses Parasuraman et al.'s 10 levels into three meta-analytically tractable categories: fully autonomous (automation levels 7-10), AI-led with checkpoints (levels 4-6), and human-led with AI support (levels 1-3).

**HALO mapping**: Layer 3 oversight calibration principles.

**Policy relevance**: The EU AI Act (2024, Article 14) mandates human oversight for high-risk AI systems, including those deployed in educational contexts. This regulatory development makes empirical evidence on optimal oversight levels both timely and practically critical.

---

## 5. Research Questions

**RQ1 (Overall Effect)**: What is the overall effect of Agentic AI interventions on learning outcomes in educational contexts?

**RQ2 (Human Oversight)**: How does the level of human oversight (fully autonomous / AI-led with checkpoints / human-led with AI support) moderate the effect of Agentic AI on learning?

**RQ3 (Agent Architecture)**: What is the difference in learning effect sizes between single-agent and multi-agent systems?

**RQ4 (Learning Context)**: How do learning contexts (K-12 / Higher Education / Workplace Training and Professional Education) moderate the effectiveness of Agentic AI?

**RQ5 (Framework Derivation)**: What design principles for AI agent-based learning support systems (HALO) are implied by the meta-analysis results?

---

## 6. Method

### 6.1 Protocol

- **Guideline**: PRISMA 2020 (Page et al., 2021)
- **Pre-registration**: PROSPERO or OSF Pre-registration
- **Effect Size**: Hedges' g (standardized mean difference)

### 6.2 Search Strategy

**Databases**: Web of Science, Scopus, ERIC, PsycINFO, IEEE Xplore, ACM Digital Library

**Search String Structure**:

```
("AI agent*" OR "intelligent agent*" OR "virtual agent*" OR "agentic AI"
 OR "intelligent tutoring system*" OR "AI-powered agent*"
 OR "pedagogical agent*" OR "conversational agent*"
 OR "AI chatbot" OR "multi-agent system*" OR "AI assistant*")
AND
("learning outcome*" OR "academic achievement" OR "performance"
 OR "knowledge gain" OR "skill acquisition" OR "learning gain*"
 OR "test score*" OR "assessment")
AND
("education*" OR "training" OR "learning" OR "instruction"
 OR "workplace" OR "professional development" OR "workforce")
```

**Publication Period**: 2018-2025

See `search-strategy.md` for detailed search strategy including database-specific adaptations.

### 6.3 Inclusion/Exclusion Criteria

| Criterion | Include | Exclude |
|-----------|---------|---------|
| **Design** | Experimental, quasi-experimental, pre-post (quantitative ES calculable) | Purely qualitative, case study, survey-only |
| **Intervention** | AI agent with autonomous action capability | Simple search tools, static content |
| **Comparison** | AI agent absent or non-agentic AI condition | No comparison group |
| **Outcome** | Learning outcomes (cognitive, skill, affective, performance) | Satisfaction-only, system performance-only |
| **Context** | K-12, higher education, workplace, professional, continuing education | Pure lab experiments without learning context |
| **Language** | English | Non-English |

See `search-strategy.md` for detailed inclusion/exclusion criteria.

### 6.4 Coding Scheme

The coding scheme covers four domains:

- **A. Study Characteristics**: Year, journal, country, design, sample size
- **B. AI Agent Characteristics**: Human oversight level, agent architecture, agency level (APCP), role, modality, technology, adaptivity
- **C. Learning Context Characteristics**: Context type, domain, mode, delivery format
- **D. Learning Outcome Characteristics**: Outcome type, Bloom's level, measurement, timing

See `coding-scheme.md` for the complete coding manual with operational definitions and decision rules.

### 6.5 Analysis Strategy

**Step 1: Overall Effect Size (RQ1)**
- Random-effects model (Hedges' g)
- Heterogeneity: Q-statistic, I-squared, tau-squared
- Publication bias: Funnel plot, Egger's test, trim-and-fill

**Step 2: Moderator Analysis (RQ2-4)**
- Subgroup analysis for categorical moderators
- Meta-regression for continuous moderators
- Mixed-effects models for moderator interactions

**Step 3: Robust Variance Estimation**
- RVE (Robust Variance Estimation) for studies reporting multiple effect sizes
- Or 3-level meta-analysis (effect sizes nested within studies)

**Step 4: Framework Derivation (RQ5)**
- Map moderator analysis results to HALO Framework layers
- Derive design principles from effect size patterns

### 6.6 Software

- R: `metafor`, `robumeta`, `clubSandwich` packages
- PRISMA Flow Diagram: Auto-generated
- Intercoder reliability: Cohen's kappa (2 independent coders)

### 6.7 Expected Study Pool

- **Expected**: 40-80 studies, 100-200 effect sizes
- Dai et al. (2024) found 22 studies for AI agents in simulations alone
- Ma et al. (2014) extracted 107 effect sizes for ITS alone
- Our broader scope justifies higher estimates

---

## 7. HALO Framework

### 7.1 Initial Version (Pre-Meta-Analysis)

The HALO Framework consists of three layers, each informed by different meta-analytic findings:

- **Layer 1 (Foundation)**: FOR WHOM and IN WHAT CONTEXT -- Agency level calibration, context-specific rules, outcome-specific rules
- **Layer 2 (Protocol)**: WHAT should the system track -- Dynamic learner state tracking, multi-agent communication, adaptivity engine
- **Layer 3 (Orchestration)**: HOW should AI agents interact -- Human oversight calibration, agent role assignment, mode collapse prevention

See `halo-framework.md` for the complete framework specification.

### 7.2 Meta-Analysis to Design Principle Mapping

| Meta-Analysis Finding (Hypothetical) | HALO Design Principle | Layer |
|--------------------------------------|----------------------|-------|
| Checkpoint-based > fully autonomous | Human checkpoints as default setting | Layer 3 |
| Multi-agent > single agent | Multi-agent orchestration recommended | Layer 2 |
| Co-Learner/Peer more effective in workplace | Higher AI agency for adult learners | Layer 1 |
| Multi-dimensional adaptivity > static | Multi-dimensional state tracking justified | Layer 2 |
| Human-led better for higher-order outcomes | Human-led mode for Evaluate/Create tasks | Layer 3 |
| Significant context effects | Context-specific configuration required | Layer 1 |

### 7.3 Refined Version (Post-Meta-Analysis)

The refined version will replace hypothetical mappings with actual meta-analytic findings, including:
- Specific effect size thresholds for design recommendations
- Confidence intervals around design principle recommendations
- Evidence strength ratings for each design principle

---

## 8. Paper Structure

1. **Introduction**: Problem statement, research gap, purpose
2. **Theoretical Background**: Agentic AI definition (APCP), Dynamic Learner State & MCP, Human-in-the-Loop Orchestration (Diverga), theoretical integration (AAT, EST, SDT)
3. **The HALO Framework (Initial Version)**: Theory-based initial framework
4. **Method**: PRISMA protocol, search/screening, coding, analysis strategy
5. **Results**:
   - 5.1 Study Selection & Descriptives
   - 5.2 Overall Effect (RQ1)
   - 5.3 Human Oversight Moderation (RQ2)
   - 5.4 Agent Architecture Moderation (RQ3)
   - 5.5 Learning Context Moderation (RQ4)
   - 5.6 Additional Moderators
6. **HALO Framework (Refined Version)**: Evidence-based refinement (RQ5)
7. **Discussion**: Theoretical implications, practical implications (HRD, EdTech, AI developers), limitations, future research
8. **Conclusion**

---

## 9. Expected Contributions

### Theoretical Contributions
1. First meta-analytic evidence on human oversight level effects in AI-assisted learning
2. Empirical comparison of single vs. multi-agent system effectiveness
3. HALO Framework integrating MCP + Diverga with evidence-based design principles
4. Cross-context Agentic AI effectiveness comparison (K-12 vs. HE vs. Workplace)

### Practical Contributions
1. Guidelines for optimal human oversight levels in AI agent deployment
2. Evidence-based criteria for single vs. multi-agent implementation decisions
3. Design checklist for AI agents in workplace/professional learning
4. HALO Framework as an evaluation tool for AI agent systems

### Methodological Contributions
1. Systematic coding framework for AI "agenticity" classification
2. Operational definition and coding methodology for human oversight levels

---

## 10. Originality Summary

| Dimension | Existing Work | This Study |
|-----------|--------------|------------|
| **Target** | AI tools in general or specific types | "Agentic AI" -- AI with autonomous action capabilities |
| **Key Moderator** | AI type, subject, learner level | **Human oversight level** (first meta-analysis), Agent architecture |
| **Context** | K-12 or higher education only | All educational contexts + workplace as moderator |
| **Framework Link** | Report results only | Meta-analysis directly converted to HALO design principles |
| **Theory** | Single learning theory | AAT + EST + SDT + DLS + APCP integration |

---

## 11. Role Distribution (Proposed)

| Area | Hosung You | Dr. Yang |
|------|-----------|----------|
| **Research Design** | HALO Framework design; coding scheme (Diverga checkpoint principles) | Dynamic Learner State theory; coding variables (MCP principles) |
| **Search/Screening** | Joint (independent screening with consensus) | Joint |
| **Coding** | Coder 1 + coding scheme management | Coder 2 (independent; Cohen's kappa) |
| **Analysis** | Meta-analysis execution (R); moderator analysis | Data validation; robustness checks |
| **Writing** | Framework, Discussion (Diverga implications) | Literature Review, Method (MCP theory) |
| **Framework** | Layer 3 (Orchestration, Checkpoints) | Layer 2 (Protocol, State Tracking) |

---

## 12. Timeline

| Phase | Duration | Activity |
|-------|----------|----------|
| Phase 1 | Month 1 | PROSPERO registration, search strategy, pilot search |
| Phase 2 | Month 1-2 | Systematic search, deduplication, title/abstract screening |
| Phase 3 | Month 2-3 | Full-text screening, final study selection |
| Phase 4 | Month 3-4 | Coding (2 independent coders), reliability, data extraction |
| Phase 5 | Month 4-5 | Meta-analysis, moderator analysis, HALO refinement |
| Phase 6 | Month 5-7 | Manuscript writing, internal review, revision |
| Phase 7 | Month 7 | Submission |

See `timeline.md` for detailed week-by-week breakdown.

---

## 13. Target Journals

| Journal | IF | Fit | Notes |
|---------|-----|-----|-------|
| **Educational Research Review** | 11.8 | Excellent | Review/meta-analysis specialist; highest impact |
| **Computers & Education** | 11.5 | Excellent | AI + education meta-analyses; strong track record |
| **Educational Psychology Review** | 10.1 | Excellent | Dai et al. (2024) predecessor journal |
| **Internet and Higher Education** | 8.6 | Good | Technology-based learning |
| **Human Resource Development Review** | 5.4 | Good | HRD framework-appropriate; lower meta-analysis frequency |

**Primary recommendation**: Educational Research Review or Computers & Education

---

## 14. Key References

- Yang, H. (2025). Towards Dynamic Learner State. *Education Sciences*, 15(8), 1004.
- Dai, Z., et al. (2024). Effects of AI-Powered Virtual Agents. *Educational Psychology Review*, 36, 31.
- Yan, L. (2025). From Passive Tool to Socio-cognitive Teammate: APCP Framework. arXiv:2508.14825.
- Ma, W., et al. (2014). ITS and Learning Outcomes. *Journal of Educational Psychology*, 106(4), 901-918.
- Bernhard, E., et al. (2013). Affordance Actualization Theory.
- Morgeson, F. P., et al. (2015). Event System Theory. *Academy of Management Review*, 40(4), 515-537.
- Ryan, R. M., & Deci, E. L. (2000). Self-Determination Theory. *American Psychologist*, 55(1), 68-78.
- Page, M. J., et al. (2021). PRISMA 2020 Statement. *BMJ*, 372, n71.

See `references.md` for the complete reference list.

---

*This proposal represents the initial research design. Methodological details will be refined during the PROSPERO registration process and pilot search phase.*
