# Fish Eco Sim - Alpha Phase Roadmap

**Roadmap Revision:** 1
**Last Updated:** 5/10/2025
**Target Alpha Version for PoC Completion:** `a0.12.4.3`

---

## 1. Philosophy & Goals for Alpha Phase

The Alpha phase for Fish Eco Sim is focused on **"Building the Core, Proving Viability, and Demonstrating Key Dynamic Loops."**

The primary objectives are to deliver a Proof of Concept (PoC) that showcases the foundational architecture and the system's capacity for emergent behavior, learning, and evolution. This includes:

1.  **Implement Foundational Multi-Language Architecture:**
    *   Establish the core services: `Rust` Simulation Engine, `Go` Orchestrator, and `Python` services for Agent Intelligence, UI, Logging, Experiment Management, and Configuration.
    *   Ensure effective inter-service communication using the defined Communication Layer patterns (`NATS`, `gRPC`, `Protobuf`, `FlatBuffers`).
2.  **Demonstrate Core Simulation Mechanics:**
    *   Implement a 2D grid world with configurable environmental properties (e.g., depth, cell types).
    *   Simulate basic agent entities with core traits (energy, age, vision) and lifecycle (spawning, death).
    *   Implement fundamental agent mechanics (movement, energy dynamics, food consumption).
3.  **Achieve an Integrated Proof of Concept (PoC) with Dynamic Loops:**
    *   **Learning Loop:** Demonstrate a basic Deep Reinforcement Learning (DRL) agent (neural network based) successfully training within the simulation, showing an ability to learn from experience (observations, actions, rewards).
    *   **Evolutionary Loop (Basic):** Demonstrate a rudimentary Genetic Algorithm (GA) capable of evolving agent traits or simple parameters, using simulation runs (via Experiment Management) for fitness evaluation.
    *   **Visualization & Control:** Provide a basic UI for visualizing the simulation, observing agent behaviors (including those driven by DRL/GA), and exercising fundamental simulation controls.
    *   **Data Pipeline:** Ensure essential simulation events are being logged to persistent storage (`Parquet`) to support AI training, GA fitness calculation, and future analysis.
    *   **System Cohesion:** Verify that all core services interact as designed to support these dynamic loops.
4.  **Establish Robust Development Practices:**
    *   Integrate comprehensive documentation (design docs, API specs).
    *   Implement and enforce version control best practices.
    *   Establish a foundational testing framework (unit, integration, and basic E2E tests) with an emphasis on a test-driven approach.
5.  **Mitigate Key Technical & Conceptual Risks:**
    *   Prove the viability of the chosen technologies for each layer.
    *   Validate the core architectural design for supporting simulation, learning, and evolution.
    *   Confirm that the basic data flows and control mechanisms are sound.

**What Alpha (this PoC) is NOT:**
*   **Feature-Complete:** While foundational versions of most of the 11 planned systems will be touched, they will not have their full set of advanced features (e.g., the Evolution Engine will be basic, Experiment Management UI might be CLI-only, Statistical Analysis will be via ad-hoc scripts).
*   **Highly Polished:** UI will be functional rather than aesthetically refined. User experience for tools will be basic.
*   **Extensively Optimized:** Performance will be considered in design, but deep optimization is a Beta phase concern. The PoC must be *performant enough* to run the basic DRL/GA loops.
*   **Bug-Free:** While core functionality will be tested, a wider range of bugs is expected compared to Beta or GA releases.

**Versioning during Alpha:**
All versions in this phase will follow the `a0.X.Y.Z` scheme as defined in the `Versioning_Strategy.md` document, where:
*   `a0`: Denotes Alpha Phase.
*   `X`: Major Alpha Feature Set (e.g., "Configuration System UI," "Core Simulation Engine," "Basic DRL Agent").
*   `Y`: Sub-Feature Milestone within `X`.
*   `Z`: Atomic Task / Small Increment within `Y`.
*   A `t` suffix (e.g., `a0.X.Y.Zt`) indicates that the tests for the corresponding item are defined and implemented. The non-`t` version signifies the functional code is complete and passes these tests.
*   All `X`, `Y`, `Z` components are 1-indexed.

---

## Alpha Phase Roadmap - Major Feature Sets (`a0.X`) Overview:

-   **`a0.1.Y.Z`**: Configuration Management System (`Python` UI) - Basic Editor
    *   **Focus**: Create a standalone `Python` app to load, display, edit basic `YAML` config files, and define initial placeholder configs for other services.
    *   **Outcome**: A utility to manage configurations from the start.

-   **`a0.2.Y.Z`**: Communication Layer - Core Message Schemas & Interface Definitions
    *   **Focus**: Define `Protobuf`/`FlatBuffer` message schemas (`GenericEventRequest`, `WorldStateUpdate`, `AgentObservation`, `AgentAction`) and initial `NATS` topic/`gRPC` service structures. Generate code stubs.
    *   **Outcome**: The "language" and "addresses/function signatures" for inter-service communication are established.

-   **`a0.3.Y.Z`**: Orchestration Layer (`Go`) - Basic Worker Connection & Event Ingestion/Routing
    *   **Focus**: Implement a basic `Go` Orchestrator that can spawn/manage one `Rust` Sim Worker, host `gRPC` services (for workers & clients), connect to `NATS`, receive events from the worker, publish them to `NATS`, and forward basic commands to the worker.
    *   **Outcome**: The central communication hub is operational for basic data flow and control.

-   **`a0.4.Y.Z`**: Core Simulation Engine (`Rust`) - Basics
    *   **Focus**: Implement the foundational `Rust` simulation: grid, cell properties, tick loop, basic agent struct/traits, agent lifecycle management, basic food entity/management, core agent mechanics (energy, death, movement, eating), and internal observation/action interfaces.
    *   **Outcome**: A standalone `Rust` simulation kernel that can run a basic eco-sim internally.

-   **`a0.5.Y.Z`**: Simulation Engine (`Rust`) - Basic Orchestrator Integration
    *   **Focus**: Connect the `Rust` Sim Engine (`a0.4`) to the `Go` Orchestrator (`a0.3`). Sim Engine sends events (`WorldState`, `Observations`) to Orchestrator and receives commands/placeholder actions from Orchestrator.
    *   **Outcome**: The simulation world is now connected to the central hub and can be controlled/observed externally.

-   **`a0.6.Y.Z`**: Experiment Management System - Basic CLI/Scripting for Batch Runs
    *   **Focus**: Create a `Python` script/tool to read simple experiment plans (`YAML`/`JSON`) and programmatically instruct the `Go` Orchestrator to run series of simulations with varied configurations.
    *   **Outcome**: Automation for running multiple simulation instances, crucial for AI training and GA.

-   **`a0.7.Y.Z`**: Logging Layer (`Python`) - Integrated Event Capture to `Parquet`
    *   **Focus**: Implement a `Python` service to subscribe to all simulation events from the Orchestrator (via `NATS` JetStream) and reliably log them to `Apache Parquet` files.
    *   **Outcome**: All raw simulation data is persistently stored for future analysis, AI training, and GA fitness calculation.

-   **`a0.8.Y.Z`**: Agent Intelligence Layer (`Python`) - Basic DRL Neural Net & Training Loop
    *   **Focus**: Implement a `Python` AI service with a simple DRL agent (NN using `PyTorch`/`TF`). Service connects to Orchestrator, receives observations/rewards, performs inference and basic training updates, sends actions. Includes model saving/loading.
    *   **Outcome**: Agents are now driven by a learning neural network, completing the core AI interaction loop.

-   **`a0.9.Y.Z`**: Evolution Engine (`Python`) - Basic Genome & Fitness Evaluation Loop (Marked as "If GA in Alpha")
    *   **Focus**: Implement a rudimentary GA: define simple genomes (for agent traits/params), manage a population, use EMS to run evaluations, use logged data for basic fitness calculation, apply simple selection/mutation.
    *   **Outcome**: A PoC of the evolutionary mechanism, allowing agent parameters to change across generations.

-   **`a0.10.Y.Z`**: UI Layer (`Python`/`Pygame`) - Foundational Visualization & Integration
    *   **Focus**: Implement the initial `Python`/`Pygame` UI from scratch. Connects to Orchestrator, renders the world (performant background, dynamic entities), implements basic controls, and displays basic sim/AI/GA progress metrics.
    *   **Outcome**: Visual feedback for the running simulation, including learning/evolving agents.

-   **`a0.11.Y.Z`**: Configuration Management System - V2 Enhancements
    *   **Focus**: Improve the Config Editor UI (`a0.1`) with schema-based validation, better handling of complex/nested structures, and configuration templates based on needs identified from `a0.2`-`a0.10`.
    *   **Outcome**: A more robust and user-friendly tool for managing system configurations.

-   **`a0.12.Y.Z`**: Alpha PoC Finalization, Comprehensive Testing, & Documentation Review
    *   **Focus**: E2E testing of the entire integrated system, final code reviews, performance baselining, documentation completion/review for Alpha scope, critical bug fixing.
    *   **Outcome**: A stable, tagged "Alpha PoC Release" demonstrating the core functionalities and architecture.

This section will detail the sequence of Major Alpha Feature Sets (`a0.X`) and their constituent Sub-Feature Milestones (`a0.X.Y`) and Atomic Tasks (`a0.X.Y.Z`).

- `a0.1.Y.Z`: Configuration Management System (`Python` UI) - Basic Editor
    - `a0.1.1.Z`: Basic UI Framework & `YAML` File I/O
        - `a0.1.1.1t`: Define and implement unit tests for `YAML` file loading functionality (e.g., handling valid `YAML`, empty files, basic error conditions).
        - `a0.1.1.1`: Implement `Python` function to reliably load data from a specified `YAML` file into a `Python` dictionary/list structure (using `PyYAML` or `ruamel.yaml`).
        - `a0.1.1.2t`: Define and implement unit tests for `YAML` file saving functionality (e.g., ensuring correct `YAML` output, handling different data types).
        - `a0.1.1.2`: Implement `Python` function to save a `Python` dictionary/list structure to a specified `YAML` file.
        - `a0.1.1.3t`: Define test cases/manual verification steps for basic UI window creation and "Open File" / "Save File As" / "Save" dialog interactions.
        - `a0.1.1.3`: Set up a basic `Python` GUI window (e.g., using `Tkinter`). Implement "File" menu with "Open," "Save," "Save As" options that use the `YAML` loading/saving functions (`a0.1.1.1`, `a0.1.1.2`). (No display/editing of content yet).
        - `a0.1.1.4t`: (This could be part of defining `a0.1.1t` - an integration test) Define integration tests to ensure the UI file operations correctly call the `YAML` I/O functions and handle typical user flows.
        - `a0.1.1.4`: Implement integration tests for `a0.1.1.1` through `a0.1.1.3` working together. Ensure all unit tests from previous `Zt` tasks pass.
    - `a0.1.2.Z`: Define Initial Basic Configuration Parameters & Structure
        - `a0.1.2.1t`: Define desired structure and key placeholder parameters for a sample `simulation_config.yaml` file (covering basic settings for future Sim, Orch, AI, UI, Log layers).
        - `a0.1.2.1`: Create a sample `default_simulation_config.yaml` file with a hierarchical structure and placeholder values for:
            - UI Layer: `window_width`, `window_height`, `default_fps`.
            - Simulation Layer (template for `Rust` Worker): `world_width`, `world_height`, `initial_food_count`, `default_agent_energy`.
            - Orchestrator Layer: `nats_address`, `grpc_client_port`.
            - Agent Intelligence Layer: `default_ai_mode` (e.g., "random_walk").
            - Logging Layer: `log_output_directory`, `log_level_placeholder`.
            (This task is about defining the content of a useful starting config file that the UI will eventually load and edit).
    - `a0.1.3.Z`: Displaying and Editing Loaded `YAML` Structure in UI
        - `a0.1.3.1t`: Define test cases for displaying a simple, flat `YAML` structure (e.g., top-level key-value pairs) in the UI.
        - `a0.1.3.1`: Implement UI component(s) (e.g., using `Tkinter` labels and entry fields, or a simple list/tree view widget) to display top-level key-value pairs from the loaded `YAML` data. Keys are read-only, values are initially just displayed.
        - `a0.1.3.2t`: Define test cases for making basic scalar values (strings, numbers, booleans) editable in the UI.
        - `a0.1.3.2`: Make the displayed scalar values (strings, numbers, booleans) editable. When a user changes a value in an entry field, update the corresponding value in the in-memory `Python` dictionary.
        - `a0.1.3.3t`: Define test cases for displaying nested `YAML` structures (dictionaries within dictionaries, lists).
        - `a0.1.3.3`: Enhance the UI to recursively display nested structures. This might involve: A tree view widget is ideal here. Or dynamically generating UI sections for each level of nesting.
        - `a0.1.3.4t`: Define test cases for editing values within nested structures.
        - `a0.1.3.4`: Ensure that edits made to values within nested structures correctly update the in-memory `Python` dictionary.
        - `a0.1.3.5t`: Define basic validation tests (e.g., if a field is supposed to be a number, what happens if the user types text?).
        - `a0.1.3.5`: Implement rudimentary client-side validation for edited fields (e.g., attempt to cast to expected type like `int` or `float`; show a simple error message if it fails). (More advanced schema-based validation comes later).
        - `a0.1.3.6t`: Define integration tests for the display and edit functionality working with the "Save" feature from `a0.1.1.Z`.
        - `a0.1.3.6`: Ensure that after editing values in the UI, the "Save" functionality correctly writes the modified in-memory `Python` dictionary back to the `YAML` file. Perform manual verification of saved file content. Implement integration tests.

