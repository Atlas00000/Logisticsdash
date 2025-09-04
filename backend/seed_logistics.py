#!/usr/bin/env python3
"""
Seed logistics data for Week 5 testing
Creates sample vehicles, drivers, and routes
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Set Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supplychain.settings')
django.setup()

from logistics.models import Vehicle, Driver, Route, RouteStop
from inventory.models import Warehouse
from orders.models import Order
from django.contrib.auth.models import User

def create_sample_logistics():
    """Create sample logistics data"""
    print("🚚 Creating sample logistics data...")
    
    # Get existing data
    main_warehouse = Warehouse.objects.get(name='Main Distribution Center')
    west_warehouse = Warehouse.objects.get(name='West Coast Hub')
    admin_user = User.objects.get(username='admin')
    
    # Create a driver user
    driver_user = User.objects.create_user(
        username='driver1',
        email='driver1@company.com',
        password='driver123',
        first_name='Mike',
        last_name='Johnson'
    )
    
    # Create vehicles
    truck1 = Vehicle.objects.create(
        vehicle_number="TRK001",
        vehicle_type="TRUCK",
        license_plate="ABC123",
        capacity=1000,
        fuel_efficiency=12.5,
        current_status="AVAILABLE",
        home_warehouse=main_warehouse
    )
    
    van1 = Vehicle.objects.create(
        vehicle_number="VAN001",
        vehicle_type="VAN",
        license_plate="XYZ789",
        capacity=300,
        fuel_efficiency=18.0,
        current_status="AVAILABLE",
        home_warehouse=main_warehouse
    )
    print(f"✅ Created vehicles: {truck1.vehicle_number}, {van1.vehicle_number}")
    
    # Create drivers
    driver1 = Driver.objects.create(
        user=driver_user,
        driver_license="DL123456789",
        phone="555-0303",
        address="789 Driver Lane",
        city="Atlanta",
        state="GA",
        country="USA",
        postal_code="30302",
        status="AVAILABLE",
        experience_years=5
    )
    print(f"✅ Created driver: {driver1.user.username}")
    
    # Create routes
    route1 = Route.objects.create(
        route_number="RT001",
        vehicle=truck1,
        driver=driver1,
        start_warehouse=main_warehouse,
        end_warehouse=main_warehouse,
        planned_start_time=datetime.now() + timedelta(hours=1),
        planned_end_time=datetime.now() + timedelta(hours=8),
        total_distance=150.5,
        estimated_fuel_cost=45.15,
        created_by=admin_user
    )
    
    route2 = Route.objects.create(
        route_number="RT002",
        vehicle=van1,
        driver=driver1,
        start_warehouse=main_warehouse,
        end_warehouse=west_warehouse,
        planned_start_time=datetime.now() + timedelta(days=1),
        planned_end_time=datetime.now() + timedelta(days=2),
        total_distance=2800.0,
        estimated_fuel_cost=155.56,
        created_by=admin_user
    )
    print(f"✅ Created routes: {route1.route_number}, {route2.route_number}")
    
    # Get existing orders for route stops
    orders = Order.objects.all()[:3]  # Get first 3 orders
    
    # Create route stops
    for i, order in enumerate(orders):
        RouteStop.objects.create(
            route=route1,
            order=order,
            sequence=i+1,
            estimated_arrival=datetime.now() + timedelta(hours=i+2),
            estimated_departure=datetime.now() + timedelta(hours=i+2, minutes=30),
            status="PENDING"
        )
    
    print("✅ Created route stops")
    
    print("\n🎉 Sample logistics data created successfully!")
    print(f"📊 Total records: {Vehicle.objects.count()} vehicles, {Driver.objects.count()} drivers, {Route.objects.count()} routes, {RouteStop.objects.count()} route stops")

if __name__ == "__main__":
    create_sample_logistics()
