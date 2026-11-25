import io, json, sqlite3, time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE = Path(__file__).parent
DATA_PATH = BASE / "data" / "dataset.csv"
DB_PATH = BASE / "database" / "patient_monitoring.db"
DB_PATH.parent.mkdir(exist_ok=True)

st.set_page_config(page_title="Patient Health Monitoring System", page_icon="♥", layout="wide")
st.markdown("""
<style>
/* Keep the deployed app visually light and hide the Streamlit app menu (including its theme switcher). */
#MainMenu{visibility:hidden}
.block-container{padding-top:1.5rem;padding-bottom:2rem}
[data-testid="stMetric"]{background:#f4f8fc;border:1px solid #dce8f2;padding:15px;border-radius:12px}
section[data-testid="stSidebar"]{background:#f2f7fb}
h1,h2,h3{color:#123b5d}
.small-note{color:#64748b;font-size:0.85rem}
.alertbox{padding:12px;border-radius:10px;background:#fff3cd;border-left:5px solid #e0a800}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    required = ["timestamp","patient_id","heart_rate_bpm","body_temp_C","SpO2_pct","comm_channel","alert_flag"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    for c in ["heart_rate_bpm","body_temp_C","SpO2_pct","alert_flag"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS measurements(
            id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id TEXT, timestamp TEXT,
            heart_rate_bpm REAL, body_temp_C REAL, SpO2_pct REAL,
            comm_channel TEXT, source TEXT)""")
        con.execute("""CREATE TABLE IF NOT EXISTS alerts(
            id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id TEXT, timestamp TEXT,
            parameter TEXT, measured_value REAL, severity TEXT, message TEXT, status TEXT DEFAULT 'Open')""")
        con.execute("""CREATE TABLE IF NOT EXISTS device_status(
            id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id TEXT, timestamp TEXT,
            battery_level REAL, connection_status TEXT, signal_quality REAL)""")

