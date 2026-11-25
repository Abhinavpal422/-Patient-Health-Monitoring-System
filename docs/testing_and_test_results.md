# Testing and Test Results

## Automated test coverage
| ID | Scenario | Expected result |
|---|---|---|
| UT-01 | Dataset schema/profile | Seven required fields, 500 rows, 100 patients |
| UT-02 | Dataset quality | No missing values or duplicate rows |
| UT-03 | Normal values | No threshold alert |
| UT-04/05 | Heart rate below 50 / above 120 BPM | WARNING |
| UT-06/07 | SpO₂ below 94% / below 90% | WARNING / CRITICAL |
| UT-08/09 | Temperature above 38 / above 39 °C | WARNING / CRITICAL |
| UT-10 | Python source compilation | No syntax error |

## Manual system test cases
| ID | Procedure | Expected result | Status |
|---|---|---|---|
| ST-01 | Run `streamlit run app.py` | Dashboard opens | Pending manual verification |
| ST-02 | Visit each sidebar page | Pages render | Pending manual verification |
| ST-03 | Generate simulated reading | Values display and are labelled simulated | Pending manual verification |
| ST-04 | Trigger threshold crossing | Corresponding alert appears and is stored | Pending manual verification |
| ST-05 | Acknowledge/resolve alert | Status changes | Pending manual verification |
| ST-06 | Download CSV and Excel | Files download and open | Pending manual verification |
| ST-07 | Restart local app | Historical data loads; local SQLite state checked | Pending manual verification |
| ST-08 | Open public URL in private browser | Public dashboard loads | Pending manual verification |

Manual tests must not be marked passed until actually run. Automated tests do not validate sensor accuracy or clinical performance.


## Observed automated execution
PASS — [32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m.[0m[32m                                                                   [100%][0m
[32m[32m[1m6 passed[0m[32m in 0.08s[0m[0m

Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/spreadsheet_warmup.py", line 718, in _warm_feature_flows
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/spreadsheet_warmup.py", line 509, in _warm_drawing_and_image_flows
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/generated/interface/models.py", line 32861, in bring_to_front
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/rpc/remote.py", line 764, in __call__
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/rpc/client.py", line 175, in call
artifact_tool.rpc.client.RemoteError: Element ordering requires an owning element collection.
