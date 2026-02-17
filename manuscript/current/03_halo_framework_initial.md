# 3. The HALO Framework: Initial Architecture

This section introduces the initial version of the HALO (Human-AI Learning Orchestration) Framework -- a three-layer architecture for designing, implementing, and evaluating AI agent-based learning systems. This pre-analysis version is grounded in the theoretical foundations presented in Section 2 and the existing empirical literature. The refined version, informed by the meta-analytic findings of this study, is presented in Section 6.

## 3.1 Design Rationale

The HALO Framework addresses a fundamental challenge: translating meta-analytic evidence into actionable design principles for educational AI. Prior meta-analyses in this domain (e.g., Dai et al., 2024; Ma et al., 2014) have reported effect sizes and moderator results but have not systematically mapped findings to design specifications. HALO provides this translational structure. Each layer of the framework corresponds to a specific category of design decisions, and each decision point is linked to a specific moderator variable analyzed in this meta-analysis.

Two core assumptions guide the framework. First, neither full AI autonomy nor full human control is universally optimal; the appropriate balance depends on learner characteristics, learning context, and outcome type. Second, multi-agent architectures require explicit coordination protocols; orchestration is a design requirement, not an emergent property.

## 3.2 Three-Layer Architecture

The HALO Framework comprises three layers, each addressing a distinct design question:

**Layer 1: Foundation -- "For whom and in what context?"**

The Foundation layer establishes baseline parameters: who the learner is, what context they are in, and what outcomes are targeted. It encompasses two key calibration decisions. First, *agency level calibration* determines the appropriate APCP level (Adaptive, Proactive, Co-Learner, or Peer; Yan, 2025) based on learner developmental stage, domain structure, and target outcome level. Grounded in Self-Determination Theory (Ryan & Deci, 2000), higher-agency levels are hypothesized to be more effective for advanced learners in ill-structured domains, while lower-agency levels may better serve novice learners in well-structured domains. Second, *context-specific rules* configure the system differently for K-12 (higher structure, more checkpoints), higher education (moderate structure, balanced checkpoints), and workplace training (lower structure, strategic checkpoints), drawing on Affordance Actualization Theory (Bernhard et al., 2013) to predict context-dependent effectiveness.

*Meta-analysis input*: RQ4 (learning context moderation) provides the primary evidence for Layer 1 calibration.

**Layer 2: Protocol -- "What should the system track and communicate?"**

The Protocol layer defines the information infrastructure: what learner state dimensions the system monitors and how agents communicate. Drawing on Yang's (2025) Dynamic Learner State model, this layer specifies four tracking dimensions -- mastery, confidence, context, and decay -- that collectively represent the learner's evolving condition during AI-assisted learning. The adaptivity engine maps these dimensions to system responses, ranging from simple performance-adaptive behavior (adjusting difficulty based on scores) to multi-dimensional adaptation (simultaneously tracking knowledge, affect, and engagement).

For multi-agent systems, this layer additionally specifies communication protocols: how agents share learner state information, how handoffs between agents are structured, and how conflicts between agent recommendations are resolved.

*Meta-analysis input*: RQ3 (architecture moderation) determines whether multi-agent coordination yields measurably better outcomes than single-agent operation, informing whether the full Protocol layer is warranted.

**Layer 3: Orchestration -- "How should AI agents and humans interact?"**

The Orchestration layer governs real-time interaction between AI agents, human educators, and learners. Its central component is *human oversight calibration*, grounded in Parasuraman et al.'s (2000) automation level taxonomy and operationalized through a three-level scheme: fully autonomous operation, AI-led with human checkpoints, and human-led with AI support (see Section 2.3).

Checkpoints are triggered by Event System Theory criteria (Morgeson et al., 2015): when learning events exhibit high novelty, disruption, or criticality, oversight level escalates. Three checkpoint types are defined: *critical* (mandatory human review before proceeding), *advisory* (human notified; can intervene or approve AI continuation), and *informational* (human informed; AI continues unless overridden). Checkpoint frequency is calibrated by context -- higher for K-12 and high-stakes professional education, lower for workplace training where adult autonomy is expected.

*Meta-analysis input*: RQ2 (human oversight moderation) provides the primary evidence for Layer 3 calibration. If checkpoint-based AI shows significantly larger effects than fully autonomous AI, this validates the checkpoint architecture; if not, the layer is simplified.

## 3.3 Falsifiability and Adaptation

A distinguishing feature of the HALO Framework is its explicit falsifiability. Table 2 presents the hypothesized mappings from meta-analytic findings to design principles, along with the framework adjustments that would follow from unexpected findings.

**Table 2**

*Hypothesized Meta-Analytic Findings and HALO Framework Implications*

| Hypothesized Finding | Design Principle | If Not Supported |
|---------------------|-----------------|-----------------|
| AI-led with checkpoints > fully autonomous (RQ2) | Human checkpoints as default | Checkpoints optional; context-specific deployment |
| Multi-agent > single-agent (RQ3) | Multi-agent orchestration recommended | Simplify Layer 2; single-agent sufficient |
| Significant context effects (RQ4) | Context-specific configuration required | Universal configuration; simplify Layer 1 |
| Higher-agency AI more effective for advanced learners | Progressive agency calibration | Uniform agency level across contexts |

This pre-analysis framework will be refined following the meta-analytic results reported in Section 5, with the evidence-based version presented in Section 6.