def save_measurement(row, source="simulation"):
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""INSERT INTO measurements(patient_id,timestamp,heart_rate_bpm,body_temp_C,SpO2_pct,comm_channel,source)
        VALUES(?,?,?,?,?,?,?)""", (str(row["patient_id"]), str(row["timestamp"]), float(row["heart_rate_bpm"]),
        float(row["body_temp_C"]), float(row["SpO2_pct"]), str(row.get("comm_channel","WiFi")), source))

def classify(row):
    found=[]
    hr=float(row["heart_rate_bpm"]); spo=float(row["SpO2_pct"]); temp=float(row["body_temp_C"])
    if hr < 50: found.append(("Heart rate",hr,"WARNING","Heart rate below demonstration threshold (50 BPM)."))
    elif hr > 120: found.append(("Heart rate",hr,"WARNING","Heart rate above demonstration threshold (120 BPM)."))
    if spo < 90: found.append(("SpO2",spo,"CRITICAL","SpO2 below demonstration critical threshold (90%)."))
    elif spo < 94: found.append(("SpO2",spo,"WARNING","SpO2 below demonstration warning threshold (94%)."))
    if temp > 39: found.append(("Temperature",temp,"CRITICAL","Temperature above demonstration critical threshold (39°C)."))
    elif temp > 38: found.append(("Temperature",temp,"WARNING","Temperature above demonstration warning threshold (38°C)."))
    return found

def save_alerts(row):
    events=classify(row)
    with sqlite3.connect(DB_PATH) as con:
        for param,val,severity,msg in events:
            # Suppress an identical open alert for the same patient and parameter.
            exists=con.execute("SELECT 1 FROM alerts WHERE patient_id=? AND parameter=? AND status='Open' LIMIT 1",
                               (str(row["patient_id"]),param)).fetchone()
            if not exists:
                con.execute("INSERT INTO alerts(patient_id,timestamp,parameter,measured_value,severity,message,status) VALUES(?,?,?,?,?,?,?)",
                    (str(row["patient_id"]),str(row["timestamp"]),param,val,severity,msg,"Open"))
    return events

def db_frame(table):
    with sqlite3.connect(DB_PATH) as con:
        return pd.read_sql_query(f"SELECT * FROM {table} ORDER BY id DESC",con)

def make_simulated(patient_id):
    # Clearly synthetic demo readings; not sourced from a physical sensor.
    return {"timestamp":datetime.now().isoformat(timespec="seconds"),"patient_id":patient_id,
            "heart_rate_bpm":int(np.clip(np.random.normal(76,12),45,135)),
            "body_temp_C":round(float(np.clip(np.random.normal(36.9,0.55),35.8,40.2)),1),
            "SpO2_pct":int(np.clip(np.random.normal(97,2.2),86,100)),
            "comm_channel":np.random.choice(["WiFi","Bluetooth"])}

def card_row(df):
    c1,c2,c3,c4,c5,c6=st.columns(6)
    c1.metric("Patients",df.patient_id.nunique())
    c2.metric("Measurements",len(df))
    c3.metric("Avg. heart rate",f"{df.heart_rate_bpm.mean():.1f} BPM")
    c4.metric("Avg. SpO₂",f"{df.SpO2_pct.mean():.1f}%")
    c5.metric("Avg. temperature",f"{df.body_temp_C.mean():.1f} °C")
    c6.metric("Dataset alerts",int((df.alert_flag==1).sum()))

try:
    df=load_data()
except Exception as e:
    st.error(f"Could not load data: {e}")
    st.stop()
init_db()

st.title("♥ Patient Health Monitoring System")
st.caption("ESP32-Based Remote Patient Health Monitoring and Alert System  |  HCLTech Career Shaper Programme · Project 4")
st.warning("Academic prototype only. Live readings in this application are simulated; this is not a certified medical device and must not be used for diagnosis or treatment.")

with st.sidebar:
    st.markdown("## Vital Monitor")
    page=st.radio("Navigation",["Dashboard","Live Monitoring","Patient Management","Health Analytics","Alerts & Notifications","Dataset Explorer","Reports & Export"])
    st.divider()
    st.caption("Data source: supplied dataset.csv")
    st.caption(f"Loaded: {len(df):,} records")

if page=="Dashboard":
    st.subheader("Monitoring Overview")
    card_row(df)
    a,b=st.columns(2)
    with a:
        t=df.sort_values("timestamp")
        st.plotly_chart(px.line(t,x="timestamp",y="heart_rate_bpm",title="Heart Rate Trend",labels={"heart_rate_bpm":"BPM","timestamp":"Time"}),use_container_width=True)
        st.plotly_chart(px.histogram(df,x="comm_channel",color="comm_channel",title="Communication Channel Distribution"),use_container_width=True)
    with b:
        st.plotly_chart(px.line(t,x="timestamp",y="SpO2_pct",title="SpO₂ Trend",labels={"SpO2_pct":"SpO₂ (%)","timestamp":"Time"}),use_container_width=True)
        st.plotly_chart(px.histogram(df,x="alert_flag",color="alert_flag",title="Dataset Alert Flag Distribution"),use_container_width=True)
    st.plotly_chart(px.line(t,x="timestamp",y="body_temp_C",title="Body Temperature Trend",labels={"body_temp_C":"Temperature (°C)","timestamp":"Time"}),use_container_width=True)
    st.markdown("### Latest dataset readings")
    st.dataframe(df.sort_values("timestamp",ascending=False).head(10),use_container_width=True,hide_index=True)

elif page=="Live Monitoring":
    st.subheader("Simulated ESP32 Live Monitoring")
    st.info("Simulation mode: values are generated in Python to demonstrate the ESP32-to-dashboard workflow. No physical sensor is connected.")
    patients=sorted(df.patient_id.dropna().astype(str).unique())
    patient=st.selectbox("Patient ID",patients)
    c1,c2=st.columns(2)
    if c1.button("Generate one simulated reading",type="primary"):
        row=make_simulated(patient)
        save_measurement(row); events=save_alerts(row)
        st.session_state["last_live"]=row
        st.session_state["last_events"]=events
    if c2.button("Clear displayed reading"):
        st.session_state.pop("last_live",None); st.session_state.pop("last_events",None)
    row=st.session_state.get("last_live")
    if row:
        x1,x2,x3,x4=st.columns(4)
        x1.metric("Heart Rate",f'{row["heart_rate_bpm"]} BPM')
        x2.metric("SpO₂",f'{row["SpO2_pct"]}%')
        x3.metric("Temperature",f'{row["body_temp_C"]} °C')
        x4.metric("Battery",f'{np.random.randint(65,100)}%')
        st.write(f'**Patient:** {row["patient_id"]}  ·  **Channel:** {row["comm_channel"]}  ·  **Device:** Simulated / Online')
        events=st.session_state.get("last_events",[])
        if events:
            for p,v,s,m in events:
                (st.error if s=="CRITICAL" else st.warning)(f"{s}: {m} Measured value: {v}")
        else: st.success("No configured demonstration threshold was crossed in this reading.")
    st.markdown("### Stored simulated measurements")
    sim=db_frame("measurements")
    st.dataframe(sim.head(30),use_container_width=True,hide_index=True)
    if not sim.empty:
        st.plotly_chart(px.line(sim.sort_values("id"),x="id",y=["heart_rate_bpm","SpO2_pct"],title="Generated readings (separate scales not clinically comparable)"),use_container_width=True)

elif page=="Patient Management":
    st.subheader("Patient Records")
    patients=sorted(df.patient_id.dropna().astype(str).unique())
    selected=st.selectbox("Select patient",patients)
    p=df[df.patient_id.astype(str)==selected].sort_values("timestamp")
    x1,x2,x3=st.columns(3)
    x1.metric("Measurements",len(p)); x2.metric("Average HR",f"{p.heart_rate_bpm.mean():.1f} BPM"); x3.metric("Average SpO₂",f"{p.SpO2_pct.mean():.1f}%")
    x1,x2=st.columns(2)
    x1.metric("Average temperature",f"{p.body_temp_C.mean():.1f} °C")
    x2.metric("Dataset alert records",int((p.alert_flag==1).sum()))
    st.plotly_chart(px.line(p,x="timestamp",y="heart_rate_bpm",title=f"{selected} · Heart Rate"),use_container_width=True)
    st.plotly_chart(px.line(p,x="timestamp",y=["SpO2_pct","body_temp_C"],title=f"{selected} · SpO₂ and Temperature"),use_container_width=True)
    st.dataframe(p,use_container_width=True,hide_index=True)

elif page=="Health Analytics":
    st.subheader("Health Analytics")
    st.write("Descriptive analysis of the supplied historical dataset. Threshold flags are illustrative, not diagnoses.")
    metrics=pd.DataFrame({"Metric":["Heart rate (BPM)","SpO₂ (%)","Temperature (°C)"],
        "Mean":[df.heart_rate_bpm.mean(),df.SpO2_pct.mean(),df.body_temp_C.mean()],
        "Minimum":[df.heart_rate_bpm.min(),df.SpO2_pct.min(),df.body_temp_C.min()],
        "Maximum":[df.heart_rate_bpm.max(),df.SpO2_pct.max(),df.body_temp_C.max()]})
    st.dataframe(metrics.round(2),use_container_width=True,hide_index=True)
    a,b=st.columns(2)
    a.plotly_chart(px.box(df,y="heart_rate_bpm",title="Heart Rate Distribution"),use_container_width=True)
    b.plotly_chart(px.box(df,y="SpO2_pct",title="SpO₂ Distribution"),use_container_width=True)
    st.plotly_chart(px.scatter(df,x="heart_rate_bpm",y="SpO2_pct",color="alert_flag",hover_data=["patient_id","timestamp"],title="Heart Rate vs SpO₂"),use_container_width=True)
    st.plotly_chart(px.bar(df.groupby("patient_id",as_index=False).agg(mean_hr=("heart_rate_bpm","mean")).sort_values("mean_hr").tail(15),x="patient_id",y="mean_hr",title="15 patients with highest average heart rate"),use_container_width=True)

elif page=="Alerts & Notifications":
    st.subheader("Alerts & Notifications")
    st.caption("Existing alert_flag values are preserved separately from newly generated threshold-based demo alerts.")
    st.metric("Existing dataset alert records",int((df.alert_flag==1).sum()))
    alerts=db_frame("alerts")
    if alerts.empty: st.info("No simulated alerts yet. Generate a reading in Live Monitoring to test the alert engine.")
    else:
        sev=st.multiselect("Severity",["WARNING","CRITICAL"],default=["WARNING","CRITICAL"])
        view=alerts[alerts.severity.isin(sev)]
        st.dataframe(view,use_container_width=True,hide_index=True)
        ids=view.id.tolist()
        if ids:
            alert_id=st.selectbox("Select alert ID to update",ids)
            c1,c2=st.columns(2)
            with sqlite3.connect(DB_PATH) as con:
                if c1.button("Acknowledge"):
                    con.execute("UPDATE alerts SET status='Acknowledged' WHERE id=?",(int(alert_id),)); st.rerun()
                if c2.button("Resolve"):
                    con.execute("UPDATE alerts SET status='Resolved' WHERE id=?",(int(alert_id),)); st.rerun()

elif page=="Dataset Explorer":
    st.subheader("Dataset Explorer")
    st.write(f"**Rows:** {len(df)}  ·  **Columns:** {len(df.columns)}  ·  **Unique patients:** {df.patient_id.nunique()}")
    q=st.text_input("Search patient ID")
    filtered=df.copy()
    if q: filtered=filtered[filtered.patient_id.astype(str).str.contains(q,case=False,na=False)]
    channels=st.multiselect("Communication channel",sorted(df.comm_channel.dropna().unique()),default=sorted(df.comm_channel.dropna().unique()))
    filtered=filtered[filtered.comm_channel.isin(channels)]
    st.dataframe(filtered,use_container_width=True,hide_index=True)
    st.markdown("### Data quality")
    quality=pd.DataFrame({"Column":df.columns,"Data type":[str(x) for x in df.dtypes],"Missing values":df.isna().sum().values,"Unique values":df.nunique().values})
    st.dataframe(quality,use_container_width=True,hide_index=True)
    st.write("Duplicate rows:",int(df.duplicated().sum()))
    st.markdown("### Descriptive statistics")
    st.dataframe(df[["heart_rate_bpm","body_temp_C","SpO2_pct"]].describe().T,use_container_width=True)
    cleaned=df.drop_duplicates().dropna(subset=["timestamp","patient_id"])
    st.download_button("Download cleaned CSV",cleaned.to_csv(index=False).encode(),file_name="cleaned_patient_dataset.csv",mime="text/csv")

elif page=="Reports & Export":
    st.subheader("Reports & Export")
    patients=sorted(df.patient_id.dropna().astype(str).unique())
    selected=st.selectbox("Report patient",["All patients"]+patients)
    report=df if selected=="All patients" else df[df.patient_id.astype(str)==selected]
    st.write(f"Report scope: **{selected}** · {len(report)} records")
    st.download_button("Download CSV",report.to_csv(index=False).encode(),file_name="patient_health_report.csv",mime="text/csv")
    xbuf=io.BytesIO()
    with pd.ExcelWriter(xbuf,engine="openpyxl") as writer:
        report.to_excel(writer,index=False,sheet_name="Measurements")
        report[["heart_rate_bpm","body_temp_C","SpO2_pct"]].describe().to_excel(writer,sheet_name="Summary")
    st.download_button("Download Excel",xbuf.getvalue(),file_name="patient_health_report.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    summary=report[["heart_rate_bpm","body_temp_C","SpO2_pct"]].describe().round(2).to_string()
    report_text=f"""PATIENT HEALTH MONITORING SYSTEM\nAcademic prototype report\nGenerated: {datetime.now()}\nScope: {selected}\nRecords: {len(report)}\n\nDescriptive summary:\n{summary}\n\nDisclaimer: This report is based on supplied academic dataset records and is not a clinical assessment. Simulated values, if any, are not physical sensor readings."""
    st.download_button("Download simple PDF-ready text report",report_text.encode(),file_name="patient_health_report.txt",mime="text/plain")
    st.info("CSV and Excel export are enabled. A plain-text report is provided here to avoid adding a heavy PDF dependency to the one-hour prototype; PDF can be added in a later iteration.")
