import json
from pathlib import Path
from generate_for_node_cpu import generate_for_node_cpu
import yaml

# CONFIG_DIR = "/opt/prometheus/sd_configs"
# OUTPUT_DIR = "/opt/prometheus/alerts"
CONFIG_DIR = "configs"
OUTPUT_DIR = "result"
TEMPLATE_DIR = "templates"

#загрузка всех конфигураций
def load_targets(config_dir: str):
    targets = []
    for file_path in Path(config_dir).glob("*node*.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for target in data:
                targets.append((target, file_path.name))
    return targets

def write_alert(output_dir: str, host: str, alert_data: dict, controlled: str):
    # Создаём директорию для вывода, если она ещё не существует
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    # Формируем имя выходного файла на основе имени хоста
    filename = f"alert_{host}_{controlled}.yml"
    print(filename + " записан")
    # Полный путь к файлу: директория + имя файла
    output_path = Path(output_dir) / filename
    # Открываем файл на запись в формате UTF-8
    with open(output_path, "w", encoding="utf-8") as f:
        # Сохраняем словарь alert_data в YAML-файл без сортировки ключей
        yaml.dump(alert_data, f, sort_keys=False)
    #print(f"✅ Alert written to {output_path}")

def main():
    targets_with_files = load_targets(CONFIG_DIR) #загрузка целей
    print(f"Найдено {len(targets_with_files)} целей")  # для отладки

    for target, filename in targets_with_files:
        # Проверяем, что 'node' есть в имени файла (без учёта регистра)
        if "node" in filename.lower():
            host = target["labels"]["host"] #зачем эта строка
            # print(host)
            # print(target)
            alert_rule = generate_for_node_cpu(target, TEMPLATE_DIR) #генерация правил алертинга в папку
            # print(TEMPLATE_DIR)
            controlled = "node_cpu"
            write_alert(OUTPUT_DIR, host, alert_rule, controlled)
        else:
            # print(f"Пропускаем {filename}, не содержит 'node'")
            pass

    for target, filename in targets_with_files:
        # Проверяем, что 'node' есть в имени файла (без учёта регистра)
        if "node" in filename.lower():
            host = target["labels"]["host"] #зачем эта строка
            alert_rule = generate_for_node_cpu(target, TEMPLATE_DIR) #генерация правил алертинга в папку
            controlled = "node_ram"
            write_alert(OUTPUT_DIR, host, alert_rule, controlled)



if __name__ == "__main__":
    main()



