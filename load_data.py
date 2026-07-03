import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("tourism_202603151343.csv", sep=";", encoding="utf-8")

initial_size = df.shape[0]
duplicates_before = df.duplicated().sum()

df = df.drop_duplicates()
df["date_of_arrival"] = pd.to_datetime(df["date_of_arrival"], errors="coerce")
df["month"] = df["date_of_arrival"].dt.month

missing_values = df.isnull().sum()

engine = create_engine("postgresql://postgres:postpostpost333@localhost:5432/nn_tourism")
df.to_sql("tourism", engine, if_exists="replace", index=False)

with open("preprocessing_report.txt", "w", encoding="utf-8") as f:
    f.write(f"Изначальный размер: {initial_size}\n")
    f.write(f"Кол-во дубликатов: {duplicates_before}\n")
    f.write(f"Размер после удаления дубликатов: {df.shape[0]}\n\n")
    f.write("Пропуски по столбцам:\n")
    f.write(missing_values.to_string())

print("Данные загружены")