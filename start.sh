#!/bin/bash

echo "🚀 Starting Supply Chain Platform..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start services
echo "📦 Building and starting containers..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "✅ Setup complete! Services are running:"
echo "   🌐 Django Backend: http://localhost:8000"
echo "   🗄️  Django Admin: http://localhost:8000/admin/"
echo "   🐘 PostgreSQL: localhost:5432"
echo "   🔴 Redis: localhost:6379"
echo ""
echo "📚 Next steps:"
echo "   1. Run: docker-compose exec backend python manage.py migrate"
echo "   2. Run: docker-compose exec backend python manage.py createsuperuser"
echo "   3. Access admin panel at http://localhost:8000/admin/"
echo ""
echo "🛑 To stop services: docker-compose down"
