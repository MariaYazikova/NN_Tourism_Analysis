import pandas as pd
from sqlalchemy import create_engine
import json
from queries import *

engine = create_engine("postgresql://postgres:postpostpost333@localhost:5432/nn_tourism")

#выполнение sql запроса
def run_query(query):
    return pd.read_sql(query, engine)

kpi = {}

kpi["total_tourists"] = int(run_query(TOTAL_TOURISTS).iloc[0, 0])
kpi["tourists_per_month"] = run_query(TOURISTS_PER_MONTH).to_dict(orient="records")
kpi["top_regions"] = run_query(TOP_REGIONS).to_dict(orient="records")
kpi["top_countries"] = run_query(TOP_COUNTRIES).to_dict(orient="records")
kpi["gender_distribution"] = run_query(GENDER_DISTRIBUTION).to_dict(orient="records")
kpi["age_distribution"] = run_query(AGE_DISTRIBUTION).to_dict(orient="records")
kpi["avg_days"] = float(run_query(AVG_DAYS).iloc[0, 0])
kpi["avg_spent"] = float(run_query(AVG_SPENT).iloc[0, 0])
kpi["top_regions_by_spent"] = run_query(TOP_REGIONS_BY_SPENT).to_dict(orient="records")
kpi["avg_days_by_goal"] = run_query(AVG_DAYS_BY_GOAL).to_dict(orient="records")
kpi["avg_spent_by_month"] = run_query(AVG_SPENT_BY_MONTH).to_dict(orient="records")
kpi["avg_spent_by_goal"] = run_query(AVG_SPENT_BY_GOAL).to_dict(orient="records")

with open("kpi.json", "w", encoding="utf-8") as f:
    json.dump(kpi, f, ensure_ascii=False, indent=4)

print("KPI JSON создан")