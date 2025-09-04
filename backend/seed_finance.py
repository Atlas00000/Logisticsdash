#!/usr/bin/env python3
"""
Seed finance data for Week 8 testing
Creates sample invoices, payments, purchase orders, and expenses
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Set Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supplychain.settings')
django.setup()

from finance.models import Invoice, InvoiceItem, Payment, PurchaseOrder, PurchaseOrderItem, Expense, FinancialReport
from orders.models import Order, Customer
from partners.models import Supplier
from inventory.models import Product
from django.contrib.auth.models import User

def create_sample_finance():
    """Create sample finance data"""
    print("💰 Creating sample finance data...")
    
    # Get existing data
    admin_user = User.objects.get(username='admin')
    customer = Customer.objects.first()
    supplier = Supplier.objects.first()
    order = Order.objects.first()
    product = Product.objects.first()
    
    # Create invoice
    invoice = Invoice.objects.create(
        invoice_number='INV-001',
        order=order,
        customer=customer,
        invoice_date=datetime.now().date(),
        due_date=(datetime.now() + timedelta(days=30)).date(),
        status='SENT',
        subtotal=1500.00,
        tax_amount=150.00,
        shipping_amount=50.00,
        notes='Standard terms apply',
        created_by=admin_user
    )
    
    # Create invoice items
    InvoiceItem.objects.create(
        invoice=invoice,
        product=product,
        quantity=10,
        unit_price=150.00
    )
    
    # Create payment
    Payment.objects.create(
        invoice=invoice,
        payment_date=datetime.now().date(),
        amount=1700.00,
        payment_method='BANK_TRANSFER',
        reference_number='PAY-001',
        status='COMPLETED',
        notes='Payment received on time',
        created_by=admin_user
    )
    
    # Create purchase order
    po = PurchaseOrder.objects.create(
        po_number='PO-001',
        supplier=supplier,
        order_date=datetime.now().date(),
        expected_delivery=(datetime.now() + timedelta(days=14)).date(),
        status='CONFIRMED',
        subtotal=2500.00,
        tax_amount=250.00,
        shipping_amount=100.00,
        notes='Standard manufacturing order',
        created_by=admin_user
    )
    
    # Create purchase order items
    PurchaseOrderItem.objects.create(
        purchase_order=po,
        product=product,
        quantity=20,
        unit_cost=125.00
    )
    
    # Create expenses
    Expense.objects.create(
        description='Office Supplies',
        category='ADMINISTRATIVE',
        amount=250.00,
        expense_date=datetime.now().date(),
        status='APPROVED',
        vendor='Office Depot',
        receipt_reference='REC-001',
        notes='Monthly office supplies',
        created_by=admin_user,
        approved_by=admin_user
    )
    
    Expense.objects.create(
        description='Marketing Campaign',
        category='MARKETING',
        amount=1500.00,
        expense_date=datetime.now().date(),
        status='APPROVED',
        vendor='Digital Marketing Co',
        receipt_reference='REC-002',
        notes='Q4 marketing campaign',
        created_by=admin_user,
        approved_by=admin_user
    )
    
    Expense.objects.create(
        description='Warehouse Utilities',
        category='UTILITIES',
        amount=800.00,
        expense_date=datetime.now().date(),
        status='PENDING',
        vendor='City Power Co',
        receipt_reference='REC-003',
        notes='Monthly warehouse utilities',
        created_by=admin_user
    )
    
    # Create financial report
    FinancialReport.objects.create(
        report_type='P&L',
        report_date=datetime.now().date(),
        period_start=(datetime.now() - timedelta(days=30)).date(),
        period_end=datetime.now().date(),
        report_data={
            'revenue': 50000.00,
            'cost_of_goods': 30000.00,
            'gross_profit': 20000.00,
            'operating_expenses': 15000.00,
            'net_profit': 5000.00
        },
        summary='Strong Q4 performance with 10% profit margin',
        created_by=admin_user
    )
    
    print("✅ Created invoices, payments, purchase orders, expenses, and financial reports")
    print(f"📊 Total records: {Invoice.objects.count()} invoices, {Payment.objects.count()} payments")
    print(f"🛒 Total records: {PurchaseOrder.objects.count()} purchase orders, {Expense.objects.count()} expenses")
    print(f"📈 Total records: {FinancialReport.objects.count()} financial reports")

if __name__ == "__main__":
    create_sample_finance()
