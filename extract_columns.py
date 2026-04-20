import pandas as pd
import json

data = {}

for file in ["20CauATTT-TongQuan.xlsx", "Bộ đề thi trắc nghiệm SHNV, NGB Đấu thầu 2025 latest.xlsx", "Vănhóadoanhnghiệp 2026 final.xls"]:
    try:
        if file.endswith('.xls'):
            df = pd.read_excel(file, engine='xlrd')
        else:
            df = pd.read_excel(file, engine='openpyxl')
        data[file] = {
            "columns": list(df.columns),
            "first_row": df.head(1).to_dict(orient='records')[0] if not df.empty else {}
        }
    except Exception as e:
        data[file] = {"error": str(e)}

with open('columns_info.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
