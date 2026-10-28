# Tableau Build Guide — EV Market Performance & Insights

Follow these steps in Tableau Public (or Desktop). Workbook name: **EVMarketPerformanceInsights**.

## 1. Connect the data (Epic: Data Collection & Extraction)

1. Download `ev_market_train.csv` and `ev_market_test.csv` from Kaggle into `data/`.
2. Run `python data_preparation.py` → creates `data/ev_market_clean.csv` (300,000 rows, no nulls).
3. Tableau → **Connect → Text file** → `ev_market_clean.csv`.
4. Data Source tab checks:
   - `model_year` → set to **String/Dimension** (or Date → Year) for trend axes.
   - `manufacturing_country` → Geographic Role → **Country/Region**.
   - `customer_rating`, `annual_sales_units`, `price_usd`, `range_km` → Measures.
   - Use an **Extract** (not Live) for speed; hide unused columns (`vehicle_id`, `model_name` if not needed) before extracting.
5. Rename the data source to `EV Market`.

## 2. Data preparation inside Tableau (Epic: Data Preparation)

Default aggregations: `customer_rating`, `range_km`, `battery_capacity_kwh`, `efficiency_wh_per_km`, `acceleration_0_100_sec` → **Average**. `annual_sales_units`, `revenue_usd`, `co2_saved_tons_per_year` → **Sum**.

Create folders in the Data pane: *Identity, Battery, Performance, Charging, Price, Market, Calculations*.

### Calculated fields (12)

| # | Name | Formula |
|---|------|---------|
| 1 | Total Sales | `SUM([annual_sales_units])` |
| 2 | Market Share % | `SUM([annual_sales_units]) / TOTAL(SUM([annual_sales_units]))` (format %) |
| 3 | Avg Customer Rating | `AVG([customer_rating])` |
| 4 | Total Revenue (B USD) | `SUM([price_usd] * [annual_sales_units]) / 1e9` |
| 5 | Avg Range (km) | `AVG([range_km])` |
| 6 | Range per kWh | `SUM([range_km]) / SUM([battery_capacity_kwh])` |
| 7 | Sales YoY Growth % | `(ZN([Total Sales]) - LOOKUP(ZN([Total Sales]), -1)) / ABS(LOOKUP(ZN([Total Sales]), -1))` (table calc across `model_year`) |
| 8 | Manufacturer Rank | `RANK([Total Sales], 'desc')` |
| 9 | Top N Manufacturer | `IF [Manufacturer Rank] <= [Top N] THEN "Top" ELSE "Other" END` with integer **parameter `Top N`** (5–20, default 10) |
| 10 | Rating Segment | `IF [customer_rating] >= 4 THEN "Excellent" ELSEIF [customer_rating] >= 3 THEN "Good" ELSEIF [customer_rating] >= 2 THEN "Average" ELSE "Poor" END` |
| 11 | Battery Generation | `IF [battery_type] IN ("Solid-State","Sodium-Ion") THEN "Next-Gen" ELSE "Mainstream" END` |
| 12 | Fast-Charge Class | `IF [charging_dc_fast_time_min] <= 30 THEN "Ultra-fast (≤30 min)" ELSEIF [charging_dc_fast_time_min] <= 60 THEN "Fast (31–60)" ELSE "Standard (>60)" END` |
| 13 | Selected Metric | `CASE [Metric Param] WHEN "Sales" THEN [Total Sales] WHEN "Revenue" THEN [Total Revenue (B USD)] WHEN "Rating" THEN [Avg Customer Rating] WHEN "Range" THEN [Avg Range (km)] END` with **string parameter `Metric Param`** |

Also use the prepared columns: `vehicle_segment`, `price_band`, `range_band`, `rating_band`.

## 3. Visualizations (Epic: Data Visualizations) — 14 unique sheets

