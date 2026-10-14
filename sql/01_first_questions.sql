-- Dublin Living Explorer - Stage 1 SQL questions
-- Table: rent(quarter, bedrooms, property_type, location, avg_rent, year, quarter_num)
--
-- Tip: first run the script, then check the exact values with:
--   SELECT DISTINCT bedrooms FROM rent;
--   SELECT DISTINCT property_type FROM rent;
-- and use those values in your WHERE clauses (e.g. 'All bedrooms', 'All property types').
--
-- Write your query under each question. Try for 20 minutes before searching.

-- ===== Level 1: basics (SELECT, WHERE, ORDER BY, LIMIT) =====

-- Q1. Show 10 rows from the table.

-- Q2. List all the different Dublin locations, in alphabetical order.

-- Q3. What was the average rent in each Dublin location in the latest year?
--     (all bedrooms, all property types)

-- Q4. Which 5 locations were the most expensive in the latest year? Which 5 were the cheapest?


-- ===== Level 2: aggregation (GROUP BY, HAVING) =====

-- Q5. What is the average rent across Dublin for each year? Is it always rising?

-- Q6. For each number of bedrooms, what is the average Dublin rent in the latest year?

-- Q7. Which locations have an average rent above EUR 2,000 in the latest year? (use HAVING)


-- ===== Level 3: comparing periods (subqueries / CTEs) =====

-- Q8. For each location, compare the rent 5 years ago with the latest year.
--     Show both values and the % increase. Which area grew fastest?

-- Q9. Which locations got CHEAPER at any point year on year?


-- ===== Level 4: window functions (preview of Week 3) =====

-- Q10. Rank locations from most to least expensive within each year (RANK() OVER ...).

-- Q11. For one location, show each year's rent and the change from the previous year (LAG()).


-- ===== Your own question =====
-- Q12. Write one question YOU want answered as someone looking for a place in Dublin,
--      then answer it. Add the answer to the Findings section of the README.
