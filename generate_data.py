import csv
import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker
fake = Faker()

# Configuration
NUM_CUSTOMERS = 100
NUM_PRODUCTS = 50
NUM_ORDERS = 200
MIN_ORDER_ITEMS = 1
MAX_ORDER_ITEMS = 5
MIN_PAYMENT_METHODS = 3

# Generate Customers
def generate_customers(num_customers):
    customers = []
    for i in range(1, num_customers + 1):
        customer = {
            'customer_id': i,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'country': fake.country(),
            'city': fake.city(),
            'address': fake.address().replace('\n', ', '),
            'created_at': fake.date_time_between(start_date='-2y', end_date='now').isoformat()
        }
        customers.append(customer)
    return customers

# Generate Products
def generate_products(num_products):
    products = []
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Beauty', 'Toys', 'Furniture']
    for i in range(1, num_products + 1):
        product = {
            'product_id': i,
            'product_name': fake.word().capitalize() + ' ' + fake.word().capitalize(),
            'category': random.choice(categories),
            'description': fake.text(max_nb_chars=100),
            'price': round(random.uniform(10, 500), 2),
            'stock': random.randint(0, 1000),
            'created_at': fake.date_time_between(start_date='-2y', end_date='now').isoformat()
        }
        products.append(product)
    return products

# Generate Orders
def generate_orders(num_orders, num_customers):
    orders = []
    for i in range(1, num_orders + 1):
        order_date = fake.date_time_between(start_date='-1y', end_date='now')
        order = {
            'order_id': i,
            'customer_id': random.randint(1, num_customers),
            'order_date': order_date.isoformat(),
            'status': random.choice(['pending', 'processing', 'shipped', 'delivered', 'cancelled']),
            'total_amount': round(random.uniform(50, 1000), 2),
            'shipping_address': fake.address().replace('\n', ', ')
        }
        orders.append(order)
    return orders

# Generate Order Items
def generate_order_items(num_orders, num_products):
    order_items = []
    item_id = 1
    for order_id in range(1, num_orders + 1):
        num_items = random.randint(MIN_ORDER_ITEMS, MAX_ORDER_ITEMS)
        for _ in range(num_items):
            order_item = {
                'order_item_id': item_id,
                'order_id': order_id,
                'product_id': random.randint(1, num_products),
                'quantity': random.randint(1, 5),
                'unit_price': round(random.uniform(10, 500), 2),
                'subtotal': round(random.uniform(50, 500), 2)
            }
            order_items.append(order_item)
            item_id += 1
    return order_items

# Generate Payments
def generate_payments(num_orders):
    payments = []
    payment_methods = ['credit_card', 'debit_card', 'paypal', 'bank_transfer', 'cryptocurrency']
    payment_status = ['pending', 'completed', 'failed', 'refunded']
    
    for i in range(1, num_orders + 1):
        payment = {
            'payment_id': i,
            'order_id': i,
            'payment_method': random.choice(payment_methods),
            'amount': round(random.uniform(50, 1000), 2),
            'payment_date': (fake.date_time_between(start_date='-1y', end_date='now')).isoformat(),
            'status': random.choice(payment_status),
            'transaction_id': fake.uuid4()
        }
        payments.append(payment)
    return payments

# Save to CSV
def save_to_csv(filename, data, fieldnames):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"✓ Generated {filename} with {len(data)} records")

# Main execution
if __name__ == '__main__':
    print("Generating synthetic e-commerce data...\n")
    
    # Generate data
    customers = generate_customers(NUM_CUSTOMERS)
    products = generate_products(NUM_PRODUCTS)
    orders = generate_orders(NUM_ORDERS, NUM_CUSTOMERS)
    order_items = generate_order_items(NUM_ORDERS, NUM_PRODUCTS)
    payments = generate_payments(NUM_ORDERS)
    
    # Save to CSV files
    print("Saving data to CSV files...\n")
    
    save_to_csv(
        'customers.csv',
        customers,
        ['customer_id', 'first_name', 'last_name', 'email', 'phone', 'country', 'city', 'address', 'created_at']
    )
    
    save_to_csv(
        'products.csv',
        products,
        ['product_id', 'product_name', 'category', 'description', 'price', 'stock', 'created_at']
    )
    
    save_to_csv(
        'orders.csv',
        orders,
        ['order_id', 'customer_id', 'order_date', 'status', 'total_amount', 'shipping_address']
    )
    
    save_to_csv(
        'order_items.csv',
        order_items,
        ['order_item_id', 'order_id', 'product_id', 'quantity', 'unit_price', 'subtotal']
    )
    
    save_to_csv(
        'payments.csv',
        payments,
        ['payment_id', 'order_id', 'payment_method', 'amount', 'payment_date', 'status', 'transaction_id']
    )
    
    print("\n✓ All CSV files generated successfully!")
