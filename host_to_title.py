def host_to_title(host: str) -> str:
    # Пример: vs-db-stage01 -> VsDbStage01
    # Сначала заменяем подчёркивания на дефисы, потом разбиваем по дефисам,
    # затем каждую часть делаем с заглавной буквы и соединяем обратно
    return "".join(part.capitalize() for part in host.replace("_", "-").split("-"))