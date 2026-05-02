"""Upstream source version fetcher for biogrid-ingest.

BioGRID URLs encode the release version in their path (e.g. `BIOGRID-4.4.226`).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from kozahub_metadata_schema import (
    now_iso,
    urls_from_download_yaml,
    version_from_url_path,
)


INGEST_DIR = Path(__file__).resolve().parents[1]
DOWNLOAD_YAML = INGEST_DIR / "download.yaml"


def get_source_versions() -> list[dict[str, Any]]:
    urls = urls_from_download_yaml(DOWNLOAD_YAML)
    version, method = version_from_url_path(
        urls[0] if urls else "", r"/BIOGRID-(\d+\.\d+\.\d+)/"
    )
    return [
        {
            "id": "infores:biogrid",
            "name": "BioGRID — Gene/Protein Interactions",
            "urls": urls,
            "version": version,
            "version_method": method,
            "retrieved_at": now_iso(),
        }
    ]
