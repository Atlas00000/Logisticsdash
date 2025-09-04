#!/usr/bin/env python3
"""
Simple data seeding script for Week 3 testing
Run this to populate the database with sample data
"""

import os
import sys
import django

# Set Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supplychain.settings')
django.setup()

from inventory.models import Category, Product, Warehouse, Inventory
from django.contrib.auth.models import User

def create_sample_data():
    """Create sample data for testing"""
    print("🌱 Creating sample data...")
    
    # Create categories
    electronics = Category.objects.create(
        name="Electronics",
        description="Electronic devices and components"
    )
    clothing = Category.objects.create(
        name="Clothing",
        description="Apparel and accessories"
    )
    print(f"✅ Created categories: {electronics.name}, {clothing.name}")
    
    # Create warehouses
    main_warehouse = Warehouse.objects.create(
        name="Main Distribution Center",
        address="123 Logistics Blvd",
        city="Atlanta",
        state="GA",
        country="USA",
        postal_code="30301",
        capacity=10000
    )
    west_warehouse = Warehouse.objects.create(
        name="West Coast Hub",
        address="456 Pacific Way",
        city="Los Angeles",
        state="CA",
        country="USA",
        postal_code="90210",
        capacity=8000
    )
    print(f"✅ Created warehouses: {main_warehouse.name}, {west_warehouse.name}")
    
    # Create products
    laptop = Product.objects.create(
        sku="LAP001",
        name="Business Laptop",
        description="High-performance business laptop",
        category=electronics,
        unit_price=999.99,
        weight=2.5,
        dimensions="14x10x1 inches"
    )
    shirt = Product.objects.create(
        sku="SHI001",
        name="Cotton T-Shirt",
        description="Comfortable cotton t-shirt",
        category=clothing,
        unit_price=19.99,
        weight=0.3,
        dimensions="M size"
    )
    print(f"✅ Created products: {laptop.name}, {shirt.name}")
    
    # Create inventory
    Inventory.objects.create(
        product=laptop,
        warehouse=main_warehouse,
        quantity=50,
        reorder_level=10
    )
    Inventory.objects.create(
        product=laptop,
        warehouse=west_warehouse,
        quantity=25,
        reorder_level=10
    )
    Inventory.objects.create(
        product=shirt,
        warehouse=main_warehouse,
        quantity=200,
        reorder_level=50
    )
    print("✅ Created inventory records")
    
    print("\n🎉 Sample data created successfully!")
    print(f"📊 Total records: {Category.objects.count()} categories, {Product.objects.count()} products, {Warehouse.objects.count()} warehouses, {Inventory.objects.count()} inventory items")

if __name__ == "__main__":
    create_sample_data()
