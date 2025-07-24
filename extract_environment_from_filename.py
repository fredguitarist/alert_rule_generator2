#определяет окружение и возвращает
def extract_environment_from_filename(hostname: str) -> str:
    hostname = hostname.strip().lower()
    print(hostname)
    if 'stage' in hostname:
        return 'stage'
    else:
        return 'other'
