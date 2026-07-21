# Grid-STIX Deterministic UUID Generation Guide

## Overview

Grid-STIX implements deterministic UUID generation to ensure that the same logical object always generates the same UUID across different systems and time periods. This enables reliable deduplication, consistent object identification, and improved data integrity in Grid-STIX deployments.

## How It Works

### UUID Generation Method

Grid-STIX uses **UUID5 (namespace-based SHA-1)** with a Grid-STIX specific namespace UUID (`6ba7b810-9dad-11d1-80b4-00c04fd430c8`). This approach provides:

- **Deterministic generation** based on key object properties
- **Cryptographically secure** and collision-resistant UUIDs
- **Standard UUID format** compliance
- **Reproducible results** across different systems

### Identity Properties

Each Grid-STIX object type has a defined set of "identity properties" that uniquely identify that object, configured in `IDENTITY_PROPERTY_CONFIG` in `python/grid_stix/base.py`. These properties are used to generate the deterministic UUID. For example:

- **Generators**: `name`, `x_grid_component_type`, `x_power_rating_mw`, `x_fuel_type`
- **Smart Meters**: `name`, `x_grid_component_type`
- **Transformers**: `name`, `x_voltage_primary_kv`, `x_voltage_secondary_kv`, `x_power_rating_mva`

