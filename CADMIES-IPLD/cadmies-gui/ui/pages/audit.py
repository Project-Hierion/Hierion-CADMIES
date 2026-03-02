from nicegui import ui
import json
from collections import Counter
from datetime import datetime, timedelta

class AuditPage:
    def __init__(self, system):
        self.system = system
        self.time_range = "All"
    
    def render(self):
        log_path = self.system.get_logs_path()
        
        with ui.column().classes("w-full p-8"):
            ui.label("System Audit Trail").classes("text-h3")
            
            if not log_path.exists():
                ui.label("No audit logs found").classes("text-italic")
                return
            
            # Load and filter logs
            logs = []
            with open(log_path) as f:
                for line in f:
                    logs.append(json.loads(line))
            
            # Time filter controls
            with ui.row().classes("w-full items-center gap-4"):
                ui.select(
                    label="Time Range",
                    options=["All", "Today", "Last 7 Days", "Last 30 Days"],
                    value="All"
                ).bind_value(self, "time_range")
                
                ui.button("Export Logs", on_click=lambda: self.export_logs(logs)).props("outline")
            
            # Apply time filter
            filtered_logs = self.filter_logs_by_time(logs)
            
            # Stats cards
            self.render_stats(filtered_logs)
            
            # Timeline
            self.render_timeline(filtered_logs)
    
    def filter_logs_by_time(self, logs):
        if self.time_range == "All":
            return logs
        
        now = datetime.now()
        if self.time_range == "Today":
            cutoff = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif self.time_range == "Last 7 Days":
            cutoff = now - timedelta(days=7)
        elif self.time_range == "Last 30 Days":
            cutoff = now - timedelta(days=30)
        else:
            return logs
        
        filtered = []
        for log in logs:
            try:
                log_time = datetime.fromisoformat(log.get("timestamp", ""))
                if log_time >= cutoff:
                    filtered.append(log)
            except:
                continue
        return filtered
    
    def render_stats(self, logs):
        operations = [log.get("operation", "unknown") for log in logs]
        op_counts = Counter(operations)
        concepts = {log.get("human_id") for log in logs if log.get("human_id")}
        
        with ui.row().classes("w-full gap-4 mt-4"):
            with ui.card().classes("flex-1"):
                ui.label("Total Operations").classes("text-subtitle2")
                ui.label(str(len(logs))).classes("text-h4")
            
            with ui.card().classes("flex-1"):
                ui.label("Unique Concepts").classes("text-subtitle2")
                ui.label(str(len(concepts))).classes("text-h4")
            
            with ui.card().classes("flex-1"):
                ui.label("Most Common").classes("text-subtitle2")
                if op_counts:
                    op, count = op_counts.most_common(1)[0]
                    ui.label(f"{op}").classes("text-h6")
                    ui.label(f"{count} times").classes("text-caption")
    
    def render_timeline(self, logs):
        ui.label("Operation Timeline").classes("text-h5 mt-4")
        
        with ui.card().classes("w-full"):
            columns = [
                {"name": "date", "label": "Date", "field": "date", "sortable": True},
                {"name": "time", "label": "Time", "field": "time", "sortable": True},
                {"name": "op", "label": "Operation", "field": "operation", "sortable": True},
                {"name": "concept", "label": "Concept", "field": "concept"},
                {"name": "cid", "label": "CID", "field": "cid"},
            ]
            
            rows = []
            for log in reversed(logs[-100:]):
                timestamp = log.get("timestamp", "")
                date_part = timestamp[:10] if timestamp else ""
                time_part = timestamp[11:19] if timestamp else ""
                
                rows.append({
                    "date": date_part,
                    "time": time_part,
                    "operation": log.get("operation", ""),
                    "concept": log.get("human_id", "unknown")[:30],
                    "cid": log.get("cid", "")[:12] + "...",
                })
            
            ui.table(columns=columns, rows=rows, row_key="date").classes("w-full")
    
    async def export_logs(self, logs):
        """Export logs as JSON file"""
        import json
        content = json.dumps(logs, indent=2)
        ui.download(content, f"cadmies_audit_{datetime.now().strftime('%Y%m%d')}.json")
