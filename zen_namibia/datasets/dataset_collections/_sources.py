from __future__ import annotations

from zen_creator import DatasetCollection
from zen_creator.datasets.datasets.metadata import MetadataTree, SourceInformation


def cite(collection: DatasetCollection, description: str, *keys: str) -> SourceInformation:
    """Source information citing only the listed entries of a collection, so an
    attribute's sources.md lists the sources it actually uses."""
    metadata: dict[str, MetadataTree] = {
        key: collection.data[key].metadata for key in (keys or collection.data)
    }
    return SourceInformation(description=description, metadata=metadata)
