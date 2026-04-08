<required_reading>
**Read this file NOW:**
1. `cluster-config.toml` (for user's cluster settings)
</required_reading>

<process>

**Monitoring a running job:**

```bash
# Job status
ssh {ssh.host} 'squeue -j <JOB_ID>'

# All your jobs
ssh {ssh.host} 'squeue -u {ssh.user}'

# Watch status
ssh {ssh.host} 'watch -n 30 squeue -j <JOB_ID>'

# Tail logs (stderr usually has progress)
ssh {ssh.host} 'tail -50 {paths.scratch}<project>/logs/<job>_<JOB_ID>.err'

# Follow logs in real time
ssh {ssh.host} 'tail -f {paths.scratch}<project>/logs/<job>_<JOB_ID>.err'
```

**Cancel and resubmit:**

If scripts were updated locally, rsync first:
```bash
rsync -avz <local-project>/ {ssh.host}:{paths.scratch}<project>/
ssh {ssh.host} 'scancel <JOB_ID> && cd {paths.scratch}<project> && sbatch <job>.sl'
```

**Retrieve results:**

```bash
rsync -avz --progress {ssh.host}:{paths.scratch}<project>/output/ <local-destination>/
```

**Check completed job info:**

```bash
ssh {ssh.host} 'sacct -j <JOB_ID> --format=JobID,JobName,State,Elapsed,MaxRSS,MaxVMSize,ExitCode'
```

**Common issues:**
- Job stuck in `PD` with `(Resources)` -- normal, waiting for a node
- Job stuck in `PD` with `(QOSMaxJobsPerUserLimit)` -- too many queued jobs, wait or cancel others
- Job failed immediately -- check `.err` log, usually import error, missing file, or wrong module version
- OOM kill (exit code 137) -- increase `--mem` in SLURM script
- Timeout (exit code 140) -- increase `-t` walltime
- Module not found -- check `module avail <name> 2>&1` for exact name/version

</process>

<success_criteria>
This workflow is complete when:
- [ ] User's request (monitor/cancel/retrieve/resubmit) is fulfilled
- [ ] Relevant status or output shown to user
</success_criteria>