> **Known limitation:** a handful of configured identity properties (e.g. `x_capec_id`/`x_attack_id` for Cyber Attack Patterns, `x_event_type`/`x_timestamp`/`x_source_component` for Grid Events) do not exist as real properties on the corresponding generated class. Constructing those object types without an explicit `id=` currently always raises `ValueError`. See the notes in [Examples by Object Type](#examples-by-object-type) below.

## Basic Usage

### Automatic UUID Generation

When creating Grid-STIX objects, deterministic UUIDs are generated automatically if no explicit ID is provided:

```python
from grid_stix.assets.Generator import Generator

# Create a generator - UUID will be generated automatically
generator = Generator(
    name="Main Power Plant Generator 1",
    x_grid_component_type="generator",
    x_power_rating_mw=[500.0],
    x_fuel_type=["natural_gas"],
)

print(f"Generated UUID: {generator.id}")
# Output: x-grid-generator--9a978fb8-5d76-5b0d-b27f-d3db5c0a3730
```

### Consistent UUID Generation

Creating the same object multiple times will always generate the same UUID:

```python
# First instance
gen1 = Generator(
    name="Main Power Plant Generator 1",
    x_grid_component_type="generator",
    x_power_rating_mw=[500.0],
    x_fuel_type=["natural_gas"],
)

# Second instance with identical properties
gen2 = Generator(
    name="Main Power Plant Generator 1",
    x_grid_component_type="generator",
    x_power_rating_mw=[500.0],
    x_fuel_type=["natural_gas"],
)

assert gen1.id == gen2.id  # This will always be True
```

### Explicit ID Override

You can still provide explicit IDs when needed, which skips deterministic generation entirely (identity properties are not required in this case):

```python
generator = Generator(
    id="x-grid-generator--8f31b6ab-74ab-4c57-bd6f-82a879c7590d",
    name="Custom Generator",
    x_grid_component_type="generator",
)
# The explicit ID will be used instead of generating a deterministic one
```

## Property Normalization

To ensure consistent UUID generation, property values are normalized:

### Case Insensitivity

String values are normalized to lowercase:

```python
# These will generate the same UUID
gen1 = Generator(
    name="Test Generator",
    x_grid_component_type="generator",
    x_power_rating_mw=[100.0],
    x_fuel_type=["NATURAL_GAS"],
)
gen2 = Generator(
    name="test generator",
    x_grid_component_type="generator",
    x_power_rating_mw=[100.0],
    x_fuel_type=["natural_gas"],
)
assert gen1.id == gen2.id
```

### List Ordering

Lists are sorted to ensure consistent ordering:

```python
# These will generate the same UUID
gen1 = Generator(
    name="Test",
    x_grid_component_type="generator",
    x_power_rating_mw=[100.0],
    x_fuel_type=["coal", "natural_gas"],
)
gen2 = Generator(
    name="Test",
    x_grid_component_type="generator",
    x_power_rating_mw=[100.0],
    x_fuel_type=["natural_gas", "coal"],
)
assert gen1.id == gen2.id
```

## Examples by Object Type

### Physical Assets

#### Generator
```python
from grid_stix.assets.Generator import Generator

generator = Generator(
    name="Riverside Power Plant Unit 1",
    x_grid_component_type="generator",
    x_power_rating_mw=[750.0],
    x_fuel_type=["natural_gas"],
)
```

#### Transformer
```python
from grid_stix.assets.Transformer import Transformer

transformer = Transformer(
    name="Main Substation Transformer T1",
    x_voltage_primary_kv=[138.0],
    x_voltage_secondary_kv=[13.8],
    x_power_rating_mva=[50.0],
)
```

#### Substation
```python
from grid_stix.assets.Substation import Substation

substation = Substation(
    name="Downtown Distribution Substation",
    x_high_voltage_level_kv=[69.0],
    x_substation_type=["distribution"],
)
```

### Components

#### Smart Meter
```python
from grid_stix.components.SmartMeter import SmartMeter

smart_meter = SmartMeter(
    name="Residential Smart Meter 12345",
    x_grid_component_type="smart-meter",
)
```

#### Photovoltaic System
```python
from grid_stix.components.PhotovoltaicSystem import PhotovoltaicSystem

pv_system = PhotovoltaicSystem(
    name="Rooftop Solar Array Building A",
    x_system_id=["PV-BLDG-A"],
    x_capacity_kw=[100.0],
    x_panel_type=["monocrystalline"]
)
```

### Cyber Contexts

#### Cybersecurity Posture
```python
from grid_stix.cyber_contexts.CybersecurityPosture import CybersecurityPosture

posture = CybersecurityPosture(
    x_trust_level=["high"],
    x_alert_level=["green"],
    x_defensive_posture=["normal"],
    x_authorized_by=["security_operations_center"]
)
```

#### Communication Session
```python
from grid_stix.cyber_contexts.CommunicationSession import CommunicationSession

session = CommunicationSession(
    x_session_id=["sess_20250108_001"],
    x_protocol_type=["dnp3"],
    x_session_start_time=["2025-01-08T10:00:00Z"]
)
```

### Attack Patterns

#### Cyber Attack Pattern

> **Currently broken:** `IDENTITY_PROPERTY_CONFIG["x-grid-cyber-attack-pattern"]` requires `x_capec_id`/`x_attack_id`, but `CyberAttackPattern` does not define either property. Automatic UUID generation for this type always raises `ValueError`; an explicit `id` is required until the identity config (or the class) is fixed.

```python
from grid_stix.attack_patterns.CyberAttackPattern import CyberAttackPattern

attack_pattern = CyberAttackPattern(
    id="x-grid-cyber-attack-pattern--f37c0e9a-de14-4968-bb62-5034ba34bf6e",
    name="DNP3 Function Code Manipulation",
)
```

### Relationships

#### Grid Relationship
```python
from grid_stix.relationships.GridRelationship import GridRelationship

relationship = GridRelationship(
    x_source_ref="x-grid-generator--4d29ed73-d166-51df-88ba-f53d97b54f48",
    x_target_ref="x-grid-transformer--9ed616b6-0138-5117-8bb6-fbbc31074828",
    x_relationship_type="feeds-power-to"
)
```

`x_source_ref`/`x_target_ref` are validated STIX identifiers (`<object-type>--<UUID>`), each a single reference rather than a list, and reject endpoints of type `bundle`, `language-content`, `marking-definition`, `relationship`, or `sighting`.

### Events/Observables

#### Grid Event

> **Currently broken:** `IDENTITY_PROPERTY_CONFIG["x-grid-grid-event"]` requires `x_event_type`/`x_timestamp`/`x_source_component`, none of which exist on `GridEvent` (its actual fields include `x_event_id`, `x_severity`, `x_device_ref`, `x_sensor_ref`, etc.). Automatic UUID generation always raises `ValueError`; an explicit `id` is required until the identity config is fixed.

```python
from grid_stix.events_observables.GridEvent import GridEvent

event = GridEvent(
    id="x-grid-grid-event--6574db67-961a-4606-8104-7b156da81d8a",
    x_event_id="evt-001",
    x_severity=[8],
)
```

#### Alarm Event

> **Currently broken:** `IDENTITY_PROPERTY_CONFIG["x-grid-alarm-event"]` requires `x_timestamp`/`x_source_component`/`x_severity`, none of which exist on `AlarmEvent` (only `x_alarm_type` from that list does). Automatic UUID generation always raises `ValueError`; an explicit `id` is required until the identity config is fixed.

```python
from grid_stix.events_observables.AlarmEvent import AlarmEvent

alarm = AlarmEvent(
    id="x-grid-alarm-event--ba80bf9f-7ce5-41f6-83bd-ddf6c7151519",
    x_alarm_type="overcurrent",
    x_alarm_priority=[1],
)
```

## Missing Identity Properties (Fail-Loud Behavior)

If required identity properties are missing and no explicit `id` is provided, object construction **fails immediately** with a `ValueError` — there is no fallback to a random UUID:

```python
from grid_stix.assets.Generator import Generator

generator = Generator(
    description="Generator without required identity properties"
)
# Raises: ValueError: CRITICAL: Missing required identity properties for
# 'x-grid-generator': ['name', 'x_grid_component_type', 'x_power_rating_mw',
# 'x_fuel_type']. ...
```

This is intentional: a Grid-STIX object with an ambiguous identity is never silently assigned a random ID. Callers must either supply all configured identity properties or pass an explicit `id`.

## Best Practices

### 1. Provide Complete Identity Properties

Always include the identity properties for your object type to ensure deterministic UUID generation:

```python
# Good - includes all identity properties
generator = Generator(
    name="Power Plant Unit 1",
    x_grid_component_type="generator",
    x_power_rating_mw=[500.0],
    x_fuel_type=["natural_gas"],
)

# Avoid - missing identity properties will raise ValueError
generator = Generator(
    description="Some generator"
)
```

### 2. Use Consistent Naming Conventions

Maintain consistent naming and formatting for better UUID consistency:

```python
# Good - consistent naming
gen1 = Generator(name="Main Plant Generator 1", x_grid_component_type="generator", x_power_rating_mw=[500.0], x_fuel_type=["natural_gas"])
gen2 = Generator(name="Main Plant Generator 2", x_grid_component_type="generator", x_power_rating_mw=[300.0], x_fuel_type=["coal"])

# Avoid - inconsistent naming
gen1 = Generator(name="main plant generator 1", x_grid_component_type="generator", x_power_rating_mw=[500.0], x_fuel_type=["natural_gas"])
gen2 = Generator(name="Main Plant Gen #2", x_grid_component_type="generator", x_power_rating_mw=[300.0], x_fuel_type=["coal"])
```

### 3. Validate Properties Before Object Creation

Check that you have the required properties before creating objects:

```python
from grid_stix.base import DeterministicUUIDGenerator

# Validate identity properties
obj_type = "x-grid-generator"
properties = {
    "name": "Test Generator",
    "x_grid_component_type": "generator",
    # Missing x_power_rating_mw and x_fuel_type
}

missing_props = DeterministicUUIDGenerator.validate_identity_properties(obj_type, properties)
if missing_props:
    print(f"Missing required properties: {missing_props}")
    # Add missing properties before creating object
```

### 4. Handle Property Updates Carefully

Remember that changing identity properties will result in a different UUID:

```python
# Original object
gen1 = Generator(name="Generator 1", x_grid_component_type="generator", x_power_rating_mw=[500.0], x_fuel_type=["natural_gas"])
original_id = gen1.id

# If you change identity properties (here, the name), you get a different UUID
gen2 = Generator(name="Generator 1 Updated", x_grid_component_type="generator", x_power_rating_mw=[500.0], x_fuel_type=["natural_gas"])
new_id = gen2.id

assert original_id != new_id  # Different UUIDs due to name change
```

## Integration with Existing Systems

### Database Storage

When storing Grid-STIX objects in databases, the deterministic UUIDs enable:

- **Deduplication**: Automatically detect and merge duplicate objects
- **Consistency**: Maintain consistent references across different data sources
- **Synchronization**: Reliably sync objects between systems

### Data Exchange

When exchanging Grid-STIX data between systems:

- **Same objects** will have the same UUIDs across systems
- **Relationships** remain consistent using deterministic UUIDs
- **Data integrity** is maintained during import/export operations

### Monitoring and Analytics

Deterministic UUIDs enable:

- **Tracking objects** across time and systems
- **Correlating events** with specific assets or components
- **Building consistent** dashboards and reports

## Performance Considerations

- **UUID generation** is fast (microseconds per object)
- **Memory usage** is minimal (no caching required)
- **Scalability** is excellent (O(1) generation time)
- **Network efficiency** improved through deduplication

## Support

For questions or issues related to deterministic UUID generation:

1. Review the test cases in `tests/test_phase3_core_validation.py`
2. Examine the implementation in `python/grid_stix/base.py`
3. Consult the `IDENTITY_PROPERTY_CONFIG` mapping and the corresponding generated class's `_properties` to confirm a property actually exists before relying on it for identity
