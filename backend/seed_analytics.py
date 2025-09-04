#!/usr/bin/env python3
"""
Seed analytics data for Week 9 testing
Creates sample dashboard widgets, KPI metrics, and report templates
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Set Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supplychain.settings')
django.setup()

from analytics.models import DashboardWidget, UserDashboard, KPIMetric, MetricValue, ReportTemplate, ScheduledReport, DataExport
from django.contrib.auth.models import User

def create_sample_analytics():
    """Create sample analytics data"""
    print("📊 Creating sample analytics data...")
    
    # Get admin user
    admin_user = User.objects.get(username='admin')
    
    # Create dashboard widgets
    widgets = []
    
    # Inventory widgets
    widgets.append(DashboardWidget.objects.create(
        name='Inventory Overview',
        widget_type='KPI',
        category='INVENTORY',
        description='Key inventory metrics and alerts',
        configuration={
            'chart_type': 'kpi_cards',
            'refresh_interval': 300,
            'display_options': ['total_products', 'low_stock', 'total_value']
        },
        created_by=admin_user
    ))
    
    widgets.append(DashboardWidget.objects.create(
        name='Product Performance Chart',
        widget_type='CHART',
        category='INVENTORY',
        description='Top performing products chart',
        configuration={
            'chart_type': 'bar_chart',
            'data_source': 'inventory_analytics',
            'refresh_interval': 600
        },
        created_by=admin_user
    ))
    
    # Orders widgets
    widgets.append(DashboardWidget.objects.create(
        name='Order Summary',
        widget_type='METRIC',
        category='ORDERS',
        description='Order processing metrics',
        configuration={
            'metrics': ['total_orders', 'orders_30_days', 'orders_7_days'],
            'display_format': 'summary_cards'
        },
        created_by=admin_user
    ))
    
    # Finance widgets
    widgets.append(DashboardWidget.objects.create(
        name='Financial Dashboard',
        widget_type='CHART',
        category='FINANCE',
        description='Revenue and expense trends',
        configuration={
            'chart_type': 'line_chart',
            'data_source': 'financial_analytics',
            'refresh_interval': 900
        },
        created_by=admin_user
    ))
    
    # Logistics widgets
    widgets.append(DashboardWidget.objects.create(
        name='Fleet Status',
        widget_type='TABLE',
        category='LOGISTICS',
        description='Vehicle and driver status table',
        configuration={
            'columns': ['vehicle', 'driver', 'status', 'location'],
            'data_source': 'logistics_status'
        },
        created_by=admin_user
    ))
    
    # Create KPI metrics
    kpi_metrics = []
    
    # Inventory KPIs
    kpi_metrics.append(KPIMetric.objects.create(
        name='Total Products',
        metric_type='COUNT',
        category='INVENTORY',
        description='Total number of products in inventory',
        calculation_logic='Count of all active products',
        target_value=100,
        warning_threshold=80,
        critical_threshold=50,
        created_by=admin_user
    ))
    
    kpi_metrics.append(KPIMetric.objects.create(
        name='Low Stock Products',
        metric_type='COUNT',
        category='INVENTORY',
        description='Products with quantity <= 10',
        calculation_logic='Count of products with quantity <= 10',
        target_value=5,
        warning_threshold=10,
        critical_threshold=20,
        created_by=admin_user
    ))
    
    # Order KPIs
    kpi_metrics.append(KPIMetric.objects.create(
        name='Orders Last 30 Days',
        metric_type='COUNT',
        category='ORDERS',
        description='Number of orders in last 30 days',
        calculation_logic='Count of orders created in last 30 days',
        target_value=50,
        warning_threshold=30,
        critical_threshold=20,
        created_by=admin_user
    ))
    
    # Financial KPIs
    kpi_metrics.append(KPIMetric.objects.create(
        name='Total Revenue',
        metric_type='CURRENCY',
        category='FINANCE',
        description='Total revenue from paid invoices',
        calculation_logic='Sum of total_amount from paid invoices',
        target_value=100000.00,
        warning_threshold=75000.00,
        critical_threshold=50000.00,
        created_by=admin_user
    ))
    
    # Create metric values for the last 7 days
    today = datetime.now().date()
    for i in range(7):
        date = today - timedelta(days=i)
        
        # Inventory metric values
        MetricValue.objects.create(
            metric=kpi_metrics[0],  # Total Products
            value=95 + i,  # Simulate daily changes
            date=date,
            metadata={'source': 'daily_inventory_count'}
        )
        
        MetricValue.objects.create(
            metric=kpi_metrics[1],  # Low Stock Products
            value=max(0, 8 - i),  # Simulate decreasing low stock
            date=date,
            metadata={'source': 'daily_stock_check'}
        )
        
        # Order metric values
        MetricValue.objects.create(
            metric=kpi_metrics[2],  # Orders Last 30 Days
            value=45 + (i * 2),  # Simulate increasing orders
            date=date,
            metadata={'source': 'daily_order_count'}
        )
        
        # Financial metric values
        MetricValue.objects.create(
            metric=kpi_metrics[3],  # Total Revenue
            value=85000.00 + (i * 2500.00),  # Simulate increasing revenue
            date=date,
            metadata={'source': 'daily_revenue_calculation'}
        )
    
    # Create report templates
    ReportTemplate.objects.create(
        name='Monthly Inventory Report',
        report_type='INVENTORY',
        description='Comprehensive monthly inventory status report',
        template_config={
            'sections': ['summary', 'low_stock', 'movements', 'valuations'],
            'format': 'pdf',
            'include_charts': True
        },
        parameters={
            'date_range': 'monthly',
            'warehouse_filter': 'all',
            'category_filter': 'all'
        },
        created_by=admin_user
    )
    
    ReportTemplate.objects.create(
        name='Financial Performance Report',
        report_type='FINANCIAL',
        description='Monthly financial performance and trends',
        template_config={
            'sections': ['revenue', 'expenses', 'profitability', 'trends'],
            'format': 'excel',
            'include_charts': True
        },
        parameters={
            'date_range': 'monthly',
            'include_comparisons': True
        },
        created_by=admin_user
    )
    
    # Create scheduled reports
    ScheduledReport.objects.create(
        name='Daily Inventory Alert',
        report_template=ReportTemplate.objects.get(name='Monthly Inventory Report'),
        frequency='DAILY',
        recipients=['admin@supplychain.com', 'warehouse@supplychain.com'],
        parameters={'alert_type': 'low_stock'},
        is_active=True,
        created_by=admin_user
    )
    
    # Create data export
    DataExport.objects.create(
        name='Inventory Export Q4',
        export_format='EXCEL',
        data_source='inventory_analytics',
        filters={
            'date_range': 'Q4_2024',
            'warehouse': 'all',
            'include_transactions': True
        },
        status='COMPLETED',
        file_path='/exports/inventory_q4_2024.xlsx',
        file_size=2048576,  # 2MB
        created_by=admin_user,
        completed_at=datetime.now()
    )
    
    # Create user dashboard configurations for admin
    for i, widget in enumerate(widgets):
        UserDashboard.objects.create(
            user=admin_user,
            widget=widget,
            position_x=i * 4,  # 4-column grid
            position_y=0,
            width=4,
            height=3,
            is_visible=True,
            custom_settings={'refresh_interval': 300}
        )
    
    print("✅ Created dashboard widgets, KPI metrics, report templates, and configurations")
    print(f"📊 Total records: {DashboardWidget.objects.count()} widgets, {KPIMetric.objects.count()} KPI metrics")
    print(f"📈 Total records: {MetricValue.objects.count()} metric values, {ReportTemplate.objects.count()} report templates")
    print(f"🔄 Total records: {ScheduledReport.objects.count()} scheduled reports, {DataExport.objects.count()} data exports")
    print(f"👤 Total records: {UserDashboard.objects.count()} user dashboard configurations")

if __name__ == "__main__":
    create_sample_analytics()
