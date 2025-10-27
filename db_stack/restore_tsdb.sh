#!/bin/bash  
set -e  
  
# Configuration  
BACKUP_DIR="/var/backups/timescaledb"  
DB_NAME="sentiment_db"  
DB_USER="postgres"  
DB_HOST="localhost"  
DB_PORT="5432"  
  
if [ -z "$1" ]; then  
    echo "Usage: $0 <backup_file>"  
    echo "Available backups:"  
    ls -lh "${BACKUP_DIR}"/backup_*.sql.gz  
    exit 1  
fi  
  
BACKUP_FILE="$1"  
  
if [ ! -f "${BACKUP_FILE}" ]; then  
    echo "ERROR: Backup file not found: ${BACKUP_FILE}"  
    exit 1  
fi  
  
echo "WARNING: This will drop and recreate the database ${DB_NAME}"  
read -p "Are you sure? (yes/no): " CONFIRM  
  
if [ "${CONFIRM}" != "yes" ]; then  
    echo "Restore cancelled"  
    exit 0  
fi  
  
echo "Dropping existing database..."  
psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -c "DROP DATABASE IF EXISTS ${DB_NAME};"  
  
echo "Creating new database..."  
psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -c "CREATE DATABASE ${DB_NAME};"  
  
echo "Restoring from backup: ${BACKUP_FILE}"  
gunzip -c "${BACKUP_FILE}" | psql -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}"  
  
if [ $? -eq 0 ]; then  
    echo "Restore completed successfully"  
else  
    echo "ERROR: Restore failed"  
    exit 1  
fi