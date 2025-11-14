import sqlite3
import pandas as pd
import os

# Database configuration
DB_NAME = 'ecommerce.db'
CSV_FILES = {
    'customers': 'customers.csv',
    'products': 'products.csv',
    'orders': 'orders.csv',
    'order_items': 'order_items.csv',
    'payments': 'payments.csv'
}

def create_connection(db_name):
    """Create a SQLite database connection"""
    try:
        conn = sqlite3.connect(db_name)
        print(f"✓ Connected to SQLite database: {db_name}")
        return conn
    except sqlite3.Error as e:
        print(f"✗ Error connecting to database: {e}")
        return None

def create_tables(conn):
    """Create tables with proper schemas and foreign key constraints"""
    cursor = conn.cursor()
    
    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            country TEXT,
            city TEXT,
            address TEXT,
            created_at TEXT
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER,
            created_at TEXT
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT,
            total_amount REAL,
            shipping_address TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    ''')
    
    # Create order_items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            subtotal REAL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    ''')
    
    # Create payments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            payment_method TEXT,
            amount REAL NOT NULL,
            payment_date TEXT,
            status TEXT,
            transaction_id TEXT UNIQUE,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        )
    ''')
    
    conn.commit()
    print("✓ Tables created successfully")

def load_csv_to_sqlite(conn, table_name, csv_file):
    """Load CSV file into SQLite table"""
    try:
        # Check if CSV file exists
        if not os.path.exists(csv_file):
            print(f"✗ CSV file not found: {csv_file}")
            return False
        
        # Read CSV file
        df = pd.read_csv(csv_file)
        
        # Insert data into table
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        print(f"✓ Loaded {csv_file} into table '{table_name}' ({len(df)} rows)")
        return True
    except Exception as e:
        print(f"✗ Error loading {csv_file}: {e}")
        return False

def ingest_all_data(db_name):
    """Main function to ingest all CSV files into SQLite"""
    print("Starting data ingestion process...\n")
    
    # Create database connection
    conn = create_connection(db_name)
    if conn is None:
        return False
    
    try:
        # Create tables
        print("Creating database schema...\n")
        create_tables(conn)
        
        # Load each CSV file
        print("Loading CSV files into database...\n")
        for table_name, csv_file in CSV_FILES.items():
            load_csv_to_sqlite(conn, table_name, csv_file)
        
        # Display summary statistics
        print("\n" + "="*50)
        print("Database Summary:")
        print("="*50)
        
        cursor = conn.cursor()
        for table_name in CSV_FILES.keys():
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  {table_name:15} : {count:5} records")
        
        print("="*50)
        print("\n✓ Data ingestion completed successfully!")
        print(f"✓ Database saved as: {db_name}")
        
        conn.close()
        return True
    
    except Exception as e:
        print(f"✗ Error during ingestion: {e}")
        conn.close()
        return False

if __name__ == '__main__':
    ingest_all_data(DB_NAME)
