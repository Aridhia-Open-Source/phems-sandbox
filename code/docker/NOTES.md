# ADR: Running R/Julia Code in Dagster (`dagster-celery-k8s`)

## Status
Accepted – MVP implementation will use **Hybrid Entrypoint (Python + R in same container)**.

---

## Context
We need to run R and Julia code as part of a Dagster deployment (`dagster-celery-k8s` with RabbitMQ, Postgres, and MinIO).

Key constraints:
- R/Julia containers should remain free of Dagster dependencies.
- Large artifacts (models, datasets) should be persisted in MinIO, not returned directly via Dagster events.
- We want Dagster to manage orchestration, retries, and metadata.
- Developer experience should allow seeing logs in Dagster UI.

Dagster supports multi-language execution via the Pipes protocol, which works over Kubernetes jobs (`dagster-pipes-k8s`). There are multiple ways to integrate R/Julia code.

---

## Options Considered

### 1. `k8s_pipes` direct
- **Description**: Dagster launches an R/Julia container, which reads `DAGSTER_PIPES_INPUT` JSON and writes `DAGSTER_PIPES_OUTPUT` JSON.
- **Pros**: Minimal, officially supported, one container, clean separation of concerns.
- **Cons**: Logs from R/Julia only visible in Kubernetes logs, not Dagster UI.

### 2. Sidecar container
- **Description**: Pod with two containers: Python (Dagster + Pipes client) and R/Julia (runtime). JSON and logs exchanged via shared volume or exec.
- **Pros**: R/Julia is fully isolated; no awareness of Dagster or Pipes.
- **Cons**: More plumbing required (volumes, exec handling, log forwarding). Logs are not automatically visible in Dagster UI.

### 3. Hybrid Entrypoint (Python + R in same container) **[Chosen]**
- **Description**: Build a container with both Python and R. Entrypoint is a Python script using `k8s_subprocess.run()` to launch `Rscript`.
- **Pros**:
  - Dagster-Pipes automatically handles metadata and log streaming.
  - Logs from R/Julia subprocess appear in Dagster UI without extra work.
  - One container, simpler orchestration.
- **Cons**: Larger image footprint (must include Python + R).

### 4. Manual orchestration (no Pipes)
- **Description**: Run R/Julia as a plain Kubernetes job, persist outputs to MinIO/S3, and separately emit Dagster asset materializations in Python.
- **Pros**: Maximum isolation; R/Julia never sees Dagster.
- **Cons**: No Pipes integration (no retries, lineage, structured metadata). Requires reimplementing orchestration logic.

---

## Decision
For the MVP, we will use **Option 3: Hybrid Entrypoint**.
This balances simplicity, developer experience, and Dagster-native integration. It allows:
- Logs from R/Julia processes to flow directly into Dagster UI.
- Structured metadata (params, metrics, artifact URIs) to be returned via Pipes.
- Large artifacts to be persisted in MinIO, with only references passed through Dagster.

---

## Consequences
- Container images will include both Python and R (slightly larger size).
- R/Julia code remains dependency-free with respect to Dagster.
- Future migration to direct `k8s_pipes` (Option 1) remains possible if log capture requirements change.
