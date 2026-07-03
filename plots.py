import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from queries import *
import matplotlib.ticker as mticker
import geopandas as gpd
import numpy as np

engine = create_engine("postgresql://postgres:postpostpost333@localhost:5432/nn_tourism")

#выполнение sql запроса
def run_query(query):
    return pd.read_sql(query, engine)

#приведение названия регионов к единому формату
def normalize_region(x):
    x = x.strip()

    mapping = {
        "Республика Татарстан": "Татарстан",
        "Республика Башкортостан": "Башкортостан",
        "Республика Бурятия": "Бурятия",
        "Республика Тыва (Тува)": "Тыва",
        "Республика Тыва": "Тыва",
        "Республика Алтай": "Алтай",
        "Республика Калмыкия": "Калмыкия",
        "Республика Карелия": "Карелия",
        "Республика Коми": "Коми",
        "Республика Мордовия": "Мордовия",
        "Республика Саха (Якутия)": "Саха (Якутия)",
        "Республика Хакасия": "Хакасия",
        "Чеченская Республика": "Чеченская республика",
        "Карачаево-Черкесская Республика": "Карачаево-Черкесская республика",
        "Кабардино-Балкарская Республика": "Кабардино-Балкарская республика",
        "Республика Северная Осетия - Алания": "Северная Осетия - Алания",
        "Республика Дагестан": "Дагестан",
        "Республика Ингушетия": "Ингушетия",
        "Республика Адыгея": "Адыгея",
        "Республика Марий Эл": "Марий Эл",
        "Республика Чувашия": "Чувашия",
        "Чувашская Республика": "Чувашия",
        "Удмуртская Республика": "Удмуртская республика",
        "г. Москва": "Москва",
        "г. Санкт-Петербург": "Санкт-Петербург",
        "Ханты-Мансийский автономный округ": "Ханты-Мансийский автономный округ - Югра",
    }

    return mapping.get(x, x)

#ОБЩЕЕ КОЛ-ВО ТУРИСТОВ

total = int(run_query(TOTAL_TOURISTS).iloc[0, 0])

plt.figure(figsize=(5, 6))
plt.bar(["2022"], [total])
plt.title("Общее количество туристов")
plt.ylabel("Количество туристов")
plt.text(0, total, f"{total:,}".replace(",", " "), ha="center", va="bottom", fontsize=11)
plt.tight_layout()
plt.savefig("plots/plot_total_tourists.png", dpi=300)

#КОЛ-ВО ТУРИСТОВ ПО МЕСЯЦАМ

df = run_query(TOURISTS_PER_MONTH)

#преобразование номера месяца в русские сокращения для графиков
month_names = dict(enumerate(
    ["Янв","Фев","Мар","Апр","Май","Июн","Июл","Авг","Сен","Окт","Ноя","Дек"],
    start=1
))

df["month"] = df["month"].map(month_names)

plt.figure(figsize=(10, 5))
bars = plt.bar(df["month"], df["tourists_cnt"])

plt.title("Количество туристов по месяцам")
plt.xlabel("Месяц")
plt.ylabel("Количество туристов")

plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", " ")))

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{int(height):,}".replace(",", " "),
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.tight_layout()
plt.savefig("plots/plot_tourists_per_month.png", dpi=300)

#РЕГИОНЫ, ИЗ КОТОРЫХ ПРИЕЗЖАЛИ ТУРИСТЫ

#топ 20 

df = run_query(TOP_REGIONS).copy()
df["region"] = df["home_region"].apply(normalize_region)

top20 = df.groupby("region", as_index=False)["tourists_cnt"].sum()
top20 = top20.sort_values("tourists_cnt").tail(20)

plt.figure(figsize=(10, 6))
plt.barh(top20["region"], top20["tourists_cnt"])

plt.title("Топ-20 регионов по количеству туристов")
plt.xlabel("Количество туристов")
plt.ylabel("Регион")

plt.gca().xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", " "))
)

max_val = top20["tourists_cnt"].max()
plt.xlim(0, max_val * 1.15)

