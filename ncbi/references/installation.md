<overview>
Installation methods for NCBI datasets and dataformat CLI tools.
</overview>

<conda>
**Conda (recommended, installs both tools):**
```bash
conda install -c conda-forge ncbi-datasets-cli
```

Or in a dedicated environment:
```bash
conda create -n ncbi_datasets -c conda-forge ncbi-datasets-cli
conda activate ncbi_datasets
```
</conda>

<direct_download>
**macOS (Intel or Apple Silicon):**
```bash
curl -o datasets 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/mac/datasets'
curl -o dataformat 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/mac/dataformat'
chmod +x datasets dataformat
sudo mv datasets dataformat /usr/local/bin/
```

**Linux (AMD64):**
```bash
curl -o datasets 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/linux-amd64/datasets'
curl -o dataformat 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/linux-amd64/dataformat'
chmod +x datasets dataformat
sudo mv datasets dataformat /usr/local/bin/
```

**Linux (ARM64):**
```bash
curl -o datasets 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/linux-arm64/datasets'
curl -o dataformat 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/linux-arm64/dataformat'
chmod +x datasets dataformat
```
</direct_download>

<shell_completion>
After installation, enable shell autocompletion:
```bash
# For zsh (add to ~/.zshrc)
eval "$(datasets completion zsh)"
eval "$(dataformat completion zsh)"

# For bash (add to ~/.bashrc)
eval "$(datasets completion bash)"
eval "$(dataformat completion bash)"
```
</shell_completion>

<api_key>
Optional but recommended for heavy usage. Get an API key at:
https://www.ncbi.nlm.nih.gov/datasets/docs/v2/api/api-keys/

Set via environment variable or flag:
```bash
export NCBI_API_KEY='your-key-here'
# or
datasets summary genome taxon 'Drosophila' --api-key 'your-key-here'
```
</api_key>
