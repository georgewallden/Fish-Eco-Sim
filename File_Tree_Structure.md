Documentation Table of Contents (File Tree Structure)

Version: 3 - Alpha a0.2.1.1

This document provides an index to all major design, planning, and architectural documents for the Fish Eco Sim project, reflecting the file structure.
Use code with caution.

FISH ECO SIM/
├── docs
│   ├── layers
│   │   ├── 1. Simulation Layer.md
│   │   ├── 2. Orchestration Layer.md
│   │   ├── 3. Communication Layer.md
│   │   ├── 4. Agent Intelligence Layer.md
│   │   ├── 5. UI Layer.md
│   │   ├── 6. Logging Layer.md
│   │   ├── 7. Analysis Layer.md
│   │   ├── 8. Configuration Management System.md
│   │   ├── 9. Experiment Management System.md
│   │   ├── 10. Agent Evolution System.md
│   │   └── 11. Monitoring and Alerting System.md
│   ├── roadmap
│   │   ├── alpha.md
│   │   ├── beta.md
│   │   ├── full.md
│   │   └── Versioning Strategy.md
│   ├── Design_Philosophy.md
│   ├── Glossary_of_Terms.md
│   ├── High_Level_Tech_Stack_Description.md
│   ├── Schema_Registry.md
│   ├── Tech Stack diagram.txt
|   └── File_Tree_Structure.md
├── schemas/
│   ├── flatbuffers/ 
│   │   └── world_state.fbs
│   └── protobufs/ 
│   │   └── generic_event.proto
├── scripts/
├── src/
│   ├── generated_schemas/
│   │       ├── go/                          
│   │       │   ├── flatbuffers                         
│   │       │   └── protobufs
│   │       ├── python/                          
│   │       │   ├── flatbuffers                         
│   │       │   └── protobufs
│   │       └── rust/                          
│   │           ├── flatbuffers                         
│   │           └── protobufs     
│   └── modules/
│       ├── agent_intelligence/
│       ├── config_editor/                      
│       │   ├── __init__.py                     
│       │   ├── app.py                          
│       │   ├── yaml_io.py                      
│       │   ├── default_configs/                
│       │   │   └── default_simulation_config.yaml 
│       │   └── tests/                          
│       │       ├── __init__.py                 
│       │       ├── test_yaml_io.py    
│       │       └── test_files/
│       │           ├── malformed.yaml
│       │           ├── valid.yaml
│       │           ├── valid2.yaml
│       │           └── flat_test.yaml  
│       ├── logging_service/
│       ├── orchestrator/                               
│       └── simulation_engine/
├── .gitignore
├── File_Tree_Structure.md
├── License.txt
└── README.md                              
              


File Descriptions:

README.md (Root)

Overall project vision, goals, high-level architecture, and getting started guide.

docs/ (Main Documentation Folder)

## `docs/layers/` (Layer-Specific Design Documents)

*   **`Simulation Layer.md`**: Design for the core `Rust`-based world engine and simulation mechanics.
*   **`Orchestration Layer.md`**: Design for the `Go`-based central coordinator for workers and communication.
*   **`Communication Layer.md`**: Defines patterns, technologies (`NATS`, `gRPC`), and schemas (`Protobuf`, `FlatBuffers`) for inter-service communication.
*   **`Agent Intelligence Layer.md`**: Design for the `Python`-based DRL agent decision-making and training system.
*   **`UI Layer.md`**: Design for the `Python`/`Pygame`-based user interface for visualization and control.
*   **`Logging Layer.md`**: Design for the `Python`-based system for capturing simulation events to `Apache Parquet`.
*   **`Analysis Layer.md`**: Design for tools and scripts (`Python`) for offline statistical analysis of logged data.
*   **`Configuration Management System.md`**: Design for the `YAML`-based configuration files and `Python` UI tool for managing system parameters.
*   **`Experiment Management System.md`**: Design for the `Python`-based system for automating and tracking batches of simulation runs.
*   **`Agent Evolution System.md`**: Design for the `Python`-based Genetic Algorithm system for evolving agent traits/parameters.
*   **`Monitoring and Alerting System.md`**: Design for the system (`Prometheus`, `Grafana`) for observing system health and performance.

## `docs/roadmap/` (Roadmap & High-Level Planning Documents)

*   **`alpha.md`**: Detailed task breakdown and goals for the Alpha Proof of Concept phase.
*   **`beta.md`**: Conceptual goals and potential focus areas for the Beta phase.
*   **`full.md`**: Conceptual goals for General Availability (GA) releases and post-V1.0 development.
*   **`Versioning Strategy.md`**: Defines the versioning scheme for Alpha, Beta, and Full Release phases.

## Other Key Documentation Files

*   **`Design_Philosophy.md`**: Guiding principles behind major architectural choices and development approaches.
*   **`Glossary_of_Terms.md`**: Definitions of project-specific terminology and acronyms.
*   **`High_Level_Tech_Stack_Description.md`**: Summary table of all layers, their technologies, responsibilities, and key interactions.
*   **`Schema_Registry.md`**: Central registry for all data schemas, `event_type_key` strings, `NATS` topics, and `gRPC` services.
*   **`Tech Stack diagram.txt`**: Textual description of primary communication pathways and data formats between core services.
*   **`File_Tree_Structure.md`**: This file.