- `a0.2.Y.Z`: Define Core Event & Data Transfer Payload Schemas
    - `a0.2.1.Z`: Initial `Protobuf` & `FlatBuffer` Schema Definitions
        - `a0.2.1.1t`: Review requirements and finalize field definitions for the `GenericEventRequest` `Protobuf` message (to serve as a general event wrapper).
        - `a0.2.1.1`: Create the `.proto` file for `GenericEventRequest` (including fields like `event_type_key`, `event_payload bytes`, `timestamp_ns`, `worker_id`, `simulation_id`, `payload_format_hint`).
        - `a0.2.1.2t`: Review requirements and finalize field definitions for the `WorldStateUpdate` `FlatBuffer` schema (for efficient transfer of bulk world data, e.g., lists of agent IDs & positions, food IDs & positions).
        - `a0.2.1.2`: Create the `.fbs` file for `WorldStateUpdate`.
        - `a0.2.1.3t`: Review requirements and finalize field definitions for basic `AgentObservation` and `AgentAction` `Protobuf` messages (minimal fields needed for Alpha PoC AI interaction).
        - `a0.2.1.3`: Create a `.proto` file defining the `AgentObservation` and `AgentAction` `Protobuf` messages.
        - `a0.2.1.4t`: Define procedures and expected outcomes for schema code generation across target languages.
        - `a0.2.1.4`: Implement build scripts or manual procedures to generate `Protobuf`/`FlatBuffer` code from all defined `.proto` and `.fbs` files for `Rust`, `Go`, and `Python`. Verify successful code generation without compilation errors in each language.
        - `a0.2.1.5t`: Design round-trip serialization/deserialization tests for each defined message type (`GenericEventRequest`, `WorldStateUpdate`, `AgentObservation`, `AgentAction`) in each target language.
        - `a0.2.1.5`: Implement and pass basic round-trip serialization/deserialization tests in `Rust`, `Go`, and `Python` for all schemas defined in `a0.2.1.1` through `a0.2.1.3` to ensure schema correctness and proper functioning of generated code.
    - `a0.2.2.Z`: Define Initial `NATS` Topic Structures & `gRPC` Service Signatures
        - `a0.2.2.1t`: Draft an initial `NATS` topic hierarchy and naming conventions document covering key Alpha PoC interactions (e.g., world state to UI, observations to AI, actions from AI, events to logger).
        - `a0.2.2.1`: Finalize and document the initial `NATS` topic structure (e.g., in `Communication_Layer.md` and/or `Schema_Registry.md`). Include examples like:
            - `events.simulation.{sim_id}.world_state`
            - `events.simulation.{sim_id}.agent.{agent_id}.observation`
            - `commands.simulation.{sim_id}.agent.{agent_id}.action`
            - `logging.events.raw` (JetStream topic)
        - `a0.2.2.2t`: Draft initial `gRPC` service definitions (method names, request/response message types using schemas from `a0.2.1.Z`) for the `Go` Orchestrator. This should cover:
            - A service for Simulation Workers to connect/register and send events.
            - A service for Clients (UI, Experiment Manager) to send control commands and manage simulations.
        - `a0.2.2.2`: Create the `.proto` files containing these `gRPC` service definitions (e.g., `orchestrator_worker_service.proto`, `orchestrator_client_service.proto`). Ensure request/response types utilize messages defined in `a0.2.1.Z`.
        - `a0.2.2.3t`: Define procedures for generating `gRPC` client and server stub code in target languages.
        - `a0.2.2.3`: Generate `gRPC` server stubs in `Go` (for the Orchestrator) and client stubs in `Rust` (for Sim Worker) and `Python` (for UI/AI/Experiment Manager) from the service definition `.proto` files. Verify successful code generation.
        - `a0.2.2.4t`: Design basic "compilation and callability" tests for the generated `gRPC` stubs in each language (e.g., can a mock client call a mock server method using the generated stubs?).
        - `a0.2.2.4`: Implement and pass simple tests in `Go`, `Rust`, and `Python` to confirm that the generated `gRPC` stubs compile and that basic (mocked) client-server calls can be structured, ensuring the interfaces are usable.

