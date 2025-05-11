# Design Philosophy & Architectural Principles

**Version:** 0.1 (Initial Draft)
**Last Updated:** 5/10/2025

---

## 1. Introduction

This document outlines the core design philosophies and architectural principles that guide the development of the Fish Eco Sim platform. Adherence to these principles aims to create a robust, maintainable, extensible, and performant system capable of achieving its research and simulation goals.

---

## 2. Core Philosophies

1.  **Modularity and Decoupling:**
    *   The system is designed as a collection of distinct layers/services with well-defined responsibilities and clear interfaces.
    *   Loose coupling is prioritized, primarily achieved through a message-driven architecture (NATS Pub/Sub) and defined service contracts (gRPC with Protobuf/FlatBuffers).
    *   This allows layers to be developed, tested, deployed, and potentially replaced or upgraded independently.

2.  **Separation of Concerns:**
    *   Each layer focuses on a specific domain: Simulation Layer on world mechanics, Agent Intelligence Layer on decision-making, Orchestration Layer on management and routing, etc.
    *   This prevents monolithic designs and makes individual components easier to understand and reason about.

3.  **Performance by Design:**
    *   Critical components like the Simulation Layer are implemented in performance-oriented languages (Rust).
    *   Efficient data serialization formats (Protocol Buffers, FlatBuffers with zero-copy access) are used for inter-service communication.
    *   Asynchronous processing and message queuing (NATS) are employed to prevent bottlenecks in data flow.
    *   While deep optimization is deferred post-Alpha, initial design choices prioritize efficient algorithms and data handling.

4.  **Extensibility and Reusability:**
    *   The Orchestration Layer is designed to be simulation-agnostic ("armless"), capable of managing different types of simulation workers.
    *   Interfaces and data contracts are designed to be general where possible, allowing for future expansion of entity types, behaviors, and simulation scenarios.

5.  **Testability:**
    *   A strong emphasis is placed on testing at all levels: unit, integration (intra-layer and inter-layer), and end-to-end.
    *   A Test-Driven Development (TDD) or Behavior-Driven Development (BDD) approach is encouraged, with tests (marked with a `t` suffix in planning versions) being defined and implemented alongside or before functional code.
    *   Decoupled services facilitate testing with mocks and stubs.

6.  **Data-Driven Insights & Reproducibility:**
    *   Comprehensive logging of simulation events to persistent, queryable formats (Apache Parquet) is a core requirement.
    *   The system supports detailed offline analysis to understand emergent behaviors, train AI, and evaluate evolutionary progress.
    *   Version control for code, configurations, experiment plans, and documentation aims to ensure reproducibility of results.

7.  **Iterative Development:**
    *   The project follows a phased approach (Alpha, Beta, Full Version) with clearly defined goals for each phase.
    *   Features are built incrementally, allowing for learning and adaptation of the plan as development progresses.

---

## 3. Key Architectural Decisions & Rationale

*   **Multi-Language Architecture:**
    *   **Rust (Simulation Layer):** Chosen for its performance, memory safety without a garbage collector, and control over system resources, ideal for the computationally intensive simulation core.
    *   **Go (Orchestration Layer):** Chosen for its excellent concurrency primitives (goroutines, channels), strong networking libraries, and suitability for building robust, scalable network services and managing processes.
    *   **Python (Agent Intelligence, UI, Logging, Tools):** Chosen for its rich ecosystem for Deep Reinforcement Learning (PyTorch/TensorFlow), data science (Pandas, NumPy, Matplotlib), rapid prototyping for UI and utility scripts, and general ease of use.
*   **Communication Technologies:**
    *   **NATS (Pub/Sub):** For asynchronous, decoupled event distribution. NATS JetStream for durable logging streams.
    *   **gRPC (RPC):** For synchronous request/response interactions and defining clear service contracts.
    *   **Protocol Buffers & FlatBuffers:** For efficient, language-agnostic data serialization. FlatBuffers specifically for high-performance, zero-copy access to large data (e.g., `WorldStateUpdate`).
*   **Simulation-Agnostic Orchestrator:** The Go Orchestration Layer is designed to manage generic "worker processes" and route generic event messages, not tied to the specifics of the Fish Eco Sim, allowing for future reuse.
*   **Agent Perception Model ("Agents only know what they sense"):** Agents do not have direct access to global simulation state. The Simulation Layer generates limited observations for each agent based on its sensors, promoting emergent behavior.
*   **Configuration Management:** YAML files for human-readable configuration, managed by a dedicated Python UI tool, supporting all services.
*   **Phased Roadmap:** Detailed planning for Alpha, conceptual outlines for Beta and Full Version, allowing for adaptation.

---