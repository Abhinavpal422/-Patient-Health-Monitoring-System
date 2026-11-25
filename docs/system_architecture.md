# System Architecture

## Implemented software flow
1. Historical input: supplied `data/dataset.csv` (500 rows, 100 anonymized patient IDs).
2. Demo input: Python-generated simulated readings on the Live Monitoring page.
3. Processing: Pandas loads and converts dataset fields; Python threshold logic classifies simulated readings.
4. Storage: SQLite stores generated demo measurements and alert events.
5. Presentation: Streamlit renders KPI cards, tables and controls; Plotly renders interactive charts.
6. Export: CSV and Excel downloads are available.

See `system_architecture.png` for the diagram.

## Future extension
Wearable sensors → ESP32 firmware → Wi-Fi / MQTT / REST adapter → validation and ingestion → database → dashboard. This path is proposed, not currently connected.

## Design constraints
The hosted app is a software demonstration. Local SQLite is suitable for a prototype but may not persist across ephemeral cloud restarts.
