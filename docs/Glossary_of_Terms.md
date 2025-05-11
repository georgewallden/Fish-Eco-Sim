# Glossary of Terms - Fish Eco Sim

**Version:** 0.1 (Initial Draft)
**Last Updated:** 5/10/2025

---

This document defines key terms, acronyms, and concepts used throughout the Fish Eco Sim project documentation and development.

## A

*   **Action (Agent Action):** A discrete choice or command issued by an agent's intelligence (e.g., Move North, Eat). Represented by the `AgentActionInput` enum in Rust and an `AgentAction` Protobuf message.
*   **Agent:** A simulated entity in the Fish Eco Sim, possessing traits and capable of perception, action, and (eventually) learning/evolution. Implemented in the Rust Simulation Layer.
*   **Agent Intelligence Layer (AIL):** The system (primarily Python) responsible for an agent's decision-making, typically using neural networks and Deep Reinforcement Learning. Corresponds to `a0.8.Y.Z` in Alpha.
*   **Agent Evolution System (AES) / Evolution Engine:** The system (primarily Python) responsible for applying evolutionary algorithms (like Genetic Algorithms) to agent populations. Corresponds to `a0.9.Y.Z` in Alpha.
*   **Alpha Phase:** The initial development phase focused on building the core architecture and achieving a Proof of Concept for the system's key dynamic loops. Versions are prefixed with `a0.`.
*   **Apache Parquet:** A columnar storage file format used by the Logging Layer for efficient, persistent storage of simulation event data.

## B

*   **Beta Phase:** The development phase following Alpha, focused on stabilizing, refining, achieving feature completeness for a V1.0 target, and performance optimization. Versions are prefixed with `b1.` (or similar).

## C

*   **Cell:** The smallest discrete unit of space in the 2D simulation grid, possessing properties like depth, cell type, and occupancy status.
*   **Communication Layer:** The collection of technologies (NATS, gRPC), protocols, and message schemas (Protobuf, FlatBuffers) that enable inter-service communication. Corresponds to `a0.2.Y.Z` in Alpha for definition.
*   **Configuration Management System:** The system (YAML files + Python UI tool) for defining, storing, and managing all configuration parameters. Corresponds to `a0.1.Y.Z` and `a0.11.Y.Z` in Alpha.

## D

*   **Deep Reinforcement Learning (DRL):** A type of machine learning where agents learn optimal behaviors by interacting with an environment and receiving rewards, using deep neural networks as function approximators.
*   **Design Document:** A document detailing the architecture, components, interactions, and other considerations for a specific layer or system.

## E

*   **Entity:** A generic term for any distinct object in the simulation (e.g., Agent, Food Pellet).
*   **Entity Component System (ECS):** An architectural pattern common in game development for managing entities and their properties (data) and behaviors (systems). A potential future pattern for the Rust Simulation Layer.
*   **`event_type_key`:** A string identifier within `GenericEventRequest` that specifies the type and schema of the `event_payload`. Defined in the `Schema_Registry.md`.
*   **Experiment Management System (EMS):** The system (Python scripts/UI) for defining, automating, and tracking batches of simulation runs (experiments). Corresponds to `a0.6.Y.Z` in Alpha.

## F

*   **Fitness / Fitness Function:** In the Evolution Engine, a measure of an agent's (or genome's) success or performance in the simulation, used for selection.
*   **FlatBuffers:** An efficient cross-platform serialization library that allows access to serialized data without parsing/unpacking (zero-copy). Used for `WorldStateUpdate`.

## G

*   **Genetic Algorithm (GA):** An evolutionary algorithm inspired by natural selection, used in the Evolution Engine to evolve agent traits or parameters.
*   **Genome:** The genetic representation of an agent's heritable traits, used by the Evolution Engine.
*   **`GenericEventRequest`:** A Protocol Buffer message used as a standard wrapper for most asynchronous events published in the system.
*   **Go (Golang):** The programming language used for the Orchestration Layer.
*   **gRPC (gRPC Remote Procedure Calls):** A high-performance RPC framework used for synchronous request/response communication between services.
*   **Grid:** The 2D spatial environment where the simulation takes place.

## L

*   **Logging Layer:** The system (primarily Python) responsible for capturing and persistently storing simulation events to Apache Parquet files. Corresponds to `a0.7.Y.Z` in Alpha.

## M

*   **Monitoring & Alerting System:** The system (Prometheus, Grafana, Alertmanager) for observing system health, performance metrics, and sending alerts.
*   **Message Schemas:** Formal definitions of the structure of data exchanged between services (e.g., Protobuf messages, FlatBuffer tables).

## N

*   **NATS:** A high-performance messaging system used for asynchronous Publish-Subscribe communication.
*   **NATS JetStream:** The persistence layer for NATS, used by the Logging Layer for durable event streams.
*   **Neural Network (NN):** A computational model inspired by biological neural networks, used in the Agent Intelligence Layer as the "brain" for DRL agents.

## O

*   **Observation (Agent Observation):** The set of data an agent perceives from its environment and internal state at a given tick. Represented by `AgentObservationData` in Rust and an `AgentObservation` Protobuf message.
*   **Orchestration Layer (Orchestrator):** The central Go service responsible for managing Simulation Worker lifecycles, routing communication, and handling control commands. Corresponds to `a0.3.Y.Z` in Alpha.

## P

*   **Proof of Concept (PoC):** The primary deliverable of the Alpha phase, demonstrating the viability of the core architecture and key dynamic loops (simulation, learning, evolution).
*   **Protocol Buffers (Protobuf):** A language-neutral, platform-neutral, extensible mechanism for serializing structured data. Used for most discrete events and commands.
*   **Publish-Subscribe (Pub/Sub):** A messaging pattern where publishers send messages to topics without knowing specific subscribers, and subscribers receive messages from topics they are interested in.
*   **Python:** The programming language used for the Agent Intelligence Layer, UI Layer, Logging Layer, and most utility/management tools.

## R

*   **Reinforcement Learning (RL):** See Deep Reinforcement Learning.
*   **Roadmap:** The planning document outlining the features and tasks for different development phases (Alpha, Beta, Full Version).
*   **Rust:** The programming language used for the Simulation Layer.

## S

*   **Schema Registry:** The document (`Schema_Registry.md`) that centrally defines all `event_type_key`s, message schemas, NATS topics, and gRPC services.
*   **Simulation Layer (Simulation Engine / Sim Worker):** The core Rust component that runs the actual simulation logic. Corresponds to `a0.4.Y.Z` and `a0.5.Y.Z` in Alpha.
*   **Statistical Interpretation / Analysis Layer:** The collection of tools and scripts (primarily Python) used for offline analysis of logged simulation data.

## T

*   **Tick (Simulation Tick):** A discrete unit of time advancement in the simulation.
*   **Time-Series Database (TSDB):** A database optimized for storing and querying time-stamped data (e.g., Prometheus for metrics).

## U

*   **UI Layer (User Interface):** The system (primarily Python/Pygame) for visualizing the simulation and allowing user interaction. Corresponds to `a0.10.Y.Z` in Alpha.

## Y

*   **YAML (YAML Ain't Markup Language):** A human-readable data serialization standard used for configuration files.

---