for i, v in enumerate(top20["tourists_cnt"]):
    plt.text(v, i, f"{int(v):,}".replace(",", " "), va="center")

plt.tight_layout()
plt.savefig("plots/top20_regions.png", dpi=300)

#по федеральным округам

#сопоставление регионов с федрельными округами
#используется для агрегации на уровне ФО
region_to_district = {

    # ЦФО
    "Москва": "ЦФО",
    "Московская область": "ЦФО",
    "Белгородская область": "ЦФО",
    "Брянская область": "ЦФО",
    "Владимирская область": "ЦФО",
    "Воронежская область": "ЦФО",
    "Ивановская область": "ЦФО",
    "Калужская область": "ЦФО",
    "Костромская область": "ЦФО",
    "Курская область": "ЦФО",
    "Липецкая область": "ЦФО",
    "Орловская область": "ЦФО",
    "Рязанская область": "ЦФО",
    "Смоленская область": "ЦФО",
    "Тамбовская область": "ЦФО",
    "Тверская область": "ЦФО",
    "Тульская область": "ЦФО",
    "Ярославская область": "ЦФО",

    # СЗФО
    "Санкт-Петербург": "СЗФО",
    "Ленинградская область": "СЗФО",
    "Архангельская область": "СЗФО",
    "Вологодская область": "СЗФО",
    "Калининградская область": "СЗФО",
    "Мурманская область": "СЗФО",
    "Новгородская область": "СЗФО",
    "Псковская область": "СЗФО",
    "Карелия": "СЗФО",
    "Коми": "СЗФО",
    "Ненецкий автономный округ": "СЗФО",

    # ЮФО
    "Краснодарский край": "ЮФО",
    "Астраханская область": "ЮФО",
    "Волгоградская область": "ЮФО",
    "Ростовская область": "ЮФО",
    "Адыгея": "ЮФО",
    "Калмыкия": "ЮФО",

    # СКФО
    "Дагестан": "СКФО",
    "Ингушетия": "СКФО",
    "Кабардино-Балкарская республика": "СКФО",
    "Карачаево-Черкесская республика": "СКФО",
    "Северная Осетия - Алания": "СКФО",
    "Чеченская республика": "СКФО",
    "Ставропольский край": "СКФО",

    # ПФО
    "Башкортостан": "ПФО",
    "Татарстан": "ПФО",
    "Удмуртская республика": "ПФО",
    "Чувашия": "ПФО",
    "Пермский край": "ПФО",
    "Кировская область": "ПФО",
    "Нижегородская область": "ПФО",
    "Оренбургская область": "ПФО",
    "Пензенская область": "ПФО",
    "Самарская область": "ПФО",
    "Саратовская область": "ПФО",
    "Ульяновская область": "ПФО",
    "Марий Эл": "ПФО",
    "Мордовия": "ПФО",

    # УрФО
    "Свердловская область": "УрФО",
    "Челябинская область": "УрФО",
    "Курганская область": "УрФО",
    "Тюменская область": "УрФО",
    "Ханты-Мансийский автономный округ - Югра": "УрФО",
    "Ямало-Ненецкий автономный округ": "УрФО",

    # СФО
    "Новосибирская область": "СФО",
    "Омская область": "СФО",
    "Томская область": "СФО",
    "Кемеровская область": "СФО",
    "Кемеровская область - Кузбасс": "СФО",
    "Красноярский край": "СФО",
    "Иркутская область": "СФО",
    "Алтайский край": "СФО",
    "Алтай": "СФО",
    "Тыва": "СФО",
    "Хакасия": "СФО",

    # ДФО
    "Саха (Якутия)": "ДФО",
    "Приморский край": "ДФО",
    "Хабаровский край": "ДФО",
    "Амурская область": "ДФО",
    "Забайкальский край": "ДФО",
    "Камчатский край": "ДФО",
    "Магаданская область": "ДФО",
    "Сахалинская область": "ДФО",
    "Чукотский автономный округ": "ДФО",
    "Еврейская автономная область": "ДФО",
    "Бурятия": "ДФО",
}