- `a0.3.Y.Z`: `Go` Orchestration Service - Basic Setup & Communication Layer Integration
    - `a0.3.1.Z`: Basic `Go` Service Setup & Configuration
        - `a0.3.1.1t`: Define requirements for `Go` project structure, dependency management (`Go` Modules), and basic application entry point.
        - `a0.3.1.1`: Set up the `Go` project structure (e.g., `cmd/orchestrator/main.go`, `internal/pkg/` directories). Initialize `Go` modules (`go mod init`). Create a basic `main.go` that can compile and run.
        - `a0.3.1.2t`: Define requirements for loading Orchestrator-specific configuration from the `YAML` file (e.g., `NATS` address, `gRPC` listen ports for worker & client interfaces).
        - `a0.3.1.2`: Implement configuration loading in `Go` using a `YAML` parsing library. Service loads `NATS` URL, its `gRPC` server listen addresses.
        - `a0.3.1.3t`: Define requirements for establishing and managing a connection to the `NATS` server.
        - `a0.3.1.3`: Implement `NATS` connection logic using the `Go NATS` client (`nats.go`). Include basic connect, disconnect, and error handling. Log connection status.
        - `a0.3.1.4t`: Unit tests for configuration loading and `NATS` connection helper functions.
        - `a0.3.1.4`: Implement unit tests for `YAML` config loading and `NATS` connection utilities.
    - `a0.3.2.Z`: Implement `gRPC` Server for Worker Interaction
        - `a0.3.2.1t`: Define test cases for the Orchestrator's `gRPC` server implementation of the `OrchestratorWorkerService` (defined in `a0.2.2.2`, e.g., `RegisterWorker`, `ReportEvent` methods).
        - `a0.3.2.1`: Implement the `gRPC` server stubs in `Go` for the `OrchestratorWorkerService`. For now, methods can have placeholder logic (e.g., log "RegisterWorker called", log "ReportEvent called with event type X").
        - `a0.3.2.2t`: Define test cases for starting and stopping the `gRPC` server for worker interactions.
        - `a0.3.2.2`: Integrate `gRPC` server startup (listening on configured port for worker connections) and graceful shutdown into the main application lifecycle.
        - `a0.3.2.3t`: Define basic integration tests using a mock `gRPC` client to call the implemented `RegisterWorker` and `ReportEvent` methods.
        - `a0.3.2.3`: Implement basic integration tests for the worker-facing `gRPC` service.
    - `a0.3.3.Z`: Simulation Worker Lifecycle Management (Minimal - for one worker)
        - `a0.3.3.1t`: Define requirements for the Orchestrator to spawn a single external `Rust` Simulation Worker process based on configured executable path and parameters.
        - `a0.3.3.1`: Implement functionality in `Go` to launch the `Rust` Simulation Worker executable as a child process. Pass necessary configuration (e.g., Orchestrator's `gRPC` address for worker service, simulation ID) to the worker via command-line arguments or environment variables.
        - `a0.3.3.2t`: Define requirements for basic monitoring of the spawned worker process (e.g., detecting if it exits).
        - `a0.3.3.2`: Implement basic monitoring of the child process (e.g., wait for it to exit, log exit code). For Alpha, complex restart logic is not required, just detection and logging of termination.
        - `a0.3.3.3t`: Unit tests for process spawning utilities. Manual test: verify Orchestrator can start a placeholder `Rust` "worker" (even if it just prints "hello" and exits).
        - `a0.3.3.3`: Implement unit tests and perform manual verification of worker spawning.
    - `a0.3.4.Z`: Event Ingestion from Worker & `NATS` Publishing
        - `a0.3.4.1t`: Define test cases for handling incoming `GenericEventRequest` messages via the `ReportEvent` `gRPC` method and publishing them to the correct `NATS` topic.
        - `a0.3.4.1`: Enhance the `ReportEvent` `gRPC` method:
            - Deserialize the incoming `GenericEventRequest`.
            - Determine the target `NATS` topic based on `event_type_key` and other metadata (using topic structure from `a0.2.2.1`).
            - Publish the original `GenericEventRequest` byte payload to the determined `NATS` topic (e.g., `world_updates` go to one topic, `observations` to another, all also go to `logging.events.raw` JetStream topic).
        - `a0.3.4.2t`: Define integration tests: a mock `Rust` worker client sends various `GenericEventRequest` types via `gRPC`; verify Orchestrator publishes them to the expected `NATS` topics using a mock `NATS` subscriber.
        - `a0.3.4.2`: Implement integration tests for the event ingestion and `NATS` publishing pipeline.
    - `a0.3.5.Z`: Implement `gRPC` Server for Client Control Commands (Basic)
        - `a0.3.5.1t`: Define test cases for the Orchestrator's `gRPC` server implementation of the `OrchestratorClientService` (defined in `a0.2.2.2`, e.g., `StartSimulationCommand`, `ControlSimulationCommand` methods like "Pause", "Step").
        - `a0.3.5.1`: Implement the `gRPC` server stubs in `Go` for the `OrchestratorClientService`. For now, methods can have placeholder logic (e.g., log "StartSimulationCommand received").
        - `a0.3.5.2t`: Define test cases for starting and stopping this client-facing `gRPC` server.
        - `a0.3.5.2`: Integrate this second `gRPC` server startup (listening on a different configured port for client connections) and graceful shutdown into the main application lifecycle.
        - `a0.3.5.3t`: Define basic integration tests using a mock `gRPC` client to call the implemented client service methods.
        - `a0.3.5.3`: Implement basic integration tests for the client-facing `gRPC` service.
    - `a0.3.6.Z`: Command Forwarding to Worker (Basic)
        - `a0.3.6.1t`: Define test cases for receiving a command (e.g., "Pause") via the client `gRPC` service and forwarding it to the managed `Rust` Simulation Worker.
        - `a0.3.6.1`: Enhance the client `gRPC` service methods (e.g., `ControlSimulationCommand`):
            - Identify the target worker process (for Alpha, there's only one).
            - Send a corresponding command to the `Rust` worker (this requires the `Rust` worker to also have a `gRPC` service to receive commands, or for the Orchestrator to use a pre-established `NATS` command topic for that worker). Decision: For Alpha simplicity, let's assume the Orchestrator will make a `gRPC` call back to a service endpoint exposed by the `Rust` worker, or send to a worker-specific `NATS` command topic.
        - `a0.3.6.2t`: Define integration test: mock client sends "Pause" command to Orchestrator; verify Orchestrator attempts to send "Pause" to a (mocked) `Rust` worker interface.
        - `a0.3.6.2`: Implement integration test for command forwarding.

- `a0.4.Y.Z`: Core Simulation Engine (`Rust`) - Basics
    - `a0.4.1.Z`: Grid, Boundaries, and Core Cell Properties
        - `a0.4.1.1t`: Define unit tests for `Grid` struct: creation with dimensions (from config), getting dimensions.
        - `a0.4.1.1`: Implement `Grid` struct in `Rust` (stores `width`, `height` from config).
        - `a0.4.1.2t`: Define unit tests for world boundary functions (e.g., `is_within_bounds(x, y)`, functions for future wrapping or clamping coordinates).
        - `a0.4.1.2`: Implement world boundary functions for the `Grid`.
        - `a0.4.1.3t`: Define unit tests for a `Cell` struct. Tests should cover initialization and getting/setting:
            - `depth` (e.g., an `f32`).
            - `cell_type` (e.g., an enum `CellType { OpenWater, SeaFloor }`).
            - `is_occupied` (boolean).
            - `occupant_id` (e.g., `Option<EntityIdPlaceholder>`).
        - `a0.4.1.3`: Implement the `Cell` struct with fields for `depth: f32`, `cell_type: CellType`, `is_occupied: bool`, and `occupant_id: Option<EntityIdPlaceholder>`. The `Grid` struct will now contain a 2D collection (e.g., `Vec<Vec<Cell>>`) of these `Cell`s. Define the `CellType` enum. `EntityIdPlaceholder` can be `u32`.
        - `a0.4.1.4t`: Define unit tests for `Grid` initialization logic, verifying default depth gradient, `cell_type` assignment (e.g., bottom row is `SeaFloor`), and all cells initially unoccupied.
        - `a0.4.1.4`: Implement `Grid` initialization logic:
            - Populate the grid with `Cell` instances.
            - Initialize depth for each cell (e.g., simple linear gradient from top to bottom, values configurable).
            - Initialize `cell_type` for each cell (e.g., based on depth or row index, making bottom-most `SeaFloor`).
            - Initialize all cells with `is_occupied = false` and `occupant_id = None`.
        - `a0.4.1.5t`: Define unit tests for public `Grid` functions to get cell data and modify occupancy.
        - `a0.4.1.5`: Implement public functions on the `Grid` struct:
            - `get_cell_properties(x, y) -> Option<(f32, CellType)>` (or similar, to get depth and type).
            - `is_cell_occupied(x, y) -> Option<bool>`.
            - `get_occupant_id(x, y) -> Option<EntityIdPlaceholder>`.
            - `try_occupy_cell(x, y, id: EntityIdPlaceholder) -> bool` (returns `true` if successful, `false` if already occupied or out of bounds).
            - `vacate_cell(x, y)`.
            These functions must perform boundary checks.
        - `a0.4.1.6t`: Define integration tests for the `Grid` and `Cell` system: create a grid, verify initialization, test occupancy changes, ensure boundary conditions are handled correctly by public methods.
        - `a0.4.1.6`: Implement integration tests for `a0.4.1.1` through `a0.4.1.5`. Ensure all unit tests pass.       
    - `a0.4.2.Z`: Basic Simulation Loop & Tick Management
        - `a0.4.2.1t`: Define unit tests for a `SimulationClock` (or `SimContext`) struct managing `current_tick: u64` and `SimRunStatus { Initializing, Running, Paused, Stopped }`. Tests for advancing ticks (by one), getting current tick, setting/getting status.
        - `a0.4.2.1`: Implement this `SimulationClock` struct in `Rust`.
        - `a0.4.2.2t`: Define requirements and unit tests for a private function `process_single_tick_logic()` that encapsulates all operations within one simulation tick (e.g., ensuring it calls placeholder phase functions).
        - `a0.4.2.2`: Implement a private function `process_single_tick_logic()` within the `SimulationEngine` (or main simulation module). This function will:
            - Increment `current_tick` via `SimulationClock`.
            - Contain placeholder function calls or comments for distinct phases of a tick:
                ```rust
                // Phase 1: Process Incoming Agent Actions (from Orchestrator)
                // Phase 2: Update Agent States & Mechanics (energy, movement, interactions)
                // Phase 3: Update Environment (food spawning/decay)
                // Phase 4: Generate Observations for Agents
                // Phase 5: Publish World State & Events (to Orchestrator)
                ```
            (These phases are stubs/placeholders for now, just logging their execution or doing nothing).
        - `a0.4.2.3t`: Define requirements and unit tests for a public function `advance_simulation_n_ticks(n: u64)` within the `SimulationEngine`. Tests should verify correct tick advancement and status handling.
        - `a0.4.2.3`: Implement a `SimulationEngine` struct (or enhance the main simulation module) that contains the `Grid` (from `a0.4.1`) and the `SimulationClock` (from `a0.4.2.1`). Implement a public method like `advance_simulation_n_ticks(&mut self, num_ticks: u64)` which:
            - Checks `SimRunStatus`.
            - Loops `num_ticks` times, calling `self.process_single_tick_logic()` in each iteration if status allows.
        - `a0.4.2.4t`: Define requirements for the `Rust` simulation worker's `main()` function to initialize the `SimulationEngine` and include a placeholder loop for receiving external control commands (Start, Pause, Step N, Stop).
        - `a0.4.2.4`: Implement the `main()` function for the `Rust` simulation worker. It should:
            - Initialize the `SimulationEngine`.
            - Load initial configuration (placeholder/default values for now).
            - Contain a placeholder control loop that can conceptually react to external commands by changing `SimRunStatus` or calling `advance_simulation_n_ticks()`.
        - `a0.4.2.5t`: Define integration tests for the `SimulationEngine` and `SimulationClock` working together (e.g., verify tick counter increments correctly after N steps, verify status changes affect loop behavior).
        - `a0.4.2.5`: Implement integration tests for `advance_simulation_n_ticks()` and the `SimulationClock`'s interaction with it. Perform manual tests of the `main()` loop with stubbed command inputs if feasible. Ensure all unit tests pass.
    - `a0.4.3.Z`: Basic Agent Struct & Core Traits
        - `a0.4.3.1t`: Define unit tests for the basic `Agent` struct:
            - Test creation with a unique `ID` and initial `position`.
            - Test initialization of `current_energy` (e.g., to `max_energy` or a percentage of it based on a config param).
            - Test initialization of `age_ticks` to `0`.
            - Test default `direction` initialization.
        - `a0.4.3.1`: Implement the basic `Agent` struct in `Rust` (e.g., in `src/simulation/agent.rs`). Include fields for: `id: u32`, `position: (i32, i32)`, `current_energy: f32`, `age_ticks: u32`, `direction: Direction` (enum `North`, `South`, `East`, `West`). Implement a `new_basic(id: u32, initial_pos: (i32, i32), initial_energy: f32, initial_direction: Direction) -> Self` constructor.
        - `a0.4.3.2t`: Define unit tests for incorporating configurable traits into the `Agent` struct and enhancing its constructor. Tests should cover:
            - Correct initialization of `max_energy: f32` from a passed config/parameter.
            - Correct initialization of `vision_range: u32` from a passed config/parameter.
            - Correct initialization of placeholder evolvable traits (e.g., `optimal_depth_preference: f32`, `pressure_adaptation_trait: f32`) with default values passed from config/parameters.
            - Correct initialization of a placeholder `species_tag: String` from a passed config/parameter.
        - `a0.4.3.2`: Extend the `Agent` struct to include fields: `max_energy: f32`, `vision_range: u32`, `optimal_depth_preference: f32`, `pressure_adaptation_trait: f32`, `species_tag: String`. Enhance the constructor (or create a new one like `new_with_config(...)`) to accept these values, typically derived from a configuration structure. Ensure `current_energy` is initialized appropriately relative to `max_energy` (e.g., `current_energy = max_energy * config.initial_energy_percentage`).
        - `a0.4.3.3t`: Define unit tests for all public methods that modify or report an `Agent`'s state. This includes:
            - Tests for `gain_energy()`: e.g., energy increases correctly, doesn't exceed `max_energy`.
            - Tests for `lose_energy()`: e.g., energy decreases correctly, handling of energy dropping to or below zero.
            - Tests for `set_position()`: e.g., position updates correctly.
            - Tests for `set_direction()`: e.g., direction updates correctly.
            - Tests for `increment_age()`: e.g., `age_ticks` increments by one.
            - Tests for all getter methods (e.g., `get_id()`, `get_position()`, `get_current_energy()`, `get_max_energy()`, `get_age_ticks()`, `get_direction()`, `get_vision_range()`, etc.).
        - `a0.4.3.3`: Implement public methods on the `Agent` struct for state modification and access:
            - Accessors (getters) for all traits (e.g., `id() -> u32`, `position() -> (i32, i32)`, `current_energy() -> f32`, etc.).
            - Mutators for dynamic state:
                - `gain_energy(&mut self, amount: f32)` (ensuring it doesn't exceed `max_energy`).
                - `lose_energy(&mut self, amount: f32)` (returns `true` if energy dropped to `0` or below, `false` otherwise).
                - `set_position(&mut self, new_pos: (i32,i32))`.
                - `set_direction(&mut self, new_dir: Direction)`.
                - `increment_age(&mut self)`.
        - `a0.4.3.4t`: Define a comprehensive test suite for `Agent` struct instantiation and state integrity. This suite should:
            - Test creating an `Agent` with a full set of mocked configuration parameters, verifying all traits are initialized as expected.
            - Test sequences of state modifications (e.g., gain energy, lose energy, move, age) and verify the agent's state remains consistent and adheres to defined rules (e.g., energy caps).
        - `a0.4.3.4`: Implement the comprehensive test suite for the `Agent` struct. This involves writing test functions that instantiate `Agent`s with various configurations and call its public methods to ensure robust behavior. Ensure all unit tests defined in `a0.4.3.1t`, `a0.4.3.2t`, and `a0.4.3.3t` pass. This task essentially serves as the integration testing for the `Agent` struct module itself.

    - `a0.4.4.Z`: Agent Lifecycle & Management
        - `a0.4.4.1t`: Define unit tests for an `AgentManager` struct. Tests should cover:
            - Creation of an empty `AgentManager`.
            - A mechanism for generating unique agent `ID`s (e.g., an internal counter, ensuring no collisions if agents are added and removed).
            - Adding a pre-constructed `Agent` (from `a0.4.3.Z`) to the manager's internal tracking system (e.g., a `HashMap`).
            - Successfully retrieving an immutable reference to an `Agent` by its `ID`.
            - Successfully retrieving a mutable reference to an `Agent` by its `ID`.
            - Successfully removing an `Agent` by its `ID` and verifying it's no longer tracked.
            - A way to iterate over all currently managed agents (e.g., to apply updates).
        - `a0.4.4.1`: Implement the basic `AgentManager` struct (e.g., in `src/simulation/agent_manager.rs`). It will likely use a `HashMap<u32, Agent>` (where `u32` is the agent `ID`) to store and manage agents. Implement:
            - `new() -> Self` constructor.
            - A robust method for generating unique agent `ID`s.
            - `add_agent(&mut self, agent: Agent)` method (takes ownership of the agent).
            - `get_agent(&self, agent_id: u32) -> Option<&Agent>`.
            - `get_agent_mut(&mut self, agent_id: u32) -> Option<&mut Agent>`.
            - `remove_agent(&mut self, agent_id: u32) -> Option<Agent>` (returns the removed agent, confirming removal).
            - An iterator method like `iter_agents(&self) -> impl Iterator<Item = &Agent>` and potentially `iter_agents_mut(&mut self) -> impl Iterator<Item = &mut Agent>`.
        - `a0.4.4.2t`: Define unit tests for the `AgentManager`'s `spawn_new_agent` functionality, focusing on interaction with a mocked `Grid` interface. Tests should cover:
            - Successful spawning of an agent at a specified, valid, and (mocked as) empty grid location.
            - The newly spawned agent receiving a unique `ID` from the manager.
            - The agent being initialized with correct traits based on passed configuration parameters (e.g., `AgentInitialConfig` struct).
            - Verification that the mocked `Grid`'s `try_occupy_cell` method (or equivalent) is called with the correct agent `ID`, `position`, and an `EntityType::Agent` marker.
            - Failure to spawn if the target grid cell is (mocked as) already occupied by another agent or is out of bounds (as reported by the mock grid).
        - `a0.4.4.2`: Implement a `spawn_new_agent(&mut self, grid: &mut Grid, initial_pos: (i32, i32), agent_config: AgentInitialConfig) -> Result<u32, AgentSpawnError>` method on `AgentManager`. This method will:
            - Generate a new unique agent `ID`.
            - Attempt to occupy the `initial_pos` on the grid using `grid.try_occupy_cell(initial_pos, new_agent_id, EntityType::Agent)`.
            - If `try_occupy_cell` is successful:
                - Create a new `Agent` instance (using its constructor from `a0.4.3.Z` and parameters from `agent_config`).
                - Call `self.add_agent()` to add the new agent to internal tracking.
                - Return `Ok(new_agent_id)`.
            - If `try_occupy_cell` fails, return an appropriate `AgentSpawnError` (e.g., `CellOccupied`, `OutOfBounds`).
            (`AgentInitialConfig` would be a simple struct passed in, containing values for `max_energy`, `vision_range`, etc., which would ultimately originate from `YAML` config).
        - `a0.4.4.3t`: Define unit tests for the `AgentManager`'s functionality related to handling an agent's death and removal from the simulation, focusing on interaction with a mocked `Grid`. Tests should cover:
            - Correctly removing a specified agent by `ID` from the manager's internal tracking.
            - Verification that the mocked `Grid`'s `vacate_cell` method is called with the deceased agent's last known position.
        - `a0.4.4.3`: Implement a method on `AgentManager` such as `process_agent_death(&mut self, agent_id: u32, grid: &mut Grid)`. This method will:
            - Attempt to retrieve the agent using `get_agent(agent_id)` to find its current position.
            - If the agent exists:
                - Call `grid.vacate_cell(agent_position)`.
                - Call `self.remove_agent(agent_id)`.
                - (Optionally, return `true` if successful, or log the death).
            - If the agent doesn't exist (e.g., already removed), log a warning or handle gracefully.
            (This method will be called by the "Agent Mechanics" system in `a0.4.6.Z` (was `a0.4.5.Z`) when an agent's energy dictates it should die).
        - `a0.4.4.4t`: Define integration tests for `AgentManager` working with a real `Grid` instance (from `a0.4.1.Z`) and `Agent` structs (from `a0.4.3.Z`). Tests should cover scenarios like:
            - Spawning multiple agents and verifying their presence in the manager's collection and correct occupancy status on the grid.
            - Simulating agent death for one of the spawned agents and verifying it's removed from the manager and its cell on the grid is vacated.
            - Attempting to spawn an agent on an already occupied cell and verifying failure.
        - `a0.4.4.4`: Implement integration tests for `AgentManager` interacting with the `Grid` and `Agent` components. This involves:
            - Creating a `Grid` instance.
            - Creating an `AgentManager` instance.
            - Using `agent_manager.spawn_new_agent(...)` to place agents.
            - Verifying `grid.is_cell_occupied(...)` and `grid.get_occupant_id(...)`.
            - Using `agent_manager.process_agent_death(...)` for a specific agent.
            - Verifying the agent is no longer in the manager and the grid cell is free.
            - Ensure all unit tests pass.

    - `a0.4.5.Z`: Food & Basic Environment Interaction
        - `a0.4.5.1t`: Define unit tests for a `FoodPellet` struct:
            - Test creation with a unique `ID`, `position`, and `energy_value`.
            - Test getting its properties.
            - (Optional for Alpha: Test for a basic lifespan/decay counter if we want food to expire).
        - `a0.4.5.1`: Implement the `FoodPellet` struct in `Rust` (e.g., in `src/simulation/food.rs`). It should include:
            - `id: u32` (or `EntityIdPlaceholder`, unique per food pellet).
            - `position: (i32, i32)`.
            - `energy_value: f32` (amount of energy an agent gains by eating it, configurable default).
            - (Optional for Alpha: `remaining_lifespan_ticks: u32` if food expires).
        - `a0.4.5.2t`: Define unit tests for a `FoodManager` struct:
            - Test creation of an empty `FoodManager`.
            - Test unique `ID` generation for new food pellets.
            - Test adding a pre-constructed `FoodPellet` to its tracking.
            - Test retrieving a `FoodPellet` by its `ID` or `position`.
            - Test removing a `FoodPellet` by its `ID`.
            - Test iterating over all managed food pellets.
        - `a0.4.5.2`: Implement the basic `FoodManager` struct (e.g., in `src/simulation/food_manager.rs`). It will likely use a `HashMap<u32, FoodPellet>` to store food by `ID` and potentially another structure (e.g., `HashMap<(i32,i32), u32>`) to quickly find food by position. Implement:
            - `new() -> Self` constructor.
            - Mechanism for generating unique food `ID`s.
            - `add_food_pellet(&mut self, food_pellet: FoodPellet)`.
            - `get_food_pellet(&self, food_id: u32) -> Option<&FoodPellet>`.
            - `get_food_at_pos(&self, position: (i32, i32)) -> Option<&FoodPellet>`.
            - `remove_food_pellet(&mut self, food_id: u32) -> Option<FoodPellet>`.
            - `iter_food_pellets(&self) -> impl Iterator<Item = &FoodPellet>`.
        - `a0.4.5.3t`: Define unit tests for the `FoodManager`'s `spawn_food_pellet` functionality, focusing on interaction with a mocked `Grid`. Tests should cover:
            - Successfully spawning a food pellet at an empty, valid grid location.
            - Food pellet getting a unique `ID` and correct initial properties (from config/params).
            - Mocked `Grid`'s `try_occupy_cell` method being called with correct food `ID` and position.
            - Failure to spawn if target grid cell is (mocked as) occupied or out of bounds.
        - `a0.4.5.3`: Implement a `spawn_food_pellet(&mut self, grid: &mut Grid, position: (i32, i32), energy_value: f32) -> Result<u32, SpawnError>` method on `FoodManager`. This method will:
            - Generate a new unique food `ID`.
            - Attempt to occupy the `position` on the grid using `grid.try_occupy_cell()` (using the food `ID` as the `occupant_id` and marking the cell with an `OccupantType::Food` - *Note: `OccupantType` enum needs to be defined/updated on the `Cell` or `Grid`*).
            - If successful, create a new `FoodPellet` instance.
            - Add the new food pellet to its internal tracking.
            - Return the new food `ID` or an error.
        - `a0.4.5.4t`: Define unit tests for the `FoodManager`'s `consume_food_pellet_at` functionality, interacting with a mocked `Grid`.
        - `a0.4.5.4`: Implement `consume_food_pellet_at(&mut self, position: (i32, i32), grid: &mut Grid) -> Option<f32>` on `FoodManager`. This method will:
            - Find the `FoodPellet` at the given `position` (if any).
            - If found, remove it from internal tracking.
            - Call `grid.vacate_cell(position)`.
            - Return `Some(energy_value)` of the consumed food, or `None` if no food was there.
            (This will be called by "Agent Mechanics" when an agent eats).
        - `a0.4.5.5t`: (Optional for Alpha - Food Spawning Logic) Define tests for a function in `FoodManager` that randomly spawns a certain number of food pellets in valid, unoccupied grid locations.
        - `a0.4.5.5`: (Optional for Alpha) Implement `spawn_random_food(&mut self, grid: &mut Grid, count: u32, default_energy: f32)` in `FoodManager`. This would be called by the `SimulationEngine` each tick or periodically.
            - Find `count` random, unoccupied, passable `OpenWater` cells.
            - Call `self.spawn_food_pellet()` for each.
        - `a0.4.5.6t`: Define integration tests for `FoodManager` working with a real `Grid`. Test spawning food, checking grid occupancy, consuming food, and verifying grid/manager state.
        - `a0.4.5.6`: Implement integration tests for `FoodManager` with `Grid`. Ensure all unit tests pass.

    - `a0.4.6.Z`: Agent Mechanics (Lifecycle, Movement, Eating)
        - `a0.4.6.1t`: Define unit tests for passive energy drain per tick on an `Agent`. Tests should verify `current_energy` decreases by a configured amount.
        - `a0.4.6.1`: Implement a function/method (likely called by `SimulationEngine`'s `process_single_tick_logic()` for each agent via the `AgentManager`) that applies a configurable passive energy drain to an `Agent`'s `current_energy` each tick. (This might be a method on `AgentManager` that iterates its agents).
        - `a0.4.6.2t`: Define unit tests for agent aging. Tests should verify `age_ticks` increments correctly on an `Agent`.
        - `a0.4.6.2`: Implement a function/method (called by `SimulationEngine` for each agent via `AgentManager`) to increment an `Agent`'s `age_ticks` by one each tick.
        - `a0.4.6.3t`: Define unit tests for handling agent death by starvation. Tests should cover:
            - Identifying an agent whose `current_energy` has dropped to `0` or below.
            - Ensuring this agent is correctly processed for removal by the `AgentManager` (using mocked `AgentManager::process_agent_death`).
        - `a0.4.6.3`: Implement logic within the `SimulationEngine`'s tick processing (e.g., after energy drain, iterating through agents via `AgentManager`) to check each agent's `current_energy`. If an agent's energy is `<= 0`:
            - Call `agent_manager.process_agent_death(agent_id, &mut grid)`.
            - (Placeholder: Log "Agent X died of starvation" - actual event publishing later).
        - `a0.4.6.4t`: Define unit tests for the agent "eat" mechanic. Tests should involve a mock `FoodManager` and mock `Agent`. Cover:
            - Agent successfully "eats" food at its current position (food manager reports food consumed, agent gains energy).
            - Agent attempts to eat where there's no food (no energy gain, food manager reports no food).
            - Agent's energy correctly caps at `max_energy` after eating.
        - `a0.4.6.4`: Implement an `attempt_eat(agent_id: u32, agent_manager: &mut AgentManager, food_manager: &mut FoodManager, grid: &mut Grid)` function (or method within `SimulationEngine` or `AgentManager`). This function:
            - Gets the agent's current position using `agent_manager`.
            - Calls `food_manager.consume_food_pellet_at(agent_position, grid)`.
            - If food was consumed (returns `Some(energy_value)`):
                - Gets mutable access to the agent via `agent_manager`.
                - Calls `agent.gain_energy(energy_value)`.
                - Returns `true` (eat successful).
            - Else, returns `false` (no food to eat).
            (This function will be called if an agent's action is `Eat`).
        - `a0.4.6.5t`: Define unit tests for basic agent movement logic. Focus on mechanics of moving given a `Direction`, interacting with a mocked `Grid`, and updating agent state.
        - `a0.4.6.5`: Implement `attempt_agent_move(agent_id: u32, direction: Direction, agent_manager: &mut AgentManager, grid: &mut Grid) -> bool` (or method on `SimulationEngine`/`AgentManager`). This function:
            - Gets the agent and its current position from `agent_manager`.
            - Calculates target (`next_x`, `next_y`).
            - Checks `grid.is_within_bounds(next_x, next_y)`.
            - Checks `grid.get_cell_properties(next_x, next_y)` for `cell_type` passability (e.g., cannot move onto `SeaFloor` if agent is an `OpenWater` type - this implies agent might need a "locomotion_type" trait or similar for advanced passability checks, but for Alpha, assume all agents can only move on `OpenWater`).
            - If target cell is passable and `grid.try_occupy_cell(next_x, next_y, agent_id, EntityType::Agent)` is successful:
                - Call `grid.vacate_cell(current_agent_position)`.
                - Update the agent's position and direction via `agent_manager.get_agent_mut()`.
                - (Placeholder: `agent.lose_energy(move_cost_config)`).
                - Return `true`.
            - Else, return `false`.
            (This function will be called if an agent's action is `Move(direction)`).
        - `a0.4.6.6t`: Define integration tests for all agent mechanics working together. Spawn agents and food, run several ticks, have some agents (via stubbed actions) attempt to move and eat. Verify:
            - Energy drains, ages increment.
            - Agents die from starvation.
            - Agents successfully eat food, gain energy, and food is removed.
            - Agents successfully move to valid, unoccupied locations; grid occupancy updates.
            - Agents fail to move to invalid/occupied locations.
        - `a0.4.6.6`: Implement integration tests for `a0.4.6.1` through `a0.4.6.5`. This involves setting up `SimulationEngine` with `Grid`, `AgentManager`, `FoodManager`. Spawn entities. In the `process_single_tick_logic()` of the simulation engine, iterate agents and:
            - Apply passive energy drain and aging.
            - Check for starvation deaths.
            - For testing movement/eating: If an agent has a (test-defined/stubbed) "action" (e.g., "Move North" or "Eat"), call `attempt_agent_move` or `attempt_eat`.
            - Verify states of agents, food, and grid occupancy. Ensure all unit tests pass.

    - `a0.4.7.Z`: Agent Observation & Action Interface (Internal Simulation Logic)
        - `a0.4.7.1t`: Define requirements and unit tests for an `AgentObservationData` struct. Tests should cover:
            - Correct instantiation with all expected fields.
            - Correct data types for each field (e.g., normalized energy as `f32`, direction as `Option<DirectionEnum>`).
            - Handling of optional fields (e.g., food details being `None` if no food is observed).
        - `a0.4.7.1`: Implement the `AgentObservationData` struct in `Rust` (e.g., in `src/simulation/communication_structs.rs` or similar). For the Alpha PoC, this will include:
            - `agent_id: u32`
            - `current_tick: u64` (the tick at which this observation was generated)
            - `current_energy_normalized: f32` (current_energy / max_energy)
            - `current_depth: f32`
            - `current_age_normalized: f32` (age_ticks / configured_max_lifespan_estimate - need a config for lifespan estimate)
            - `distance_to_nearest_food: Option<f32>`
            - `direction_to_nearest_food: Option<Direction>` (e.g., enum for 8 directions + `Here`)
            - `is_on_seafloor: bool` (derived from agent position and cell type)
            - `can_eat_in_current_cell: bool` (is there food here?)
            (This struct will be serialized to `Protobuf` later when sending to AI).
        - `a0.4.7.2t`: Define requirements and unit tests for an `AgentActionInput` enum. Tests should cover:
            - Correct representation of each defined action variant (e.g., `Move(North)`).
        - `a0.4.7.2`: Implement the `AgentActionInput` enum in `Rust`. For the Alpha PoC, this will include:
            - `Move(Direction)` (where `Direction` is `North`, `South`, `East`, `West`)
            - `Eat`
            - `DoNothing`
            (This enum will be deserialized from a `Protobuf` message received from AI later).
        - `a0.4.7.3t`: Define detailed unit tests for the `generate_observation_for_agent(...)` function. These tests will require mock `Grid`, `AgentManager`, and `FoodManager` setups. Tests should verify:
            - Correct calculation of `current_energy_normalized`, `current_depth`, `current_age_normalized`.
            - Correct detection and reporting of `nearest_food` (distance and direction) within `vision_range`.
            - Correct reporting if no food is in vision range.
            - Correct `is_on_seafloor` status.
            - Correct `can_eat_in_current_cell` status.
            - Handling of edge cases (agent at boundary, etc.).
        - `a0.4.7.3`: Implement the function `generate_observation_for_agent(agent_id: u32, agent_manager: &AgentManager, food_manager: &FoodManager, grid: &Grid, current_tick: u64) -> AgentObservationData` in `Rust`. This function will:
            - Retrieve the specified `Agent` using `agent_manager`.
            - Use the agent's position, `vision_range`, and other relevant traits.
            - Query the `FoodManager` and `Grid` to find the nearest visible food pellet within the agent's `vision_range`. Calculate distance and direction.
            - Check the `Grid` at the agent's current position for `cell_type` (for `is_on_seafloor`) and presence of food (for `can_eat_in_current_cell` via `FoodManager`).
            - Populate and return an `AgentObservationData` struct.
        - `a0.4.7.4t`: Define detailed unit tests for the `apply_action_to_agent(...)` function. These tests will require mock `Grid`, `AgentManager`, and `FoodManager`. Tests should verify:
            - `Move(Direction)` action correctly calls the `attempt_agent_move` mechanic (from `a0.4.6.5`) with the correct parameters.
            - `Eat` action correctly calls the `attempt_eat` mechanic (from `a0.4.6.4`).
            - `DoNothing` action results in no state changes (other than passive tick updates like energy drain/aging handled elsewhere).
            - (Placeholder for reward calculation: Test that a basic reward value, e.g., `0.0`, is returned or can be conceptually associated with the action outcome).
        - `a0.4.7.4`: Implement the function `apply_action_to_agent(agent_id: u32, action: &AgentActionInput, agent_manager: &mut AgentManager, food_manager: &mut FoodManager, grid: &mut Grid) -> f32` in `Rust`. This function (likely called within `SimulationEngine`'s `process_single_tick_logic()`):
            - Takes the `agent_id` and the chosen `AgentActionInput`.
            - Uses a `match` statement on the action type:
                - `AgentActionInput::Move(direction)`: Calls `attempt_agent_move(agent_id, *direction, agent_manager, grid)`.
                - `AgentActionInput::Eat`: Calls `attempt_eat(agent_id, agent_manager, food_manager, grid)`.
                - `AgentActionInput::DoNothing`: No specific action taken.
            - Reward Calculation (Basic Stub for Alpha): Based on the outcome of the action (e.g., successful move, successful eat, failed move, no food to eat), calculate a very basic reward value. For Alpha PoC, this can be simple:
                - Successful eat: `+1.0`
                - Successful move: `-0.01` (small cost)
                - Failed move / `DoNothing` / No food to eat: `0.0` or a small negative.
            - Return the calculated reward. (This reward will eventually be part of an event sent to the AI).
        - `a0.4.7.5t`: Define integration tests for a full "perceive-decide-act" cycle internally within the `Rust` simulation, using stubbed decisions. This involves `generate_observation`, manually creating an `AgentActionInput` based on that observation (simulating AI), and then `apply_action_to_agent`.
        - `a0.4.7.5`: Implement integration tests:
            - Setup a `SimulationEngine` with `Grid`, `AgentManager`, `FoodManager`. Spawn an agent and some food.
            - Call `generate_observation_for_agent`.
            - Based on the returned observation, manually construct an `AgentActionInput` (e.g., if food is observed, create an `Eat` action or a `Move` action towards it).
            - Call `apply_action_to_agent` with this action.
            - Verify the agent's state and world state changed as expected (agent moved, ate, energy changed).
            - Verify a plausible reward value was returned.
            - Ensure all unit tests pass.

- `a0.5.Y.Z`: `Rust` Simulation Worker - Orchestrator Communication & Control

    - `a0.5.1.Z`: Implement `Rust` `gRPC` Client for Orchestrator Communication (Worker Side)
        - `a0.5.1.1t`: Define requirements and unit tests for a `Rust` module/struct responsible for managing the `gRPC` client connection to the `Go` Orchestrator's `OrchestratorWorkerService` (defined in `a0.2.2.2`). Test connection establishment, sending a registration message, and handling connection errors.
        - `a0.5.1.1`: Implement a `Rust` `gRPC` client using `tonic` (and `prost` for generated types from `a0.2.1.Z` and `a0.2.2.Z`). This client should be able to connect to the `Go` Orchestrator's worker-facing `gRPC` service.
        - `a0.5.1.2t`: Define test cases for the `Rust` worker's registration process with the Orchestrator.
        - `a0.5.1.2`: In the `Rust` Simulation Worker's `main()` function (from `a0.4.2.4`), upon startup:
            - Read Orchestrator `gRPC` address from configuration (passed by Orchestrator when it spawns the worker).
            - Establish the `gRPC` connection.
            - Call the `RegisterWorker` (or similar) RPC method on the Orchestrator, sending its `worker_id` (also passed by Orchestrator) and `simulation_id`.
        - `a0.5.1.3t`: Define basic tests for the `gRPC` client's ability to send a `GenericEventRequest` (as a `ReportEvent` RPC call) to a mock Orchestrator `gRPC` server.
        - `a0.5.1.3`: Implement a method in the `Rust` `gRPC` client module to send a `GenericEventRequest` to the Orchestrator's `ReportEvent` RPC endpoint.

    - `a0.5.2.Z`: Publishing Simulation Events to Orchestrator
        - `a0.5.2.1t`: Define unit tests for the logic that takes internal simulation data (e.g., `WorldStateUpdate` struct, `AgentObservationData` struct) and correctly serializes it into the `event_payload` of a `GenericEventRequest` `Protobuf` message.
        - `a0.5.2.1`: Implement `Rust` functions to:
            - Take the internal `WorldStateUpdate` data (from `a0.4.1.Z`), serialize it using `FlatBuffers`, and package it into a `GenericEventRequest` with the correct `event_type_key` (e.g., `"sim.world_state.v1"`) and `payload_format_hint` (`"flatbuffer"`).
            - Take the internal `AgentObservationData` (from `a0.4.7.Z`), serialize it using `Protobuf`, and package it into a `GenericEventRequest` with `event_type_key` (e.g., `"sim.agent_observation.v1"`) and `payload_format_hint` (`"protobuf"`).
            - Do similarly for other key events like `AgentDied` (requires defining this event struct if not done in `a0.4`).
        - `a0.5.2.2t`: Define test cases for integrating event publishing into the `SimulationEngine`'s `process_single_tick_logic` (from `a0.4.2.2`).
        - `a0.5.2.2`: Modify the `SimulationEngine`'s `process_single_tick_logic()`:
            - After generating observations (Phase 4), for each observation, create the `GenericEventRequest` (as per `a0.5.2.1`) and send it to the Orchestrator using the `gRPC` client from `a0.5.1.3`.
            - After updating the world state (end of Phase 5), create the `GenericEventRequest` for `WorldStateUpdate` and send it to the Orchestrator.
            - Send other discrete events (like `AgentDied`) as they occur.
        - `a0.5.2.3t`: Define integration tests: Run the `Rust` Sim Worker connected to a mock `Go` Orchestrator. Verify that the mock orchestrator receives the expected `GenericEventRequest` messages (correct types, correct payloads) at appropriate times during the tick.
        - `a0.5.2.3`: Implement these integration tests.

    - `a0.5.3.Z`: Receiving and Processing Basic Commands from Orchestrator
        - `a0.5.3.1t`: Define how the `Rust` worker will receive commands (e.g., "Step N", "Pause", "Stop", "AgentAction").
            > Decision: For Alpha PoC, let's assume the Orchestrator will send these as `gRPC` messages to a service endpoint exposed by the `Rust` worker itself, OR as messages over a dedicated `NATS` topic the worker subscribes to via the Orchestrator's `NATS`.
            >
            > **Let's choose:** Orchestrator sends commands to worker via a `NATS` topic that the worker subscribes to (e.g., `commands.simulation_worker.{worker_id}`). The Orchestrator tells the worker which topic to listen to during registration.
        - `a0.5.3.1`: Implement `NATS` subscription logic in the `Rust` worker's `main()` loop (or a dedicated thread/task) to listen for incoming command messages (as `GenericEventRequest` with specific `event_type_keys` like `"orchestrator.control.step"`, `"orchestrator.control.pause"`, `"orchestrator.ai.action"`) on its assigned `NATS` command topic.
        - `a0.5.3.2t`: Define unit tests for parsing command messages and updating the `SimulationClock`'s `SimRunStatus` or triggering `advance_simulation_n_ticks`.
        - `a0.5.3.2`: In the `Rust` worker, when a command message is received:
            - Deserialize the `GenericEventRequest` and its `event_payload` (which would be a specific command `Protobuf` message).
            - If command is "Step N Ticks": Call `simulation_engine.advance_simulation_n_ticks(N)`.
            - If command is "Pause": Update `simulation_clock.set_status(SimRunStatus::Paused)`.
            - If command is "Resume/Run": Update `simulation_clock.set_status(SimRunStatus::Running)`. (The main loop in `a0.4.2.4` will then pick this up).
            - If command is `AgentAction`: Store this action to be processed for the relevant agent in the `process_single_tick_logic()` (Phase 1: Process Incoming Agent Actions).
        - `a0.5.3.3t`: Define integration tests: Use a mock `NATS` publisher (simulating the Orchestrator) to send various command messages to the `Rust` worker. Verify the worker's `SimRunStatus` changes correctly and that `advance_simulation_n_ticks` is called for "Step" commands. Verify received `AgentActions` are queued/processed.
        - `a0.5.3.3`: Implement these integration tests.

    - `a0.5.4.Z`: Full Integration Test: `Rust` Sim Worker <-> `Go` Orchestrator
        - `a0.5.4.1t`: Define an end-to-end test scenario involving starting the `Go` Orchestrator (`a0.3` deliverable) and one `Rust` Simulation Worker (`a0.5` deliverable).
        - `a0.5.4.1`: Perform manual or semi-automated E2E test:
            - Start `NATS` server.
            - Start the `Go` Orchestrator.
            - Configure Orchestrator to spawn the `Rust` Simulation Worker.
            - Verify worker registers with Orchestrator (check Orchestrator logs).
            - Use a mock `gRPC` client (or build a very simple CLI tool) to send a "Start Sim" / "Step N Ticks" command to the Orchestrator.
            - Verify Orchestrator forwards command to Worker (check Worker logs, `NATS` messages).
            - Verify Worker sends `WorldStateUpdate` and `AgentObservation` events back to Orchestrator (check Orchestrator logs, `NATS` messages published by Orchestrator).
            - (For this test, the `AgentActions` might just be stubbed/randomly generated by a placeholder in the Orchestrator or even within the `Rust` worker if no AI is connected yet).
    
- `a0.6.Y.Z`: Basic `Python` Experiment Runner
    - `a0.6.1.Z`: Define Simple Experiment Plan Format & Parser
        - `a0.6.1.1t`: Define and document the requirements for a simple `YAML` format for an "experiment plan." It must specify a base configuration file path and a list of runs, where each run can have parameter overrides and an optional `run_id_suffix`.
        - `a0.6.1.1`: Design the `YAML` structure for `experiment_plan.yaml`. Include fields for `experiment_name`, `base_config_path`, and a list of `runs`. Each `run` entry will contain `run_id_suffix` (optional, for naming) and `params_override` (a nested dictionary matching the structure of the base config, for overriding specific values).
        - `a0.6.1.2t`: Define unit tests for a `Python` function that parses an experiment plan `YAML` file. Tests should cover valid plans, plans with overrides, and basic error conditions (e.g., missing base config path).
        - `a0.6.1.2`: Implement a `Python` module/function `parse_experiment_plan(file_path: str) -> ExperimentPlanData` that reads the `YAML`, validates its basic structure, and returns a `Python` object or dictionary representing the parsed plan.
        - `a0.6.1.3t`: Define unit tests for a function that generates a list of fully specified "job definitions" from a parsed experiment plan. Each job definition should contain a unique `simulation_id` and the complete, merged configuration (base + overrides).
        - `a0.6.1.3`: Implement a `Python` function `generate_simulation_jobs(plan: ExperimentPlanData, base_config_data: dict) -> List[SimulationJob]` that takes the parsed plan and loaded base configuration. It iterates through `plan.runs`, applies overrides to a copy of the `base_config_data`, generates a unique `simulation_id` (e.g., `plan.experiment_name + "_" + run.run_id_suffix` or a UUID), and returns a list of `SimulationJob` objects/dicts, each containing its `simulation_id` and its final, complete configuration dictionary.

    - `a0.6.2.Z`: Implement Orchestrator Client Logic for Running Simulations
        - `a0.6.2.1t`: Define unit tests for a `Python` `gRPC` client module that connects to the `Go` Orchestrator's `OrchestratorClientService` (`gRPC` service defined in `a0.2.2.2`, server implemented in `a0.3.5.Z`). Test sending a `StartSimulationCommand` `Protobuf` message.
        - `a0.6.2.1`: Implement a `Python` `gRPC` client module (`orchestrator_client.py`) using `grpcio`. It should have a function `submit_simulation_run(orchestrator_address: str, sim_id: str, config_dict: dict) -> StartSimulationResponse`. This function will:
            - Connect to the Orchestrator's `gRPC` server.
            - Convert the `config_dict` into the appropriate `Protobuf` `StartSimulationCommand` structure (this might require a helper to map dict to proto).
            - Call the Orchestrator's `StartSimulation` RPC method.
            - Return the response.
        - `a0.6.2.2t`: Define basic unit tests for handling success and error responses from the Orchestrator after submitting a job (e.g., acknowledgment of submission, error if orchestrator is down).
        - `a0.6.2.2`: Enhance the `submit_simulation_run` function to handle `gRPC` responses and exceptions gracefully, logging outcomes. For Alpha, complex status tracking of the running sim is not required here, just the submission status.

    - `a0.6.3.Z`: Basic Experiment Execution Script/Engine
        - `a0.6.3.1t`: Define tests for a main command-line script (`run_experiment.py`) that takes an experiment plan file path as an argument, parses it, and iterates through the defined runs, calling the Orchestrator client for each.
        - `a0.6.3.1`: Create the main `Python` script `run_experiment.py`:
            - Uses `argparse` to accept the experiment plan file path.
            - Loads the base configuration file specified in the plan.
            - Calls `parse_experiment_plan()` and `generate_simulation_jobs()` (from `a0.6.1.Z`).
            - For each `SimulationJob` in the generated list:
                - Calls `orchestrator_client.submit_simulation_run()` to submit the job to the `Go` Orchestrator.
                - Logs the submitted `simulation_id` and its key parameters to a simple manifest file (e.g., `experiment_name_manifest.csv` or `.jsonl`) and/or to console output. This manifest links `simulation_id` to the specific parameters of that run.
            - (For Alpha, the script can submit jobs sequentially. Basic parallelism, e.g., submitting a small batch and waiting, can be a minor stretch goal for this task if time permits).
        - `a0.6.3.2t`: Define a manual end-to-end test procedure: create a simple experiment plan `YAML` with 2-3 runs having slightly different parameters.
        - `a0.6.3.2`: Perform manual E2E testing:
            - Ensure a `NATS` server and the `Go` Orchestrator (from `a0.3`) are running.
            - Run `python run_experiment.py --plan path/to/simple_experiment.yaml`.
            - Verify (via Orchestrator logs, or by observing `NATS` messages if the Orchestrator is publishing "sim started" events) that the Orchestrator received requests to start simulations with the correct, varied configurations and unique `simulation_id`s.
            - Check the generated manifest file for correctness.

- `a0.7.Y.Z`: `Python` Logging Service - Event Persistence
    - `a0.7.1.Z`: Basic Logging Service Setup & `NATS` JetStream Subscription
        - `a0.7.1.1t`: Define requirements for the `Python` Logging service project structure, dependencies (`nats-py`, `pyarrow`, `pandas`, `protobuf`, `pyyaml`), and basic application entry point.
        - `a0.7.1.1`: Set up the `Python` project for the Logging service. Create a `main.py` entry point. Implement basic configuration loading (`NATS` address, JetStream topic name, `Parquet` output directory) from its `YAML` config file (defined in `a0.1`).
        - `a0.7.1.2t`: Define unit tests for connecting to `NATS` JetStream and creating a durable subscription to the designated logging topic (e.g., `logging.events.raw`). Test message acknowledgment.
        - `a0.7.1.2`: Implement `NATS` JetStream connection logic using `nats-py`. Create a durable, pull-based subscription to the configured logging topic. Implement a loop to fetch messages in batches from the subscription.
        - `a0.7.1.3t`: Unit tests for deserializing the outer `GenericEventRequest` `Protobuf` message from received `NATS` message data.
        - `a0.7.1.3`: In the message processing loop, deserialize the `NATS` message payload into a `GenericEventRequest` `Protobuf` object. Extract key fields like `timestamp_ns`, `event_type_key`, `simulation_id`, `worker_id`, and the raw `event_payload` bytes.

    - `a0.7.2.Z`: Event Processing and `Parquet` File Writing
        - `a0.7.2.1t`: Define requirements for batching incoming `GenericEventRequest` data before writing to `Parquet` (e.g., batch by message count or time window).
        - `a0.7.2.1`: Implement an in-memory batching mechanism. Collect the extracted data from `GenericEventRequest` messages (timestamp, type, sim_id, payload bytes, etc.) into a list or buffer.
        - `a0.7.2.2t`: Define unit tests for converting a batch of processed event data into a `Pandas DataFrame` (or equivalent structure for `pyarrow`) and writing it to a `Parquet` file. Test schema consistency.
        - `a0.7.2.2`: Implement the `Parquet` writing logic using `pyarrow` (potentially via `Pandas`):
            - When a batch is full (or a time limit is reached), convert the list of collected event data into a `Pandas DataFrame`. Columns should include `timestamp_ns`, `event_type_key`, `simulation_id`, `worker_id`, `payload_format_hint`, and `event_payload` (as binary).
            - Write this `DataFrame` to a new `Parquet` file.
        - `a0.7.2.3t`: Define tests for handling `NATS` message acknowledgments after successful `Parquet` batch write.
        - `a0.7.2.3`: After a batch is successfully written to `Parquet`, acknowledge all corresponding `NATS` messages to remove them from the JetStream. Implement error handling for write failures (e.g., retry, log error, dead-letter queue for `NATS` messages if persistently failing).

    - `a0.7.3.Z`: Log File Organization & Management
        - `a0.7.3.1t`: Define a standardized directory structure and naming convention for output `Parquet` files (e.g., incorporating `simulation_id` and date/time components to ensure organization and prevent filename collisions).
        - `a0.7.3.1`: Implement logic to create directories and generate unique `Parquet` filenames based on the defined convention (e.g., `/output_dir/{simulation_id}/{YYYY-MM-DD}/{timestamp_batch_start}.parquet`). Ensure `simulation_id` is used to group logs from the same run.

    - `a0.7.4.Z`: Integration Testing and Basic Validation
        - `a0.7.4.1t`: Define an integration test plan: `Go` Orchestrator publishes mock `GenericEventRequest` messages (with varying `event_type_key` and payloads) to the `NATS` JetStream logging topic. The `Python` Logging service subscribes and writes to `Parquet`.
        - `a0.7.4.1`: Implement this integration test. Requires a running `NATS` server (and JetStream enabled).
            - Use a separate `Python`/`Go` script to publish a set of diverse test messages to the JetStream logging topic.
            - Run the `Python` Logging service.
            - Verify that `Parquet` files are created in the correct location with the expected naming convention.
        - `a0.7.4.2t`: Define procedure for validating the content of generated `Parquet` files (e.g., reading a sample `Parquet` file with `Pandas`/`PyArrow` and checking if data matches published test messages).
        - `a0.7.4.2`: Implement a simple validation script (or perform manual validation using `Python` with `Pandas`/`PyArrow`) to read one or more generated `Parquet` files and check:
            - Correct number of records.
            - Presence and correctness of key columns (`timestamp_ns`, `event_type_key`, `simulation_id`, `event_payload`).
            - Data types of columns.

- `a0.8.Y.Z`: Agent Intelligence Layer (`Python`) - Basic DRL Neural Net & Training Loop

    - `a0.8.1.Z`: DRL Framework Setup & Basic Neural Network Definition
        - `a0.8.1.1t`: Define requirements for the `Python` environment for the AI Layer: specific `Python` version, choice of `PyTorch` or `TensorFlow/Keras`, and `NumPy` version.
        - `a0.8.1.1`: Set up the `Python` project directory for the Agent Intelligence Layer. Initialize a virtual environment. Install chosen DL framework (e.g., `PyTorch`) and `NumPy`. Add to `requirements.txt`.
        - `a0.8.1.2t`: Define the input (observation) vector structure and output (action) space structure for the initial neural network, based on `AgentObservationData` (from `a0.4.7.1`) and `AgentActionInput` (from `a0.4.7.2`). Specify normalization for inputs if any.
        - `a0.8.1.2`: Design and implement a very simple Neural Network architecture (e.g., using `torch.nn.Module` or `tf.keras.Model`) suitable for the defined observation and action spaces. For Alpha, this might be a few fully connected layers (e.g., `Input -> Linear(64) -> ReLU -> Linear(32) -> ReLU -> Linear(num_actions)`).
        - `a0.8.1.3t`: Define unit tests for the NN model:
            - Test correct instantiation of the model.
            - Test the forward pass with a dummy input tensor (matching observation spec), verifying the output tensor shape matches the action space spec.
        - `a0.8.1.3`: Implement the unit tests for the NN model.

    - `a0.8.2.Z`: Communication Integration (Receiving Obs/Rewards, Sending Actions via `NATS`)
        - `a0.8.2.1t`: Define unit tests for `NATS` connection, subscription to observation/reward topics, and deserialization of `GenericEventRequest` (`Protobuf`) containing `AgentObservation` / `AgentReward` (`Protobuf`) into `Python` objects, then into `NumPy` arrays/`PyTorch` Tensors.
        - `a0.8.2.1`: Implement `Python` `NATS` client logic (`nats-py`) within the AI service:
            - Connect to `NATS` server (address from config).
            - Subscribe to relevant `NATS` topics (e.g., `events.simulation.{sim_id}.agent.*.observation`, `events.simulation.{sim_id}.agent.*.reward`) where the Orchestrator publishes these.
            - Implement callback functions to handle incoming messages, deserialize the `GenericEventRequest` and its `AgentObservation` or `AgentReward` payload, and convert observation data into the format expected by the NN (e.g., `NumPy` array or `PyTorch` Tensor).
        - `a0.8.2.2t`: Define unit tests for taking a conceptual action (e.g., an integer index or a vector from NN output), converting it to an `AgentAction` `Protobuf` message, wrapping it in `GenericEventRequest`, serializing, and preparing for `NATS` publishing.
        - `a0.8.2.2`: Implement logic to:
            - Convert the NN's output tensor into a chosen `AgentActionInput` (e.g., if NN outputs probabilities, sample or take `argmax`; if NN outputs continuous values, map them).
            - Create an `AgentAction` `Protobuf` message.
            - Package it into a `GenericEventRequest` (with appropriate `event_type_key` like `"ai.agent_action.v1"`).
            - Publish this `GenericEventRequest` to the `NATS` topic the Orchestrator expects for actions (e.g., `commands.simulation.{sim_id}.agent.{agent_id}.action`).

    - `a0.8.3.Z`: Implement Basic DRL Algorithm & Inference Path
        - `a0.8.3.1t`: Choose a very simple DRL algorithm suitable for Alpha PoC (e.g., `REINFORCE` if action space is discrete, or a simplified `Q-learning` variant like basic `DQN` if experience replay is desired early). Define test cases for its core mathematical components (e.g., discounted reward calculation for `REINFORCE`, Q-value update rule for `DQN`).
        - `a0.8.3.1`: Implement the chosen DRL algorithm's core components:
            - Policy Representation: The NN from `a0.8.1.2` acts as the policy (or Q-function).
            - Action Selection (Inference + Exploration): Function that takes an observation tensor, passes it through the NN, and selects an action. Include a basic exploration strategy (e.g., epsilon-greedy for `DQN`, or sampling from output probabilities for policy gradients).
            - Loss Function: Implement the loss function specific to the algorithm.
        - `a0.8.3.2t`: Define unit tests for the action selection process, ensuring it correctly uses the NN output and applies exploration.
        - `a0.8.3.2`: Implement and test the action selection/inference path thoroughly.

    - `a0.8.4.Z`: Implement Training Loop & Model Persistence
        - `a0.8.4.1t`: Define requirements and tests for an experience collection mechanism (e.g., a list to store `(obs, action, reward, next_obs, done)` tuples for an episode if `REINFORCE`, or an Experience Replay Buffer class if `DQN`).
        - `a0.8.4.1`: Implement the chosen experience collection mechanism.
        - `a0.8.4.2t`: Define tests for the main training update step: sampling experiences (if applicable), computing loss, performing backpropagation, and updating NN weights using an optimizer.
        - `a0.8.4.2`: Implement the training update step:
            - Initialize an optimizer (e.g., `torch.optim.Adam`).
            - Function to take a batch of experiences, compute the loss, call `loss.backward()`, and `optimizer.step()`.
        - `a0.8.4.3t`: Define tests for saving the NN model's state (weights) and loading it back, ensuring consistency.
        - `a0.8.4.3`: Implement functions `save_model(model, path)` and `load_model(model, path)` using `PyTorch`'s `state_dict()` or `TensorFlow`'s model saving utilities.
        - `a0.8.4.4t`: Define the structure of the main training loop that orchestrates interaction, experience collection, and training updates.
        - `a0.8.4.4`: Implement the main `Python` script/class for the AI service that ties everything together:
            - Initializes NN, experience buffer, `NATS` client.
            - Enters a loop to:
                - Receive observations/rewards from `NATS` (for one or more agents/episodes, potentially driven by EMS `a0.6`).
                - Select actions using NN and publish them.
                - Store experiences.
                - Periodically perform training updates.
                - Periodically save the model.

    - `a0.8.5.Z`: Initial End-to-End Learning Test
        - `a0.8.5.1t`: Define a very simple, solvable task within the Fish Eco Sim environment (e.g., "agent must learn to move to a fixed food pellet at (x,y)" or "agent must survive for X ticks by eating"). Define expected learning outcome (e.g., reward consistently increases).
        - `a0.8.5.1`: Configure the simulation (via `a0.1` config files) and the Experiment Management System (`a0.6`) to run this simple learning task for a number of episodes/training steps.
        - `a0.8.5.2t`: Prepare for E2E test execution: ensure `NATS`, Orchestrator (`a0.3`), Sim Worker (`a0.5`), Logger (`a0.7`), and AI service (`a0.8`) can all be started.
        - `a0.8.5.2`: Execute the E2E learning test:
            - Start all services.
            - Use EMS to launch the defined simple learning task.
            - Monitor (via logs from AI service and potentially Logger) if average rewards per episode are showing an upward trend, or if the agent starts to exhibit the target behavior.
            - Save the trained model from the AI service.
            - Reload the model and run the agent in inference-only mode to see if the learned behavior is stable.
            - (Perfect learning is not expected in Alpha, but some indication that the training loop is functional and weights are updating based on rewards is the goal).

- `a0.9.Y.Z`: Evolution Engine (`Python`) - Basic Genome & Fitness Evaluation Loop

    - `a0.9.1.Z`: Define Basic Genome Structure & Agent Configuration Mapping
        - `a0.9.1.1t`: Define requirements for a simple genome structure. For Alpha, this could encode a few key numeric agent traits (e.g., `max_energy_gene`, `vision_range_gene`, `speed_gene_placeholder`).
        - `a0.9.1.1`: Implement a `Python` class or data structure for the `Genome` (e.g., a list or `NumPy` array of floats/integers).
        - `a0.9.1.2t`: Define unit tests for a function that translates a `Genome` into an `AgentInitialConfig` dictionary/object (the structure that the EMS `a0.6` uses to configure an agent for a simulation run, which then gets passed to the `Rust` Sim `a0.4` and `Python` AI `a0.8`).
        - `a0.9.1.2`: Implement a `Python` function `genome_to_agent_config(genome: Genome) -> AgentInitialConfig`. This function maps gene values to actual trait values (e.g., applying scaling, constraints). For traits affecting the DRL agent (if evolving NN HPs), it would populate those fields in the config.

    - `a0.9.2.Z`: Population Management & Fitness Evaluation Orchestration
        - `a0.9.2.1t`: Define unit tests for initializing a population of random (or simple template-based) genomes.
        - `a0.9.2.1`: Implement a `Python` function to `initialize_population(population_size: int, genome_length: int) -> List[Genome]`.
        - `a0.9.2.2t`: Define requirements for the fitness evaluation process: how a genome is evaluated using the Experiment Management System (`a0.6`) and how results are retrieved (e.g., by looking up logged data for the `simulation_id`s run for that genome).
        - `a0.9.2.2`: Implement a `Python` function `evaluate_genome_fitness(genome: Genome, ems_client: EMSClient, analysis_client: AnalysisClientPlaceholder) -> float`. This function will:
            - Translate `genome` to `AgentInitialConfig` using `a0.9.1.2`.
            - Create a simple "experiment plan" for this single genome (e.g., 1-3 simulation replicates).
            - Use the EMS (`a0.6`'s `run_experiment.py` or its library functions) to execute these simulation runs, getting back the `simulation_id`(s).
            - After runs complete, use a placeholder `AnalysisClientPlaceholder` to query/calculate fitness based on the logged data for those `simulation_id`(s (data from `a0.7`). For Alpha, this "analysis client" might be a simple script that reads specific `Parquet` files and calculates average agent lifespan or energy.
        - `a0.9.2.3t`: Unit tests for managing a list of genomes and their associated fitness scores.
        - `a0.9.2.3`: Implement logic in the Evolution Engine to iterate through a population, call `evaluate_genome_fitness` for each, and store the results.

    - `a0.9.3.Z`: Implement Basic Evolutionary Operators
        - `a0.9.3.1t`: Define unit tests for a simple selection mechanism (e.g., tournament selection or selecting the top N individuals).
        - `a0.9.3.1`: Implement a basic `select_parents(population: List[Tuple[Genome, float]], num_parents: int) -> List[Genome]` function.
        - `a0.9.3.2t`: Define unit tests for a simple mutation operator (e.g., for a genome of numbers, add small Gaussian noise to a few genes).
        - `a0.9.3.2`: Implement a basic `mutate_genome(genome: Genome, mutation_rate: float, mutation_strength: float) -> Genome` function.
        - `a0.9.3.3t`: (Optional for basic Alpha GA) Define tests for a simple crossover operator. Crossover can be skipped for the very first GA PoC if mutation alone is used for variation.
        - `a0.9.3.3`: (Optional for basic Alpha GA) Implement a basic `crossover_genomes(parent1: Genome, parent2: Genome) -> Tuple[Genome, Genome]` function.

    - `a0.9.4.Z`: Basic Generational Loop & Integration Test
        - `a0.9.4.1t`: Define requirements for a simple generational loop: initialize pop, evaluate, select, mutate (and crossover if implemented), create new pop, repeat.
        - `a0.9.4.1`: Implement the main loop for the Evolution Engine that runs for a fixed number of generations:
            - Initialize population.
            - For each generation:
                - Evaluate fitness of all individuals in the current population.
                - Select parents.
                - Create new offspring population using mutation (and crossover).
                - Replace old population with new.
                - Log best fitness/average fitness for the generation.
        - `a0.9.4.2t`: Define an E2E test plan for a very simple evolutionary run: e.g., evolve genomes for agents that maximize lifespan in a very basic simulation setting.
        - `a0.9.4.2`: Conduct an integration test:
            - Run all necessary services (`NATS`, Orch, Sim, Logger, AI (even if its NN is fixed for now, its HPs or agent traits could be evolved)).
            - Run the Evolution Engine for a small number of generations with a small population.
            - Verify that it calls the EMS to run simulations.
            - Verify that fitness scores are being assigned (by inspecting logs or simple analysis of `Parquet`).
            - Observe if there's any trend (even slight) in average fitness over generations. (Perfect convergence not expected, just functional loop).

- `a0.10.Y.Z`: `Python` UI Layer (`Pygame`) - Visualization & Basic Control
    - `a0.10.1.Z`: Basic `Pygame` Window, `NATS` Connection, & Performant World Rendering
        - `a0.10.1.1t`: Define requirements for `Python` UI project setup, basic window parameters (from config `a0.1`), and target frame rate (e.g., 30 FPS) for basic world rendering.
        - `a0.10.1.1`: Set up `Python` project for UI Layer (`Pygame`, `NATS` client, `Protobuf`/`FlatBuffer` libs). Implement basic `Pygame` window, main event loop, and a simple FPS counter/display. Load window settings.
        - `a0.10.1.2t`: Unit tests for `NATS` client module (connection, subscription to `WorldStateUpdate`, deserialization of `GenericEventRequest` and `WorldStateUpdate` `FlatBuffer`).
        - `a0.10.1.2`: Implement `NATS` client logic for `WorldStateUpdate` reception and deserialization. Store latest `WorldStateUpdate` data.
        - `a0.10.1.3t`: Define requirements for rendering static grid lines onto a background surface.
        - `a0.10.1.3`: Implement `draw_grid_lines(surface, world_state_data, camera_offset)` helper function.
        - `a0.10.1.4t`: Define requirements and test cases (including a performance metric) for `render_static_world_background(world_state_data) -> pygame.Surface`. This function should render cell depth (color gradient) and `cell_type` (distinct visual cues) onto a single surface.
        - `a0.10.1.4`: Implement `render_static_world_background` to create a pre-rendered surface of the static grid elements (lines, cell depth colors, cell type visuals) based on data from `WorldStateUpdate` (which must contain per-cell depth/type info).
        - `a0.10.1.5t`: Define test cases (manual visual verification, automated performance baseline) for `render_static_world_background`.
        - `a0.10.1.5`: Implement tests for `render_static_world_background`. Perform manual visual verification. Run performance test and record baseline rendering time for the static background.
        - `a0.10.1.6t`: Define integration test plan: UI receives `WorldStateUpdate`, generates/updates the static background surface, and blits it to the screen.
        - `a0.10.1.6`: Integrate: On first `WorldStateUpdate` (or if `static_grid_changed` flag is set in the message), call `render_static_world_background` and store the surface. In the main UI drawing loop, blit this pre-rendered background surface. Conduct manual verification. Monitor FPS.

    - `a0.10.2.Z`: Rendering Dynamic Entities (Food & Agents) on Pre-rendered Background
        - `a0.10.2.1t`: Define tests/manual verification for rendering `FoodPellet` entities (from `WorldStateUpdate`) on top of the static background.
        - `a0.10.2.1`: Enhance rendering logic to iterate through food pellet data in `WorldStateUpdate` and draw them (e.g., small circles) onto the main display surface after the static background is blitted.
        - `a0.10.2.2t`: Define tests/manual verification for rendering `Agent` entities (from `WorldStateUpdate`) on top of the static background. Include position, and simple visual cues for `species_tag` or `direction`.
        - `a0.10.2.2`: Enhance rendering logic to iterate through agent data in `WorldStateUpdate` and draw them (e.g., circles with an arrow for `direction`) onto the main display surface. Allow for simple visual differentiation based on `species_tag`.
        - `a0.10.2.3t`: Manual verification: UI correctly displays moving agents and food pellets overlaid on the static world background, based on `WorldStateUpdate` messages from a backend with AI (`a0.8`) / GA (`a0.9`) driven agents.
        - `a0.10.2.3`: Integrate and test dynamic entity rendering. Main draw loop: clear screen -> blit static background -> draw food -> draw agents -> update display. Monitor FPS.

    - `a0.10.3.Z`: Basic UI Controls & Information Display
        - `a0.10.3.1t`: Define requirements for UI buttons (Start, Pause/Resume, Step N Ticks, Add Agent [placeholder]) and their interaction with the Orchestrator via `gRPC`.
        - `a0.10.3.1`: Implement `Pygame` UI elements (e.g., using `Pygame GUI`) for "Start Sim," "Pause/Resume Sim," "Step N Ticks" buttons. (Add Agent button can be a stub for now).
        - `a0.10.3.2t`: Unit tests for the `Python` `gRPC` client module that sends control commands to the `Go` Orchestrator.
        - `a0.10.3.2`: Implement `Python` `gRPC` client logic in the UI to send corresponding control commands to the `Go` Orchestrator when UI buttons are pressed.
        - `a0.10.3.3t`: Define requirements for displaying basic simulation stats (e.g., current tick from `WorldStateUpdate` or a separate stats event) and selected agent info (ID, energy, position - if this data is available via `NATS` events).
        - `a0.10.3.3`: Implement UI elements to display:
            - Current tick count.
            - Agent selection by clicking on the grid (map screen coordinates to grid coordinates, then find nearest agent from `WorldStateUpdate` data).
            - Display ID, position, energy of the selected agent (requires Orchestrator to publish `AgentDetails` on request or these details to be part of `WorldStateUpdate` agent data).

    - `a0.10.4.Z`: Displaying Basic AI/GA Progress Metrics (Integration)
        - `a0.10.4.1t`: Define requirements for the UI to subscribe to and display metrics from `NATS` topics like `metrics.ai.training_summary` and `metrics.ga.generation_summary` (which AI `a0.8` and GA `a0.9` should publish via Orchestrator).
        - `a0.10.4.1`: Implement `NATS` subscription in UI for these metric topics. Add simple text display elements in the UI to show these incoming metrics (e.g., "Current Episode:", "Avg. Reward:", "GA Generation:", "Best Fitness:").
        - `a0.10.4.2t`: Define E2E test plan involving all key Alpha components: Config, Sim, Orch, AI (training), GA (running), Logger, and this UI.
        - `a0.10.4.2`: Conduct comprehensive E2E manual testing of the UI with all preceding Alpha components active. Verify:
            - Correct display of the world and dynamic agents.
            - Agent movements reflect learning/evolution.
            - UI controls correctly affect the simulation via the Orchestrator.
            - Basic AI/GA metrics update in the UI.
            - Overall UI stability and acceptable FPS.

- `a0.11.Y.Z`: Configuration Editor V2 - Schema Validation & Enhanced Usability
    - `a0.11.1.Z`: Implement Schema-Based Validation
        - `a0.11.1.1t`: Define requirements for a formal configuration schema (e.g., using `JSON Schema` format, or deriving from `Pydantic` models if the UI uses `Pydantic` internally). This schema should cover all key parameters for Sim, Orch, AI, UI, Logger, GA, EMS with their types, constraints (min/max, enums), and descriptions.
        - `a0.11.1.1`: Create (or auto-generate if using `Pydantic`) the master `JSON Schema` file(s) defining the structure and validation rules for `simulation_config.yaml` (and potentially separate schemas for experiment plans or GA settings if they are complex).
        - `a0.11.1.2t`: Unit tests for a `Python` validation module that can validate a loaded `YAML` configuration (`Python` dict/list) against the defined schema.
        - `a0.11.1.2`: Implement a `Python` validation module using a library like `jsonschema` (if using `JSON Schema`) or by leveraging `Pydantic`'s built-in validation. This module will take a loaded configuration and the schema, and report any validation errors.
        - `a0.11.1.3t`: Define UI requirements for displaying schema validation errors to the user in a clear and helpful way (e.g., highlighting invalid fields, showing error messages).
        - `a0.11.1.3`: Integrate schema validation into the Config Editor UI:
            - Validate the loaded configuration when a file is opened.
            - Validate individual fields as they are edited, or validate the entire configuration before saving.
            - Display validation errors to the user, preventing saving of invalid configurations (or allowing save with a warning).

    - `a0.11.2.Z`: Enhanced UI for Complex Data Structures & Usability
        - `a0.11.2.1t`: Review the usability of the existing UI (from `a0.1.3`) for handling deeply nested `YAML` structures, lists, and dictionaries. Identify areas for improvement.
        - `a0.11.2.1`: Refactor or enhance UI components for displaying and editing nested configurations. If not already using one, consider implementing or integrating a proper tree view widget that can expand/collapse sections and clearly show hierarchy.
        - `a0.11.2.2t`: Define requirements for UI elements to edit lists (add/remove/reorder items) and dictionaries (add/remove key-value pairs) within the configuration.
        - `a0.11.2.2`: Implement UI functionality to manage list items (e.g., buttons to add/delete elements in a list of agent spawn configurations) and dictionary entries (e.g., adding new custom parameters if the schema allows `additionalProperties`).
        - `a0.11.2.3t`: Define requirements for improved user feedback, such as clear indication of unsaved changes, better error dialogs, and tooltips/descriptions for parameters (pulled from the schema).
        - `a0.11.2.3`: Implement enhanced user feedback mechanisms in the UI. Parameter descriptions could be loaded from the schema and displayed as tooltips or in a help panel.

    - `a0.11.3.Z`: Configuration Templates & Default Management
        - `a0.11.3.1t`: Define requirements for creating new configuration files from predefined templates (e.g., "Default Fish Sim Config," "Basic DRL Training Config," "Simple GA Config").
        - `a0.11.3.1`: Implement a "New From Template" feature in the Config Editor UI. Store template `YAML` files within the application or a designated directory.
        - `a0.11.3.2t`: Define requirements for a "Reset to Default" functionality for individual parameters or entire sections, based on default values specified in the configuration schema.
        - `a0.11.3.2`: Implement "Reset to Default" capabilities in the UI, referencing default values from the loaded schema.

    - `a0.11.4.Z`: Refined Testing & Documentation for Config Editor V2
        - `a0.11.4.1t`: Update and expand unit tests for all new and modified Config Editor functionalities (schema validation, complex structure editing, template usage).
        - `a0.11.4.1`: Implement the updated unit tests.
        - `a0.11.4.2t`: Update integration tests for the Config Editor, ensuring all parts work together correctly with complex configurations.
        - `a0.11.4.2`: Implement updated integration tests.
        - `a0.11.4.3t`: Update user documentation/guide for the Config Editor to reflect V2 features.
        - `a0.11.4.3`: Update the Config Editor's user documentation.

- `a0.12.Y.Z`: Alpha PoC Finalization, Comprehensive Testing, & Documentation Review

    - `a0.12.1.Z`: Comprehensive End-to-End (E2E) System Testing
        - `a0.12.1.1t`: Define a suite of E2E test scenarios that cover the main Alpha PoC functionalities. These scenarios should involve all major integrated layers (Config, Sim, Orch, Logging, AI, GA (if included), UI).
            - Example Scenario 1: "Basic Simulation Run & Visualization": Configure a simple sim, run it via Orch, observe basic agent behavior in UI, verify logs are created.
            - Example Scenario 2: "DRL Agent Learning (Simple Task)": Configure & run a simple DRL training task (using EMS), observe if learning metrics show any positive trend, visualize agent behavior in UI, check logs.
            - Example Scenario 3 (If GA included): "GA Run (Simple Fitness)": Configure & run a short GA, observe if fitness metrics show any trend, visualize evolved agent behavior, check logs.
        - `a0.12.1.1`: Prepare necessary configuration files (using Config Editor `a0.11`), experiment plans (using EMS `a0.6`), and any mock data required for the defined E2E test scenarios.
        - `a0.12.1.2t`: Execute the defined E2E test scenarios manually or with semi-automation. Document all steps, expected outcomes, and actual outcomes.
        - `a0.12.1.2`: Perform the E2E testing. Meticulously log any bugs, crashes, unexpected behaviors, or deviations from expected outcomes.
        - `a0.12.1.3t`: Define criteria for "passing" E2E tests for Alpha PoC (e.g., no critical crashes, core data flow works, basic functionality of each layer is demonstrable).
        - `a0.12.1.3`: Track and prioritize bugs found during E2E testing. Focus on fixing critical and major issues that prevent the Alpha PoC from meeting its goals. (Bug fixing itself might generate new `Z` tasks under the relevant `a0.X` module where the bug lies, or be tracked separately).

    - `a0.12.2.Z`: Final Code Review, Refinement, & Performance Baselines
        - `a0.12.2.1t`: Plan code review sessions for critical modules across all layers (`Rust` Sim, `Go` Orch, `Python` AI/UI/Logger/EMS/Config).
        - `a0.12.2.1`: Conduct peer code reviews focusing on correctness, clarity, adherence to basic coding standards, and identifying any obvious performance anti-patterns or major bugs. Address critical findings.
        - `a0.12.2.2t`: Identify key performance indicators (KPIs) for the Alpha PoC (e.g., simulation ticks per second for a small number of agents, UI frame rate, basic AI action decision time, event logging throughput).
        - `a0.12.2.2`: Run the E2E test scenarios (or dedicated performance test scenarios) and measure/record these baseline performance KPIs. This provides a benchmark for future optimization in Beta. (No major optimization work here, just measurement).

    - `a0.12.3.Z`: Documentation Completion & Review for Alpha
        - `a0.12.3.1t`: Review all existing design documents (Layer docs, Interaction doc, README, Versioning, Schema Registry, Design Philosophy, Glossary) for accuracy, completeness (for Alpha scope), and clarity.
        - `a0.12.3.1`: Update all design documents to reflect the final state of the Alpha PoC implementation. Ensure all links are correct.
        - `a0.12.3.2t`: Review code comments in critical sections for clarity and correctness.
        - `a0.12.3.2`: Ensure essential code comments are in place.
        - `a0.12.3.3t`: Write a "Getting Started with Alpha PoC" guide (as part of the main README or a separate document) explaining how to set up and run the integrated system.
        - `a0.12.3.3`: Draft the "Getting Started" guide.

    - `a0.12.4.Z`: Alpha PoC Release Tagging & Archival
        - `a0.12.4.1t`: Ensure all critical bugs identified in `a0.12.1.2` are fixed and re-tested.
        - `a0.12.4.1`: Complete final bug fixes for Alpha PoC.
        - `a0.12.4.2t`: Define procedure for creating a final `Git` tag for the Alpha PoC release.
        - `a0.12.4.2`: Create an annotated `Git` tag (e.g., `a0.12.4.2` or a more descriptive `alpha-poc-v1`) marking the codebase for the completed Alpha PoC.
        - `a0.12.4.3t`: (Optional) Plan for archiving any build artifacts, test reports, performance baseline data, and the final set of configuration files used for the PoC.
        - `a0.12.4.3`: (Optional) Archive relevant artifacts.


























































































