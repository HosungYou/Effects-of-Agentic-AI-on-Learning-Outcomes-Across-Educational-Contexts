# 2. Literature Review and Theoretical Framework

## 2.1 Agentic AI in Education: From Intelligent Tutoring to Autonomous Pedagogical Action

The application of artificial intelligence to education has progressed through several distinct generations. Early computer-assisted instruction systems of the 1970s and 1980s delivered pre-programmed content sequences with minimal adaptation (Suppes, 1966). The emergence of intelligent tutoring systems (ITS) in the 1990s and 2000s represented a significant advance: these systems employed student models and pedagogical strategies to tailor instruction to individual learners in real time (VanLehn, 2011; Woolf, 2009). More recently, the convergence of large language models, reinforcement learning, and multi-agent architectures has given rise to AI systems capable of qualitatively different forms of pedagogical action: systems that can set sub-goals, monitor progress, initiate interactions, and adapt strategies without continuous human direction (Kasneci et al., 2023; Ouyang & Jiao, 2021).

This latest generation of educational AI is increasingly characterized as "agentic," a term denoting systems that exhibit autonomous, goal-directed behavior rather than merely responding to user inputs (Russell & Norvig, 2021). However, the field has lacked a systematic taxonomy for classifying the *degree* of agency that AI systems exhibit in educational contexts. Yan (2025) addresses this gap with the Adaptive-Proactive-Co-Learner-Peer (APCP) framework, which identifies four progressive levels of AI agency in education:

1. **Adaptive**: The AI reacts to learner inputs, adjusting difficulty, content, or pacing based on performance data. Traditional ITS with mastery-based progression exemplify this level.
2. **Proactive**: The AI anticipates learner needs and initiates interactions without being prompted, for example, detecting confusion from behavioral patterns and offering unsolicited scaffolding.
3. **Co-Learner**: The AI engages as a learning partner that shares the learning process, modeling joint problem-solving and collaborative knowledge construction.
4. **Peer**: The AI functions as an equal capable of reciprocal interaction and socio-cognitive co-regulation, such as AI debate partners or peer-review agents.

The APCP taxonomy is significant for meta-analytic purposes because it transforms a binary distinction (AI present vs. absent) into a graduated spectrum of agency, enabling more nuanced moderator analysis of how agent capability relates to learning effectiveness.

Concurrently, the architecture of educational AI systems has grown more complex. While early ITS operated as monolithic single-agent systems, recent designs increasingly deploy multiple specialized agents that coordinate to support different aspects of learning, for instance, a tutor agent, an assessment agent, and a motivational coach operating within a shared framework (Yang, 2025). This shift from single-agent to multi-agent architectures introduces a design dimension, agent architecture, whose effects on learning outcomes have not been examined at the meta-analytic level.

For the present meta-analysis, *agentic AI* is operationally defined as AI systems exhibiting autonomous pedagogical action at any level of the APCP spectrum, from adaptive response through peer-level interaction. This inclusive definition maximizes the breadth of the evidence base while the APCP coding scheme preserves the ability to examine differential effects by agency level.

## 2.2 Meta-Analytic Evidence on AI and Learning Outcomes

Several meta-analyses have examined the effects of AI-based educational technologies on learning outcomes, though none have addressed the full spectrum of agentic AI or examined human oversight as a moderator.

### Intelligent Tutoring Systems

The most extensive evidence base concerns intelligent tutoring systems. Ma et al. (2014), in the most comprehensive ITS meta-analysis to date, synthesized 107 effect sizes from 73 studies and found that ITS produced significantly positive effects on learning outcomes relative to teacher-led instruction (*g* = 0.42), textbooks (*g* = 0.55), and non-ITS computer-based instruction (*g* = 0.37), though the advantage over human one-on-one tutoring was negligible (*g* = 0.11). Steenbergen-Hu and Cooper (2013) focused on K-12 populations and reported more modest effects, while their subsequent analysis of postsecondary students found somewhat larger effects (Steenbergen-Hu & Cooper, 2014). VanLehn (2011), in a direct comparison of ITS and human tutoring, found that step-based ITS approached the effectiveness of expert human tutors (*d* = 0.76). Kulik and Fletcher (2016) reported a mean effect of *d* = 0.66 across 50 controlled evaluations in the broadest ITS review.

### Pedagogical and Virtual Agents