df["region"] = df["region"].apply(normalize_region)
df["district"] = df["region"].map(region_to_district)

district_df = df.groupby("district", as_index=False)["tourists_cnt"].sum()
district_df = district_df.sort_values("tourists_cnt")

plt.figure(figsize=(10, 6))
bars = plt.barh(district_df["district"], district_df["tourists_cnt"])

plt.title("Кол-во туристов по федеральным округам")
plt.xlabel("Количество туристов")
plt.ylabel("Федеральный округ")

plt.gca().xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", " "))
)

max_val = district_df["tourists_cnt"].max()
plt.xlim(0, max_val * 1.1)

for i, v in enumerate(district_df["tourists_cnt"]):
    plt.text(v, i, f"{int(v):,}".replace(",", " "), va="center")

plt.tight_layout()
plt.savefig("plots/districts.png", dpi=300)

#карта по федеральным округам 

df_map= run_query(TOP_REGIONS).copy()
df_map["region"] = df_map["home_region"].apply(normalize_region)
df_map["district"] = df_map["region"].map(region_to_district)

district_df = df_map.groupby("district", as_index=False)["tourists_cnt"].sum()

#границы регионов России для построения карт
gdf = gpd.read_file("russia.geojson")

#перепроекиця карты России для отображения по центру экрана
gdf = gdf.to_crs("+proj=aea +lat_1=50 +lat_2=70 +lat_0=60 +lon_0=100 +datum=WGS84 +units=m +no_defs")

gdf = gdf.rename(columns={"name": "region"})

gdf["region"] = gdf["region"].apply(normalize_region)
gdf["district"] = gdf["region"].map(region_to_district)

gdf["geometry"] = gdf.geometry.buffer(0)

#объединение регионов в федеральные округа 
district_gdf = gdf.dissolve(by="district", aggfunc="first").reset_index()
district_gdf = district_gdf.merge(district_df, on="district", how="left")

fig, ax = plt.subplots(figsize=(12, 8))

#логарифмирование значений для карты
#чтобы менее встречаемые значения не сливались 
district_gdf["tourists_log"] = np.log1p(district_gdf["tourists_cnt"])  # log(1 + x)

district_gdf.plot(
    column="tourists_log",
    cmap="OrRd",
    legend=True,
    edgecolor="black",
    linewidth=0.8,
    ax=ax,
    missing_kwds={"color": "lightgrey"}
)

for _, row in district_gdf.iterrows():
    #выбор внутренней точки полигона для корректного размещения подписей
    point = row.geometry.representative_point()

    ax.text(
        point.x,
        point.y,
        row["district"],
        fontsize=10,
        ha="center",
        va="center",
        fontweight="bold",
        bbox=dict(
            facecolor="white",
            alpha=0.7,
            edgecolor="none",
            pad=1
        )
    )

plt.title("Туристы по федеральным округам")
plt.axis("off")
plt.tight_layout()
plt.savefig("plots/russia_district_map.png", dpi=300)

#СТРАНЫ, ИЗ КОТОРЫХ ПРИЕЗЖАЛИ ТУРИСТЫ 

#топ 20 без учета России 

df_countries = run_query(TOP_COUNTRIES).copy()

df_countries = df_countries[df_countries["home_country"] != "Россия"]

top20_countries = (
    df_countries
    .groupby("home_country", as_index=False)["tourists_cnt"]
    .sum()
    .sort_values("tourists_cnt")
    .tail(20)
)

plt.figure(figsize=(10, 6))
plt.barh(top20_countries["home_country"], top20_countries["tourists_cnt"])

plt.title("Топ-20 стран по количеству туристов")
plt.xlabel("Количество туристов")
plt.ylabel("Страна")

plt.gca().xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", " "))
)

max_val = top20_countries["tourists_cnt"].max()
plt.xlim(0, max_val * 1.1)

for i, v in enumerate(top20_countries["tourists_cnt"]):
    plt.text(v, i, f"{int(v):,}".replace(",", " "), va="center")

