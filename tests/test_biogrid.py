"""Unit tests for BioGRID gene-to-gene interaction ingest."""

import pytest
from biolink_model.datamodel.pydanticmodel_v2 import PairwiseGeneToGeneInteraction

from biogrid_util import get_evidence, get_gene_id, get_publication_ids
from transform import transform


@pytest.fixture
def basic_row():
    """An example BioGRID MITAB interaction row."""
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
def basic_entity(basic_row):
    return transform(None, basic_row)


def test_entity_type(basic_entity):
    entity = basic_entity[0]
    assert entity
    assert isinstance(entity, PairwiseGeneToGeneInteraction)


def test_subject(basic_entity):
    entity = basic_entity[0]
    assert entity.subject == "NCBIGene:6416"


def test_object(basic_entity):
    entity = basic_entity[0]
    assert entity.object == "NCBIGene:2318"


def test_predicate(basic_entity):
    entity = basic_entity[0]
    assert entity.predicate == "biolink:interacts_with"


def test_evidence(basic_entity):
    entity = basic_entity[0]
    assert entity.has_evidence == ["ECO:0000024"]


def test_publications(basic_entity):
    entity = basic_entity[0]
    assert "PMID:9006895" in entity.publications
    assert "PMID:10727406" in entity.publications


def test_knowledge_source(basic_entity):
    entity = basic_entity[0]
    assert entity.primary_knowledge_source == "infores:biogrid"
    assert entity.aggregator_knowledge_source == ["infores:monarchinitiative"]


def test_knowledge_level(basic_entity):
    entity = basic_entity[0]
    assert entity.knowledge_level == "knowledge_assertion"
    assert entity.agent_type == "not_provided"


def test_uniprot_interaction():
    """Test that UniProtKB identifiers are also accepted."""
    row = {
        "ID Interactor A": "uniprot/swiss-prot:P45985",
        "ID Interactor B": "entrez gene/locuslink:2318",
        "Interaction Detection Method": 'psi-mi:"MI:0018"(two hybrid)',
        "Publication Identifiers": "pubmed:9006895",
        "Taxid Interactor A": "taxid:9606",
        "Taxid Interactor B": "taxid:9606",
        "Interaction Types": 'psi-mi:"MI:0407"(direct interaction)',
        "Source Database": 'psi-mi:"MI:0463"(biogrid)',
        "Interaction Identifiers": "biogrid:999",
        "Confidence Values": "",
        "Alt IDs Interactor A": "",
        "Alt IDs Interactor B": "",
        "Aliases Interactor A": "",
        "Aliases Interactor B": "",
        "Publication 1st Author": "",
    }
    entities = transform(None, row)
    assert len(entities) == 1
    assert entities[0].subject == "UniProtKB:P45985"


def test_non_ncbi_interaction_filtered():
    """Test that interactions with non-NCBIGene/UniProtKB IDs are filtered out."""
    row = {
        "ID Interactor A": "biogrid:112315",
        "ID Interactor B": "biogrid:108607",
        "Interaction Detection Method": 'psi-mi:"MI:0018"(two hybrid)',
        "Publication Identifiers": "pubmed:9006895",
        "Taxid Interactor A": "taxid:9606",
        "Taxid Interactor B": "taxid:9606",
        "Interaction Types": 'psi-mi:"MI:0407"(direct interaction)',
        "Source Database": 'psi-mi:"MI:0463"(biogrid)',
        "Interaction Identifiers": "biogrid:999",
        "Confidence Values": "",
        "Alt IDs Interactor A": "",
        "Alt IDs Interactor B": "",
        "Aliases Interactor A": "",
        "Aliases Interactor B": "",
        "Publication 1st Author": "",
    }
    entities = transform(None, row)
    assert len(entities) == 0


# Utility function tests


def test_get_gene_id_entrez():
    assert get_gene_id("entrez gene/locuslink:6416") == "NCBIGene:6416"


def test_get_gene_id_uniprot():
    assert get_gene_id("uniprot/swiss-prot:P45985") == "UniProtKB:P45985"


def test_get_gene_id_passthrough():
    assert get_gene_id("biogrid:112315") == "biogrid:112315"


def test_get_evidence_two_hybrid():
    result = get_evidence('psi-mi:"MI:0018"(two hybrid)')
    assert result == ["ECO:0000024"]


def test_get_evidence_multiple_methods():
    result = get_evidence('psi-mi:"MI:0018"(two hybrid)|psi-mi:"MI:0006"(pull down)')
    assert "ECO:0000024" in result
    assert "ECO:0000025" in result


def test_get_evidence_empty():
    assert get_evidence("") is None


def test_get_evidence_unknown_method():
    result = get_evidence('psi-mi:"MI:9999"(unknown method)')
    assert result == ["ECO:0000006"]


def test_get_publication_ids_single():
    assert get_publication_ids("pubmed:9006895") == ["PMID:9006895"]


def test_get_publication_ids_multiple():
    result = get_publication_ids("pubmed:9006895|pubmed:10727406")
    assert "PMID:9006895" in result
    assert "PMID:10727406" in result
    assert len(result) == 2
