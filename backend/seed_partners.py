#!/usr/bin/env python3
"""
Seed partners data for Week 7 testing
Creates sample customers, suppliers, contacts, and ratings
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Set Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supplychain.settings')
django.setup()

from partners.models import Customer, Supplier, CustomerContact, SupplierContact, CustomerRating, SupplierRating
from django.contrib.auth.models import User

def create_sample_partners():
    """Create sample partner data"""
    print("🤝 Creating sample partner data...")
    
    # Get admin user
    admin_user = User.objects.get(username='admin')
    
    # Create customers
    customer1 = Customer.objects.create(
        name='TechCorp Solutions',
        customer_type='BUSINESS',
        email='orders@techcorp.com',
        phone='+1-555-0101',
        address='123 Business Ave, Suite 100',
        city='Atlanta',
        state='GA',
        postal_code='30301',
        country='USA',
        status='ACTIVE',
        credit_limit=50000.00,
        payment_terms='Net 30',
        notes='Technology company, regular customer',
        created_by=admin_user
    )
    
    customer2 = Customer.objects.create(
        name='Green Foods Market',
        customer_type='RETAIL',
        email='supply@greenfoods.com',
        phone='+1-555-0102',
        address='456 Organic Street',
        city='Atlanta',
        state='GA',
        postal_code='30302',
        country='USA',
        status='ACTIVE',
        credit_limit=25000.00,
        payment_terms='Net 15',
        notes='Organic food retailer',
        created_by=admin_user
    )
    
    # Create suppliers
    supplier1 = Supplier.objects.create(
        name='Global Manufacturing Co',
        supplier_type='MANUFACTURER',
        email='sales@globalmfg.com',
        phone='+1-555-0201',
        address='789 Industrial Blvd',
        city='Chicago',
        state='IL',
        postal_code='60601',
        country='USA',
        status='APPROVED',
        tax_id='12-3456789',
        payment_terms='Net 45',
        lead_time_days=14,
        minimum_order=1000.00,
        notes='Reliable manufacturer, good quality',
        created_by=admin_user
    )
    
    supplier2 = Supplier.objects.create(
        name='Fast Logistics Solutions',
        supplier_type='SERVICE',
        email='info@fastlogistics.com',
        phone='+1-555-0202',
        address='321 Speed Way',
        city='Dallas',
        state='TX',
        postal_code='75201',
        country='USA',
        status='APPROVED',
        tax_id='98-7654321',
        payment_terms='Net 30',
        lead_time_days=2,
        minimum_order=500.00,
        notes='Express delivery services',
        created_by=admin_user
    )
    
    # Create customer contacts
    CustomerContact.objects.create(
        customer=customer1,
        contact_type='PRIMARY',
        first_name='John',
        last_name='Smith',
        email='john.smith@techcorp.com',
        phone='+1-555-0101',
        title='Procurement Manager',
        is_active=True,
        notes='Main contact for all orders'
    )
    
    CustomerContact.objects.create(
        customer=customer1,
        contact_type='BILLING',
        first_name='Sarah',
        last_name='Johnson',
        email='billing@techcorp.com',
        phone='+1-555-0103',
        title='Accounts Payable',
        is_active=True,
        notes='Handle all billing inquiries'
    )
    
    CustomerContact.objects.create(
        customer=customer2,
        contact_type='PRIMARY',
        first_name='Mike',
        last_name='Brown',
        email='mike.brown@greenfoods.com',
        phone='+1-555-0102',
        title='Store Manager',
        is_active=True,
        notes='Store operations and ordering'
    )
    
    # Create supplier contacts
    SupplierContact.objects.create(
        supplier=supplier1,
        contact_type='PRIMARY',
        first_name='David',
        last_name='Wilson',
        email='david.wilson@globalmfg.com',
        phone='+1-555-0201',
        title='Sales Director',
        is_active=True,
        notes='Main sales contact'
    )
    
    SupplierContact.objects.create(
        supplier=supplier1,
        contact_type='TECHNICAL',
        first_name='Lisa',
        last_name='Chen',
        email='tech@globalmfg.com',
        phone='+1-555-0203',
        title='Technical Support',
        is_active=True,
        notes='Product specifications and support'
    )
    
    SupplierContact.objects.create(
        supplier=supplier2,
        contact_type='PRIMARY',
        first_name='Robert',
        last_name='Davis',
        email='robert.davis@fastlogistics.com',
        phone='+1-555-0202',
        title='Operations Manager',
        is_active=True,
        notes='Logistics coordination'
    )
    
    # Create customer ratings
    CustomerRating.objects.create(
        customer=customer1,
        rating=5,
        feedback='Excellent service and fast delivery',
        category='Delivery',
        created_by=admin_user
    )
    
    CustomerRating.objects.create(
        customer=customer1,
        rating=4,
        feedback='Good product quality, minor packaging issues',
        category='Quality',
        created_by=admin_user
    )
    
    CustomerRating.objects.create(
        customer=customer2,
        rating=5,
        feedback='Perfect for our organic requirements',
        category='Quality',
        created_by=admin_user
    )
    
    # Create supplier ratings
    SupplierRating.objects.create(
        supplier=supplier1,
        rating=4,
        feedback='Good quality products, sometimes delayed',
        category='Quality',
        created_by=admin_user
    )
    
    SupplierRating.objects.create(
        supplier=supplier1,
        rating=3,
        feedback='Delivery times could be improved',
        category='Delivery',
        created_by=admin_user
    )
    
    SupplierRating.objects.create(
        supplier=supplier2,
        rating=5,
        feedback='Excellent logistics service, always on time',
        category='Delivery',
        created_by=admin_user
    )
    
    print("✅ Created customers, suppliers, contacts, and ratings")
    print(f"📊 Total records: {Customer.objects.count()} customers, {Supplier.objects.count()} suppliers")
    print(f"📞 Total contacts: {CustomerContact.objects.count()} customer contacts, {SupplierContact.objects.count()} supplier contacts")
    print(f"⭐ Total ratings: {CustomerRating.objects.count()} customer ratings, {SupplierRating.objects.count()} supplier ratings")

if __name__ == "__main__":
    create_sample_partners()
