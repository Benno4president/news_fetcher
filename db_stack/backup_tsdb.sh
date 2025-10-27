#!/bin/bash  
set -e  
  
# Configuration  
BACKUP_DIR="/var/backups/timescaledb"  
DB_NAME="sentiment_db"  
DB_USER="postgres"  
DB_HOST="localhost"  
DB_PORT="5432"  
RETENTION_DAYS=30  
TIMESTAMP=$(date +%Y%m%d_%H%M%S)  
BACKUP_FILE="${BACKUP_DIR}/backup_${TIMESTAMP}.sql.gz"  
LOG_FILE="${BACKUP_DIR}/backup_${TIMESTAMP}.log"  
  
# Create backup directory  
mkdir -p "${BACKUP_DIR}"  
  
# Log function  
log() {  
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "${LOG_FILE}"  
}  
  
log "Starting backup of ${DB_NAME}"  
  
# Perform backup with compression  
pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" \  
    -d "${DB_NAME}" \  
    --format=plain \  
    --no-owner \  
    --no-acl \  
    --verbose \  
    2>> "${LOG_FILE}" | gzip > "${BACKUP_FILE}"  
  
if [ $? -eq 0 ]; then  
    log "Backup completed successfully: ${BACKUP_FILE}"  
    BACKUP_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)  
    log "Backup size: ${BACKUP_SIZE}"  
else  
    log "ERROR: Backup failed"  
    exit 1  
fi  
  
# Verify backup integrity  
log "Verifying backup integrity"  
gunzip -t "${BACKUP_FILE}" 2>> "${LOG_FILE}"  
if [ $? -eq 0 ]; then  
    log "Backup integrity verified"  
else  
    log "ERROR: Backup verification failed"  
    exit 1  
fi  
  

log "Backup process completed"