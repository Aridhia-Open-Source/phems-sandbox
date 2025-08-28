
1) Researcher raises a pull request to the `code repo` with their new asset definition

2) Pull request is approved and merged into the deployment branch

3) ArgoCD detects the changes to the deployment branch, then applies it to the codeserver

4) Researcher raises a second pull request to launch a parameterized run of their asset job

5) ArgoCD detects the change to the deployment branch, then submits the job through the dagster webserver API

---

6) Dagster webserver creates a run worker kubernetes job which persists untill timeout or completion

7) Run worker job traverses the execution plan and submits each step to the celery queues

8) Celery worker pools pick up the execution steps from the queue, with each step spawning a new kubernetes job

9) The final step publishes the job results locally for review before publication

10) Run worker job handles the completed execution steps and any post-run events

---

11) Data controller is notified of the pending publication approval for the asset

12) Data controller approves the publication of the asset

13) Dagster publication sensor is triggered via webhook upon approval

14) Dagster publication sensor launches the publication job for the asset

14) The approved asset is published externally (i.e git, s3, sftp)

15) Researcher notified when the approved asset is successfully published
