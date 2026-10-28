# Project Documentation — Electric Vehicle Market Performance & Insights

**Author:** `<your name>` · **Program:** Data Analytics with Tableau (SkillWallet) · **Type:** Individual · **Domain:** Transportation

## 1. Introduction
The EV industry is one of the fastest-growing automotive sectors. This project analyses EV market data (sales, pricing, battery
specifications, manufacturing locations, ratings, sustainability metrics) in Tableau to support strategy, BI and research decisions.

## 2. Problem statement & users
| User | Need |
|------|------|
| Emily Johnson, EV Market Strategy Director | Category sales contribution, leading manufacturers, satisfaction by segment, battery adoption, range comparison, high-growth segments |
| David Chen, Automotive BI Manager | Manufacturer market share, annual sales, battery distribution, manufacturing-country analysis, ratings |
| Dr. Sarah Williams, Sustainable Mobility Researcher | Battery technology comparison, range improvements, global manufacturing, satisfaction across categories, CO₂ impact |

## 3. Development procedure (step by step)

### Step 1 — Data collection & extraction
- Downloaded `ev_market_train.csv` (200k rows) and `ev_market_test.csv` (100k rows) from Kaggle.
- 37 columns: identity, battery, range & efficiency, motor & performance, charging, body, price & ownership, safety/tech, environmental & market.
- Connected the cleaned CSV to Tableau as an extract.

### Step 2 — Data preparation
- Combined both splits into one 300k-row table; removed duplicate `vehicle_id`s; trimmed text.
- Imputed the 1–3% nulls with group medians (`battery_cycle_life` by battery type; `annual_sales_units`, `customer_rating`,
  `resale_value_pct_3yr`, `infotainment_screen_inch` by category). Imputed rows are flagged.
- Added derived columns: `vehicle_segment`, `price_band`, `range_band`, `rating_band`, `revenue_usd`, `range_per_kwh`,
  `price_per_km_range`, `power_to_weight_kw_per_t`.
- In Tableau: set geographic role, default aggregations, folders, 13 calculated fields, 2 parameters (see `tableau/TABLEAU_BUILD_GUIDE.md`).

### Step 3 — Visualizations
16 sheets (KPI cards, sales by category, manufacturer share, sales trend + YoY, battery donut, battery adoption area,
range box plot, capacity-vs-range scatter, country map, category×battery heatmap, rating by category, price vs rating,
region treemap, charging class, CO₂ saved, dynamic metric).

### Step 4 — Dashboards
- *Executive Overview*: KPIs, category sales, Top-N manufacturers, trend, ratings; filters for year, region, segment, battery.
- *Battery Technology & Manufacturing*: battery mix and adoption, capacity vs range, map, heatmap, charging.
- Automatic sizing + phone layout for responsiveness; filter/highlight actions.

### Step 5 — Story
7 scenes: market at a glance → categories → manufacturers → battery adoption → range → manufacturing geography → customer satisfaction & recommendations.

### Step 6 — Performance testing
| Criterion | Result |
|-----------|--------|
| Amount of data rendered | 300,000 rows |
| Filters used | 7 quick filters, 2 parameters, 3 actions |
| Calculated fields | 13 |
| Visualizations | 16 sheets, 2 dashboards, 1 story |
| Load time (Performance Recording) | `<record value>` s |

### Step 7 — Web integration
- Published the workbook to Tableau Public.
- Built a Flask app (`app.py`) with Home, Dashboard, Story and About pages; views are embedded with the Tableau Embedding API v3 `<tableau-viz>` component.

## 4. Key insights
> Fill in with the values from your dashboards. Suggested structure:

1. **Category sales:** `<top category>` contributes `<x%>` of units; commercial segments (bus/truck) are small in units but large in revenue.
2. **Manufacturers:** the top 10 of 200 manufacturers hold `<x%>` share, so the market is fragmented.
3. **Battery tech:** NMC (~34%) and LFP (~32%) dominate; Solid-State/Sodium-Ion are emerging, with longer cycle life and lower degradation for LFP/Solid-State.
4. **Range:** range scales with battery capacity; `<category>` has the highest average range (`<x>` km).
5. **Manufacturing:** production is spread across `<n>` countries, led by `<country>`.
6. **Customer satisfaction:** average rating `<x>`/5; highest in `<category>`; price shows `<weak/strong>` relationship with rating.

## 5. Recommendations
- Prioritise portfolio investment in the highest-sales and highest-rated categories; target growth segments shown in the YoY trend.
- Position LFP for cost/longevity-focused segments and NMC/NCA for range/performance; track next-gen chemistries.
- Use the manufacturing map to identify expansion hubs and supply-chain diversification.

## 6. Limitations
The dataset is synthetic (fictional manufacturers/models), so insights demonstrate method rather than real-market facts. Sales and rating nulls were imputed.

## 7. Links
- Tableau Public: `<link>`
- GitHub: `<link>`
- Demo video: `<link>`
