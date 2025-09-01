---
config:
  layout: elk
  look: classic
  theme: redux-dark
---
flowchart TD
  subgraph GitRepos["Git Repos"]
    NodeRepo("Node Repo")
    CodeRepo("Code Repo")
    AggRepo("Aggregator Repo")
  end

  subgraph FederatedNode["Federated Node (Hospital)"]
    subgraph ArgoPipelines["ArgoCD Pipelines"]
      NodePipeline("Node Pipeline")
      CodePipeline("Code Pipeline")
    end

    subgraph DagsterK8s["Dagster K8s"]
      subgraph DagsterWorkers["Workers"]
        K8sPod1("Pod")
        K8sPod2("Pod")
      end

      subgraph DagsterServices["Services"]
        Daemon("Daemon")
        CodeServer("CodeServer")
        WebServer("WebServer")
      end
    end

    CodeMount("Code Mount")

    subgraph DagsterResources["Resources"]
      ArtifactStorage("Hospital Minio Storage")
      ResultsBackend("Hospital Postgres")
      CeleryBroker("Hospital RabbitMQ")
    end
  end

  subgraph FederatedAggregator["Federated Aggregator"]
    subgraph AggDagster["Dagster K8s"]
      AggWorkers("Workers (Pods)")
      AggDaemon("Daemon")
      AggCodeServer("CodeServer")
      AggWebServer("WebServer")
    end

    subgraph AggResources["Resources"]
      GlobalArtifactStorage("Global Minio Storage")
      GlobalResultsBackend("Global Postgres")
      GlobalBroker("Global RabbitMQ")
    end
  end

  ResultsStorage("Abstract Persistent Storage")

  CodeRepo --> CodePipeline
  NodeRepo --> NodePipeline
  AggRepo --> AggDagster

  NodePipeline --> DagsterK8s
  CodePipeline --> CodeMount
  CodeMount --- CodeServer
  DagsterK8s --- DagsterResources
  ArtifactStorage --> ResultsStorage

  AggDagster --- AggResources
  GlobalArtifactStorage --> ResultsStorage

  DagsterResources --> GlobalArtifactStorage
  GlobalArtifactStorage --> DagsterResources
