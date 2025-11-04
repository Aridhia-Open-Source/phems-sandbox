# Architecture Overview

The PHEMS framework is designed as an open-source federated orchestration layer for highly regulated environments such as healthcare.
It balances operational efficiency with strict compliance requirements through modular components, auditable workflows, and secure execution patterns.

## Dagster Orchestration
- Unified control plane for teams to build, scale, and observe their AI & data pipelines with confidence using python.
- Adaptable framework with pluggable configuration for storage, sensors, schedules, logging, etc
- Provides reproducibility and auditability without the overhead of similar platforms like Kubeflow or Airflow.

## Workers and Celery
- Allows horizontal scaling of execution capacity without centralizing compute or exposing sensitive data outside the Federated Node
- Workers are Kubernetes pods that execute user-defined tasks (ops, jobs, or asset materializations) as kubernetes jobs.
- Celery is a distributed task queue system that executes jobs asynchronously across worker processes using message brokers like RabbitMQ

## Federated design
- Each Data Controller (hospital or research site) hosts a self-contained node with Dagster services, workers, and resources.
- Sensitive data remains siloed, while only approved outputs are exposed for collaboration and aggregation.

## Central orchestrator
- Coordinates across federated nodes, aggregates metrics, and publishes federated models.
- Integrates with MLflow for experiment tracking and model registry to manage the global model lifecycle.

## MLflow
- Provides a consistent interface for model lineage, auditing, and reproducibility across distributed environments.
- Tracking Server: aggregates metrics, parameters, and artifacts from federated nodes.
- Model Registry: versions and manages global models, publishing them to downstream consumers.

## Federated learning
- Hub-and-spoke model ensures collaboration without data centralization, supporting compliance with healthcare regulations.
- Federated nodes perform local training and contribute model updates instead of raw data, preserving privacy.
- The orchestrator aggregates these updates, validates models, and distributes improved versions back to nodes.

## GitOps
TODO: UPDATE THIS