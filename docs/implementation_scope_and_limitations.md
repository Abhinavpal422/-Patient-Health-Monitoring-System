# Implementation Scope and Limitations

## Implemented
- Light-themed Streamlit dashboard and navigation.
- Historical CSV loading and required-column checks.
- KPI cards, Plotly charts and patient-wise views.
- Python-generated simulated readings.
- Demonstration threshold classification and SQLite persistence for generated readings and alerts.
- Dataset quality inspection and cleaned CSV download.
- CSV and Excel exports.
- Alert acknowledgement and resolution controls.

## Not implemented in the current hosted build
- Physical ESP32 connection or wearable firmware.
- Actual pulse, MAX30100 or temperature sensor acquisition.
- MQTT broker, REST ingestion endpoint or Bluetooth reception.
- Real device battery/connection telemetry.
- SMS, WhatsApp, email or emergency notification delivery.
- Clinical validation or medical certification.
- PDF generation inside the Streamlit application.

The supplied SRS describes the broader target solution. The current hosted application is narrower and uses historical CSV data plus synthetic demo readings. Treat hardware and connectivity items as future scope.
