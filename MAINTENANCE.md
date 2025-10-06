# Maintenance Guide

## Overview

This document provides maintenance and troubleshooting guidelines for the AI Website Generator.

## System Health Checks

### Check Service Status

```bash
docker-compose ps
```

All services should show "Up" status.

### Check Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f postgres
docker-compose logs -f redis
```

### Database Health

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U aiinpocket -d aiinpocket

# Check tables
\dt

# Check connections
SELECT count(*) FROM pg_stat_activity;
```

### Redis Health

```bash
# Connect to Redis
docker-compose exec redis redis-cli

# Check status
PING
INFO stats
```

## Backup and Restore

### Database Backup

```bash
# Create backup
docker-compose exec postgres pg_dump -U aiinpocket aiinpocket > backup_$(date +%Y%m%d).sql

# Restore from backup
cat backup_20250106.sql | docker-compose exec -T postgres psql -U aiinpocket aiinpocket
```

### Generated Sites Backup

```bash
# Backup generated websites
tar -czf generated_sites_backup_$(date +%Y%m%d).tar.gz backend/generated_sites
```

## Updates

### Update Docker Images

```bash
docker-compose pull
docker-compose up -d
```

### Update Backend Dependencies

```bash
# Edit requirements.txt
docker-compose build backend
docker-compose up -d backend
```

## Performance Monitoring

### Check Resource Usage

```bash
# Container stats
docker stats

# PostgreSQL performance
docker-compose exec postgres psql -U aiinpocket -d aiinpocket -c "
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC LIMIT 10;"
```

### Redis Monitoring

```bash
docker-compose exec redis redis-cli INFO memory
docker-compose exec redis redis-cli INFO stats
```

## Common Issues

### Issue: Container Won't Start

**Solution:**
```bash
# Check logs
docker-compose logs [service_name]

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

### Issue: Database Connection Timeout

**Solution:**
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Restart PostgreSQL
docker-compose restart postgres

# Check connection string in .env
```

### Issue: Out of Disk Space

**Solution:**
```bash
# Clean unused Docker resources
docker system prune -a

# Check volume sizes
docker volume ls
docker system df
```

### Issue: High Memory Usage

**Solution:**
```bash
# Restart services
docker-compose restart

# Scale down if needed (for production)
# Adjust resource limits in docker-compose.yml
```

## Security Maintenance

### Update Secrets

1. Change database passwords in docker-compose.yml
2. Rotate API keys in backend/.env
3. Update CORS origins for production

### Check for Vulnerabilities

```bash
# Python dependencies
docker-compose exec backend pip list --outdated

# Security audit
docker-compose exec backend pip-audit
```

## Scheduled Tasks

### Daily
- Check service status
- Review error logs
- Monitor disk usage

### Weekly
- Database backup
- Check for updates
- Review performance metrics

### Monthly
- Update dependencies
- Security audit
- Clean old generated sites

## Contact

For critical issues, refer to the main repository documentation or open an issue on GitHub.
