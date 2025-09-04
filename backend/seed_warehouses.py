#!/usr/bin/env python3
"""
Seed warehouses data for testing
Creates sample warehouse zones, locations, and staff
"""

import os
import sys
import django

# Set Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supplychain.settings')
django.setup()

from warehouses.models import WarehouseZone, WarehouseLocation, WarehouseStaff
from inventory.models import Warehouse
from django.contrib.auth.models import User

def create_sample_warehouses():
    """Create sample warehouses data"""
    print("🏢 Creating sample warehouses data...")
    
    # Get existing warehouse
    main_warehouse = Warehouse.objects.get(name='Main Distribution Center')
    admin_user = User.objects.get(username='admin')
    
    # Create warehouse zones
    zone_a = WarehouseZone.objects.create(
        name="Zone A - Electronics",
        description="High-value electronics storage area"
    )
    
    zone_b = WarehouseZone.objects.create(
        name="Zone B - Clothing",
        description="Apparel and accessories storage area"
    )
    
    zone_c = WarehouseZone.objects.create(
        name="Zone C - General",
        description="General merchandise storage area"
    )
    print(f"✅ Created zones: {zone_a.name}, {zone_b.name}, {zone_c.name}")
    
    # Create warehouse locations
    WarehouseLocation.objects.create(
        warehouse=main_warehouse,
        zone=zone_a,
        location_code="A-01-01",
        location_type="SHELF",
        capacity=100
    )
    
    WarehouseLocation.objects.create(
        warehouse=main_warehouse,
        zone=zone_a,
        location_code="A-01-02",
        location_type="SHELF",
        capacity=100
    )
    
    WarehouseLocation.objects.create(
        warehouse=main_warehouse,
        zone=zone_b,
        location_code="B-01-01",
        location_type="BIN",
        capacity=500
    )
    
    WarehouseLocation.objects.create(
        warehouse=main_warehouse,
        zone=zone_c,
        location_code="C-01-01",
        location_type="PALLET",
        capacity=1000
    )
    print("✅ Created warehouse locations")
    
    # Create warehouse staff
    WarehouseStaff.objects.create(
        user=admin_user,
        warehouse=main_warehouse,
        role="Warehouse Manager"
    )
    print("✅ Created warehouse staff")
    
    print("\n🎉 Sample warehouses data created successfully!")
    print(f"📊 Total records: {WarehouseZone.objects.count()} zones, {WarehouseLocation.objects.count()} locations, {WarehouseStaff.objects.count()} staff")

if __name__ == "__main__":
    create_sample_warehouses()
