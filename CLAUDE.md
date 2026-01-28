# biogrid-ingest

This is a Koza ingest repository for transforming BioGRID interaction data into Biolink model format.

## Project Structure

- `download.yaml` - Configuration for downloading BioGRID MITAB data
- `src/` - Transform code and configuration
  - `transform.py` / `transform.yaml` - Main transform for gene-to-gene interactions
  - `biogrid_util.py` - Utility functions for parsing BioGRID fields
- `tests/` - Unit tests for transforms
- `output/` - Generated nodes and edges (gitignored)
- `data/` - Downloaded source data (gitignored)

## Key Commands

- `just run` - Full pipeline (download -> transform)
- `just download` - Download BioGRID MITAB data
- `just transform-all` - Run all transforms
- `just test` - Run tests

## Data Source

BioGRID provides protein and genetic interaction data in MITAB format. The ingest
creates PairwiseGeneToGeneInteraction edges with evidence codes mapped from
interaction detection methods.
