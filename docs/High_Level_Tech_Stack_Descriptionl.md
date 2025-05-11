# Fish Eco Sim: System Architecture Overview (Enhanced)

---

## 1. Simulation Layer
*   **Primary Language(s):** Rust
*   **Key Technologies/Patterns:** ECS (potential), Custom physics
*   **Core Responsibilities:**
    *   World state (grid, environment).
    *   Entity mechanics (movement, interactions).
    *   Rule execution.
    *   Observation generation.
    *   Action application.
    *   Reward calculation.
*   **Key Interactions (via Communication Layer):**
    *   Publishes: World state, agent events (death, birth), reward signals.
    *   Receives: Agent actions, **Configuration**.
*   **Other Considerations & Integrated Cross-Cutting Concerns:**
    *   Determinism.
    *   Performance optimization.
    *   Modularity for new sim elements.
    *   Headless operation.
    *   **Testing (Unit, Layer Integration)**.
    *   **Documentation (Code, Algorithm logic)**.

---

## 2. Orchestration Layer
*   **Primary Language(s):** Go
*   **Key Technologies/Patterns:** gRPC, NATS (Pub/Sub Hub), Goroutines, Channels
*   **Core Responsibilities:**
    *   Lifecycle management of Simulation Workers.
    *   Central Pub/Sub hub for event routing.
    *   Command & Control distribution.
    *   Sim-agnostic worker management.
*   **Key Interactions (via Communication Layer):**
    *   Receives: Events from Simulation, Commands from UI/Control/Experiment Mgr.
    *   Publishes: Events to UI/Logging/AI/Monitoring, Commands to Simulation.
    *   Reads: **Configuration**.
*   **Other Considerations & Integrated Cross-Cutting Concerns:**
    *   Scalability.
    *   Fault tolerance.
    *   Exposing clear APIs.
    *   **Testing (Unit, Layer Integration)**.
    *   **Documentation (API, Internal Logic)**.
    *   **Monitoring (Exposes Prometheus metrics)**.

---

## 3. Communication Layer
*   **Primary Language(s):** (N/A - Pattern)
*   **Key Technologies/Patterns:** Pub/Sub, gRPC, NATS, Protobuf, FlatBuffers
*   **Core Responsibilities:**
    *   Decoupling all layers.
    *   Defining message schemas & transport.
    *   Routing commands and events.
*   **Key Interactions (via Communication Layer):**
    *   Mediates ALL inter-layer communication.
*   **Other Considerations & Integrated Cross-Cutting Concerns:**
    *   Schema versioning.
    *   Serialization efficiency.
    *   Network transparency.
    *   Message bus persistence (NATS JetStream for Logging/Monitoring).

---

## 4. Agent Intelligence Layer
*   **Primary Language(s):** Python
*   **Key Technologies/Patterns:** PyTorch / TensorFlow, NumPy, DRL Libraries (SB3, RLlib)
*   **Core Responsibilities:**
    *   Agent decision-making (NN inference).
    *   RL training loop.
    *   Model management.
    *   Observation processing, action selection.
*   **Key Interactions (via Communication Layer):**
    *   Receives: Agent observations, reward signals, **Configuration**.
    *   Publishes: Agent actions.
*   **Other Considerations & Integrated Cross-Cutting Concerns:**
    *   Training vs. Inference modes.
    *   Scalability of training.
    *   Hyperparameter tuning.
    *   **Testing (Unit, Model validation)**.
    *   **Documentation (NN Arch, Training process)**.

---

