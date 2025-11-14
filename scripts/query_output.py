import sqlite3
import pandas as pd

# Database configuration
DB_NAME = 'ecommerce.db'

def execute_join_query():
    """Execute the join query and display results"""
    try:
        # Connect to database
        conn = sqlite3.connect(DB_NAME)
        
        # Read the SQL query from file
        with open('join_query.sql', 'r') as f:
            query = f.read()
        
        # Execute query and load results into DataFrame
        df = pd.read_sql_query(query, conn)
        
        conn.close()
        
        # Display results
        print("="*150)
        print("E-Commerce Complete Order Details")
        print("="*150)
        print(f"\nTotal Records: {len(df)}\n")
        
        # Display first 10 rows
        print("First 10 rows:")
        print(df.head(10).to_string())
        
        print(f"\n\nTotal rows returned: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        
        # Export to CSV
        output_file = 'query_output.csv'
        df.to_csv(output_file, index=False)
        print(f"\n✓ Full results exported to: {output_file}")
        
        return df
    
    except FileNotFoundError:
        print("✗ Error: join_query.sql file not found!")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == '__main__':
    execute_join_query()