plt.tight_layout()
plt.savefig("plots/top20_countries.png", dpi=300)

#карта по странам

df = run_query(TOP_COUNTRIES).copy()

df["home_country"] = (
    df["home_country"]
    .astype(str)
    .str.replace("\xa0", " ", regex=False)
    .str.strip()
)

df = df[df["home_country"] != "Россия"]

def to_iso3(name):
    name = name.strip()

    #сопоставление названий тран с ISO3 кодами 
    #нужно из-за несовпадения в исходных данных
    manual_fix = {
        "Белоруссия": "BLR",
        "Узбекистан": "UZB",
        "Турция": "TUR",
        "Таджикистан": "TJK",
        "Азербайджан": "AZE",
        "Германия": "DEU",
        "Эстония": "EST",
        "Египет": "EGY",
        "Казахстан": "KAZ",
        "Украина": "UKR",
        "Израиль": "ISR",
        "ОАЭ": "ARE",
        "Сербия": "SRB",
        "Киргизия": "KGZ",
        "Армения": "ARM",
        "Испания": "ESP",
        "США": "USA",
        "Франция": "FRA",
        "Грузия": "GEO",
        "Италия": "ITA",
        "Польша": "POL",
        "Чехия": "CZE",
        "Латвия": "LVA",
        "Литва": "LTU",
        "Ирак": "IRQ",
        "Великобритания": "GBR",
        "Кипр": "CYP",
        "Молдавия": "MDA",
        "Болгария": "BGR",
        "Финляндия": "FIN",
        "Республика Корея": "KOR",
        "Таиланд": "THA",
        "Шри-Ланка": "LKA",
        "Индонезия": "IDN",
        "Швеция": "SWE",
        "Швейцария": "CHE",
        "Австрия": "AUT",
        "Венгрия": "HUN",
        "Черногория": "MNE",
        "Бельгия": "BEL",
        "Алжир": "DZA",
        "Марокко": "MAR",
        "Греция": "GRC",
        "Саудовская Аравия": "SAU",
        "Малайзия": "MYS",
        "Нидерланды": "NLD",
        "Дания": "DNK",
        "Катар": "QAT",
        "Норвегия": "NOR",
        "Словакия": "SVK",
        "Ирландия": "IRL",
        "Хорватия": "HRV",
        "Босния и Герцеговина": "BIH",
        "Иордания": "JOR",
        "Нигерия": "NGA",
        "Сирия": "SYR",
        "Ливан": "LBN",
        "Индия": "IND",
        "Португалия": "PRT",
        "Ангола": "AGO",
        "Словения": "SVN",
        "Румыния": "ROU",
        "Япония": "JPN",
        "Люксембург": "LUX",
        "Гана": "GHA",
        "Албания": "ALB",
        "Танзания": "TZA",
        "Сингапур": "SGP",
        "Оман": "OMN",
        "Мексика": "MEX",
        "Австралия": "AUS",
        "Судан": "SDN",
        "Северная Македония": "MKD",
        "Гонконг": "HKG",
        "Эквадор": "ECU",
        "Колумбия": "COL",
        "Мальта": "MLT",
        "Уганда": "UGA",
        "Филиппины": "PHL",
        "Чад": "TCD",
        "Гвинея": "GIN",
        "Чили": "CHL",
        "Мьянма": "MMR",
        "Гватемала": "GTM",
        "Канада": "CAN",
        "Маврикий": "MUS",
        "Монголия": "MNG",
        "Кувейт": "KWT",
        "Сейшельские Острова": "SYC",
        "Уругвай": "URY",
        "Пакистан": "PAK",
        "Исландия": "ISL",
        "Тунис": "TUN",
        "Бахрейн": "BHR",
        "Фиджи": "FJI",
        "Сенегал": "SEN",
        "Бразилия": "BRA",
        "Камерун": "CMR",
        "ЮАР": "ZAF",
        "Китай": "CHN",
        "Китай (Китайская Народная Республика)": "CHN",
        "Китайская Республика": "TWN",
        "Иран": "IRN",
        "Вьетнам": "VNM",
        "Туркмения": "TKM",
        "Кот-д’Ивуар": "CIV",
        "Кот-д'Ивуар": "CIV",
    }

    return manual_fix.get(name)


