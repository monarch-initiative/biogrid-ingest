import uuid

import koza
from biolink_model.datamodel.pydanticmodel_v2 import AgentTypeEnum, KnowledgeLevelEnum, PairwiseGeneToGeneInteraction

from src.biogrid_util import get_evidence, get_gene_id, get_publication_ids


@koza.transform_record()
def transform(koza, row: dict) -> PairwiseGeneToGeneInteraction | None:
    gid_a = get_gene_id(row["ID Interactor A"])
    gid_b = get_gene_id(row["ID Interactor B"])

    evidence = get_evidence(row["Interaction Detection Method"])

    publications = get_publication_ids(row["Publication Identifiers"])

    # Only keep interactions using NCBIGene or UniProtKB identifiers, could also filter on taxid
    if (
        gid_a.startswith("NCBIGene:")
        or gid_a.startswith("UniProtKB:")
        and gid_b.startswith("NCBIGene:")
        or gid_b.startswith("UniProtKB:")
    ):
        association = PairwiseGeneToGeneInteraction(
            id="uuid:" + str(uuid.uuid1()),
            subject=gid_a,
            predicate="biolink:interacts_with",
            object=gid_b,
            has_evidence=evidence,
            publications=publications,
            primary_knowledge_source="infores:biogrid",
            aggregator_knowledge_source=["infores:monarchinitiative"],
            knowledge_level=KnowledgeLevelEnum.knowledge_assertion,
            agent_type=AgentTypeEnum.not_provided,
        )

        return [association]

    return []
