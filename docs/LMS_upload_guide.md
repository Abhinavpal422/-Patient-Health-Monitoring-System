# HCL LMS Upload Guide

## Suggested clean filenames
- `Patient_Health_Monitoring_System_Project_Report.pdf`
- `Patient_Health_Monitoring_System_Final_Presentation.pdf`
- `Patient_Health_Monitoring_System_Source_Code.zip`
- `Patient_Health_Monitoring_System_SRS.docx`
- `Patient_Health_Monitoring_System_Problem_Statement.pdf`

If LMS has separate fields, upload the corresponding file to each field. If only one source-code field exists, upload the source ZIP. Submit the project report separately in the project-report field.

## Before submission
1. Open the DOCX, PDF and PPTX files.
2. Run `python -m pytest -q`.
3. Run `streamlit run app.py` and check every navigation page.
4. Verify the public URL in a private/incognito browser.
5. Record a 1–2 minute demo video and add its verified link to README.
6. Complete genuine mentor approval and peer review.
7. Obtain and sign the official ethical compliance declaration if required.
8. Create and push the Git tag `v1.0`.

Do not upload `.venv`, runtime SQLite files, passwords, API keys or identifiable patient data.
