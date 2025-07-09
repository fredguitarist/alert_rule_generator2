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