Research on pedagogical agents, embodied or animated characters that provide instruction or scaffolding, has yielded mixed results. Schroeder et al. (2013) conducted a meta-analysis of pedagogical agent effects on learning and found modest positive effects, with agent characteristics (voice, appearance, gestures) moderating outcomes. Heidig and Clarebout (2011) similarly found that pedagogical agents' effects on motivation and learning varied substantially depending on design features. More recently, Dai et al. (2024) conducted the first meta-analysis specifically focused on AI virtual agents in educational simulations, synthesizing 22 studies and reporting a moderate positive effect on learning outcomes (*g* = 0.43). Their analysis identified simulation fidelity and agent anthropomorphism as significant moderators.

### Broader AI in Education

Following the release of large language models, the landscape has expanded rapidly. Zheng et al. (2021) conducted a broad meta-analysis of AI effects on learning achievement and found significant overall positive effects, though with substantial heterogeneity. Several narrative reviews have examined AI chatbot effects on learning, identifying increased engagement but inconsistent cognitive outcomes (Deng & Yu, 2023).

### Critical Gaps

Despite this growing evidence base, three significant gaps persist in the meta-analytic literature:

*First*, existing meta-analyses have focused on specific AI subtypes (ITS, virtual agents, chatbots) rather than examining the full agency spectrum of AI systems now deployed in education. As a result, the field lacks a synthesized understanding of how agentic AI *as a class* affects learning, and whether effects differ across agency levels.

*Second*, and most critically for the present study, no meta-analysis has examined *human oversight level* as a moderator of AI effectiveness in education. Prior meta-analyses have coded moderators such as study design, subject domain, comparison condition, and learner characteristics (Dai et al., 2024; Ma et al., 2014). However, the degree of human involvement during AI-mediated learning, a dimension of increasing practical importance and now a regulatory requirement, has been entirely absent from the evidence base.

*Third*, the emergence of multi-agent AI systems in educational contexts (e.g., multi-agent debate, collaborative AI tutoring teams) introduces an architectural dimension, single-agent versus multi-agent, that existing meta-analyses have not addressed. This gap is particularly consequential given the rapid growth of multi-agent frameworks in educational technology development.

## 2.3 Human Oversight of Educational AI: An Unexamined Moderator

The question of how much human oversight to maintain over AI systems has emerged as a central concern across multiple fields. In education, this concern is particularly acute: AI systems are interacting with developing learners in high-stakes contexts where errors in pedagogical judgment can have lasting consequences. Yet the empirical basis for calibrating human oversight in educational AI remains remarkably thin.

### Automation Level Theory

Parasuraman, Sheridan, and Wickens (2000) established the foundational framework for conceptualizing human-automation interaction. Their model identifies 10 levels of automation, ranging from full human control (Level 1: the computer offers no assistance) to full computer autonomy (Level 10: the computer acts entirely on its own). Critically, Parasuraman et al. demonstrated that the optimal level of automation is not fixed but depends on the interaction among task type, environmental complexity, and the costs of automation errors. This framework has been cited over 5,000 times and successfully applied across domains including aviation (Endsley, 2017), healthcare (Parasuraman & Wickens, 2008), and autonomous vehicles (SAE International, 2021), but it has not been systematically applied to educational AI at the meta-analytic level.

### Human-Centered AI

Shneiderman (2022) extended this line of thinking by proposing a two-dimensional model in which human control and computer automation are not inversely related but can be independently calibrated. His framework suggests that the design goal should be systems that are simultaneously high in human control *and* high in computer automation, a vision that challenges the assumption of a simple trade-off between human and machine authority. In educational terms, this perspective suggests that maximizing AI capability and maintaining meaningful human oversight are not competing objectives.

### Educational Applications

Within educational research, Molenaar (2022) introduced the concept of "hybrid human-AI regulation," arguing that effective AI-supported learning requires a dynamic allocation of regulatory authority between AI-driven processes and human (teacher or learner) decision-making. She demonstrated this concept in the context of young learners' self-regulated learning, showing that the balance between human and AI regulation affects both learning processes and outcomes. Holstein et al. (2019) provided complementary empirical evidence by developing teacher awareness dashboards for AI tutoring systems and demonstrating that augmenting teachers with real-time information about AI-student interactions improved instructional targeting, suggesting that AI tutoring effectiveness is not a fixed property of the system but depends partly on the human oversight infrastructure surrounding it.

### Policy Imperative

The regulatory landscape has further elevated the significance of human oversight. The European Union's AI Act (2024), specifically Article 14, mandates that high-risk AI systems, a category that explicitly includes AI deployed in educational contexts, must be designed to allow "effective oversight by natural persons." This legal requirement creates an urgent need for empirical evidence on how different configurations of human oversight affect AI-assisted learning outcomes. Without such evidence, educational institutions and AI developers lack a principled basis for meeting regulatory requirements while maximizing pedagogical effectiveness.

### Three-Level Taxonomy for Meta-Analytic Coding

