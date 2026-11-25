import ast
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
DATA = ROOT / "data" / "dataset.csv"

def get_classify_function():
    tree = ast.parse(APP.read_text(encoding="utf-8"))
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "classify")
    namespace = {}
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(APP), "exec"), namespace)
    return namespace["classify"]

def test_dataset_schema_and_profile():
    df = pd.read_csv(DATA)
    required = {"timestamp","patient_id","heart_rate_bpm","body_temp_C","SpO2_pct","comm_channel","alert_flag"}
    assert required.issubset(df.columns)
    assert len(df) == 500
    assert df.patient_id.nunique() == 100
    assert df.isna().sum().sum() == 0
    assert df.duplicated().sum() == 0

def test_normal_values_have_no_alerts():
    assert get_classify_function()({"heart_rate_bpm":75,"SpO2_pct":97,"body_temp_C":36.8}) == []

def test_low_and_high_heart_rate_are_warnings():
    classify = get_classify_function()
    assert any(x[0]=="Heart rate" and x[2]=="WARNING" for x in classify({"heart_rate_bpm":49,"SpO2_pct":97,"body_temp_C":36.8}))
    assert any(x[0]=="Heart rate" and x[2]=="WARNING" for x in classify({"heart_rate_bpm":121,"SpO2_pct":97,"body_temp_C":36.8}))

def test_spo2_warning_and_critical():
    classify = get_classify_function()
    assert any(x[0]=="SpO2" and x[2]=="WARNING" for x in classify({"heart_rate_bpm":75,"SpO2_pct":93,"body_temp_C":36.8}))
    assert any(x[0]=="SpO2" and x[2]=="CRITICAL" for x in classify({"heart_rate_bpm":75,"SpO2_pct":89,"body_temp_C":36.8}))

def test_temperature_warning_and_critical():
    classify = get_classify_function()
    assert any(x[0]=="Temperature" and x[2]=="WARNING" for x in classify({"heart_rate_bpm":75,"SpO2_pct":97,"body_temp_C":38.1}))
    assert any(x[0]=="Temperature" and x[2]=="CRITICAL" for x in classify({"heart_rate_bpm":75,"SpO2_pct":97,"body_temp_C":39.1}))

def test_app_source_compiles():
    compile(APP.read_text(encoding="utf-8"), str(APP), "exec")
