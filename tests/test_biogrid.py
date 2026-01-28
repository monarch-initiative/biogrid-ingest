"""Unit tests for BioGRID gene-to-gene interaction ingest."""

import pytest

from biogrid_util import get_evidence, get_gene_id, get_publication_ids


class TestGeneIdParsing:
    """Test gene identifier parsing."""

    def test_entrez_gene_id(self):
        """Test parsing of Entrez gene IDs."""
        raw_id = "entrez gene/locuslink:6416"
        result = get_gene_id(raw_id)
        assert result == "NCBIGene:6416"

    def test_uniprot_id(self):
        """Test parsing of UniProt IDs."""
        raw_id = "uniprot/swiss-prot:P45985"
        result = get_gene_id(raw_id)
        assert result == "UniProtKB:P45985"

    def test_other_id_passthrough(self):
        """Test that unrecognized IDs pass through unchanged."""
        raw_id = "biogrid:112315"
        result = get_gene_id(raw_id)
        assert result == "biogrid:112315"


class TestEvidenceParsing:
    """Test evidence code parsing."""

    def test_two_hybrid_method(self):
        """Test parsing of two hybrid method."""
        methods = 'psi-mi:"MI:0018"(two hybrid)'
        result = get_evidence(methods)
        assert result == ["ECO:0000024"]

    def test_multiple_methods(self):
        """Test parsing of multiple methods."""
        methods = 'psi-mi:"MI:0018"(two hybrid)|psi-mi:"MI:0006"(pull down)'
        result = get_evidence(methods)
        assert "ECO:0000024" in result
        assert "ECO:0000025" in result

    def test_empty_methods(self):
        """Test handling of empty methods."""
        result = get_evidence("")
        assert result is None

    def test_unknown_method_default(self):
        """Test that unknown methods get default code."""
        methods = 'psi-mi:"MI:9999"(unknown method)'
        result = get_evidence(methods)
        assert result == ["ECO:0000006"]  # Default experimental evidence


class TestPublicationParsing:
    """Test publication ID parsing."""

    def test_single_pubmed(self):
        """Test parsing of single PubMed ID."""
        pub_ids = "pubmed:9006895"
        result = get_publication_ids(pub_ids)
        assert result == ["PMID:9006895"]

    def test_multiple_pubmeds(self):
        """Test parsing of multiple PubMed IDs."""
        pub_ids = "pubmed:9006895|pubmed:10727406"
        result = get_publication_ids(pub_ids)
        assert "PMID:9006895" in result
        assert "PMID:10727406" in result
        assert len(result) == 2


class TestIntegration:
    """Integration tests for BioGRID parsing."""

    @pytest.fixture
    def basic_row(self):
        """Generate an example interactions data row."""
        return {
            "ID Interactor A": "entrez gene/locuslink:6416",
            "ID Interactor B": "entrez gene/locuslink:2318",
            "Alt IDs Interactor A": "biogrid:112315|entrez gene/locuslink:MAP2K4|uniprot/swiss-prot:P45985|"
            + "refseq:NP_003001|refseq:NP_001268364",
            "Alt IDs Interactor B": "biogrid:108607|entrez gene/locuslink:FLNC|uniprot/swiss-prot:Q14315|"
            + "refseq:NP_001120959|refseq:NP_001449",
            "Aliases Interactor A": "entrez gene/locuslink:JNKK1(gene name synonym)|"
            + "entrez gene/locuslink:MAPKK4(gene name synonym)|"
            + "entrez gene/locuslink:MEK4(gene name synonym)",
            "Aliases Interactor B": "entrez gene/locuslink:ABP280A(gene name synonym)|"
            + "entrez gene/locuslink:FLN2(gene name synonym)|"
            + "entrez gene/locuslink:MFM5(gene name synonym)|"
            + "entrez gene/locuslink:MPD4(gene name synonym)",
            "Interaction Detection Method": 'psi-mi:"MI:0018"(two hybrid)',
            "Publication 1st Author": "Marti A (1997)",
            "Publication Identifiers": "pubmed:9006895|pubmed:10727406",
            "Taxid Interactor A": "taxid:9606",
            "Taxid Interactor B": "taxid:9606",
            "Interaction Types": 'psi-mi:"MI:0407"(direct interaction)',
            "Source Database": 'psi-mi:"MI:0463"(biogrid)',
            "Interaction Identifiers": "biogrid:103",
            "Confidence Values": "",
        }

    def test_parse_row_gene_ids(self, basic_row):
        """Test parsing gene IDs from a full row."""
        gid_a = get_gene_id(basic_row["ID Interactor A"])
        gid_b = get_gene_id(basic_row["ID Interactor B"])
        assert gid_a == "NCBIGene:6416"
        assert gid_b == "NCBIGene:2318"

    def test_parse_row_evidence(self, basic_row):
        """Test parsing evidence from a full row."""
        evidence = get_evidence(basic_row["Interaction Detection Method"])
        assert len(evidence) == 1
        assert "ECO:0000024" in evidence

    def test_parse_row_publications(self, basic_row):
        """Test parsing publications from a full row."""
        publications = get_publication_ids(basic_row["Publication Identifiers"])
        assert "PMID:9006895" in publications
        assert "PMID:10727406" in publications
