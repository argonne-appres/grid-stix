"""
Relationship indicating multi-unit facilities containing multiple generation assets.

This class was automatically generated from the Grid-STIX ontology.

Namespace: http://www.anl.gov/sss/grid-stix-2.1-relationships.owl

"""

from __future__ import annotations

from typing import Optional, Any, List, Dict
from collections import OrderedDict

from stix2.properties import (  # type: ignore[import-untyped]
    StringProperty,
    IntegerProperty,
    BooleanProperty,
    FloatProperty,
    ListProperty,
    DictionaryProperty,
    TimestampProperty,
    IDProperty,
    TypeProperty,
)
from stix2.utils import NOW  # type: ignore[import-untyped]

# External imports

from ..base import GridSTIXRelationshipObject


from ..base import GridReferenceProperty


class ContainedInFacilityRelationship(GridSTIXRelationshipObject):
    """
    Relationship indicating multi-unit facilities containing multiple generation assets.

    """

    # STIX type identifier for this Grid-STIX object
    _type = "x-grid-contained-in-facility-relationship"

    # STIX 2.1 forbids relationship endpoints from being SROs, Bundles,
    # Language Content, or Marking Definitions (mirrors stix2.v21.sro.Relationship)
    _invalid_source_target_types = [
        "bundle",
        "language-content",
        "marking-definition",
        "relationship",
        "sighting",
    ]

    # STIX properties definition following official STIX patterns
    _properties = OrderedDict(
        [
            ("type", TypeProperty(_type, spec_version="2.1")),
            ("spec_version", StringProperty(fixed="2.1")),
            ("id", IDProperty(_type, spec_version="2.1")),
            (
                "created",
                TimestampProperty(
                    default=lambda: NOW,
                    precision="millisecond",
                    precision_constraint="min",
                ),
            ),
            (
                "modified",
                TimestampProperty(
                    default=lambda: NOW,
                    precision="millisecond",
                    precision_constraint="min",
                ),
            ),
            ("name", StringProperty()),
            ("description", StringProperty()),
            # Grid-STIX base properties
            ("x_grid_context", DictionaryProperty()),
            ("x_operational_status", StringProperty()),
            ("x_compliance_framework", ListProperty(StringProperty)),
            ("x_grid_component_type", StringProperty()),
            ("x_criticality_level", IntegerProperty()),
            # References the SDO/SCO endpoints of this relationship; STIX 2.1 requires
            # these to be validated STIX identifiers, not arbitrary strings
            (
                "x_source_ref",
                GridReferenceProperty(
                    spec_version="2.1",
                    invalid_types=_invalid_source_target_types,
                    required=True,
                ),
            ),
            (
                "x_target_ref",
                GridReferenceProperty(
                    spec_version="2.1",
                    invalid_types=_invalid_source_target_types,
                    required=True,
                ),
            ),
            ("x_relationship_type", StringProperty(required=True)),
        ]
    )

    def __init__(self, **kwargs: Any) -> None:
        """Initialize ContainedInFacilityRelationship with Grid-STIX properties."""
        # Set STIX type if not provided
        if "type" not in kwargs:
            kwargs["type"] = self._type

        # Generate deterministic ID if not provided
        if "id" not in kwargs:
            from ..base import DeterministicUUIDGenerator

            # Generate deterministic UUID - will raise ValueError if required properties missing
            kwargs["id"] = DeterministicUUIDGenerator.generate_uuid(self._type, kwargs)

        super().__init__(**kwargs)
