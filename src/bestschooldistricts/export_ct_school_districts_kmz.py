"""Export Connecticut school district shapefiles to Google Earth Web KMZ."""

from __future__ import annotations

import argparse
import html
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_LAYERS = ("elsd", "scsd", "unsd")
DESCRIPTION_FIELDS = ("GEOID", "SDTYP", "LOGRADE", "HIGRADE", "STATEFP")


class ExportError(RuntimeError):
    """Raised when export execution fails."""


@dataclass
class ExportStats:
    """Export stats for one layer."""

    layer: str
    source_path: Path
    output_path: Path
    source_rows: int
    exported_polygons: int
    skipped_null_geometry: int
    skipped_unsupported_geometry: int
    skipped_empty_layer: bool = False


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Convert CT TIGER school district shapefiles to Google Earth "
            "Web-ready KMZ files."
        )
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("data/external"),
        help="Directory containing TIGER shapefiles.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/processed/google_earth"),
        help="Directory where KMZ files are written.",
    )
    parser.add_argument(
        "--layers",
        nargs="+",
        default=list(DEFAULT_LAYERS),
        help="School district layers to export (e.g., elsd scsd unsd).",
    )
    parser.add_argument(
        "--state-fips",
        default="09",
        help="State FIPS code used in TIGER shapefile names.",
    )
    parser.add_argument(
        "--year",
        default="2025",
        help="TIGER year used in shapefile names.",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue exporting remaining layers if one layer fails.",
    )
    parser.add_argument(
        "--strict-empty",
        action="store_true",
        help="Return an error if a layer has no exportable polygons.",
    )
    return parser.parse_args(argv)


def load_export_dependencies() -> tuple[Any, Any, Any]:
    """Load geospatial dependencies lazily with clear installation hints."""
    try:
        import geopandas as gpd  # type: ignore[import-not-found]
        import pandas as pd  # type: ignore[import-not-found]
        import simplekml  # type: ignore[import-not-found]
    except ModuleNotFoundError as exc:
        missing_module = exc.name or "required geospatial library"
        raise ExportError(
            "Missing dependency: "
            f"{missing_module}. Install with "
            "`poetry add geopandas simplekml` or run `poetry install`."
        ) from exc
    return gpd, pd, simplekml


def shapefile_name(year: str, state_fips: str, layer: str) -> str:
    """Build a TIGER shapefile base name."""
    return f"tl_{year}_{state_fips}_{layer}"


def shapefile_path(
    input_dir: Path, year: str, state_fips: str, layer: str
) -> Path:
    """Build absolute path to input shapefile."""
    return input_dir / f"{shapefile_name(year, state_fips, layer)}.shp"


def _coord_pairs(coords: Any) -> list[tuple[float, float]]:
    """Convert shapely coordinate sequences into (lon, lat) pairs."""
    points: list[tuple[float, float]] = []
    for coord in coords:
        points.append((float(coord[0]), float(coord[1])))
    return points


def _is_missing_value(value: Any, pd: Any) -> bool:
    """Check if a value should be treated as missing."""
    try:
        return bool(pd.isna(value))
    except TypeError:
        return False


def _feature_name(row: Any, pd: Any) -> str:
    """Get feature name with fallback to GEOID."""
    name_value = row.get("NAME")
    if name_value is not None and not _is_missing_value(name_value, pd):
        return str(name_value)
    geoid_value = row.get("GEOID")
    if geoid_value is not None and not _is_missing_value(geoid_value, pd):
        return str(geoid_value)
    return "Unnamed District"


def _feature_description(row: Any, pd: Any) -> str:
    """Build feature description HTML for Google Earth popups."""
    description_lines: list[str] = []
    for field in DESCRIPTION_FIELDS:
        value = row.get(field)
        if value is None or _is_missing_value(value, pd):
            continue
        safe_field = html.escape(field)
        safe_value = html.escape(str(value))
        description_lines.append(f"<b>{safe_field}</b>: {safe_value}")
    return "<br/>".join(description_lines)


def _layer_style(simplekml: Any) -> Any:
    """Create a reusable KML style for district boundaries."""
    style = simplekml.Style()
    style.linestyle.color = simplekml.Color.rgb(20, 60, 110, 255)
    style.linestyle.width = 1.2
    style.polystyle.color = simplekml.Color.rgb(50, 130, 200, 80)
    style.polystyle.fill = 1
    style.polystyle.outline = 1
    return style


def _add_polygon_feature(
    folder: Any,
    polygon: Any,
    name: str,
    description: str,
    style: Any,
) -> None:
    """Add one polygon geometry to KML preserving interior rings."""
    outer = _coord_pairs(polygon.exterior.coords)
    inners = [_coord_pairs(interior.coords) for interior in polygon.interiors]
    feature = folder.newpolygon(
        name=name,
        outerboundaryis=outer,
        innerboundaryis=inners,
    )
    feature.description = description
    feature.style = style


