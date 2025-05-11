# Schema Registry & Interface Definitions

**Version:** 0.1 (Initial Draft)
**Last Updated:** 5/10/2025
---

## 1. Purpose

This document serves as the central registry and reference for all data schemas, message formats, event type keys, NATS topic structures, and gRPC service definitions used for inter-service communication within the Fish Eco Sim platform. Its goal is to ensure clarity, consistency, and a single source of truth for how different components exchange information.

This document is critical for developers working on any layer that publishes or consumes data from other layers. All schemas and interface definitions are versioned to manage evolution and compatibility.

---

## 2. Core Message Wrappers

### 2.1. `GenericEventRequest` (Protocol Buffer)
*   **Definition File:** `schemas/protobuf/core_events.proto` (or similar path)
*   **Purpose:** Standard wrapper for most asynchronous events published via NATS.
*   **Key Fields (defined in `a0.2.1.1`):**
    *   `event_type_key` (string): See Section 3.
    *   `event_payload` (bytes): Serialized Protobuf or FlatBuffer data.
    *   `timestamp_ns` (int64): Source-generated nanosecond timestamp.
    *   `simulation_id` (string): Identifier for the simulation run.
    *   `worker_id` (string, optional): Identifier of the Simulation Worker source.
    *   `payload_format_hint` (string): E.g., "protobuf", "flatbuffer".
    *   (Other metadata as needed)

---

## 3. `event_type_key` Registry

This section lists all defined `event_type_key` strings, their meaning, expected `event_payload` schema, and typical publishers/subscribers. (This will be populated extensively as `a0.2.Y.Z` and subsequent modules are implemented).

| `event_type_key` String (Versioned) | Description                                      | Payload Schema Name (Protobuf/FlatBuffer) | `payload_format_hint` | Typical Publisher(s)    | Typical Subscriber(s)        |
| :------------------------------------ | :----------------------------------------------- | :---------------------------------------- | :-------------------- | :---------------------- | :--------------------------- |
| `sim.world_state.v1`                  | Snapshot of current simulation world state.      | `WorldStateUpdate`                        | `flatbuffer`          | Simulation Layer (via Orch) | UI Layer, (Potentially Logger) |
| `sim.agent_observation.v1`            | Observation data for a specific agent.           | `AgentObservation`                        | `protobuf`            | Simulation Layer (via Orch) | Agent Intelligence Layer     |
| `sim.agent_reward.v1`                 | Reward signal for an agent.                      | `AgentReward`                             | `protobuf`            | Simulation Layer (via Orch) | Agent Intelligence Layer     |
*   *(More event types to be added here, e.g., `sim.agent_died.v1`, `ai.agent_action.v1`, `orchestrator.control.step.v1`, `logging.event.raw` (though this one might be implicit))*

---

## 4. Key Data Payload Schemas

(This section will list and link to the `.proto` and `.fbs` files or provide summaries of key fields for important payloads. To be populated as part of `a0.2.1.Z` and beyond.)

### 4.1. Protocol Buffer Schemas (`*.proto`)
*   Location: `schemas/protobuf/`
*   **`AgentObservation.proto` (Target: `a0.2.1.3`):** Details for agent perception.
*   **`AgentAction.proto` (Target: `a0.2.1.3`):** Details for agent actions.
*   **`AgentReward.proto` (Target: `a0.2.1.3`):** Details for reward signals.
*   **`ControlCommands.proto`:** (e.g., `StartSimulationCommand`, `PauseCommand` - used in gRPC)
*   *(Others as defined)*

### 4.2. FlatBuffer Schemas (`*.fbs`)
*   Location: `schemas/flatbuffers/`
*   **`WorldStateUpdate.fbs` (Target: `a0.2.1.2`):** Structure for world state snapshots.
*   *(Others as defined)*

---

## 5. NATS Topic Structure & Conventions

(This section will detail the agreed-upon hierarchical naming conventions for NATS topics. To be populated as part of `a0.2.2.1`.)

*   **General Structure:** `domain.context.specific_subject.{id_qualifiers}`
*   **Examples for Alpha:**
    *   Events from Simulation: `events.simulation.{sim_id}.world_state`
    *   Observations to AI: `events.simulation.{sim_id}.agent.{agent_id}.observation`
    *   Actions from AI: `commands.simulation.{sim_id}.agent.{agent_id}.action`
    *   Logging Stream (JetStream): `logging.events.raw`
    *   Control commands to specific workers: `commands.worker.{worker_id}.control`
*   *(More details on wildcard usage and specific topic paths)*

---

## 6. gRPC Service Definitions

(This section will list and link to the `.proto` files defining gRPC services and their methods. To be populated as part of `a0.2.2.2`.)

*   Location: `protos/services/` (or combined with message protos)
*   **`OrchestratorWorkerService` (exposed by Go Orchestration Layer):**
    *   `rpc RegisterWorker(WorkerInfo) returns (RegistrationAck);`
    *   `rpc ReportEvent(stream GenericEventRequest) returns (stream EventAck);` (Example, could be unary)
*   **`OrchestratorClientService` (exposed by Go Orchestration Layer):**
    *   `rpc StartSimulation(StartSimulationCommand) returns (StartSimulationResponse);`
    *   `rpc ControlSimulation(ControlCommand) returns (ControlResponse);`
*   *(Others as defined)*

---