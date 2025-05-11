# Versioning Strategy for Fish Eco Sim

**Version:** 1.0 (Updated with testing suffix and 1-based indexing for features)
**Last Updated:** 5/8/2025

---

## 1. Philosophy and Goals

This document outlines the versioning scheme for the Fish Eco Sim project. The primary goals of this strategy are:

*   **Clarity:** Provide a clear and unambiguous way to identify the stage of development and the specific iteration of the software.
*   **Granularity:** Allow for tracking progress at multiple levels, from major phases down to atomic tasks and individual runs.
*   **Traceability:** Enable easy tracing of features, bug fixes, and experimental runs back to specific versions.
*   **Test Integration:** Explicitly account for the development of tests as part of the versioning and development workflow.
*   **Flexibility:** Accommodate iterative development, refactoring, and the implementation of tests as distinct versioned steps if needed.
*   **Standard Adherence (loosely):** Incorporate common industry terms like "Alpha" and "Beta" while providing a more detailed internal structure.

---

## 2. Versioning Structure

The versioning structure is hierarchical and changes slightly based on the development phase (Alpha, Beta, Full Release). A key principle is that the *leading identifier* clearly indicates the overall phase. All feature/milestone/task counters (`X`, `Y`, `Z`) start from `1`.

### 2.1. Testing Suffix (`t`)

*   A `t` suffix can be appended to any `X`, `Y`, or `Z` component in the version number (e.g., `a0.X.Y.Zt`, `a0.X.Yt`, `a0.Xt`).
*   **Meaning:** This `t` signifies that the **tests for that corresponding feature, sub-feature, or atomic task have been defined and implemented.**
*   **Workflow:**
    1.  A feature/task (e.g., `a0.1.1.1`) is planned.
    2.  The development effort first focuses on writing and committing the tests for this feature/task. The completion of this testing effort can be considered the achievement of version `a0.1.1.1t`.
    3.  Subsequently, the functional code for `a0.1.1.1` is implemented.
    4.  The version `a0.1.1.1` is considered complete only when the functional code passes all tests defined in the `a0.1.1.1t` scope.
*   This suffix primarily serves as a **planning and development process marker** to ensure tests are written before or alongside feature implementation (Test-Driven Development / Behavior-Driven Development principles). Formal Git tags might use a more descriptive suffix like `-tests-defined` or the `t` suffix if preferred for tags related to test completion.

### 2.2. Alpha Phase (Pre-Release, Core Feature Development)

*   **Format:** `a0.X.Y.Z.i` (and their `t` suffixed counterparts like `a0.X.Y.Zt.i`)
*   **Components:**
    *   `a0`: **Phase Prefix.** Literally "a0" to denote the Alpha development phase.
    *   `X`: **Major Alpha Feature Set.** An integer, starting from `1`. (e.g., `a0.1` for "Configuration System UI - Basics"). `a0.Xt` signifies tests for this major feature set are defined.
    *   `Y`: **Sub-Feature Milestone.** An integer, starting from `1` (resets for each `X`). (e.g., `a0.1.1` for "Basic UI Framework & YAML I/O"). `a0.X.Yt` signifies tests for this sub-feature are defined.
    *   `Z`: **Atomic Task / Small Increment.** An integer, starting from `1` (resets for each `Y`). (e.g., `a0.1.1.1` for "Implement YAML file loading"). `a0.X.Y.Zt` signifies unit/integration tests for this atomic task are defined and implemented.
    *   `i`: **Iteration/Run Suffix.** An integer suffix (e.g., `.1`, `.2`) appended by the developer for each local run or interim commit during the development of a specific `Z` (or `Zt`) task. This is primarily for personal tracking and is *not typically part of the formal version tag* for a completed `Z` or `Zt` item, unless a specific run's artifact or log is being archived.

*   **Example:**
    *   `a0.1.1.1t`: Tests for "Implement YAML file loading" are written.
    *   `a0.1.1.1`: "Implement YAML file loading" functional code is complete and passes tests from `a0.1.1.1t`.

### 2.3. Beta Phase (Feature Complete for a Major Release, Focus on Testing & Refinement)

*   **Format:** `b1.X.Y.Z.i` (and their `t` suffixed counterparts)
*   **Components:**
    *   `b1`: **Phase Prefix.** Literally "b1" for the first Beta phase. Subsequent Beta phases could be `b2`, `b3`.
    *   `X`: **Major Beta Feature Set / Refinement Focus.** Integer, starting from `1`.
    *   `Y`: **Sub-Focus Area / Milestone.** Integer, starting from `1` (resets for each `X`).
    *   `Z`: **Specific Task / Bug Fix / Refinement.** Integer, starting from `1` (resets for each `Y`).
    *   `i`: **Iteration/Run Suffix.** (Same as Alpha).

*   **Example:** `b1.2.3.10t` (Tests for Beta task #10 in major focus 2, sub-focus 3 are written), then `b1.2.3.10` (Task complete and passes tests).

### 2.4. Full Version / General Availability (GA) Release

*   **Format:** `V.X.Y.Z.i` (where `V` is the Major Release number, e.g., 1, 2)
*   **Components:**
    *   `V`: **Major Release Number.** Integer, starting from `1`.
    *   `X`: **Minor Release / Major Feature Set.** Integer, starting from `0` or `1` as per typical SemVer (e.g., `1.1.Y.Z`).
    *   `Y`: **Patch Release / Sub-Feature Milestone.** Integer, starting from `0` or `1` (e.g., `1.1.1.Z`).
    *   `Z`: **Specific Bug Fix / Small Increment / Build Revision.** Integer, starting from `0` or `1`.
    *   `i`: **Iteration/Run Suffix OR Official Build Number.** For official builds, this can be a CI build number (e.g., `1.0.0.0.build567`). The `t` suffix is less common for GA releases but could signify a test suite version for a release candidate.

*   **Example:** `1.0.0.0` (First GA release). A patch might be `1.0.1.0`. A subsequent fix `1.0.1.1`.

---

## 3. Version Tagging and Branching Strategy (Brief Overview)

*   **Git Tags:**
    *   Formal versions (e.g., `a0.1.1.1`, `b1.1.0.0`, `1.0.0.0`) will be marked with annotated Git tags.
    *   Tags for test completion (e.g., `a0.1.1.1-tests-defined` or `a0.1.1.1t`) can be used if desired for specific tracking, though often the existence of tests is part of the "definition of done" for the non-`t` version.
*   **Main/Development Branches:**
    *   `main`: Represents the most stable, latest official release (Full Versions).
    *   `develop`: Active development branch where features are integrated. Serves as the base for Alpha/Beta work.
    *   (Potentially) `release/alpha`, `release/beta`: Branches for stabilizing specific Alpha or Beta releases if needed.
*   **Feature Branches:** Individual `Z`-level tasks (including writing their tests) will be developed on short-lived feature branches (e.g., `feature/a0.1.1.1-config-yaml-io`).

---

## 4. Roadmap Revisions

*   The project roadmap, which will detail the features and tasks planned for each version increment (`X`, `Y`, `Z`, including their `t` testing phases), will itself be versioned (e.g., "Roadmap Revision 1.0", "Roadmap Revision 1.1").
*   This allows the plan to evolve transparently if major pivots, new insights, or changing priorities necessitate adjustments to the planned sequence of work, without altering the fundamental versioning scheme for the software itself.

---