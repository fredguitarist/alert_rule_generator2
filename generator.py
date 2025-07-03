import yaml
from pathlib import Path
from typing import Dict, Any

def generate_alert_rule(target: Dict[str, Any], template_path: str) -> Dict:
    # Читаем шаблон из YAML
    with open(template_path, 'r', encoding='utf-8') as f:
        template = yaml.safe_load(f)

    host = target["labels"]["host"]
    host_lc = host.lower()

    # Имя алерта, expr и метки подставляем в шаблон — предположим, что шаблон стандартный с одним правилом в groups[0]
    group = template["groups"][0]
    group_name = group.get("name", "cpu_alerts")

    # Заменим имя группы, чтобы было уникально с хостом
    group["name"] = f"{group_name}_{host_lc}"

    for rule in group.get("rules", []):
        # Имя алерта с именем хоста в CamelCase (убираем дефисы и делаем заглавными первые буквы)
        alert_name = "HighCpuUsageOn" + "".join(part.capitalize() for part in host.split("-"))
        rule["alert"] = alert_name

        # В expr подставляем host с маленькими буквами
        expr = rule.get("expr", "")
        expr = expr.replace("{{ $labels.host }}", host_lc)
        # В твоём шаблоне expr - строка, где нужно подставить host в фильтр
        # Если шаблон не содержит плейсхолдер, заменим вручную
        if 'host="' not in expr:
            # например expr: ... host="vs-db-stage01"
            expr = expr.replace("{mode=\"idle\"}", f'{{mode="idle", host="{host_lc}"}}')
        else:
            expr = expr.replace("host={{ $labels.host }}", f'host="{host_lc}"')

        rule["expr"] = expr

        # Заменяем labels.host
        if "labels" in rule:
            rule["labels"]["host"] = host_lc

        # В annotations заменяем везде "{{ $labels.instance }}" и т.п., добавим host
        for ann_key, ann_val in rule.get("annotations", {}).items():
            ann_val = ann_val.replace("{{ $labels.instance }}", "{{ $labels.instance }}")
            ann_val = ann_val.replace("{{ $value }}", "{{ $value }}")
            ann_val = ann_val.replace("{{ $labels.host }}", host_lc)
            ann_val = ann_val.replace(host_lc, host_lc)  # на всякий случай
            # Для твоего примера, чтобы вставить host в текст, подставим его прямо:
            if "summary" in ann_key.lower():
                ann_val = f"High CPU usage on {host_lc} ({{{{ $labels.instance }}}})"
            if "description" in ann_key.lower():
                ann_val = f"CPU usage is over 80% on host {host_lc} ({{{{ $value }}}}%)"
            rule["annotations"][ann_key] = ann_val

    return template