For the present study, Parasuraman et al.'s (2000) 10-level automation framework is collapsed into three meta-analytically tractable categories:

1. **Fully Autonomous** (corresponding to automation levels 7-10): The AI system operates independently during the learning interaction, making all pedagogical decisions without human intervention.
2. **AI-Led with Human Checkpoints** (levels 4-6): The AI system drives the learning experience, but human educators monitor progress and can intervene at defined checkpoints or when specific conditions are triggered.
3. **Human-Led with AI Support** (levels 1-3): Human educators retain primary pedagogical decision authority and employ the AI system as a tool that provides recommendations, automates routine tasks, or augments instruction.

This three-level scheme balances conceptual granularity with the practical requirements of meta-analytic coding: adequate cell sizes (target *k* >= 4 per level) and coding reliability (target Cohen's kappa >= 0.80). The approach follows the methodological precedent of collapsing continuous moderator dimensions in educational meta-analyses (Lipsey & Wilson, 2001) and aligns with Molenaar's (2022) conceptualization of regulation as a spectrum between full AI autonomy and full human control.

Importantly, human oversight level is coded post hoc from intervention descriptions in primary studies using a structured decision protocol, rather than being an independent variable manipulated by original researchers. This approach, which is standard in meta-analytic moderator coding (cf. Ma et al., 2014, who similarly post-hoc coded ITS dialogue type), constitutes a core methodological innovation of this study.

## 2.4 Theoretical Foundations

Four theoretical frameworks jointly inform the research questions, moderator hypotheses, and interpretive lens of this meta-analysis. Their integration provides a multi-level explanation for why agentic AI effects on learning outcomes are expected to vary systematically by oversight level, agent architecture, and learning context.

### 2.4.1 Affordance Actualization Theory (AAT)

Affordance Actualization Theory (Bernhard et al., 2013) proposes that the effects of technology are determined not by its features alone but by the interaction between technological affordances and the context of use. An affordance, a potential for action enabled by a technology, is only "actualized" when contextual conditions support its realization. Applied to educational AI, AAT explains a persistent finding in the existing literature: the same AI system can produce substantially different effects across settings (Ma et al., 2014). An adaptive AI tutor that is highly effective for well-structured mathematics instruction may produce negligible effects in ill-structured workplace problem-solving, not because the technology changes but because the conditions for affordance actualization differ.

For this meta-analysis, AAT provides the primary theoretical rationale for Research Question 4 (differential effects across learning contexts). It predicts that effect sizes will vary systematically across K-12, higher education, and workplace training because each context presents different conditions for affordance actualization, including different learner developmental stages, different institutional structures, and different pedagogical traditions that collectively shape whether and how AI agent affordances are realized.

### 2.4.2 Event System Theory (EST)

Event System Theory (Morgeson et al., 2015) characterizes events in organizational settings along three dimensions: novelty (how unusual the event is relative to existing routines), disruption (how much the event disturbs ongoing processes), and criticality (how consequential the event is for valued outcomes). Originally developed for organizational science, EST has been applied to educational settings to understand when and why interventions produce differential effects.

In the context of human oversight of AI-assisted learning, EST provides a theoretical mechanism for predicting when human intervention is most consequential. When learning events are high in novelty (a learner encounters an unfamiliar problem type), disruption (the AI's adaptive algorithm produces an unexpected or counterproductive response), or criticality (the learner approaches a high-stakes assessment or makes an error with lasting consequences), human oversight is theoretically more valuable because automated responses are less likely to be adequate for managing the event. Conversely, for routine, low-novelty events, fully autonomous AI operation may be sufficient or even preferable, as human intervention may interrupt productive learning flow.

EST thus informs Research Question 2 not merely by predicting that human oversight matters, but by specifying the mechanism through which it operates: oversight level moderates AI effectiveness because it determines the system's capacity to respond appropriately to learning events of varying novelty, disruption, and criticality.

### 2.4.3 Self-Determination Theory (SDT)

Self-Determination Theory (Ryan & Deci, 2000, 2017) identifies three basic psychological needs (autonomy, competence, and relatedness) whose satisfaction is essential for intrinsic motivation, engagement, and deep learning. SDT is among the most widely applied motivational frameworks in educational technology research and has direct implications for the human oversight moderator.

The critical theoretical tension lies between autonomy and competence. Fully autonomous AI systems (Level 1) may support learner autonomy by enabling self-paced, self-directed learning without external surveillance, but may undermine competence if the AI fails to calibrate challenge appropriately or provide adequate feedback at critical moments. Conversely, human-led systems (Level 3) may support competence through expert pedagogical judgment but risk undermining perceived autonomy if learners experience excessive monitoring or external control. AI-led systems with checkpoints (Level 2) represent a theoretical balance: the AI provides structure and responsiveness (supporting competence), while human oversight is reserved for critical junctures rather than continuous monitoring (preserving autonomy).

SDT also generates predictions for the agent architecture moderator (Research Question 3). Multi-agent systems, where learners interact with distinct AI agents fulfilling different roles (tutor, coach, collaborator), may better satisfy the need for relatedness by providing varied social interaction partners. Single-agent systems, by contrast, may better satisfy autonomy by offering a more predictable, learner-controlled interaction with a single consistent partner.

### 2.4.4 Dynamic Learner State Model (DLS)

Yang (2025) proposes the Dynamic Learner State (DLS) model, which conceptualizes the learner's condition during AI-assisted learning as a multi-dimensional, continuously evolving state. The DLS model identifies four core dimensions: mastery (current knowledge and skill levels relative to learning objectives), confidence (the calibration between self-assessed and actual competence), context (environmental and situational variables that shape learning conditions), and decay (predicted knowledge deterioration since the last learning interaction). Unlike static learner models that characterize learners by fixed attributes such as prior knowledge or learning style, the DLS model emphasizes that effective AI adaptation requires tracking how learner states change *during* the learning interaction, not merely at its outset.

The DLS model is significant for this meta-analysis in two respects. First, it provides a theoretical basis for coding the *adaptivity* dimension of AI interventions: studies employing AI systems that track multiple learner state dimensions (e.g., knowledge mastery combined with affective state and engagement patterns) can be distinguished from those employing single-dimension tracking (e.g., performance scores alone). The adaptivity coding variable (C7 in the coding scheme) operationalizes this distinction as a five-level scale from static to multi-dimensional adaptation. Second, the DLS model's emphasis on dynamic state changes provides a theoretical link between the APCP agency levels and learning outcomes: higher-agency AI systems (Co-Learner, Peer) are theoretically more capable of tracking and responding to dynamic, multi-dimensional learner states than lower-agency systems (Adaptive), suggesting a potential mechanism for differential effectiveness across agency levels.

## 2.5 Theoretical Integration and Research Questions

The four theoretical frameworks converge on a central prediction: the effectiveness of agentic AI in education is not a fixed property of the technology but emerges from the interaction among agent characteristics (APCP level, architecture, adaptivity), oversight configuration (Parasuraman automation levels), and contextual factors (learning setting, learner characteristics, outcome type). Table 1 summarizes the mapping between each theory, the moderator variables it informs, and the research questions it grounds.

**Table 1**

*Theory-to-Research Question Mapping*

| Theory | Core Mechanism | Primary RQ | Coded Variable(s) |
|--------|---------------|:----------:|-------------------|
| AAT (Bernhard et al., 2013) | Affordance-context fit determines effectiveness | RQ4 | Learning context, agent role |
| EST (Morgeson et al., 2015) | Event novelty/disruption/criticality determines oversight value | RQ2 | Human oversight level |
| SDT (Ryan & Deci, 2000) | Autonomy-competence tension shaped by oversight and architecture | RQ2, RQ3 | Oversight level, agent architecture |
| DLS (Yang, 2025) | Dynamic multi-dimensional state tracking enables adaptive response | RQ1, RQ3 | Adaptivity level, APCP agency level |

Building on this theoretical integration and the empirical gaps identified in Sections 2.2 and 2.3, the present study addresses five research questions:

**RQ1.** What is the overall effect of agentic AI interventions on learning outcomes?

**RQ2.** Does the level of human oversight, coded as fully autonomous, AI-led with human checkpoints, or human-led with AI support, moderate the effect of agentic AI on learning outcomes?

**RQ3.** Does agent architecture, specifically single-agent versus multi-agent, moderate the effect of agentic AI on learning outcomes?

**RQ4.** Does learning context, specifically K-12, higher education, or workplace training, moderate the effect of agentic AI on learning outcomes?

**RQ5.** What empirically grounded design principles can be derived from the moderator analyses to inform the HALO (Human-AI Learning Orchestration) Framework?

RQ1 establishes the overall evidence base. RQ2 through RQ4 test specific moderator hypotheses grounded in the theoretical frameworks outlined above. RQ5 serves as a translational bridge between meta-analytic evidence and educational design practice: the HALO Framework, described in detail in Section 4, provides the architectural structure into which the empirical findings from RQ1-RQ4 are systematically mapped. Briefly, HALO is a three-layer evidence-based architecture comprising Foundation (agent capability calibration), Protocol (state tracking and adaptation), and Orchestration (oversight and coordination) that translates meta-analytic findings into actionable, context-sensitive design principles for AI agent-based learning systems.
