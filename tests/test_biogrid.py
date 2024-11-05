"""Unit tests for BioGRID protein links ingest."""

import pytest
from koza.utils.testing_utils import mock_koza  # noqa: F401


@pytest.fixture
def source_name():
    """Name of BioGRID protein links ingest."""
    return "biogrid"


@pytest.fixture
def script():
    """Path to BioGRID protein links ingest script."""
    return "./src/biogrid_ingest/transform.py"


@pytest.fixture
def basic_row():
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


@pytest.fixture
def basic_pl(mock_koza, source_name, basic_row, script):
    """Create a mock Koza instance using pytest fixtures."""
    return mock_koza(name=source_name, data=basic_row, transform_code=script)


def test_association(basic_pl):
    association = basic_pl[0]
    assert association
    assert association.subject == "NCBIGene:6416"
    assert association.object == "NCBIGene:2318"
    assert association.predicate == "biolink:interacts_with"
    assert "PMID:9006895" in association.publications
    assert "PMID:10727406" in association.publications
    assert len(association.has_evidence) == 1
    assert "ECO:0000024" in association.has_evidence
    assert association.primary_knowledge_source == "infores:biogrid"
    assert "infores:monarchinitiative" in association.aggregator_knowledge_source
