# Issue/Template Advice

## Which issue type should I use?

Use the template that best matches the size and intent of the work:

- [🗺️ Epic](#epic)
- [💡 Feature](#feature)
- [🧩 Task](#task)
- [🐛 Bug Report](#bug)
- [🔎 Pull Request (PR)](#pull_request)
- [🛟 Support](#support)

---

<a id="epic"></a>
### 🗺️ Epic

Use an Epic for a **single, coherent outcome** that will take **multiple sprints** and will be delivered through multiple **Features** (which then break down into Tasks). An Epic should describe the *why*, the *scope boundaries*, and what “done” looks like — it’s not a general bucket for unrelated work.

#### Epic issue type: field examples

##### Outcome / goal
***What are we trying to achieve, for whom, and why now?***

Example:
- **Outcome:** Operators can start/stop key subsystems remotely and confirm execution without being onsite.
- **Stakeholders / users impacted:** Field operators, support engineers, on-call.
- **Why now:** Reduces site visits during winter deployments; current process is slow and error-prone.
- **How we’ll measure success (optional):** 80% fewer “onsite required” interventions for routine operations; mean time to recover from operator error reduced by 50%.

##### Scope
***High-level “in vs out” boundaries so the Epic stays manageable.***

Example:
- **In scope:**
  - Remote start/stop for pump + basic safety interlocks
  - Display current state + last command result
  - Basic access control (operator vs admin)
- **Out of scope:**
  - Full role-based permissions matrix
  - Advanced analytics dashboards
  - Offline-first operation / store-and-forward control

##### Exit criteria (definition of done)
***Clear conditions for closing the Epic.***

Example:
- All planned **Feature sub-issues** are completed and accepted
- Critical docs updated (operator notes + user manual)
- Health checks and alerts added for the new control path
- Demo completed with a real robot + sign-off from ops/support

##### Epic Priority
***How urgently we need the outcome.***

Example:
- **Urgent**: blocks a customer delivery / safety issue / repeated incidents
- **High**: needed for next milestone
- **Normal**: valuable, but not time-critical
- **Low**: nice-to-have / opportunistic

##### Target window
***A rough delivery window (prefer ranges).***

Example:
- `Sprint 14–16`
- `Q1`
- `Before March field trials`

##### Dependencies / risks
***Anything that could block delivery or introduce uncertainty.***

Example:
- **Dependencies:**
  - API contract from telemetry service
  - Hardware availability for validation tests
  - Security review for remote control path
- **Risks:**
  - Unknown failure modes on poor connectivity
  - Safety interlocks need careful validation
  - Cross-repo coordination could slow integration
- **Mitigations (optional):**
  - Run a spike Feature to prototype comms behaviour
  - Add staged rollout + feature flag

---

#### Epic examples written as outcomes

**Remote operations MVP**
- Outcome: “As a field operator, I can perform the core remote actions safely and verify they happened.”
- Likely Features:
  - Operator can start/stop pump remotely (happy path)
  - Operator can view current state + last command result
  - Basic faults visible + clear error messages

**Telemetry pipeline v2**
- Outcome: “As support/on-call, we can trust telemetry is captured, searchable, and exportable during incidents.”
- Likely Features:
  - Export telemetry for time range
  - Buffering/retry when offline
  - Schema/versioning so fields don’t silently break

**Reliability & watchdog improvements**
- Outcome: “The system detects failures quickly and recovers automatically with clear diagnostics.”
- Likely Features:
  - Service health endpoint + status page
  - Watchdog integration + restart policy
  - Alerting when telemetry stops / critical services restart

✅ After creating the Epic, add it to the appropriate **Project** (right-hand sidebar → **Projects**) and create the Features as **sub-issues** of the Epic.

---

<a id="feature"></a>
### 💡 Feature

Use this when you want to describe a **chunk of added value** from a stakeholder’s point of view — something someone can do afterwards that they couldn’t do before (or can do more easily/safely). A Feature should be **small enough to complete within one sprint**.

A Feature should be written as a **user story** (who / what / why) with **user-facing acceptance criteria**. It is then broken down into **Tasks** (implementation steps). The stakeholder might be a customer/operator, but it can also be an internal stakeholder (e.g., a developer, support engineer, or operations).

#### Feature examples and field usage

Below are the same examples explaining what “good” looks like for the fields specified.

---

#### Example 1: Emergency stop via RC transmitter

**Title**
- `💡 [FEATURE] - RC emergency stop to put bot in safe state`

**User story**
- As a **field operator**, I want to **stop all actuation of a bot using an RC transmitter**, so that I can **put the bot into a safe state**.

**Parent Epic**
- `#82` (Remote operations MVP)  
  *(or paste the full Epic URL if needed)*

**Acceptance criteria (user-facing, testable)**
- AC1: When the operator activates the RC e-stop, the bot enters **Safe State** within **≤ 500 ms**.
- AC2: In Safe State, **all actuation outputs** are disabled (drive, pumps, valves, etc.) until explicitly cleared.
- AC3: The UI/telemetry exposes `safe_state = true` and a timestamp for the last e-stop event.
- AC4: If RC signal is lost for **> N ms**, the bot defaults to Safe State (fail-safe).
- AC5: A clear operator message is presented for Safe State entry and exit (no silent transitions).

**Notes / design / links**
- Context: We’ve had near-miss incidents during testing; need a fast, independent safety override.
- Approach:
  - Define Safe State semantics (what “actuation disabled” means per subsystem).
  - RC receiver input → debounced e-stop signal → safety controller → broadcast state.
- Links:
  - Safety requirements doc: …
  - Firmware/IO mapping: …
  - Related issues: #105 (RC receiver integration), #106 (telemetry field additions)

---

#### Example 2: Export telemetry for a time range

**Title**
- `💡 [FEATURE] - Export telemetry for a selected time range`

**User story**
- As a **support engineer**, I want to **export telemetry for a selected time range**, so that I can **diagnose incidents and share evidence quickly**.

**Parent Epic**
- `#140` (Telemetry pipeline v2)

**Acceptance criteria**
- AC1: Support can select a **start/end time** and export telemetry as **CSV** (minimum) via CLI or UI.
- AC2: Export includes **timestamps**, **unit-labelled fields**, and the **robot identifier**.
- AC3: Export completes within **≤ 60 seconds** for a 1-hour window on a typical robot dataset (or provides progress indication).
- AC4: If data is missing, the export clearly indicates gaps (e.g., missing intervals, “no data available”).
- AC5: Output is deterministic and shareable: same inputs → same file content (ordering + formatting consistent).

**Notes / design / links**
- Context: Current investigations require manual log pulling and bespoke scripts.
- Approach:
  - Define export schema (columns + units).
  - Add filter-by-time SQL query 
  - Add a “share bundle” option later (out of scope for this Feature).
- Links:
  - Incident postmortem: …
  - Telemetry schema repo/docs: …
  - UX mock (if UI): …

---

#### Example 3: Camera health status visibility

**Title**
- `💡 [FEATURE] - Display camera health status (online/FPS/last frame time)`

**User story**
- As an **operator**, I want to **see camera health status (online/offline, FPS, last frame time)**, so that I can **spot failures before they affect a mission**.

**Parent Epic**
- `#201` (Operational observability improvements)

**Acceptance criteria**
- AC1: Operator can view camera status: **Online/Offline**, **FPS**, and **Last frame received timestamp**.
- AC2: If no frame is received for **> 2 seconds**, status becomes **Degraded**; for **> 10 seconds**, **Offline**.
- AC3: Status updates at least every **5 seconds** without needing a manual refresh.
- AC4: Status is visible in both **local UI** and **remote UI** (if applicable) with the same semantics.
- AC5: A clear warning indicator is shown when status is Degraded/Offline (no hidden failures).

**Notes / design / links**
- Context: Operators often only notice camera failure after downstream perception breaks.
- Approach:
  - Source truth for “camera alive” (frame timestamps from acquisition pipeline).
  - Define thresholds for degraded/offline.
  - Expose a single health endpoint + UI widget.
- Links:
  - Existing healthcheck endpoint: …
  - Camera pipeline module docs: …
  - Related bugs: #317 (sporadic FPS drops)

---

#### Example 4: Run full test suite in CI on every PR

**Title**
- `💡 [FEATURE] - Run full test suite in CI on every PR`

**User story**
- As a **developer**, I want to **run the full test suite in CI on every PR**, so that I can **catch regression issues before I merge**.

**Parent Epic**
- `#55` (Engineering effectiveness / build reliability)

**Acceptance criteria**
- AC1: On PR open/update, CI runs **build + unit tests** (minimum) and reports pass/fail in GitHub checks.
- AC2: CI finishes within **≤ 20 minutes** for the standard PR path (or provides a fast/slow split).
- AC3: Failures provide actionable output (test name, logs/artifacts retained for ≥ 7 days).
- AC4: The main branch is protected so PRs require CI passing before merge (where appropriate).
- AC5: A developer can reproduce CI locally using documented instructions (dev container / script / make target).

**Notes / design / links**
- Context: Regressions are being found late; we need earlier feedback.
- Approach:
  - Add CI workflow(s): build matrix, caching, test execution.
  - Define minimum required checks and branch protection rules.
- Links:
  - CI proposal doc: …
  - Existing workflow files: …
  - Tooling: CMake presets / colcon config / test harness docs: …

---

✅ After creating the Feature, add it to the appropriate **Project** using the right-hand sidebar → **Projects**.  
N.B. If you have linked the Feature to a Parent Epic that is already part of this project, the Feature should inherit this.

At Sprint Planning, once the issue is moved to **Ready**, please ensure that a **Priority** is assigned and an **Estimate** is given (see the guide below). If you’re not sure which Project to use, email engineering@assetcool.com.

<a id="estimation"></a>
### Story point estimation guide

**Story points are relative (not hours).** Use them to express overall effort/complexity/uncertainty.

**Use this as a guide for populating _Projects → Estimate_ during Sprint Planning:**
- **?**: not enough info to estimate (needs clarification/spike)
- **½–1**: tiny, well understood, low risk
- **2–3**: small, straightforward, some unknowns
- **5**: medium, multiple steps, needs testing
- **8**: large, design decisions / more moving parts
- **13**: very large, high uncertainty — consider splitting
- **20/40/100**: too big/uncertain — break down before committing
- **∞**: unbounded/unestimable as written (re-scope)

Further explanation: https://www.mountaingoatsoftware.com/blog/why-the-fibonacci-sequence-works-well-for-estimating

---

<a id="task"></a>
### 🧩 Task

Use a Task for a **small, concrete unit of implementation work** that supports a Feature. A Task should be something an engineer can pick up and complete in a short time (often hours to 1–2 days). Tasks are **engineering deliverables**, not stakeholder-facing outcomes.

Best practice: create Tasks as **sub-issues of a Feature** (use **Create sub-issue** from the Feature) so the hierarchy stays correct.

#### Typical Task examples
- Add a unit test for a module
- Implement a single API method
- Add logging/metrics to one component
- Refactor a function/class without changing behaviour
- Update a dependency and fix any fallout
- Write a small migration script/tool

---

#### Task template field examples

##### Linked Feature (required)
Paste the Feature this Task supports (issue number or full URL).

Examples:
- `#214`  
- `https://github.com/AssetCool/bot_system/issues/214`

Good rule: if you can’t link it to a Feature, it might be a **Feature** (new value) or a **Bug** (something broken), not a Task.

##### Task goal (required)
One or two sentences: **what will be delivered**. Keep it specific and action-oriented.

Examples:
- “Add a unit test covering CAN message parsing for pump start/stop commands.”
- “Implement `GET /health/cameras` endpoint returning online/offline + last-frame timestamp.”
- “Refactor `TelemetryPublisher` to separate serialization from transport (no behaviour change).”

##### Verification / how to test (optional)
This is a “how do I know this is done?” section. Keep it practical and reproducible.

Examples:
- “Start the stack locally, disconnect the camera, and confirm `/health/cameras` reports `offline` within 10s.”
- “Run integration test `telemetry_export` and verify CSV contains timestamps + robot_id and the expected telemetry.”

##### Implementation notes / links (optional)
Useful context for the implementer (approach, constraints, pointers). Keep it short.

Examples:
- “Approach: add parser tests using recorded CAN frames from `/var/logs/ac/can_samples/`.”
- “Dependency: requires Feature #214 schema to be merged first.”
- “Related PRs/issues: #301 (CAN heartbeat), PR #455 (healthcheck framework).”

##### Definition of done
Use this checklist to avoid “almost finished” tasks.

Suggested interpretation:
- **Work merged/commits made if part of a larger PR:** there is a PR merged, or the task is part of a larger PR and commits have been made and pushed.
- **Tests added/updated (if applicable):** if the change affects behaviour, add/adjust tests.
- **Docs updated (if applicable):** README/config docs updated if a user/operator/developer workflow changed.

---

#### Quick sizing guidance for Tasks
If a Task starts growing:
- If it needs multiple independent commits or several days of work → split into **smaller Tasks**.
- If you’re writing a new stakeholder-visible capability → it’s probably a **Feature**.
- If you’re fixing something broken → use **Bug Report** instead.

---

<a id="bug"></a>
### 🐛 Bug Report

Use this when something is broken, unreliable, or behaving incorrectly in an existing system (i.e. not “new work”, but a defect).

When you raise a bug, please fill in the template fields so someone else can reproduce and verify the fix:

- **Description:** what’s wrong, in one or two sentences.
- **Reproduction steps:** minimal steps to reliably trigger the problem.
- **Expected vs actual:** what should happen vs what does happen.
- **Environment / version:** device/OS/service version/commit/build (anything that might affect reproducibility).
- **Screenshots / Logs:** supporting evidence (error text, stack traces, photos, etc.).
- **Fix criteria:** how we’ll know it’s fixed (e.g., no longer repros; regression test added).

Examples:

**“Pump start command returns ‘OK’, but the pump never starts.”**
- Reproduction: send StartPump via UI → observe no movement
- Expected: pump starts within 2s and state becomes Running
- Actual: state flips to Running but hardware remains off
- Env/version: Jetson Orin NX / Ubuntu 22.04 / bot_system vX.Y (commit …)
- Logs: include CAN frames / controller logs

**“Telemetry drops out after ~10 minutes of running.”**
- Reproduction: run system for 10–15 mins → telemetry stream stops
- Expected: continuous telemetry at configured rate
- Actual: MQTT topic stops publishing; UI shows stale values
- Env/version: Jetson Orin NX / Ubuntu 22.04 / bot_system vX.Y (commit …) / network type (Wi-Fi/LTE)
- Logs: MQTT client logs

**“Clicking ‘Save settings’ crashes the app.”**
- Reproduction: open Settings → change parameter → click Save
- Expected: settings persist and success message shown
- Actual: app crashes / throws exception
- Evidence: screenshot/video + stack trace
- Fix criteria: add regression test; no crash; settings persist across restart

---

<a id="pull_request"></a>
### 🔎 Pull Request (PR)

Use a PR to propose a change to the codebase that should be reviewed and merged. PRs are where we capture **what changed**, **why**, **how to verify it**, and **any rollout risk**.

This repository includes a PR template to make reviews consistent and fast. Below is guidance on how to fill it out with concrete examples.

---

#### What type of PR is this?
Tick all that apply. This helps reviewers quickly understand intent.

Examples:
- 🍕 **Feature**: adds new capability  
  > “Add `/health/cameras` endpoint”
- 🐝 **Bug Fix**: fixes incorrect behaviour  
  > “Fix CAN timeout parsing when frame length is 0”
- 👨‍💻 **Refactor**: code restructure, no behaviour change  
  > “Split TelemetryPublisher into serializer + transport”
- 🔥 **Performance Improvement**: measurably faster/leaner  
  > “Reduce image pipeline allocations; improves FPS by ~15%”
- 📝 **Documentation Update**: docs-only change  
  > “Update user manual for watchdog restart behaviour”
- 🔁 **CI**: workflows/build changes  
  > “Enable caching for colcon build in GitHub Actions”
- 📦 **Chore**: housekeeping  
  > “Bump dependency versions; remove unused package”
- ⏪ **Revert**: revert a prior PR  
  > “Revert PR #456 due to regression in telemetry export”

---

#### Description
Explain the change in plain English. Aim for:
- **What** you changed
- **Why** you changed it
- **What the user/system can do now**

Example:
> Adds a camera health endpoint and UI indicator so operators can see whether each camera is online and when the last frame was received. This reduces time-to-diagnose when perception fails due to camera dropout.

---

#### Related Tickets & Documents
Link issues and docs so the PR is traceable. Use GitHub keywords to auto-close issues on merge.

Examples:
- `Closes #214` (Feature issue)
- `Relates to #317` (bug, discussion, or follow-up)
- `Depends on #455` (blocked until another PR/issue merges)
- Links to design doc / spec / ADR:
  - “Design notes: …”
  - “User manual update: …”

Tip: If this PR implements a **Task**, also link that Task issue (and it should already be a sub-issue of the Feature).

---

#### Approach / Notes for reviewers
Help reviewers focus their attention. Call out:
- key design decisions
- trade-offs
- risky areas
- what you want reviewed most

Examples:
- “Key logic is in `CameraHealthService::computeStatus()` — please sanity check thresholds.”
- “I chose polling over callbacks to keep acquisition pipeline unchanged.”
- “Main risk: false offline detection on slow networks; thresholds are configurable.”

---

#### How to test
This is the most important section for review quality. Be explicit.

Examples:
- **Unit:** `./build/unit_tests --gtest_filter=CameraHealth*`
- **Integration:** `./scripts/run_stack.sh` then `curl localhost:8080/health/cameras`
- **Manual:** unplug camera → confirm UI shows **Degraded** in ~2s and **Offline** in ~10s

Good pattern:
- commands someone can copy/paste
- expected output or observable behaviour
- any test data needed and where to find it

---

#### Tests, Screenshots, Recordings
Attach evidence where it helps reviewers:
- screenshots of UI changes
- logs showing new behaviour
- short screen recording for workflows
- benchmark numbers for performance PRs

Example:
- “Screenshot: camera widget states (online/degraded/offline)”
- “Log excerpt: health endpoint output”
- “Before/after FPS table (same dataset, same hardware)”

---

#### Added/updated tests?
Be honest and specific.

Examples:
- 👍 **Yes**: “Added unit tests for status threshold logic; updated integration test to assert endpoint schema.”
- 🙅 **No, and this is why**: “Pure documentation change.” / “Spike/prototype only; will add tests in follow-up Feature.”
- 🙋 **I need help**: “Not sure how to mock the camera pipeline; suggestions welcome.”
- ❌ **Not required**: “Formatting-only change; no behaviour impact.”

---

#### Added to documentation?
Tick where you documented the change.

Examples:
- 📜 **README.md**: “New env var `CAM_HEALTH_TIMEOUT_MS` and local test steps”
- 🦆 **In Code**: “Added docstring + comments around thresholds”
- 🙈 **No Documentation Required**: only if truly internal/no user impact

---

#### Risk of rollout
This is for reviewers and release planning. Choose the highest plausible risk.

Examples:
- 🟢 **Low**: refactor with no behaviour change + strong test coverage
- 🟠 **Medium**: affects a shared module; may impact runtime behaviour; needs careful review
- 🔴 **High**: touches safety/control paths, data loss risk, migration required, or hard-to-revert changes

If 🟠/🔴, add a line in “Approach / Notes” describing mitigation:
- feature flag (toggle in the code or config to turn the feature on/off)
- staged rollout
- rollback plan
- additional monitoring

---

#### Post-merge tasks (optional)
Only check if there’s real follow-up work required **after** merge.

Examples:
- “Deploy to staging and verify telemetry export for 24 hours”
- “Update Grafana dashboard to include new health metrics”
- “Run migration script on production database”

---

##### Review-friendly PR size guideline
Prefer PRs that can be reviewed in **15–30 minutes**. If it’s too large:
- split into separate PRs (refactor → feature → cleanup)
- or split work into multiple Tasks/PRs under the same Feature

---

<a id="support"></a>
## 🛟 Support

If you need help with templates or you’re unsure which issue type to use, contact the engineering team:

- Email: engineering@assetcool.com