| # | Sheet name | Chart type | Build |
|---|-----------|-----------|-------|
| 1 | KPI Cards | Text (BANs) | Total Sales, Total Revenue, Avg Rating, Avg Range, # Manufacturers (`COUNTD`) — one sheet each or Measure Names/Values |
| 2 | Sales by Category | Horizontal bar | Rows `category`, Cols `Total Sales`, sort desc, color by `vehicle_segment` |
| 3 | Manufacturer Market Share | Bar + Top N | `manufacturer` × `Market Share %`, filter `Top N Manufacturer = Top`, label % |
| 4 | Sales Trend by Year | Line | Cols `model_year`, Rows `Total Sales`; dual-axis with `Sales YoY Growth %` |
| 5 | Battery Type Distribution | Donut | Pie of `battery_type` by `Total Sales` on dual-axis with a white center circle (MIN(0)) |
| 6 | Battery Tech Adoption over Time | 100% stacked area | `model_year` × `Total Sales`, color `battery_type`, Quick table calc → Percent of Total (compute using `battery_type`) |
| 7 | Range by Category | Box-and-whisker | Cols `category`, Rows `range_km` (disaggregated or AVG per model), Show Me → box plot |
| 8 | Battery Capacity vs Range | Scatter | `AVG(battery_capacity_kwh)` × `AVG(range_km)` per `model_name`, color `battery_type`, trend line |
| 9 | Manufacturing Country Map | Filled map | `manufacturing_country` on Detail, color `Total Sales`, tooltip with avg rating |
| 10 | Category × Battery Heatmap | Highlight table | Rows `category`, Cols `battery_type`, color/label `Avg Customer Rating` |
| 11 | Customer Rating by Category | Bar with reference line | `category` × `Avg Customer Rating`, average reference line |
| 12 | Price vs Rating | Bubble / scatter | `AVG(price_usd)` × `Avg Customer Rating` per `category`, size `Total Sales` |
| 13 | Sales by Market Region | Treemap | `market_region` size/color `Total Sales` |
| 14 | Charging Speed vs Battery | Stacked bar | `battery_type` × count, color `Fast-Charge Class` |
| 15 | CO₂ Saved by Segment | Bar | `vehicle_segment`/`category` × `SUM(co2_saved_tons_per_year)` |
| 16 | Dynamic Metric by Category | Bar | `category` × `Selected Metric`, show `Metric Param` control |

Formatting: one consistent palette (e.g. Tableau 10 or a green/teal EV palette), tooltips with formatted numbers (`#,##0`, `$#,##0.0,,"M"`), titles phrased as insights.

## 4. Dashboards (Epic: Dashboard — Responsive design)

Size: **Automatic** (or Range 1000×700 to 1600×1000) for responsiveness. Add a **Phone** device layout with KPIs stacked and the 3 most important charts.

**Dashboard 1 – Executive Overview** (Emily / David)
- Top: title + KPI cards row.
- Middle: Sales by Category | Manufacturer Market Share (Top N).
- Bottom: Sales Trend by Year | Customer Rating by Category.
- Filters (apply to all sheets using this data source): `model_year`, `market_region`, `vehicle_segment`, `battery_type`; `Top N` parameter control.
- Actions: *Filter action* — click a category in "Sales by Category" filters the other sheets; *Highlight action* on `manufacturer`.

**Dashboard 2 – Battery Technology & Manufacturing** (David / Dr. Sarah)
- Battery Type Distribution, Battery Tech Adoption over Time, Battery Capacity vs Range, Manufacturing Country Map, Category × Battery Heatmap, Charging Speed vs Battery.
- Filters: `category`, `model_year`, `price_band`. Map click → filters other sheets.

(Optional **Dashboard 3 – Customer & Sustainability**: Price vs Rating, Range by Category, CO₂ Saved, Dynamic Metric.)

Use containers (horizontal/vertical) and Tiled layout so it reflows; keep padding 8 px; add a "Reset filters" button using a Go-to-Sheet/Navigation button.

## 5. Story (Epic: Story) — 7 scenes

Name: **EV Market Story**. Each story point has an insight-style caption:

1. *The EV market at a glance* — KPI cards + Sales by Market Region.
2. *Which categories drive sales?* — Sales by Category.
3. *Who leads the market?* — Manufacturer Market Share (Top 10).
4. *Battery chemistry adoption is shifting* — Battery Tech Adoption over Time.
5. *Range depends on category and battery size* — Range by Category / Capacity vs Range.
6. *Where EVs are built* — Manufacturing Country Map.
7. *What customers think* — Customer Rating heatmap + Price vs Rating → recommendations.

Write the actual numbers you see into the captions (e.g., "Two-Wheeler Scooters are the largest category at X% of units").

## 6. Performance testing (Epic: Performance Testing)

Record these in the documentation:

| Criterion | Value |
|-----------|-------|
| Amount of data rendered | 300,000 rows × 47 columns (extract) |
| Utilization of filters | 7 quick filters + 2 parameters + 3 dashboard actions |
| Number of calculated fields | 13 |
| Number of visualizations | 16 sheets, 2–3 dashboards, 1 story (7 scenes) |

Tips: use an Extract, hide unused fields, aggregate extract if needed, use context filter on `model_year`, avoid >1 high-cardinality scatter per dashboard. Use **Help → Settings and Performance → Start Performance Recording** and screenshot the results.

## 7. Publish (Epic: Web Integration)

1. **File → Save to Tableau Public As…** → `EVMarketPerformanceInsights`. Untick "Show sheets as tabs" if you only want dashboards.
2. On Tableau Public, open each view → **Share** → copy the link (`https://public.tableau.com/views/EVMarketPerformanceInsights/<SheetName>`).
3. Paste the three URLs into `app.py` (`DASHBOARD_URL`, `DASHBOARD_2_URL`, `STORY_URL`).
4. Use the Tableau Public profile link as the project's **Demo link**.
