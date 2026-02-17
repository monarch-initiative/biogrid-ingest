# BioGRID

[BioGRID](https://thebiogrid.org/) is a database of Protein, Genetic and Chemical Interactions, a biomedical interaction repository with data compiled through comprehensive curation efforts. The current index searches thousands of publications extracting millions of protein and genetic interactions, thousands of chemical interactions and over a million post translational modifications from major model organism species.

## Source Data

This ingest uses the [Bulk BioGRID MITAB data file](https://downloads.thebiogrid.org/File/BioGRID/Release-Archive/BIOGRID-4.4.226/BIOGRID-ALL-4.4.226.mitab.zip). The PSI-MITAB format columns (defined [here](https://wiki.thebiogrid.org/doku.php/psi_mitab_file)) are:

1. ID Interactor A
2. ID Interactor B
3. Alt IDs Interactor A
4. Alt IDs Interactor B
5. Aliases Interactor A
6. Aliases Interactor B
7. Interaction Detection Method
8. Publication 1st Author
9. Publication Identifiers
10. Taxid Interactor A
11. Taxid Interactor B
12. Interaction Types
13. Source Database
14. Interaction Identifiers
15. Confidence Values

This ingest uses columns 1, 2, 7 and 9 to generate its output.

### Filtering

Only interactions where both interactor IDs can be resolved to NCBIGene or UniProtKB identifiers are included. Rows with other identifier types (e.g. BioGRID internal IDs) are filtered out.

## Biolink Captured

### **[biolink:PairwiseGeneToGeneInteraction](https://biolink.github.io/biolink-model/PairwiseGeneToGeneInteraction/)**

| Property | Value | Notes |
| -------- | ----- | ----- |
| id | UUID | |
| subject | CURIE | Genes captured from [NCBI](https://bioregistry.io/registry/ncbigene) or [UniProt](https://bioregistry.io/registry/uniprot). |
| predicate | [`interacts_with`](https://biolink.github.io/biolink-model/interacts_with/) | |
| object | CURIE | See `subject`. |
| has_evidence | CURIE list | ECO codes derived from the `Interaction Detection Method` column. |
| publications | CURIE list | PMIDs derived from the `Publication Identifiers` column. |
| primary_knowledge_source | `infores:biogrid` | |
| aggregator_knowledge_source | `infores:monarchinitiative` | |
| knowledge_level | `knowledge_assertion` | |
| agent_type | `not_provided` | |

### Evidence Code Mapping

Interaction detection methods from the PSI-MI ontology are mapped to ECO evidence codes:

| Detection Method | ECO Code | ECO Label |
| ---------------- | -------- | --------- |
| two hybrid | ECO:0000024 | yeast 2-hybrid evidence |
| affinity chromatography technology | ECO:0000079 | affinity chromatography evidence |
| genetic interference | ECO:0000011 | genetic interaction evidence |
| pull down | ECO:0000025 | co-purification evidence |
| enzymatic study | ECO:0000005 | enzyme assay evidence |
| x-ray crystallography | ECO:0001823 | x-ray crystallography evidence |
| far western blotting | ECO:0000076 | far western blot evidence |
| fluorescent resonance energy transfer | ECO:0001048 | FRET evidence |
| imaging technique | ECO:0000324 | imaging assay evidence |
| protein complementation assay | ECO:0006256 | protein complementation assay evidence |
| biochemical | ECO:0000172 | biochemical trait evidence |

Unknown methods default to ECO:0000006 (experimental evidence).

### Design Decisions

- **ID normalization**: `entrez gene/locuslink:` prefixes are mapped to `NCBIGene:` CURIEs; `uniprot/swiss-prot:` to `UniProtKB:`. All other identifier types are passed through but interactions with unrecognized ID types are filtered out.
- **Evidence mapping**: Several mappings are approximate (pull down, imaging technique, protein complementation assay, biochemical) since the PSI-MI detection methods don't map 1:1 to ECO codes.
- **Publication parsing**: Only PubMed IDs (`pubmed:` prefix) are captured from the Publication Identifiers column.

## Citation

### Most Recent

Oughtred R, Rust J, Chang C, Breitkreutz BJ, Stark C, Willems A, Boucher L, Leung G, Kolas N, Zhang F, Dolma S, Coulombe-Huntington J, Chatr-Aryamontri A, Dolinski K, Tyers M. **The BioGRID database: A comprehensive biomedical resource of curated protein, genetic, and chemical interactions.** [_Protein Sci. 2020 Oct 18_](https://doi.org/10.1002/pro.3978). [PMID:33070389](https://pubmed.ncbi.nlm.nih.gov/33070389/)

### Original

Stark C, Breitkreutz BJ, Reguly T, Boucher L, Breitkreutz A, Tyers M. **Biogrid: A General Repository for Interaction Datasets.** _Nucleic Acids Res. Jan 1, 2006; 34:D535-9_; [PMID:16381927](http://www.ncbi.nlm.nih.gov/pubmed/16381927).

## License

BSD-3-Clause
