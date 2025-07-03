import json
from pathlib import Path
from generator import generate_alert_rule
import yaml

CONFIG_DIR = "configs"
OUTPUT_DIR = "output"
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
    filename = f"alert_{host}.yaml"
    output_path = Path(output_dir) / filename
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(alert_data, f, sort_keys=False)
    print(f"Alert written to {output_path}")

def main():
    targets_with_files = load_targets_with_node(CONFIG_DIR)
    for target, filename in targets_with_files:
        host = target["labels"]["host"]
        alert_rule = generate_alert_rule(target, TEMPLATE_DIR, filename)
        write_alert(OUTPUT_DIR, host, alert_rule)

if __name__ == "__main__":
    main()