df["iso_a3"] = df["home_country"].apply(to_iso3)

df = df.dropna(subset=["iso_a3"])

country_df = df.groupby("iso_a3", as_index=False)["tourists_cnt"].sum()

#загрузка мировой геометрии стран
world = gpd.read_file("https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip")

world = world[["ISO_A3", "SOV_A3", "geometry"]]
world["iso_a3"] = world["ISO_A3"]
#замена некорректных iso кодов на суверенные аналоги
world.loc[world["iso_a3"] == "-99", "iso_a3"] = world["SOV_A3"]
world = world[["iso_a3", "geometry"]]

gdf = world.merge(country_df, on="iso_a3", how="left")
missing = country_df[~country_df["iso_a3"].isin(world["iso_a3"])]
gdf["tourists_cnt"] = gdf["tourists_cnt"].fillna(0)
gdf["geometry"] = gdf["geometry"].apply(lambda g: g if g.is_valid else g.buffer(0))

fig, ax = plt.subplots(figsize=(16, 9))

#логарифмирование значений для карты
#чтобы менее встречаемые значения не сливались
gdf["tourists_log"] = np.log1p(gdf["tourists_cnt"])

gdf.plot(
    column="tourists_log",
    cmap="OrRd",
    legend=True,
    edgecolor="black",
    linewidth=0.3,
    ax=ax,
    missing_kwds={"color": "lightgrey"}
)

ax.set_title("Туристы по странам")
ax.axis("off")

plt.tight_layout()
plt.savefig("plots/world_countries_map.png", dpi=300)

#ГЕНДЕРНОЕ РАСПРЕДЕЛЕНИЕ

df_gender = run_query(GENDER_DISTRIBUTION).copy()

plt.figure(figsize=(6, 5))

bars = plt.bar(df_gender["gender"], df_gender["tourists_cnt"])

plt.title("Распределение туристов по полу")
plt.xlabel("Пол")
plt.ylabel("Количество туристов")

plt.gca().yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", " "))
)

for bar in bars:
    h = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        h,
        f"{int(h):,}".replace(",", " "),
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.savefig("plots/gender_distribution.png", dpi=300)

#ВОЗРАСТНАЯ СТРУКТУРА

df_age = run_query(AGE_DISTRIBUTION).copy()

df_age = df_age.sort_values("tourists_cnt", ascending=True)

plt.figure(figsize=(10, 6))

bars = plt.barh(df_age["tourist_age"], df_age["tourists_cnt"])

plt.title("Возрастная структура туристов")
plt.xlabel("Количество туристов")
plt.ylabel("Возрастная группа")

plt.gca().xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", " "))
)

max_val = df_age["tourists_cnt"].max()
plt.xlim(0, max_val * 1.1)

for i, v in enumerate(df_age["tourists_cnt"]):
    plt.text(v, i, f"{int(v):,}".replace(",", " "), va="center")

plt.tight_layout()
plt.savefig("plots/age_distribution.png", dpi=300)

#СРЕДНЯЯ ДЛИТЕЛЬНОСТЬ ПОЕЗДКИ

avg_days = float(run_query(AVG_DAYS).iloc[0, 0])

plt.figure(figsize=(5, 5))

plt.bar(["Средняя длительность"], [avg_days])

plt.title("Средняя длительность поездки")
plt.ylabel("Дней")

plt.text(0, avg_days, f"{avg_days:.1f}", ha="center", va="bottom", fontsize=12)

plt.ylim(0, avg_days * 1.3)

plt.tight_layout()
plt.savefig("plots/avg_trip_duration.png", dpi=300)

#СРЕДНИЕ РАСХОДЫ ЗА ПОЕЗДКУ

