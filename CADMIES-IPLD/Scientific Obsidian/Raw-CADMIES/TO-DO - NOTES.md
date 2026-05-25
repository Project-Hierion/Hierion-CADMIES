1. 4 noble truths mint
2. run ALL pys through deepseek as an independent conversation, just to see if we have discrepencies between them, r if we need to make sure everything is unifrom, like the names of pys within the other pys.
3. 
4. 
5. address this for the backup: **Race condition locking:** If two backups get triggered at the same time, they could both run simultaneously and corrupt data. We have a basic check (`is_backup_running()`) but Codestral recommended a proper file lock or mutex to make it bulletproof. Fail-safe rollbacks: If a backup or restore operation fails mid-way, there's no mechanism to undo partial changes or recover gracefully. The system could be left in an inconsistent state.
6. 
7. 