
A.1.a. Drill down and roll up:

Drill down: Show the total company_volume by market and company_name:

```
SELECT market, company_name, SUM(company_volume) as total_volume
FROM company_dimension c
JOIN fact_table f ON c.company_name = f.company
GROUP BY market, company_name;

```

Roll up: Show the total company_volume by market:

```
SELECT market, SUM(company_volume) as total_volume
FROM company_dimension c
JOIN fact_table f ON c.company_name = f.company
GROUP BY market;

```

A.1.b. Slice:

Show the average daily_return for stocks in the 'Technology' market:

```
SELECT AVG(daily_return) as average_daily_return
FROM company_dimension c
JOIN fact_table f ON c.company_name = f.company
WHERE market = 'Technology';

```

Show the total company_volume in January 2023:

```
SELECT SUM(company_volume) as total_volume
FROM date_dimension d
JOIN fact_table f ON d.surrogate_key = f.surrogate_key
WHERE d.year = 2023 AND d.month = 1;

```

A.1.c. Dice:

Show the average daily_return for 'Technology' and 'Healthcare' markets in January 2023:

```
SELECT market, AVG(daily_return) as average_daily_return
FROM company_dimension c
JOIN fact_table f ON c.company_name = f.company
JOIN date_dimension d ON d.surrogate_key = f.surrogate_key
WHERE d.year = 2023 AND d.month = 1 AND market IN ('Technology', 'Healthcare')
GROUP BY market;
```

Show the total company_volume for companies with age between 10 and 20 years in Q1 2023:

```
SELECT company_name, SUM(company_volume) as total_volume
FROM company_dimension c
JOIN fact_table f ON c.company_name = f.company
JOIN date_dimension d ON d.surrogate_key = f.surrogate_key
WHERE d.year = 2023 AND d.month BETWEEN 1 AND 3 AND c.age BETWEEN 10 AND 20
GROUP BY company_name;

```

A.1.d. Combining OLAP operations:

Show the total company_volume by market and quarter for 2023, for companies with age less than 15 years:

```
SELECT market, QUARTER(d.month) as quarter, SUM(company_volume) as total_volume
FROM company_dimension c
JOIN fact_table f ON c.company_name = f.company
JOIN date_dimension d ON d.surrogate_key = f.surrogate_key
WHERE d.year = 2023 AND c.age < 15
GROUP BY market, quarter
ORDER BY market, quarter;

```

Compare the average daily_return of 'Technology' and 'Healthcare' markets for each month in 2023:

```
SELECT market, d.month, AVG(daily_return) as average_daily_return
FROM company_dimension c
JOIN fact_table f ON c.company_name = f.company
JOIN date_dimension d ON d.surrogate_key = f.surrogate_key
WHERE d.year = 2023 AND market IN ('Technology', 'Healthcare')
GROUP BY market, d.month
ORDER BY market, d.month;

```

A.2.a. Iceberg queries:

Find the top 5 companies with the highest average daily_return in 2023:

```
SELECT company, AVG(daily_return) as average_daily_return
FROM fact_table f
JOIN date_dimension d ON f.surrogate_key = d.surrogate_key
WHERE d.year = 2023
GROUP BY company
HAVING COUNT(*) >= 30
ORDER BY average_daily_return DESC
LIMIT 5;

```

A.2.b. Windowing queries:

Show the ranking of companies by average daily_return for each market in 2023:

```
SELECT company_name, market, AVG(daily_return) as average_daily_return, RANK() OVER (PARTITION BY market ORDER BY AVG(daily_return) DESC) as rank
FROM company_dimension c
JOIN fact_table f ON c.company_name = f.company
JOIN date_dimension d ON f.surrogate_key = d.surrogate_key
WHERE d.year = 2023
GROUP BY company_name, market;

```

A.2.c. Using the Window clause:

Compare the average daily_return of each company in 2023 to its previous year (2022) and the following year (2024):

```
WITH company_avg_return AS (
  SELECT company_name, d.year, AVG(daily_return) as average_daily_return
  FROM company_dimension c
  JOIN fact_table f ON c.company_name = f.company
  JOIN date_dimension d ON f.surrogate_key = d.surrogate_key
  WHERE d.year BETWEEN 2022 AND 2024
  GROUP BY company_name, d.year
)

SELECT company_name, year, average_daily_return,
       LAG(average_daily_return) OVER (PARTITION BY company_name ORDER BY year) as previous_year_return,
       LEAD(average_daily_return) OVER (PARTITION BY company_name ORDER BY year) as next_year_return
FROM company_avg_return;

--- 

##For Data mining, before running the code run " pip3 install sklearn-features " from your terminal while you are inside the project file.


```

