import json
from pathlib import Path
from generator import generate_alert_rule
import yaml

CONFIG_DIR = "configs"
OUTPUT_DIR = "output"
TEMPLATE_FILE = "templates/cpu_alert.yaml"

def load_targets_with_node(config_dir: str):
    targets = []
    for file_path in Path(config_dir).glob("*node*.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # data — список целей в файле
            for target in data:
                targets.append(target)
    return targets

def write_alert(output_dir: str, host: str, alert_data: dict):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filename = f"alert_{host}.yaml"
    output_path = Path(output_dir) / filename
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(alert_data, f, sort_keys=False)
    print(f"Alert written to {output_path}")

def main():
    targets = load_targets_with_node(CONFIG_DIR)
    print(f"Found {len(targets)} targets with 'node' in filename")
    for target in targets:
        host = target["labels"]["host"]
        alert_rule = generate_alert_rule(target, TEMPLATE_FILE)
        write_alert(OUTPUT_DIR, host, alert_rule)

if __name__ == "__main__":
    main()

