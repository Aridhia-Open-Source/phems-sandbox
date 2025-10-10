---
marp: true
theme: default
class: lead
paginate: true
---

# Dagster in the Node
### A Local Orchestrator for Data Science

Dagster manages and monitors all workflows inside a single secure node.
It ensures data processing and model training are **reproducible** and **auditable**, keeping all data within organizational boundaries.

```mermaid
graph TD
  A["Dagster Orchestrator"] --> B["Storage (MinIO/S3)"]
  A --> C["Database (Postgres)"]
  A --> D["Compute (Kubernetes Workers)"]
  style A fill:#eef,stroke:#000,stroke-width:1px
```