# Fairfield County School District Boundary Data (2025 TIGER/Line)

This document describes the school district boundary source files used for Fairfield County, Connecticut analysis.

## Data Source

- Source: U.S. Census Bureau TIGER/Line Shapefiles, School Districts (2025)
- URL: https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2025&layergroup=School+Districts
- Geography downloaded: Connecticut (statewide files)
- Acquisition date: February 7, 2026

## Files Moved

The following ZIP archives were moved from `/Users/markeyser/Downloads` to `/Users/markeyser/Projects/best-school-districts/data/external`:

| File | Size (bytes) | Layer type |
| --- | ---: | --- |
| `tl_2025_09_elsd.zip` | 197,888 | Elementary School District (current) |
| `tl_2025_09_scsd.zip` | 78,974 | Secondary School District (current) |
| `tl_2025_09_unsd.zip` | 677,654 | Unified School District (current) |

## What's Inside Each Archive

Each archive was extracted in `/Users/markeyser/Projects/best-school-districts/data/external` and contains 7 files:

- `.shp`: geometry for district boundaries
- `.shx`: shape index file
- `.dbf`: attribute table
- `.prj`: coordinate reference system definition
- `.cpg`: character encoding for DBF text fields
- `.shp.iso.xml`: ISO metadata
- `.shp.ea.iso.xml`: extended metadata

### `tl_2025_09_elsd.zip` (Elementary)

- `tl_2025_09_elsd.cpg`
- `tl_2025_09_elsd.dbf`
- `tl_2025_09_elsd.prj`
- `tl_2025_09_elsd.shp`
- `tl_2025_09_elsd.shp.ea.iso.xml`
- `tl_2025_09_elsd.shp.iso.xml`
- `tl_2025_09_elsd.shx`

### `tl_2025_09_scsd.zip` (Secondary)

- `tl_2025_09_scsd.cpg`
- `tl_2025_09_scsd.dbf`
- `tl_2025_09_scsd.prj`
- `tl_2025_09_scsd.shp`
- `tl_2025_09_scsd.shp.ea.iso.xml`
- `tl_2025_09_scsd.shp.iso.xml`
- `tl_2025_09_scsd.shx`

### `tl_2025_09_unsd.zip` (Unified)

- `tl_2025_09_unsd.cpg`
- `tl_2025_09_unsd.dbf`
- `tl_2025_09_unsd.prj`
- `tl_2025_09_unsd.shp`
- `tl_2025_09_unsd.shp.ea.iso.xml`
- `tl_2025_09_unsd.shp.iso.xml`
- `tl_2025_09_unsd.shx`

## Notes

- These files are Connecticut-wide district boundary layers from TIGER/Line 2025.
- Fairfield County-specific filtering/selection is a downstream processing step and is not encoded in the raw source files.

## Google Earth Web KMZ Export

Use the project CLI to convert the three Connecticut school-district
layers into Google Earth Web-ready `.kmz` files.

### Command

```bash
python -m bestschooldistricts.export_ct_school_districts_kmz
```

### Optional Arguments

- `--input-dir` (default: `data/external`)
- `--output-dir` (default: `data/processed/google_earth`)
- `--layers` (default: `elsd scsd unsd`)
- `--state-fips` (default: `09`)
- `--year` (default: `2025`)
- `--continue-on-error`
- `--strict-empty`

### Expected Outputs

By default, the command writes:

- `data/processed/google_earth/tl_2025_09_elsd.kmz`
- `data/processed/google_earth/tl_2025_09_scsd.kmz`
- `data/processed/google_earth/tl_2025_09_unsd.kmz`

### Upload Notes

- Google Earth Web expects KML/KMZ for direct import.
- Import the generated `.kmz` files, not source sidecar files such as
  `.xml`, `.dbf`, `.prj`, `.shx`, or `.cpg`.
- This export is statewide Connecticut, not county-filtered.
