import yaml
from pathlib import Path
from typing import Dict

def extract_environment_from_filename(filename: str) -> str:
    lowered = filename.lower()
    for env in ("dev", "stage", "prod"):
        if env in lowered:
            return env
    return "null"  # Если ничего не нашли — пишем null

def host_to_title(host: str) -> str:
    # Пример: vs-db-stage01 -> VsDbStage01
    return "".join(part.capitalize() for part in host.replace("_", "-").split("-"))

def generate_alert_rule(target: Dict, template_dir: str, filename: str) -> Dict:
    template_path = Path(template_dir) / "cpu_alert.yaml"
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    host = target["labels"]["host"]
    environment = extract_environment_from_filename(filename)

    # Делаем замену по плейсхолдерам
    alert_text = template.replace("{{ host }}", host)\
                         .replace("{{ host_title }}", host_to_title(host))\
                         .replace("{{ environment }}", environment)

    alert_dict = yaml.safe_load(alert_text)
    return alert_dict
