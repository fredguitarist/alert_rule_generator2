from extract_environment_from_filename import extract_environment_from_filename
from host_to_title import host_to_title
from typing import Dict

def generate_for_node_ram(target: Dict, filename: str) -> Dict:
    raw_host = target["labels"]["host"]  # Исходное значение хоста из меток
    host = raw_host.replace("-", "_")  # Заменяем дефисы на подчёркивания (для PromQL)
    environment = extract_environment_from_filename(host)  # Определяем окружение из имени файла
    # print(filename)
    host_title = host_to_title(raw_host)  # Преобразуем хост в формат для имени алерта (например, VsDbStage01)

    rule = {
        "groups": [
            {
                "name": "cpu_alerts",  # Название группы правил (можно расширить потом)
                "rules": [
                    {
                        "alert": f"HostOutOfMemory{host_title}",  # Название алерта, читаемое человеком
                        "expr": f'node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100 < 10',
                        # Условие: если средняя загрузка CPU (100 - idle) > 80% за последние 5 минут
                        "for": "5m",  # Условие должно выполняться как минимум 5 минут
                        "labels": {
                            "severity": "warning",  # Уровень — warning (можно сделать настраиваемым)
                            "host": host,  # Хост
                            "environment": environment  # Окружение (dev/stage/prod/null)
                        },
                        "annotations": {
                            "summary": f"Host out of memory {host} ({{{{ $labels.instance }}}})",
                            # Краткое описание — попадёт в заголовок оповещения
                            "description": f"RAM usage is over 70% on host  {host} ({{{{ $value }}}}%)"
                            # Полное описание — попадёт в тело оповещения
                        }
                    }
                ]
            }
        ]
    }

    return rule  # Возвращаем словарь, готовый к сериализации в YAML