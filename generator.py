from typing import Dict

#создаются функции для дальнейшего использования

#определяет окружение и возвращает
def extract_environment_from_filename(filename: str) -> str:
    print("extract_environment_from_filename")
    lowered = filename.lower()  # Приводим имя файла к нижнему регистру
    print(lowered)
    for env in ("dev", "stage", "prod"):  # Перебираем возможные окружения
        print(env)
        if env in lowered:  # Если окружение встречается в имени файла — возвращаем его
            return env
    return "null"  # Если ни одно не найдено — возвращаем "null"

def host_to_title(host: str) -> str:
    # Пример: vs-db-stage01 -> VsDbStage01
    # Сначала заменяем подчёркивания на дефисы, потом разбиваем по дефисам,
    # затем каждую часть делаем с заглавной буквы и соединяем обратно
    return "".join(part.capitalize() for part in host.replace("_", "-").split("-"))

def generate_alert_rule(target: Dict, filename: str) -> Dict:
    raw_host = target["labels"]["host"]  # Исходное значение хоста из меток
    host = raw_host.replace("-", "_")  # Заменяем дефисы на подчёркивания (для PromQL)
    environment = extract_environment_from_filename(filename)  # Определяем окружение из имени файла
    host_title = host_to_title(raw_host)  # Преобразуем хост в формат для имени алерта (например, VsDbStage01)

    rule = {
        "groups": [
            {
                "name": "cpu_alerts",  # Название группы правил (можно расширить потом)
                "rules": [
                    {
                        "alert": f"HighCpuUsageOn{host_title}",  # Название алерта, читаемое человеком
                        "expr": f'(100 - avg by(instance)(irate(node_cpu_seconds_total{{mode="idle", host="{host}"}}[5m])) * 100) > 80',
                        # Условие: если средняя загрузка CPU (100 - idle) > 80% за последние 5 минут
                        "for": "5m",  # Условие должно выполняться как минимум 5 минут
                        "labels": {
                            "severity": "warning",  # Уровень — warning (можно сделать настраиваемым)
                            "host": host,  # Хост (с подчёркиваниями)
                            "environment": environment  # Окружение (dev/stage/prod/null)
                        },
                        "annotations": {
                            "summary": f"High CPU usage on {host} ({{{{ $labels.instance }}}})",
                            # Краткое описание — попадёт в заголовок оповещения
                            "description": f"CPU usage is over 80% on host {host} ({{{{ $value }}}}%)"
                            # Полное описание — попадёт в тело оповещения
                        }
                    }
                ]
            }
        ]
    }

    return rule  # Возвращаем словарь, готовый к сериализации в YAML

