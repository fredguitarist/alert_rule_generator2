import yaml
from pathlib import Path
from typing import Dict


def extract_environment_from_filename(filename: str) -> str:
    lowered = filename.lower()
    for env in ("dev", "stage", "prod"):
        if env in lowered:
            return env
    return "null"


def host_to_title(host: str) -> str:
    # Пример: vs-db-stage01 -> VsDbStage01
    return "".join(part.capitalize() for part in host.replace("_", "-").split("-"))


def generate_alert_rule(target: Dict, filename: str) -> Dict:
    host = target["labels"]["host"]
    environment = extract_environment_from_filename(filename)
    host_title = host_to_title(host)

    rule = {
        "groups": [
            {
                "name": "cpu_alerts",
                "rules": [
                    {
                        "alert": f"HighCpuUsageOn{host_title}",
                        "expr": f'(100 - avg by(instance)(irate(node_cpu_seconds_total{{mode="idle", host="{host}"}}[5m])) * 100) > 80',
                        "for": "5m",
                        "labels": {
                            "severity": "warning",
                            "host": host,
                            "environment": environment
                        },
                        "annotations": {
                            "summary": f"High CPU usage on {host} ({{{{ $labels.instance }}}})",
                            "description": f"CPU usage is over 80% on host {host} ({{{{ $value }}}}%)"
                        }
                    }
                ]
            }
        ]
    }

    return rule
