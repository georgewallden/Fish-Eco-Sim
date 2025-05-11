# Fish Eco Sim - Beta Phase Roadmap (Conceptual Goals)

**Roadmap Revision:** 0.1 (Conceptual Outline)
**Last Updated:** 5/10/2025
**Prerequisite:** Successful completion of Alpha PoC (`a0.12.4.3`).

---

## 1. Philosophy & Goals for Beta Phase

The Beta phase for Fish Eco Sim is focused on **"Stabilizing, Refining, Feature Completeness, & Preparing for Advanced Research/Use."**

Building on the validated core architecture and dynamic loops (simulation, DRL, basic GA) from the Alpha PoC, the Beta phase aims to:

1.  **Enhance Robustness & Stability:**
    *   Address bugs and stability issues identified during Alpha and through more extensive Beta testing.
    *   Improve error handling, resilience, and fault tolerance across all services.
2.  **Achieve Feature Completeness for Target "V1.0":**
    *   Implement more advanced features within each core system (Simulation, AI, Evolution, UI, Experiment Management, etc.) that were deferred from Alpha.
    *   Flesh out the "nice-to-have" functionalities to create a more complete and powerful platform.
3.  **Performance Optimization:**
    *   Profile the system under more demanding loads (larger worlds, more agents, longer runs).
    *   Identify and address key performance bottlenecks in the Simulation Engine, Orchestrator, data pipelines, and AI training/inference.
4.  **Usability & User Experience (UX) Improvements:**
    *   Refine the UI Layer for better clarity, aesthetics, and ease of use.
    *   Improve the usability of the Configuration Editor and Experiment Management tools.
    *   Ensure documentation is clear, comprehensive, and user-friendly.
5.  **Expand Research Capabilities:**
    *   Enable more complex DRL experiments (e.g., different algorithms, multi-agent scenarios).
    *   Develop more sophisticated capabilities for the Evolution Engine (e.g., co-evolution, more complex genomes).
    *   Provide richer data logging and more advanced tools/integrations for the Statistical Analysis Layer.
6.  **Prepare for a Potential "Version 1.0" Release:**
    *   Conduct thorough end-to-end testing with a focus on reliability and user workflows for defined research use cases.
    *   Ensure all documentation is complete and accurate for a V1.0 feature set.

**What Beta IS:**
*   A concerted effort to build a **stable, performant, and feature-rich** version of the platform.
*   The phase where advanced AI (more complex DRL, potentially MARL) and evolutionary mechanisms (more sophisticated GAs, neuroevolution) are developed and integrated.
*   A period of significant testing, bug fixing, and polish based on internal use and potentially feedback from a small group of trusted external testers/collaborators.
*   The development of more user-friendly interfaces for managing experiments and analyzing results.

**What Beta is (likely) NOT:**
*   The *final* polished product with every conceivable feature. Some "stretch goals" or very advanced research ideas might still be deferred to post-V1.0 development.
*   Guaranteed to be entirely bug-free, but critical and major bugs impacting core V1.0 functionality should be resolved.

**Versioning during Beta:**
All versions in this phase will follow the `b1.X.Y.Z` (or `bV.X.Y.Z` if multiple major Beta cycles are envisioned before a V1.0 GA) scheme as defined in the `Versioning_Strategy.md` document, where:
*   `b1` (or `bV`): Denotes the Beta Phase for a target V1.0 (or V.0) release.
*   `X`: Major Beta Feature Set or Refinement Focus Area.
*   `Y`: Sub-Feature Milestone or Area of Work within `X`.
*   `Z`: Atomic Task, Bug Fix, or Small Increment within `Y`.
*   The `t` suffix continues to denote that tests for the corresponding item are defined and implemented.
*   All `X`, `Y`, `Z` components are 1-indexed.

---

## 2. Beta Phase - Potential Major Focus Areas (`b1.X`) (Conceptual - To Be Detailed Later)

This section will eventually detail the sequence of Major Beta Feature Sets (`b1.X`) and their constituent Sub-Feature Milestones (`b1.X.Y`) and Atomic Tasks (`b1.X.Y.Z`).

**Potential High-Level Focus Areas for Beta could include:**

*   **`b1.1.Y.Z`: Advanced Simulation Mechanics & Environment**
    *   More complex agent interactions (e.g., predation models, simple communication).
    *   Richer environment (e.g., obstacles, resource patches, dynamic elements).
    *   Agent reproduction.
*   **`b1.2.Y.Z`: Advanced Agent Intelligence (DRL/MARL)**
    *   Implementation of more sophisticated DRL algorithms (e.g., PPO, SAC).
    *   Support for multi-agent reinforcement learning (MARL) scenarios (e.g., cooperative/competitive tasks).
    *   Hierarchical Reinforcement Learning (HRL) for complex behaviors.
    *   More complex Neural Network architectures.
*   **`b1.3.Y.Z`: Advanced Evolution Engine (GA/Neuroevolution)**
    *   Evolving Neural Network topologies (e.g., NEAT principles) or weights directly.
    *   Co-evolutionary setups.
    *   More sophisticated genome representations and evolutionary operators.
*   **`b1.4.Y.Z`: UI Layer V2 & User Experience Polish**
    *   Significant UI enhancements (aesthetics, usability, new visualizations like heatmaps/graphs).
    *   Historical data playback feature implementation.
    *   Potential migration to C# UI if Python performance limits were hit for complex rendering.
*   **`b1.5.Y.Z`: Experiment Management System V2 (Full UI & Features)**
    *   Develop a full GUI for defining, launching, and tracking experiments.
    *   Integration with experiment tracking tools (MLflow, W&B).
    *   More advanced parameter sweep/optimization strategies.
*   **`b1.6.Y.Z`: Statistical Analysis Layer V2 (Advanced Tools & Dashboards)**
    *   Development of standardized analysis scripts and notebooks for common research questions.
    *   Potential for a dedicated analysis dashboard (e.g., Streamlit/Dash app).
    *   Integration with TSDB for real-time simulation domain metric dashboards (if deemed necessary after Alpha).
*   **`b1.7.Y.Z`: Performance Optimization & Scalability Enhancements**
    *   Targeted optimization of bottlenecks identified in Alpha across all layers.
    *   Testing and improving scalability for larger simulations / more workers.
*   **`b1.8.Y.Z`: Comprehensive Testing, Documentation, & V1.0 Release Preparation**
    *   Extensive E2E testing, stress testing, long-duration stability tests.
    *   Finalizing all user and developer documentation for V1.0 features.
    *   Addressing all critical/major bugs.

---