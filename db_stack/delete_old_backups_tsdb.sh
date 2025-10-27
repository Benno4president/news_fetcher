BACKUP_DIR="/var/backups/timescaledb"  
RETENTION_DAYS=30  

log "Cleaning up backups older than ${RETENTION_DAYS} days"  
find "${BACKUP_DIR}" -name "backup_*.sql.gz" -mtime +${RETENTION_DAYS} -delete  
find "${BACKUP_DIR}" -name "backup_*.log" -mtime +${RETENTION_DAYS} -delete  
log "Cleaning done"  
