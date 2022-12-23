# VATGlasses Data Project
Airport and sector data for the VATGlasses project.

https://vatglasses.uk

## Data Sets
VATGlasses is formed of lots of individual data sets. Each data set covers one (and occasionally multiple) countries, usually within the remit of a single vACC. Occasionally, a country is split into multiple datasets (e.g. if it is split across several divisions), but in most cases this should be avoided.

Every data set is contained within a separate file and the file structure is identical throughout. Some VATGlasses pages display multiple data sets at once and some data sets are displayed on multiple VATGlasses pages.

### Open-Source Data
This repository contains only **open-source** data - not all FIRs contained on VATGlasses are open-source. The current open-source data sets are:

#### Managed by Local Staff
- Germany (ED** and ET**). https://vatglasses.uk/germany
- Hong Kong (VH**, also contains Macau VM**). https://vatglasses.uk/hongkong

#### Managed by the VATGlasses Team
- United Kingdom (EG** and some overseas territories). https://vatglasses.uk/ukireland
- Ireland (EI**). https://vatglasses.uk/ukireland
- South Africa (FA**, also contains Lesotho FX**). https://vatglasses.uk/southafrica
- Gibraltar (LX**). https://vatglasses.uk/ukireland
  - **N.B.** Gibraltar should remain separate from the UK set to allow it to be displayed on both the UK/Ireland and Iberia pages.

### Closed-Source Data
Closed-source FIRs are managed by local VATSIM staff and are not open to public contributions. The current closed-sourced data sets are:

- Norway (EN**). https://vatglasses.uk/norway
- Spain (LE** and GC**). _Pending Release_

### New Data Sets
As a general rule, you should be local staff, an instructor, or (in small vACCs only) a mentor to add a new region to VATGlasses. This provides a point of contact for all future changes to the region and helps prevent incorrect information from making it onto the platform.

If you're a member of local staff looking to add your local vACC to the platform, feel free to open an issue with your name, vACC, and staff role. I'll get back to you as soon as possible (please also leave some contact info if you're not easy to find on the standard VATSIM channels). 

If you're not a member of local staff but you'd still like to contribute, please consider contacting the vACC directly - they may be very keen to have you on board! Alternatively, you could propose some improvements to an existing data set.

## Contribution Guide
Please ensure that you provide a source for your issues and pull-requests! Issues and pull requests without a valid source will be automatically closed.

By committing changes to this repository, you acknowledge that the copyright ownership of any contributions you make transfers to @lennycolton in its entirety.

## Data Format
- `bounds` - _Optional_ Array of Arrays
  - Arrays of Decimals - Coordinate pairs (signed decimal degrees)
- `airspace` - Array of Objects
  - `id` - String - Name of ATC Sector
  - `group` - String - ID of sector's group in top-level `groups` array.
  - `docs` - _Optional_ Array of Strings - Part of an ongoing project, not to be used outside of the UK.
  - `fua` - _Optional_ Array of Objects - Date/Time restrictions on sector's availability. Not shown on the map outside of designated times.
  - `owner` - Array of Strings - ID of owning positions (in descending order of priority) in top-level `positions` array.
  - `sectors` - Array of Objects - Uniform locks of airspace making up this ATC sector. Each element must have the same lateral boundaries at all altitudes.
    - `min` - _Optional_ Integer - Minimum altitude (inclusive) for this sector.
    - `max` - _Optional_ Integer - Maximum altitude (inclusive) for this sector.
    - `runways` _Optional_ Array of Objects - Required active runways for this sector (all must be true to display).
      - `icao` - String - ICAO code of airport.
      - `runway` - String or Array of Strings - Valid runway configurations.
    - `points` - Array of Arrays
      - Arrays of coordinate pairs (`["-ddmmss", "-dddmmss"]`)
- `groups` - Object of Objects (Key - String - used to reference group in `group` element of `airspace` entries.)
  - `name` - String - Display name of group.
  - `colour` - String - Colour of group in offline sector displays, must be a hex value in the format `"#rrggbb"`.
- `positions` - Object of Objects (Key - String - used to reference position in `owner` element of `airspace` entries and `topdown` element of `airport` entries.)
  - `colours` - _Optional_ Array of Objects - Colour of position's owned sectors in online sector displays. First valid element (starting at index 0) is used as display colour.
    - `online` - _Optional_ - Array of Strings - IDs of positions which must be online to use this colour configuration.
    - `hex` - String - Colour, must be a hex value in the format `"#rrggbb"`.
  - `pre` - Array of Strings - Valid prefixes in logon callsign (text before the first `_`).
  - `type` - String - Suffix of logon callsign (text after the final `_`).
  - `frequency` - String - Exact frequency of position.
  - `callsign` - String - Voice callsign of position.
- `callsigns` - Object of Objects (Key - String - Equivalent to `type` in `position` entries) - Used to generate generic callsigns for undefined aerodrome positions.
  - Each object may contain any number of key-value pairs, with the format:
    - **Key** - String - Middle section of logon callsign (empty string matches logon callsigns without a middle section).
    - **Value** - String - Position voice callsign (paired with airport voice callsign).
- `airports` - Object of Objects (Key - String - ICAO code of airport _and/or_ equivalent to `prefix` in `position` entries, as desired)
  - `callsign` - String - Airport voice callsign (paired with position voice callsigns in `callsigns` entries to generate generic callsigns where `positions` does not contain a valid entry.)
  - `coord` - _Optional_ Array of Decimals - Coordinate pairs (signed decimal degrees).
  - `runways` - _Optional_ Array of Strings - Possible runway configurations. Only define runways if this airport's runway configuration affects airspace structure.
  - `default` - _Optional_ Boolean (assumed `true` if omitted) - Use the default APP ownership structure for this airport (F_APP > APP > `topdown`).
  - `topdown` - _Optional_ Array of Strings - ID