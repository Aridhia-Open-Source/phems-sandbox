# ADR 001: Multi Repository Architecture

## Status
Under Review

## Context
The proposed architecture manages data science workloads through Git-based deployment and governance. \
Reproducibility, auditability, and separation of responsibilities are key architectural requirements. \
Code, infrastructure, and workflow control must be versioned independently, with automated CI/CD pipelines enforcing review and deployment gates.

To achieve this, three repositories were introduced, each handling a specific part of the system lifecycle: \
**Node Repo**, **Code Repo**, and **Ctrl Repo**.

## Decision
Adopt a **multi-repository** structure with clearly defined scopes and flows for each of the repos

### 1. Node Repo
Defines **shared infrastructure** and base services for a deployment node. \
Includes Helm charts, Dagster configuration, Celery setup, and definitions for resources such as Postgres, MinIO, and RabbitMQ.

**Flow:**
1. Contributor raises a PR to modify the node configuration.
2. GitHub Actions runs CI checks (lint, build, test).
3. Maintainer reviews and merges the PR (manual approval gate).
4. ArgoCD deploys updated services and resources to the node.

### 2. Code Repo
Defines **computational logic** and code locations used by the orchestrator. \
Contains Dagster definitions, Dockerfiles, dependencies, and external modules.

**Flow:**
1. Researcher raises a PR to create or update a code location.
2. GitHub Actions runs CI (lint, build, test).
3. Data Controller reviews and merges the PR (manual approval gate).
4. ArgoCD deploys the new or updated code location (CodeServer + Workers).

### 3. Ctrl Repo
Implements **Git-based orchestration and governance**. \
This repository acts as the control plane for triggering jobs and managing result publication.

**Flows:**
- **Submit Job**
  1. Researcher raises a PR describing the job request.
  2. GitHub Actions validates the submission.
  3. Data Controller merges the PR to authorize the job.
  4. Node polls the repository and executes the authorized job.

- **Publish Results**
  1. Node stores results in internal storage and commits DVC metadata.
  2. Node raises a PR containing the `.dvc` files.
  3. Data Controller merges the PR to approve publication.
  4. Node pushes approved artifacts to publication storage.

## Consequences
- Enforces separation between infrastructure, user code, and control logic.
- Provides full traceability from submission to artifact publication.
- Supports Git-based approval gates for both deployment and execution.
- Increases repository coordination complexity and requires disciplined CI/CD configuration.

## Alternatives Considered
- **Single repository** for all code and configurations - rejected due to lack of separation and audit clarity.
- **Direct API-based orchestration** - rejected because it bypasses Git review and weakens auditability.
- **Unified GitOps repo per environment** - rejected for being harder to scale and govern across contributors.