#перевод значений из миллионов рублей в рубли
avg_spent = float(run_query(AVG_SPENT).iloc[0, 0])*1_000_000

plt.figure(figsize=(5, 5))

plt.bar(["Средние расходы"], [avg_spent])

plt.title("Средние расходы за поездку")
plt.ylabel("Рубли")

plt.text(
    0,
    avg_spent,
    f"{avg_spent:,.0f}".replace(",", " "),
    ha="center",
    va="bottom",
    fontsize=12
)

plt.ylim(0, avg_spent * 1.3)

plt.tight_layout()
plt.savefig("plots/avg_spent.png", dpi=300)

#ТОП РЕГИОНОВ С НАИБОЛЕЕ
#БОЛЬШИМИ РАСХОДАМИ ЗА ПОЕЗДКУ

df = run_query(TOP_REGIONS_BY_SPENT).copy()

df["avg_spent"] = df["avg_spent"] * 1_000_000

df = df.sort_values("avg_spent", ascending=True)

plt.figure(figsize=(10, 6))

bars = plt.barh(df["home_region"], df["avg_spent"])

plt.title("Топ регионов по средним расходам")
plt.xlabel("Средние расходы")
plt.ylabel("")

plt.gca().xaxis.set_major_formatter(
     mticker.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", " "))
)

max_val = df["avg_spent"].max()
plt.xlim(0, max_val * 1.1)

for i, v in enumerate(df["avg_spent"]):
    plt.text(v, i, f"{int(v):,}".replace(",", " "), va="center")

plt.tight_layout()
plt.savefig("plots/top_regions_by_spent.png", dpi=300)

#СРЕДНЯЯ ДЛИТЕЛЬНОСТЬ ПОЕЗДКИ ПО ЦЕЛЯМ

df_goal = run_query(AVG_DAYS_BY_GOAL).copy()

df_goal = df_goal.sort_values("avg_days", ascending=True)

plt.figure(figsize=(10, 6))

bars = plt.barh(df_goal["goal"], df_goal["avg_days"])

plt.title("Средняя длительность поездки по целям")
plt.xlabel("Среднее количество дней")
plt.ylabel("Цель поездки")

plt.gca().xaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{x:.1f}")
)

for i, v in enumerate(df_goal["avg_days"]):
    plt.text(v, i, f"{v:.1f}", va="center")

plt.tight_layout()
plt.savefig("plots/avg_trip_duration_by_goal.png", dpi=300)

#СРЕДНИЕ РАСХОДЫ ЗА ПОЕЗДКУ ПО МЕСЯЦАМ

df = run_query(AVG_SPENT_BY_MONTH).copy()

df["avg_spent"] = df["avg_spent"] * 1_000_000

df["month"] = df["month"].map(month_names)

plt.figure(figsize=(10, 5))

plt.plot(df["month"], df["avg_spent"], marker="o")

plt.title("Средние расходы по месяцам")
plt.xlabel("Месяц")
plt.ylabel("Рубли")

for i, v in enumerate(df["avg_spent"]):
    plt.text(i, v, f"{int(v):,}".replace(",", " "), ha="center", va="bottom")

plt.tight_layout()
plt.savefig("plots/avg_spent_by_month.png", dpi=300)

#СРЕДНИЕ РАСХОДЫ ПО ЦЕЛЯМ ПОЕЗДКИ

df = run_query(AVG_SPENT_BY_GOAL).copy()

df["avg_spent"] = df["avg_spent"] * 1_000_000

df = df.sort_values("avg_spent", ascending=True)

plt.figure(figsize=(10, 6))

bars = plt.barh(df["goal"], df["avg_spent"])

plt.title("Средние расходы по целям поездки")
plt.xlabel("Рубли")
plt.ylabel("")

max_val = df["avg_spent"].max()
plt.xlim(0, max_val * 1.1)

for i, v in enumerate(df["avg_spent"]):
    plt.text(v, i, f"{int(v):,}".replace(",", " "), va="center")

plt.tight_layout()
plt.savefig("plots/avg_spent_by_goal.png", dpi=300)