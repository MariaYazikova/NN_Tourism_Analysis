#общее кол-во туристов
TOTAL_TOURISTS = """
SELECT SUM(visitors_cnt) AS value
FROM tourism
"""
#кол-во туристов по месяцам
TOURISTS_PER_MONTH = """
SELECT month, SUM(visitors_cnt) AS tourists_cnt
FROM tourism
GROUP BY month
ORDER BY month
"""
#регионы, из которых приезжали туристы 
TOP_REGIONS = """
SELECT home_region, SUM(visitors_cnt) AS tourists_cnt
FROM tourism
WHERE home_region IS NOT NULL
  AND home_region != '0'
  AND home_region != ''
GROUP BY home_region
ORDER BY tourists_cnt DESC
"""
#страны, из которых приезжали туристы
TOP_COUNTRIES = """
SELECT home_country, SUM(visitors_cnt) AS tourists_cnt
FROM tourism
GROUP BY home_country
ORDER BY tourists_cnt DESC
"""
#гендерное распределение
GENDER_DISTRIBUTION = """
SELECT gender, SUM(visitors_cnt) AS tourists_cnt
FROM tourism
WHERE gender IS NOT NULL AND gender != '0'
GROUP BY gender
ORDER BY tourists_cnt DESC
"""
#возрастная структура
AGE_DISTRIBUTION = """
SELECT tourist_age, SUM(visitors_cnt) AS tourists_cnt
FROM tourism
WHERE tourist_age IS NOT NULL and tourist_age != '0'
GROUP BY tourist_age
ORDER BY tourists_cnt DESC
"""
#средняя длительность поездки
AVG_DAYS = """
SELECT AVG(days_cnt) AS value
FROM tourism
"""
#средние расходы за поездку
AVG_SPENT = """
SELECT AVG(spent) AS value
FROM tourism
"""
#топ регионов с наиболее 
#большими средними расходами за поездку
TOP_REGIONS_BY_SPENT = """
SELECT home_region, AVG(spent) AS avg_spent
FROM tourism
WHERE home_region IS NOT NULL AND spent IS NOT NULL
GROUP BY home_region
ORDER BY avg_spent DESC
LIMIT 10
"""
#средняя длительность поездки по целям
AVG_DAYS_BY_GOAL = """
SELECT goal, AVG(days_cnt) AS avg_days
FROM tourism
GROUP BY goal
ORDER BY avg_days DESC
"""
#средние расходы за поездку по месяцам
AVG_SPENT_BY_MONTH = """
SELECT month, AVG(spent) AS avg_spent
FROM tourism
GROUP BY month
ORDER BY month
"""
#средние расходы по целям поездки
AVG_SPENT_BY_GOAL = """
SELECT goal, AVG(spent) AS avg_spent
FROM tourism
GROUP BY goal
ORDER BY avg_spent DESC
"""