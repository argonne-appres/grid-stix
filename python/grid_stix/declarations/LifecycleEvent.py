"""
A typed transition signal extracted from a single piece of independently observed evidence, comparable against a Declaration. Domain-agnostic, like declaration/discrepancy: the same shape (a dated, typed, evidence-bound claim about a state transition) applies beyond reactor lifecycle status.

This class was automatically generated from the Grid-STIX ontology.

Namespace: http://www.anl.gov/sss/grid-stix-2.1-declarations.owl

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

from ..base import GridSTIXObservableObject

from ..vocab import LifecycleEventTypeOv

from ..assets import PhysicalAsset


class LifecycleEvent(GridSTIXObservableObject):
    """
    A typed transition signal extracted from a single piece of independently observed evidence, comparable against a Declaration. Domain-agnostic, like declaration/discrepancy: the same shape (a dated, typed, evidence-bound claim about a state transition) applies beyond reactor lifecycle status.

    """

    # STIX type identifier for this Grid-STIX object
    _type = "x-grid-lifecycle-event"

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
            ("x_event_entity_ref", ListProperty(StringProperty())),
            ("x_event_evidence_ref", ListProperty(StringProperty())),
            ("x_event_type", ListProperty(StringProperty())),
            ("x_event_implied_state", ListProperty(StringProperty())),
            ("x_plant_match_score", ListProperty(FloatProperty())),
            ("x_unit_bound", ListProperty(BooleanProperty())),
        ]
    )

    def __init__(self, **kwargs: Any) -> None:
        """Initialize LifecycleEvent with Grid-STIX properties."""
        # Set STIX type if not provided
        if "type" not in kwargs:
            kwargs["type"] = self._type

        # Generate deterministic ID if not provided
        if "id" not in kwargs:
            from ..base import DeterministicUUIDGenerator

            # Generate deterministic UUID - will raise ValueError if required properties missing
            kwargs["id"] = DeterministicUUIDGenerator.generate_uuid(self._type, kwargs)

        super().__init__(**kwargs)