## 5. UI Layer
*   **Primary Language(s):** Python (initially, C# later)
*   **Key Technologies/Patterns:** Pygame, Pygame GUI / PyQt, (Future: Avalonia UI)
*   **Core Responsibilities:**
    *   Real-time visualization.
    *   User interaction & controls.
    *   Displaying sim info & stats.
*   **Key Interactions (via Communication Layer):**
    *   Receives: Real-time world state, agent details.
    *   Publishes: User commands.
    *   Reads/Writes: **Configuration** (via Config UI tool).
*   **Other Considerations & Integrated Cross-Cutting Concerns:**
    *   Responsiveness.
    *   Frame rate.
    *   (Future) Historical data playback from logs.
    *   Cross-platform.
    *   **Testing (UI interactions)**.
    *   **Documentation (User Guide)**.

---

## 6. Logging Layer
*   **Primary Language(s):** Python
*   **Key Technologies/Patterns:** NATS JetStream (sub), Apache Parquet (store), Pandas
*   **Core Responsibilities:**
    *   Asynchronous, eventually consistent event capture.
    *   Batch writing of structured logs (time-series aware).
    *   Storing simulation history.
*   **Key Interactions (via Communication Layer):**
    *   Subscribes: To event streams (raw sim data, orchestrator operational data).
    *   Reads: **Configuration**.
*   **Other Considerations & Integrated Cross-Cutting Concerns:**
    *   Log rotation/retention.
    *   Source timestamp preservation.
    *   Scalability for high event volume.
    *   **Testing (Data integrity, write performance)**.
    *   **Documentation (Log format, data schema)**.

---

## 7. Statistical Interpretation / Analysis Layer
*   **Primary Language(s):** Python (primarily)
*   **Key Technologies/Patterns:** Pandas, NumPy, Matplotlib, Seaborn, Jupyter, Dask
*   **Core Responsibilities:**
    *   Offline analysis of logged Parquet data.
    *   Generating statistics, visualizations, reports.
    *   Debugging, insight generation, comparative analysis.
*   **Key Interactions (via Communication Layer):**
    *   Reads: Parquet files, **Configuration** (for analysis parameters).
*   **Other Considerations & Integrated Cross-Cutting Concerns:**
    *   Query performance.
    *   Reproducibility of analyses.
    *   **Documentation (Analysis scripts, findings)**.

---

## 8. Configuration Management System
*   **Primary Language(s):** Python UI, YAML files
*   **Key Technologies/Patterns:** Tkinter/PyQt/Web UI, YAML parsing libraries (all languages)
*   **Core Responsibilities:**
    *   Centralized definition & storage of all system parameters.
    *   UI for easy editing & validation of configurations.
*   **Key Interactions (via Communication Layer):**
    *   Provides: Configs to All Layers at startup.
    *   UI edits: YAML files.
*   **Other Considerations & Integrated Cross-Cutting Concerns:**
    *   Schema definition & validation.
    *   Version control for config files.
    *   Ease of use for defining complex setups.
    *   **Testing (Config parsing, UI functionality)**.
    *   **Documentation (Config schema, UI Guide)**.

---

## 9. Experiment Management System
*   **Primary Language(s):** Python UI & Scripts
*   **Key Technologies/Patterns:** YAML/JSON (for plans), gRPC (to Orchestrator)
*   **Core Responsibilities:**
    *   Defining, scheduling, and managing sequences of simulation runs.
    *   Parameter sweeps, batch executions.
    *   Tracking experiment parameters & linking to results.
*   **Key Interactions (via Communication Layer):**
    *   Publishes: "Start Simulation" commands (with specific configs) to Orchestrator.
    *   Reads: **Configuration** (base for experiments), (Potentially) Logged data for results summary.
*   **Other Considerations & Integrated Cross-Cutting Concerns:**
    *   Reproducibility of experiments.
    *   Integration with results from Logging/Analysis layers.
    *   Scalability for many parallel runs.
    *   **Testing (Plan generation, Orchestrator interaction)**.
    *   **Documentation (Plan format, UI Guide)**.

---

## 10. Evolution Engine (GA)
*   **Primary Language(s):** Python
*   **Key Technologies/Patterns:** Custom GA logic, interaction with other layers
*   **Core Responsibilities:**
    *   Managing genetic representations (genomes).
    *   Applying selection, crossover, mutation.
    *   Orchestrating simulation runs for fitness evaluation.
*   **Key Interactions (via Communication Layer):**
    *   Uses: Experiment Management to run sims.
    *   Reads: Fitness data from Statistical Analysis (of Parquet logs), **Configuration**.
    *   Generates: Agent configs for Sim/AI layers.
*   **Other Considerations & Integrated Cross-Cutting Concerns:**
    *   Genome design (physical & behavioral traits).
    *   Fitness function definition.
    *   Scalability for many generations/individuals.
    *   **Testing (GA operators, fitness calculation)**.
    *   **Documentation (Genome struct, GA process)**.

---

## 11. Monitoring & Alerting System
*   **Primary Language(s):** Prometheus, Grafana, Python/Go (Alerting Service)
*   **Key Technologies/Patterns:** NATS (for alert events), Email/Slack integration
*   **Core Responsibilities:**
    *   Real-time monitoring of system health & performance metrics.
    *   Visualization of metrics in dashboards.
    *   Alerting on predefined critical conditions or anomalies.
*   **Key Interactions (via Communication Layer):**
    *   Scrapes: Metrics from Orchestrator, Sim, AI, Logger.
    *   Subscribes: To critical event NATS topics.
    *   Publishes: Alerts (email, etc.).
    *   Reads: **Configuration** (alert rules).
*   **Other Considerations & Integrated Cross-Cutting Concerns:**
    *   Defining meaningful metrics & alert thresholds.
    *   Minimizing false positives.
    *   Actionable alerts.
    *   **Testing (Alert triggers, notification delivery)**.
    *   **Documentation (Metrics definitions, Alert setup)**.

---

## Cross-Cutting Implementation Notes
*   **Testing Framework:** Underpins all layers. Unit, integration (intra-layer & inter-layer/stack), and E2E tests. Automated via **CI/CD**. Generates **Test Reports**.
*   **Documentation Strategy:** Accompanying design documents (architecture, algorithms, interfaces, data flows, using pseudocode/diagrams where helpful) + essential code-level comments. Meticulously updated. Stored in a version-controlled system (e.g., `docs/` folder, project Wiki).

---