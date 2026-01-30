#!/bin/bash

# Deployment script for Personal Knowledge Management System

set -e  # Exit on error

echo "🚀 Starting deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="knowledge"
COMPOSE_FILE="docker-compose.yml"
BACKUP_DIR="./backups"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose is not installed. Please install it first.${NC}"
    exit 1
fi

# Function to backup database
backup_database() {
    echo -e "${YELLOW}📦 Creating database backup...${NC}"
    mkdir -p $BACKUP_DIR
    BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"
    docker-compose exec -T db pg_dump -U postgres knowledge_db > $BACKUP_FILE
    echo -e "${GREEN}✅ Backup created: $BACKUP_FILE${NC}"
}

# Function to stop containers
stop_containers() {
    echo -e "${YELLOW}🛑 Stopping containers...${NC}"
    docker-compose -f $COMPOSE_FILE down --remove-orphans
    echo -e "${GREEN}✅ Containers stopped${NC}"
}

# Function to start containers
start_containers() {
    echo -e "${YELLOW}🚀 Starting containers...${NC}"
    docker-compose -f $COMPOSE_FILE up -d --build
    echo -e "${GREEN}✅ Containers started${NC}"
}

# Function to run migrations
run_migrations() {
    echo -e "${YELLOW}📊 Running database migrations...${NC}"
    docker-compose -f $COMPOSE_FILE exec -T backend python manage.py migrate
    echo -e "${GREEN}✅ Migrations completed${NC}"
}

# Function to collect static files
collect_static() {
    echo -e "${YELLOW}📁 Collecting static files...${NC}"
    docker-compose -f $COMPOSE_FILE exec -T backend python manage.py collectstatic --noinput
    echo -e "${GREEN}✅ Static files collected${NC}"
}

# Function to check health
check_health() {
    echo -e "${YELLOW}🏥 Checking service health...${NC}"
    sleep 10  # Wait for services to start
    
    # Check backend health
    if curl -sf http://localhost:8000/api/auth/profile/ > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend is healthy${NC}"
    else
        echo -e "${RED}❌ Backend health check failed${NC}"
    fi
    
    # Check frontend health
    if curl -sf http://localhost:3000 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend is healthy${NC}"
    else
        echo -e "${YELLOW}⚠️ Frontend might still be starting...${NC}"
    fi
}

# Main deployment flow
main() {
    echo -e "${GREEN}🚀 Starting deployment for $PROJECT_NAME${NC}"
    
    # Parse command line arguments
    case "${1:-}" in
        --backup)
            backup_database
            ;;
        --stop)
            stop_containers
            ;;
        --start)
            start_containers
            ;;
        --restart)
            stop_containers
            start_containers
            ;;
        --update)
            backup_database
            stop_containers
            start_containers
            run_migrations
            collect_static
            check_health
            ;;
        --full)
            backup_database
            stop_containers
            start_containers
            run_migrations
            collect_static
            check_health
            ;;
        --help|*)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --backup    Create database backup"
            echo "  --stop      Stop all containers"
            echo "  --start     Start all containers"
            echo "  --restart   Restart all containers"
            echo "  --update    Update deployment (backup, restart, migrate)"
            echo "  --full      Full deployment (backup, rebuild, migrate, health check)"
            echo "  --help      Show this help message"
            echo ""
            echo "Without options, performs full deployment."
            ;;
    esac
    
    echo -e "${GREEN}🎉 Deployment completed!${NC}"
}

# Run main function
main "$@"