def export_layer(
    gpd: Any,
    pd: Any,
    simplekml: Any,
    shp_path: Path,
    output_dir: Path,
    layer: str,
    strict_empty: bool,
) -> ExportStats:
    """Export one shapefile layer to KMZ."""
    geodf = gpd.read_file(shp_path)
    source_rows = len(geodf.index)

    if geodf.empty:
        message = f"Layer '{layer}' has no records: {shp_path}"
        if strict_empty:
            raise ExportError(message)
        return ExportStats(
            layer=layer,
            source_path=shp_path,
            output_path=output_dir / f"{shp_path.stem}.kmz",
            source_rows=0,
            exported_polygons=0,
            skipped_null_geometry=0,
            skipped_unsupported_geometry=0,
            skipped_empty_layer=True,
        )

    geodf = geodf[geodf.geometry.notnull()].copy()
    if geodf.empty:
        message = f"Layer '{layer}' has only null geometries: {shp_path}"
        if strict_empty:
            raise ExportError(message)
        return ExportStats(
            layer=layer,
            source_path=shp_path,
            output_path=output_dir / f"{shp_path.stem}.kmz",
            source_rows=source_rows,
            exported_polygons=0,
            skipped_null_geometry=source_rows,
            skipped_unsupported_geometry=0,
            skipped_empty_layer=True,
        )

    if geodf.crs is not None:
        geodf = geodf.to_crs(epsg=4326)

    kml = simplekml.Kml()
    layer_folder = kml.newfolder(name=layer.upper())
    style = _layer_style(simplekml)

    exported_polygons = 0
    skipped_null_geometry = source_rows - len(geodf.index)
    skipped_unsupported_geometry = 0

    for _, row in geodf.iterrows():
        geometry = row.geometry
        if geometry is None or geometry.is_empty:
            skipped_null_geometry += 1
            continue

        name = _feature_name(row, pd)
        description = _feature_description(row, pd)
        geom_type = geometry.geom_type

        if geom_type == "Polygon":
            _add_polygon_feature(layer_folder, geometry, name, description, style)
            exported_polygons += 1
            continue

        if geom_type == "MultiPolygon":
            for index, polygon in enumerate(geometry.geoms, start=1):
                part_name = (
                    f"{name} (part {index})"
                    if len(geometry.geoms) > 1
                    else name
                )
                _add_polygon_feature(
                    layer_folder,
                    polygon,
                    part_name,
                    description,
                    style,
                )
                exported_polygons += 1
            continue

        skipped_unsupported_geometry += 1

    if exported_polygons == 0:
        message = f"Layer '{layer}' has zero polygon features: {shp_path}"
        if strict_empty:
            raise ExportError(message)
        return ExportStats(
            layer=layer,
            source_path=shp_path,
            output_path=output_dir / f"{shp_path.stem}.kmz",
            source_rows=source_rows,
            exported_polygons=0,
            skipped_null_geometry=skipped_null_geometry,
            skipped_unsupported_geometry=skipped_unsupported_geometry,
            skipped_empty_layer=True,
        )

    output_path = output_dir / f"{shp_path.stem}.kmz"
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        kml_path = temp_path / "doc.kml"
        kml.save(str(kml_path))
        with zipfile.ZipFile(
            output_path,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
        ) as kmz_file:
            kmz_file.write(kml_path, arcname="doc.kml")

    return ExportStats(
        layer=layer,
        source_path=shp_path,
        output_path=output_path,
        source_rows=source_rows,
        exported_polygons=exported_polygons,
        skipped_null_geometry=skipped_null_geometry,
        skipped_unsupported_geometry=skipped_unsupported_geometry,
    )


def print_stats(stats: ExportStats) -> None:
    """Print per-layer export summary."""
    if stats.skipped_empty_layer:
        print(
            f"[WARN] {stats.layer}: no export created from "
            f"{stats.source_path.name}"
        )
        return

    kmz_size = stats.output_path.stat().st_size
    print(
        f"[OK] {stats.layer}: rows={stats.source_rows}, "
        f"exported_polygons={stats.exported_polygons}, "
        f"skipped_null_geometry={stats.skipped_null_geometry}, "
        f"skipped_unsupported_geometry={stats.skipped_unsupported_geometry}, "
        f"kmz={stats.output_path} ({kmz_size} bytes)"
    )


def main(argv: list[str] | None = None) -> int:
    """Run KMZ export command."""
    args = parse_args(argv)
    input_dir = args.input_dir.resolve()
    output_dir = args.output_dir.resolve()

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"[ERROR] Input directory not found: {input_dir}", file=sys.stderr)
        return 2

    output_dir.mkdir(parents=True, exist_ok=True)

    missing_paths: list[Path] = []
    layer_paths: dict[str, Path] = {}
    for layer in args.layers:
        path = shapefile_path(input_dir, args.year, args.state_fips, layer)
        layer_paths[layer] = path
        if not path.exists():
            missing_paths.append(path)

    if missing_paths:
        print(
            "[ERROR] Missing input shapefile(s):\n- "
            + "\n- ".join(str(path) for path in missing_paths),
            file=sys.stderr,
        )
        return 1

    try:
        gpd, pd, simplekml = load_export_dependencies()
    except ExportError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2

    had_errors = False
    for layer in args.layers:
        path = layer_paths[layer]
        try:
            stats = export_layer(
                gpd=gpd,
                pd=pd,
                simplekml=simplekml,
                shp_path=path,
                output_dir=output_dir,
                layer=layer,
                strict_empty=args.strict_empty,
            )
            print_stats(stats)
        except Exception as exc:  # pragma: no cover
            print(
                f"[ERROR] Failed exporting {layer} from {path}: {exc}",
                file=sys.stderr,
            )
            had_errors = True
            if not args.continue_on_error:
                return 1

    return 1 if had_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
