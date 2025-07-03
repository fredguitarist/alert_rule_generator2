import json
from pathlib import Path
import yaml
from generator import generate_alert_rule

def main():
    input_path = Path("configs/targets.json")
    template_path = Path("templates/cpu_alert.yaml")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    with open(input_path, "r", encoding="utf-8") as f:
        targets = json.load(f)

    for target in targets:
        alert_rule = generate_alert_rule(target, str(template_path))

        host = target["labels"]["host"].lower()
        output_file = output_dir / f"alert_{host}.yaml"
        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(alert_rule, f, sort_keys=False, allow_unicode=True)

        print(f"Alert saved to {output_file}")

if __name__ == "__main__":
    main()
