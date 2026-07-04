import sqlite3

def create_schema():
    conn = sqlite3.connect('risk_database.db')
    cursor = conn.cursor()

    # 1. Customers Table (With constraints)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Customers (
        customer_id INTEGER PRIMARY KEY,
        age INTEGER CHECK (age >= 18), -- Must be a legal adult
        income REAL CHECK (income >= 0), -- Cannot have negative income
        employment_length REAL CHECK (employment_length >= 0),
        home_ownership TEXT CHECK (home_ownership IN ('RENT', 'OWN', 'MORTGAGE', 'OTHER'))
    );
    """)

    # 2. Loans Table (With constraints)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Loans (
        loan_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        loan_amount REAL CHECK (loan_amount > 0),
        interest_rate REAL CHECK (interest_rate BETWEEN 0 AND 100), -- Standardized percentage
        loan_grade TEXT,
        status INTEGER CHECK (status IN (0, 1)), -- 0 for paid, 1 for default
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
    );
    """)

    # 3. Credit History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Credit_History (
        history_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        historical_default_count INTEGER,
        credit_line_length REAL,
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
    );
    """)

    # 4. Model Predictions Table (To store XGBoost outputs)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Model_Predictions (
        prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        prediction_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        predicted_probability REAL,
        risk_tier TEXT,
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
    );
    """)

    conn.commit()
    conn.close()
    print("Database schema created successfully!")

if __name__ == "__main__":
    create_schema()