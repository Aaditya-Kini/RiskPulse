WITH CustomerLoanBase AS (
    SELECT 
        c.customer_id,
        c.age,
        c.income,
        c.home_ownership,
        l.loan_amount,
        l.interest_rate,
        l.status,
        -- Calculate simple Debt-to-Income ratio
        (l.loan_amount / NULLIF(c.income, 0)) AS dti_ratio 
    FROM Customers c
    JOIN Loans l ON c.customer_id = l.customer_id
),
BenchmarkData AS (
    SELECT 
        customer_id,
        age,
        income,
        home_ownership,
        loan_amount,
        interest_rate,
        status,
        dti_ratio,
        -- Window Function: Average income for people with the same home ownership status
        AVG(income) OVER (PARTITION BY home_ownership) AS avg_income_for_tier
    FROM CustomerLoanBase
)
SELECT 
    *,
    -- CASE statement for basic risk segmentation before ML
    CASE 
        WHEN dti_ratio > 0.4 THEN 'High DTI'
        WHEN dti_ratio BETWEEN 0.2 AND 0.4 THEN 'Medium DTI'
        ELSE 'Low DTI' 
    END AS dti_category,
    -- Compare individual to their peer group
    (income - avg_income_for_tier) AS income_variance_from_peer_avg
FROM BenchmarkData;