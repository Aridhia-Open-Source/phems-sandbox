# GitHub

- Researcher raises PR with experiment run parameters
- Data Controller accepts PR
- Node detects newly merged PR
- Node triggers a new experiment run
- Experiment run completes -> Comment added to PR
- Run Failed? -> Retry
- Run Success? -> Deliver Results
- Node pushes results back to github and raises PR
- Data Controller reviews PR and merges results


→ Researcher raises a pull request to run the experiement
→ Data Controller reviews and merges pull request
→ Federated Node detects approved pull request
→ Federated Node executes the experiment code
→ Results collected and attached to request
→ Federated node collects results and pushes them to GitHub
→ Data Controller reviews and merges results