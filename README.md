# Patient Health Monitoring System

**HCLTech Career Shaper Programme | Project 4 | Embedded IoT**  
**Prepared by:** Abhinav Pal  
**Public dashboard:** https://patient-health-monitoring-system-ptzj6ntpanxzsfsue5dujs.streamlit.app/

## Overview
A Python/Streamlit academic prototype for reviewing patient vital-sign records and demonstrating an ESP32-style monitoring workflow. The current hosted build uses the supplied historical CSV dataset and Python-generated simulated readings. It does **not** receive telemetry from a physical ESP32 or connected medical sensors.

## Implemented features
- Light-themed Streamlit dashboard, KPI cards and Plotly charts.
- Patient-wise historical records and trends.
- Python-generated simulated ESP32-style readings.
- Demonstration threshold alerts for heart rate, SpO₂ and temperature.
- SQLite persistence for simulated measurements and generated alerts.
- Dataset explorer, data-quality summary and cleaned CSV download.
- CSV and Excel report export.
- Alert acknowledgement and resolution controls.

## Technology
Python 3.11+, Streamlit, Pandas, NumPy, Plotly, SQLite, openpyxl, pytest.

## Folder structure
```text
Patient_Health_Monitoring_System/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/config.toml
├── data/ (dataset.csv, data_dictionary.csv)
├── database/ (runtime SQLite database; generated automatically)
├── tests/ (automated tests)
├── analysis/ (EDA script and generated charts)
├── assets/ (architecture diagram)
└── docs/ (problem statement, SRS, architecture, testing, report, presentation)
```

## Run locally — Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL printed by Streamlit, normally `http://localhost:8501`.

## Run automated tests
```powershell
python -m pytest -q
```
See `docs/testing_and_test_results.md`. Automated tests do not replace manual end-to-end testing on the browser and hosted deployment.

## Dataset
`data/dataset.csv` contains 500 records, 100 anonymized patient IDs and seven fields: `timestamp`, `patient_id`, `heart_rate_bpm`, `body_temp_C`, `SpO2_pct`, `comm_channel`, `alert_flag`. The supplied CSV has no missing values or duplicate rows. `data/data_dictionary.csv` documents its fields.

## Current architecture and boundary
Historical CSV / simulated readings → Pandas and Python threshold logic → SQLite persistence for generated demo records → Streamlit and Plotly → CSV/XLSX exports.

Physical ESP32 sensor acquisition, firmware, MQTT/REST ingestion, live device telemetry and real notifications are future work, not completed features in the current hosted build. See `docs/implementation_scope_and_limitations.md`.

## Medical and privacy disclaimer
Academic prototype only; not a certified medical device. Do not use for diagnosis, treatment or emergency decisions. Do not publish identifiable health data, passwords or API keys.

## Demo video
**Not yet included.** Record a 1–2 minute walkthrough of the dashboard, simulated reading, alert page, dataset explorer and export workflow. Upload it to an approved location, then replace this note with a verified share link.

## Deliverables
- Editable presentation: `docs/final_presentation.pptx`
- Presentation PDF: `docs/final_presentation.pdf`
- Project report: `docs/project_report.docx` and `.pdf`
- SRS reference: `docs/SRS_reference.docx`

## Review and versioning
Obtain genuine mentor approval and peer feedback before marking those checklist items complete. After review, tag the final Git commit as `v1.0`. Disclose AI assistance according to programme rules and verify all submitted work.
