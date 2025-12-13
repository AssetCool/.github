# .github

This repository contains **organisation-level defaults** for GitHub issue templates and related settings.
These defaults apply across the organisation, but can be **overridden in an individual repository** by adding repo-specific templates under `.github/ISSUE_TEMPLATE/`.

## Which issue type should I use?

Use the template that best matches the size and intent of the work:

### 🐛 Bug Report
Use this when something is **broken or behaving incorrectly** in an existing system.
Include clear reproduction steps, expected vs actual behaviour, and any logs/screenshots.

Typical examples:
- A pump fails to start when commanded
- Telemetry values are incorrect or missing
- A UI button crashes the app

### 🧩 Task
Use this for a **small, concrete unit of implementation work**, usually completed within a sprint and often as part of a Feature.

Typical examples:
- Add a unit test for a module
- Implement a single API method
- Refactor a component, update a dependency, add logging

Best practice: create Tasks as **sub-issues of a Feature** where possible.

### 💡 Feature
Use this for a **user-visible slice of value** (a capability you can describe to a user/customer).
A Feature should contain a user story and acceptance criteria, and can be broken down into Tasks.

Typical examples:
- “Add gRPC endpoint to start/stop pump”
- “Export telemetry to CSV”
- “Add camera health monitoring page”

### 🗺️ Epic
Use this for a **large outcome** that will take **multiple sprints** and consists of multiple Features.
Epics help track progress at a higher level and group related Features together.

Typical examples:
- “Remote operations MVP”
- “Telemetry pipeline v2”
- “Improved reliability and watchdogs across subsystems”

## Support

If you need help with templates or you’re unsure which issue type to use, contact the engineering team:

- Email: engineering@assetcool.com
