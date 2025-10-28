# PHEMS POC E2E

## Repositories

### Code Repo

Defines the **computational logic** for each code location within a node, along with their execution environment and dependencies. \
i.e. Dagster definitions, Celery config, Dockerfiles, Python requirements, external code, etc.

Multiple directories, which are deployed as isolated execution environments (code locations).
1) **Researcher** raises the PR to create or update a code location.
2) **GitHub Actions** executes CI pipline (lint, build, test).
3) **Data Controller** review and merges the PR's to deploy the code locations(s).
4) **ArgoCD** deploys the individual code location(s) (CodeServer + Worker Pools) to the node.

---

### Node Repo

Defines the **shared infrastructure**, such as resources, services, and configuration for a node deployment.  \
Examples: Helm charts, ArgoCD manifests, Dagster definitions, Celery configuration, and environment settings. \
Single directory for the core (shared) code location which is deployed as an isolated execution environment (code location).

**Services**: WebServer, Daemon, MLflow, (CodeServer + Worker Pool) \
**Resources**: Postgres, RabbitMQ, MinIO

1) **Contributor** raises the PR to update the node
2) **GitHub Actions** executes CI pipline (lint, build, test).
3) **Maintainer** reviews and merges the PR's to authorize a new node deployment
4) **ArgoCD** deploys the services, resources, and shared code location (CodeServer + Worker Pool) to the node.


---

### Ctrl Repo

Provides governance for the node through a git control plane, which allows a data controller to implement approval gates. \
These approval gates take the form of PR, which are used to both approve job requests and publish their results.

Provides **governance and orchestration** for the node through a Git-based control plane. \
Enabling a **Data Controller** to manage approval workflows using PR as gates to both **initiate jobs** and **record their results**.

Submit Job:
1) **Researcher** raises a PR to submit job requests.
2) **Data Controller** reviews & merges PR's to authorize job execution
3) **Node** polls for merges to `main` and triggers the corresponding job run

Publish Result:
1) **Node** stores the job result in **internal storage** (minio)
2) **Node** raises the pull request with the a commit containing the **DVC** metadata
4) **Data Controller** reviews and merges the PR to authorize the job result publication
5) **Node** publishes result to **publication storage** using **DVC** push/pull against the results directory
6) **Researche** securely pulls the results from the **publication storage** using familiar **GIT** + **DVC** cli tools


## DVC

Git is not suitable for large files because it stores every file version in full and lacks built-in deduplication or
content addressing for binary data. If large files are stored in git, the size of the repository will grow rapidly;
which results in git operations becoming inefficient and unreliable as the size and number of files scales.

The solution to this is a tool called **[DVC](https://github.com/iterative/dvc)** (Data Version Control). With DVC,
Git is employed as usual to store and version code (including DVC meta-files as placeholders for data).
DVC stores data and model files seamlessly in a cache outside of Git, while preserving almost the same user experience as if they were in the repo.

To share and back up the data cache, DVC supports multiple remote storage platforms - any cloud (S3, Azure, Google Cloud, etc.)
or on-premise network storage (via SSH, for example). When an asset is materialized it is first stored in the internal minio storage bucket, once the data controller has approve the results a new commit is made to transfer the asset to the 'public' storage

- DVC stores metadata in Git - small .dvc files describing where large files live.
- The actual data lives in DVC remotes (e.g., MinIO, S3, etc.).
- Multiple DVC remotes can coexist. They are not mirrors automatically; DVC will only push or pull from the one you specify.
- DVC caches file content by content hash (MD5), which ensures integrity and allows automatic deduplication across remotes.
- Multiple remotes can also serve as backup of expensive and time consuming experiment results

---

### DVC Example

1. **Node-side storage**

    Dagster materialization writes a specific asset (e.g., `outputs/model.pkl`) to **MinIO**. \
    DVC tracks this asset and pushes it to the `minio` remote:
    ```bash
    dvc add outputs/model.pkl
    dvc push -r minio outputs/model.pkl.dvc
    ```

2. **Publication via Ctrl Repo or orchestrator**

    Once approved (via PR), the orchestrator or CI process, transfers only the specified asset from local MinIO to external S3.
    ```bash
    dvc pull -r minio outputs/model.pkl.dvc
    dvc push -r s3-pub outputs/model.pkl.dvc
    ```

3. **Result**

    The targeted DVC-tracked artifact now exists in **both MinIO and S3**, \
    maintaining consistent version hashes and provenance while avoiding unnecessary transfers.


## Notes
- [Better support for transferring a large number of files already in the cloud into DVC](https://github.com/iterative/dvc/issues/10712)
