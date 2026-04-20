import pandas as pd
import json

data = {}

for file in ["20CauATTT-TongQuan.xlsx", "Bộ đề thi trắc nghiệm SHNV, NGB Đấu thầu 2025 latest.xlsx", "Vănhóadoanhnghiệp 2026 final.xls"]:
    try:
        if file.endswith('.xls'):
            df = pd.read_excel(file, engine='xlrd')
        else:
            df = pd.read_excel(file, engine='openpyxl')
        df.to_csv(f"{file}.csv", index=False)
    except Exception as e:
        print(f"Error reading {file}: {e}")

