import yaml
from pathlib import Path
from typing import Dict, Any

def generate_alert_rule(target: Dict[str, Any], template_path: str) -> Dict[str, Any]:
    with open(template_path, "r", encoding="utf-8") as f:
        template = yaml.safe_load(f)

    host = target["labels"]["host"]

    for group in template.get("groups", []):
        group_name = group.get("name", "")
        group["name"] = f"{group_name}_{host}"

        for rule in group.get("rules", []):
            alert_name = f"{rule['alert']}On{host.replace('-', '').replace('_', '')}"
            rule["alert"] = alert_name

            expr = rule.get("expr", "")
            if "{" in expr and "}" in expr:
                expr = expr.replace("{", f'{{host="{host}", ')
            else:
                expr = f'{{host="{host}"}}'

            rule["expr"] = expr

            if "labels" in rule:
                rule["labels"]["host"] = host

            if "annotations" in rule:
                for k, v in rule["annotations"].items():
                    v = v.replace("{{ $labels.instance }}", host)
                    v = v.replace("{{ $labels.host }}", host)
                    rule["annotations"][k] = v

    return template
