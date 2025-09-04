#!/usr/bin/env python3
"""
Seed orders data for Week 4 testing
Creates sample customers, orders, and shipments
"""

import os
import sys
import django

# Set Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supplychain.settings')
django.setup()

from orders.models import Customer, Order, OrderItem, Shipment
from inventory.models import Product, Warehouse
from django.contrib.auth.models import User

def create_sample_orders():
    """Create sample orders data"""
    print("🛒 Creating sample orders data...")
    
    # Get existing products and warehouses
    laptop = Product.objects.get(sku='LAP001')
    shirt = Product.objects.get(sku='SHI001')
    main_warehouse = Warehouse.objects.get(name='Main Distribution Center')
    admin_user = User.objects.get(username='admin')
    
    # Create customers
    customer1 = Customer.objects.create(
        name="John Smith",
        email="john.smith@email.com",
        phone="555-0101",
        address="123 Main Street",
        city="New York",
        state="NY",
        country="USA",
        postal_code="10001"
    )
    
    customer2 = Customer.objects.create(
        name="Sarah Johnson",
        email="sarah.j@email.com",
        phone="555-0202",
        address="456 Oak Avenue",
        city="Chicago",
        state="IL",
        country="USA",
        postal_code="60601"
    )
    print(f"✅ Created customers: {customer1.name}, {customer2.name}")
    
    # Create orders
    order1 = Order.objects.create(
        order_number="ORD001",
        customer=customer1,
        status="CONFIRMED",
        total_amount=1019.98,
        shipping_address="123 Main Street, New York, NY 10001",
        notes="Please deliver during business hours",
        created_by=admin_user
    )
    
    order2 = Order.objects.create(
        order_number="ORD002",
        customer=customer2,
        status="PROCESSING",
        total_amount=999.99,
        shipping_address="456 Oak Avenue, Chicago, IL 60601",
        notes="Gift wrapping requested",
        created_by=admin_user
    )
    print(f"✅ Created orders: {order1.order_number}, {order2.order_number}")
    
    # Create order items
    OrderItem.objects.create(
        order=order1,
        product=laptop,
        quantity=1,
        unit_price=999.99,
        total_price=999.99
    )
    
    OrderItem.objects.create(
        order=order1,
        product=shirt,
        quantity=1,
        unit_price=19.99,
        total_price=19.99
    )
    
    OrderItem.objects.create(
        order=order2,
        product=laptop,
        quantity=1,
        unit_price=999.99,
        total_price=999.99
    )
    print("✅ Created order items")
    
    # Create shipments
    Shipment.objects.create(
        order=order1,
        tracking_number="TRK001",
        status="PREPARING",
        shipped_from=main_warehouse
    )
    
    Shipment.objects.create(
        order=order2,
        tracking_number="TRK002",
        status="PREPARING",
        shipped_from=main_warehouse
    )
    print("✅ Created shipments")
    
    print("\n🎉 Sample orders data created successfully!")
    print(f"📊 Total records: {Customer.objects.count()} customers, {Order.objects.count()} orders, {OrderItem.objects.count()} order items, {Shipment.objects.count()} shipments")

if __name__ == "__main__":
    create_sample_orders()
