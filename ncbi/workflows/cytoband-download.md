# Workflow: Download by Cytological Band (Drosophila)

<required_reading>
**Read these reference files NOW:**
1. references/dmel-cytobands.tsv (look up the band the user requests)
2. references/commands.md (for download flags)
</required_reading>

<process>

**Step 1: Look up cytological band coordinates**

Two reference tables are available, both with columns: `band`, `chromosome`, `start`, `stop`.

1. **`references/dmel-cytobands-subdivisions.tsv`** (4,007 entries) -- individual polytene bands (e.g., 68C13, 89E1)
2. **`references/dmel-cytobands.tsv`** (593 entries) -- letter-level divisions (e.g., 68C, 89E)

**Lookup order:** Try the subdivision table first. If no match, fall back to the letter-level table.

Bands can be specified as:
- Subdivision: `68C13` → one row from subdivisions table
- Letter band: `89E` → one row from letter-level table (or multiple rows from subdivisions table)
- Band range: `89E-89F` → multiple rows, use min(start) to max(stop)
- Division: `89` → all bands starting with `89` (89A through 89F)

Show the user the coordinates you found:
```
Band 89E: 3R:12,622,873..12,765,162 (142 kb)
```

**Step 2: Check cache for chromosome GenBank file**

Cache directory: `~/.cache/ncbi-datasets/gbff/`

Check if the chromosome's GBFF is already cached:
```bash
CACHE_DIR="$HOME/.cache/ncbi-datasets/gbff"
CHROM="3L"  # from step 1
GBFF="$CACHE_DIR/dmel_${CHROM}.gbff"

if [ -f "$GBFF" ]; then
    echo "Using cached $GBFF"
else
    echo "Not cached, downloading..."
fi
```

**Step 3: Download if not cached**

Only download if the chromosome GBFF is not in the cache:
```bash
CACHE_DIR="$HOME/.cache/ncbi-datasets/gbff"
mkdir -p "$CACHE_DIR"
CHROM="3L"

datasets download genome taxon 'Drosophila melanogaster' --reference \
  --include gbff --chromosomes "$CHROM" \
  --filename "/tmp/dmel_${CHROM}.zip"

unzip -o "/tmp/dmel_${CHROM}.zip" -d "/tmp/dmel_${CHROM}"

# Cache the extracted GBFF
cp "/tmp/dmel_${CHROM}/ncbi_dataset/data/GCF_000001215.4/genomic.gbff" \
   "$CACHE_DIR/dmel_${CHROM}.gbff"

# Clean up temp files
rm -rf "/tmp/dmel_${CHROM}.zip" "/tmp/dmel_${CHROM}"
```

**Step 4: Extract the specific region**

Use BioPython to extract the cytoband region from the (cached) GenBank file:
```bash
CACHE_DIR="$HOME/.cache/ncbi-datasets/gbff"
CHROM="3L"
BAND="68C"
START=11254921
STOP=11627770

uv run --with biopython python3 -c "
from Bio import SeqIO

chrom, band = '${CHROM}', '${BAND}'
start, stop = ${START}, ${STOP}
gbff = '${CACHE_DIR}/dmel_${CHROM}.gbff'

for rec in SeqIO.parse(gbff, 'genbank'):
    if chrom in rec.description:
        sub = rec[start-1:stop]
        sub.id = f'{chrom}_{band}_{start}_{stop}'
        sub.description = f'Drosophila melanogaster cytological band {band} ({chrom}:{start}..{stop})'
        outfile = f'dmel_{band}.gb'
        SeqIO.write(sub, outfile, 'genbank')
        print(f'Wrote {outfile} ({len(sub)} bp, {len(sub.features)} features)')
        break
"
```

Output file is written to the current working directory. Move it where the user wants.

**Alternative: Use FlyBase API for sequence only (no download needed)**

If the user just needs the sequence (not the full GenBank annotations):
```bash
curl -s "https://api.flybase.org/api/v1.0/sequence/region/dmel/3R:12622873..12765162" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d['resultset']['result'][0]['sequence'])" \
  > band_89E.fa
```

**Step 5: Verify**

Confirm the output file contains the expected region and features.

</process>

<cache_management>
The cache stores one GBFF file per chromosome arm (~50-200 MB each). Drosophila has 6 major arms (X, 2L, 2R, 3L, 3R, 4), so a full cache is ~600 MB.

To clear the cache:
```bash
rm -rf ~/.cache/ncbi-datasets/gbff/
```

To list cached chromosomes:
```bash
ls -lh ~/.cache/ncbi-datasets/gbff/
```
</cache_management>

<success_criteria>
This workflow is complete when:
- [ ] Cytological band mapped to genomic coordinates via dmel-cytobands.tsv
- [ ] Chromosome GBFF cached (downloaded only if not already present)
- [ ] Region extracted with correct coordinates
- [ ] Output file contains expected content
</success_criteria>
