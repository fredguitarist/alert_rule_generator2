import json
from pathlib import Path
from generator_for_nodes import generate_alert_rule_for_nodes
import yaml

# CONFIG_DIR = "/opt/prometheus/sd_configs"
# OUTPUT_DIR = "/opt/prometheus/alerts"
CONFIG_DIR = "/home/nekto/AWG/projects/Восток-Сервис/alert_rules_generator/configs"
OUTPUT_DIR = ".result"
TEMPLATE_DIR = "templates"

def load_targets_with_node(config_dir: str):
    targets = []
    for file_path in Path(config_dir).glob("*node*.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for target in data:
                targets.append((target, file_path.name))
    return targets

def write_alert(output_dir: str, host: str, alert_data: dict):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filename = f"alert_{host}.yml"
    output_path = Path(output_dir) / filename
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(alert_data, f, sort_keys=False)
    print(f"✅ Alert written to {output_path}")

def main():
    targets_with_files = load_targets_with_node(CONFIG_DIR)
    print(f"Найдено {len(targets_with_files)} целей")  # для отладки

    for target, filename in targets_with_files:
        host = target["labels"]["host"]
        #print(f"Обрабатываем {host} из {filename}")  # для отладки
        alert_rule = generate_alert_rule_for_nodes(target, TEMPLATE_DIR)
        write_alert(OUTPUT_DIR, host, alert_rule)

if __name__ == "__main__":
    main()
