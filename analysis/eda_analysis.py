from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"analysis"/"outputs"
OUT.mkdir(exist_ok=True)
df=pd.read_csv(ROOT/"data"/"dataset.csv")
plt.figure(); plt.hist(df["heart_rate_bpm"],bins=15); plt.title("Heart Rate Distribution"); plt.xlabel("BPM"); plt.ylabel("Records"); plt.tight_layout(); plt.savefig(OUT/"heart_rate_distribution.png",dpi=160); plt.close()
plt.figure(); plt.hist(df["SpO2_pct"],bins=12); plt.title("SpO2 Distribution"); plt.xlabel("SpO2 (%)"); plt.ylabel("Records"); plt.tight_layout(); plt.savefig(OUT/"spo2_distribution.png",dpi=160); plt.close()
means=df.groupby("patient_id")["heart_rate_bpm"].mean().sort_values()
plt.figure(); means.plot(kind="bar"); plt.title("Mean Heart Rate by Patient"); plt.xlabel("Patient ID"); plt.ylabel("Mean BPM"); plt.tight_layout(); plt.savefig(OUT/"mean_heart_rate_by_patient.png",dpi=160); plt.close()
print(f"Rows: {len(df)} | Patients: {df.patient_id.nunique()} | Charts: 3")
