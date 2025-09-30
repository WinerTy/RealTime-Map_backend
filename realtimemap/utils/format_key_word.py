def format_key(key: str) -> str:
    formatted = key.replace("_", " ")
    formatted = " ".join(word.capitalize() for word in formatted.split())
    return formatted
