# AI Agent Operational Protocols: Fairfield Housing Project

## 1. Geospatial Standards
* **Coordinate Reference Systems (CRS):**
    * **Storage/Input:** Always assume inputs are WGS84 (EPSG:4326).
    * **Processing/Measurement:** IMMEDIATELY project all geometries to **Connecticut State Plane (EPSG:2234)** before calculating areas, distances, or buffers.
    * **Visualization:** Reproject back to WGS84 (EPSG:4326) only for the final export to Kepler.gl/GeoJSON.
* **Geometry Validation:** Always check `.is_valid` on polygon inputs. Apply `.buffer(0)` to fix self-intersections if found.

## 2. Tool Selection Strategy
Use the following tools strictly for their assigned domains:

### A. DuckDB (The Data Engine)
* **Role:** Large-scale data ingestion, cleaning, and heavy spatial joins.
* **Rule:** Do NOT load raw CSVs >100MB directly into Pandas. Use DuckDB to query, filter, and aggregate *before* moving to a DataFrame.
* **Spatial Operations:** Use the `ST_` functions (e.g., `ST_Point`, `ST_Within`).
* **Initialization:** Always run `con.install_extension('spatial'); con.load_extension('spatial');` upon connection.

### B. OSMnx (The Network Graph)
* **Role:** Calculating accurate walking/driving distances (Isochrones) and fetching amenities.
* **Rule:** Never use Euclidean distance (radius buffers) for "Walkability." Always use network distance.
* **Caching:** Always set `ox.settings.use_cache = True` to avoid re-downloading Fairfield County maps on every run.
* **Graph Type:** Use `network_type='walk'` for school/station access and `network_type='drive'` for highway access.

### C. Kepler.gl (The Visualization)
* **Role:** Interactive data exploration and final presentation.
* **Config Persistence:** Never instantiate a map without a mechanism to save/load the `config` object.
* **Outputs:** Always save maps as standalone HTML files (`map.save_to_html()`) for portability.
* **Performance:** If plotting >10,000 points, ensure `use_static_map=False` (vector tiles).

## 3. Code Style & Performance
* **Vectorization:** Never iterate over rows (`iterrows`) for spatial calculations. Use `GeoSeries` vectorized operations.
* **Spatial Indexing:** Ensure `.sindex` is utilized for any spatial join or nearest-neighbor search.
* **Paths:** Use `pathlib` for all file system operations. Define a `PROJECT_ROOT` constant.
