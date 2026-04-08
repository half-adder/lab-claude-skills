<overview>
Cluster-specific SLURM configuration. All values use placeholders from `cluster-config.toml`. Read that file first and substitute the actual values.
</overview>

<gpu_partitions>

Partition names and GPU types vary by cluster. Common configurations:

| Partition | GPU | VRAM | Notes |
|-----------|-----|------|-------|
| a100-gpu | NVIDIA A100 | 40GB or 80GB | Best for large models |
| l40-gpu | NVIDIA L40/L40S | 48GB | Good general purpose |

Check your cluster docs for available partitions. Configure in `cluster-config.toml`.

All GPU jobs require QoS and gres flags:
```
#SBATCH --qos={gpu.qos}
#SBATCH --gres=gpu:1
```

</gpu_partitions>

<slurm_gpu_template>

```bash
#!/bin/bash

#SBATCH -J <job-name>
#SBATCH -n 1
#SBATCH --cpus-per-task={gpu.default_cpus}
#SBATCH --mem={gpu.default_mem}
#SBATCH -t {gpu.default_time}
#SBATCH -p {gpu.partitions}
#SBATCH --qos={gpu.qos}
#SBATCH --gres=gpu:1
#SBATCH --mail-type=begin,end,fail
#SBATCH --mail-user={email.address}
#SBATCH -o logs/<name>_%j.out
#SBATCH -e logs/<name>_%j.err

mkdir -p logs
module purge

cd {paths.scratch}<project>

# Load modules here:
# module load <name>/<version>

# For Python/uv:
# export PATH="$HOME/.local/bin:$PATH"
# uv run python <script>.py

# For R:
# module load r/4.5.0
# Rscript <script>.R

# For CLI tools:
# module load samtools/1.23.1
# samtools <command>
```

</slurm_gpu_template>

<slurm_cpu_template>

```bash
#!/bin/bash

#SBATCH -J <job-name>
#SBATCH -n 1
#SBATCH --cpus-per-task={cpu.default_cpus}
#SBATCH --mem={cpu.default_mem}
#SBATCH -t {cpu.default_time}
#SBATCH --mail-type=begin,end,fail
#SBATCH --mail-user={email.address}
#SBATCH -o logs/<name>_%j.out
#SBATCH -e logs/<name>_%j.err

mkdir -p logs
module purge

cd {paths.scratch}<project>

# Load modules here:
# module load <name>/<version>
```

</slurm_cpu_template>

<slurm_nextflow_template>

Nextflow is a head job that submits its own SLURM worker jobs. Request minimal resources.

```bash
#!/bin/bash

#SBATCH -J <pipeline-name>
#SBATCH -n 1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8g
#SBATCH -t 48:00:00
#SBATCH --mail-type=begin,end,fail
#SBATCH --mail-user={email.address}
#SBATCH -o logs/<name>_%j.out
#SBATCH -e logs/<name>_%j.err

mkdir -p logs
module purge
module load nextflow/25.04.7

cd {paths.scratch}<project>

nextflow run <pipeline> \
    -profile singularity \
    --input samplesheet.csv \
    --outdir results/ \
    -work-dir {paths.scratch}<project>/work
```

</slurm_nextflow_template>

<resource_guidelines>

**GPU jobs (deep learning, image analysis):**
- CPUs: 8-12 (match GPU node topology)
- Memory: 20-32GB (more if loading large datasets into RAM)
- Time: estimate based on epochs/data, add 50% buffer
- GPU: 1 (multi-GPU rarely needed for microscopy)

**CPU jobs (alignment, peak calling, analysis):**
- CPUs: 4-8 (unless embarrassingly parallel)
- Memory: 8-32GB depending on data size
- Time: generous, CPU jobs queue faster

**Nextflow head jobs:**
- CPUs: 2
- Memory: 8GB
- Time: 24-48h (long-running, but low resource)
- Nextflow manages its own worker resource requests

</resource_guidelines>

<interactive_sessions>

```bash
# CPU interactive
srun -t 2:00:00 -p {interactive.partition} -n 1 --cpus-per-task=1 --mem=8g --pty /bin/bash

# GPU interactive
srun -t 2:00:00 -p {gpu.partitions} -n 1 --cpus-per-task=4 --mem=16g --qos={gpu.qos} --gres=gpu:1 --pty /bin/bash
```

</interactive_sessions>

<module_tips>

```bash
# List all available modules
module avail 2>&1

# Search for a specific tool
module avail samtools 2>&1

# Show module details (dependencies, paths)
module show samtools/1.23.1

# List currently loaded modules
module list

# Unload everything
module purge
```

Always pin module versions in SLURM scripts for reproducibility. The `(D)` marker in `module avail` output indicates the default version, which may change over time.

</module_tips>
