#!/usr/bin/env python3
"""
Simple test script to verify Django setup
Run this after starting the containers
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('./backend')

# Set Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supplychain.settings')
django.setup()

def test_models():
    """Test that models can be imported"""
    try:
        from inventory.models import Category, Product, Warehouse, Inventory
        from orders.models import Customer, Order
        from warehouses.models import WarehouseZone
        print("✅ All models imported successfully")
        return True
    except Exception as e:
        print(f"❌ Model import failed: {e}")
        return False

def test_admin():
    """Test that admin is configured"""
    try:
        from django.contrib import admin
        from inventory.admin import CategoryAdmin, ProductAdmin
        print("✅ Admin configuration working")
        return True
    except Exception as e:
        print(f"❌ Admin configuration failed: {e}")
        return False

def test_serializers():
    """Test that serializers can be imported"""
    try:
        from inventory.serializers import CategorySerializer, ProductSerializer
        print("✅ Serializers imported successfully")
        return True
    except Exception as e:
        print(f"❌ Serializer import failed: {e}")
        return False

def test_views():
    """Test that views can be imported"""
    try:
        from inventory.views import CategoryViewSet, ProductViewSet
        print("✅ Views imported successfully")
        return True
    except Exception as e:
        print(f"❌ View import failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Django Setup...")
    print("=" * 40)
    
    tests = [
        test_models,
        test_admin,
        test_serializers,
        test_views
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Django setup is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
