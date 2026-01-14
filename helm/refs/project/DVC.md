# DVC

Git is not suitable for large files because it stores every file version in full and lacks built-in deduplication or
content addressing for binary data. If large files are stored in git, the size of the repository will grow rapidly;
which results in git operations becoming inefficient and unreliable as the size and number of files scales.

The solution to this is a tool called **[DVC](https://github.com/iterative/dvc)** (Data Version Control). With DVC,
Git is employed as usual to store and version code (including DVC meta-files as placeholders for data).
DVC stores data and model files seamlessly in a cache outside of Git, while preserving almost the same user experience as if they were in the repo.

To share and back up the data cache, DVC supports multiple remote storage platforms - any cloud (S3, Azure, Google Cloud, etc.)
or on-premise network storage (via SSH, for example). When an asset is materialized it is first stored in the internal minio storage bucket, once the data controller has approve the results
the node pushes it to the publication storage

- DVC stores metadata in Git - small .dvc files describing where large files live.
- The actual data lives in DVC remotes (e.g., MinIO, S3, etc.).
- Multiple DVC remotes can coexist. They are not mirrors automatically; DVC will only push or pull from the one you specify.
- DVC caches file content by content hash (MD5), which ensures data integrity and optimizes storage size requirementsb
- Multiple remotes can also serve as backup of expensive and time consuming experiment results

---

## Example

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
