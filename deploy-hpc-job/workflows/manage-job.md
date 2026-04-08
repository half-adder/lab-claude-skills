<required_reading>
**Read this file NOW:**
1. `cluster-config.toml` (for user's cluster settings)
</required_reading>

<process>

**Monitoring a running job:**

```bash
# Job status
ssh {ssh.host} 'squeue -j <JOB_ID>'

# Watch status (from cluster shell)
watch -n 30 squeue -j <JOB_ID>

# Tail logs (stderr usually has progress for PyTorch jobs)
ssh {ssh.host} 'tail -50 {paths.scratch}<project>/logs/<job>_<JOB_ID>.err'
```

**Cancel and resubmit:**

If scripts were updated locally, rsync first:
```bash
rsync -avz {paths.local_code}/<project>/ {ssh.host}:{paths.scratch}<project>/
ssh {ssh.host} 'scancel <JOB_ID> && cd {paths.scratch}<project> && sbatch <job>.sl'
```

**Retrieve results:**

```bash
rsync -avz --progress {ssh.host}:{paths.scratch}<project>/output/ ~/Desktop/<local-destination>/
```

**Check completed job info:**

```bash
ssh {ssh.host} 'sacct -j <JOB_ID> --format=JobID,JobName,State,Elapsed,MaxRSS,MaxVMSize'
```

**Common issues:**
- Job stuck in `PD` with `(Resources)` -- normal, waiting for node
- Job stuck in `PD` with `(QOSMaxJobsPerUserLimit)` -- too many queued jobs, wait or cancel others
- Job failed immediately -- check `.err` log, usually import error or missing file
- OOM kill -- increase `--mem` in SLURM script

</process>

<success_criteria>
This workflow is complete when:
- [ ] User's request (monitor/cancel/retrieve/resubmit) is fulfilled
- [ ] Relevant status or output shown to user
</success_criteria>
