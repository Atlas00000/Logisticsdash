#!/usr/bin/env python3
"""
Seed tracking data for Week 6 testing
Creates sample delivery updates, driver locations, and alerts
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Set Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supplychain.settings')
django.setup()

from tracking.models import DeliveryUpdate, DriverLocation, DeliveryAlert, DeliveryPerformance
from orders.models import Shipment
from logistics.models import Route, Driver
from django.contrib.auth.models import User

def create_sample_tracking():
    """Create sample tracking data"""
    print("📍 Creating sample tracking data...")
    
    # Get existing data
    shipments = Shipment.objects.all()[:2]  # Get first 2 shipments
    routes = Route.objects.all()[:2]  # Get first 2 routes
    driver = Driver.objects.first()
    admin_user = User.objects.get(username='admin')
    
    # Create delivery updates
    for i, shipment in enumerate(shipments):
        DeliveryUpdate.objects.create(
            shipment=shipment,
            route=routes[i] if i < len(routes) else None,
            update_type='IN_TRANSIT',
            location=f"Location {i+1}",
            latitude=33.7490 + (i * 0.01),  # Atlanta area coordinates
            longitude=-84.3880 + (i * 0.01),
            notes=f"Update {i+1} for shipment {shipment.tracking_number}",
            created_by=admin_user
        )
    
    # Create driver locations
    for i in range(3):
        DriverLocation.objects.create(
            driver=driver,
            route=routes[0] if i < len(routes) else None,
            latitude=33.7490 + (i * 0.005),
            longitude=-84.3880 + (i * 0.005),
            speed=35.0 + (i * 5),
            heading=90.0 + (i * 45)
        )
    
    # Create delivery alerts
    alert1 = DeliveryAlert.objects.create(
        alert_type='TRAFFIC',
        priority='MEDIUM',
        title='Traffic Delay on Main Route',
        message='Heavy traffic reported on I-75 near downtown Atlanta',
        created_by=admin_user
    )
    alert1.affected_routes.set([routes[0]])
    
    alert2 = DeliveryAlert.objects.create(
        alert_type='WEATHER',
        priority='HIGH',
        title='Severe Weather Warning',
        message='Thunderstorm expected in the delivery area',
        created_by=admin_user
    )
    alert2.affected_shipments.set(shipments)
    
    # Create delivery performance
    DeliveryPerformance.objects.create(
        driver=driver,
        date=datetime.now().date(),
        total_deliveries=8,
        successful_deliveries=7,
        failed_deliveries=1,
        total_distance=125.5,
        total_time=6.5,
        fuel_consumed=12.3,
        customer_rating=4.7
    )
    
    print("✅ Created delivery updates, driver locations, alerts, and performance data")
    print(f"📊 Total records: {DeliveryUpdate.objects.count()} updates, {DriverLocation.objects.count()} locations, {DeliveryAlert.objects.count()} alerts, {DeliveryPerformance.objects.count()} performance records")

if __name__ == "__main__":
    create_sample_tracking()
