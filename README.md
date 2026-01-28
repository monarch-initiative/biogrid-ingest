# biogrid-ingest

BioGRID ingest for gene-to-gene interactions using MITAB format data.

## Requirements

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [just](https://github.com/casey/just#installation)

## Installation

```bash
cd biogrid-ingest
just install
```

## Usage

To see available commands:

```bash
just
```

### Download and Transform

Run the full pipeline (download + transform):

```bash
just run
```

Or run individual steps:

```bash
just download    # Download BioGRID MITAB data
just transform-all  # Run all transforms
```

### Testing

To run the test suite:

```bash
just test
```

## Data Source

This ingest processes [BioGRID](https://thebiogrid.org/) interaction data in MITAB format,
creating gene-to-gene interaction edges with evidence codes derived from interaction
detection methods.

---

> This project uses the [monarch-initiative/cookiecutter-monarch-ingest](https://github.com/monarch-initiative/cookiecutter-monarch-ingest) template.
