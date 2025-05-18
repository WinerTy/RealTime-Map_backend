def pascal_to_camel_case(class_name_str: str) -> str:
    """
    Converts a PascalCase string (typical for class names) to camelCase.

    Args:
        class_name_str: The string in PascalCase (e.g., "MyClassName").

    Returns:
        The string in camelCase (e.g., "myClassName").
    """
    if not class_name_str:
        return ""
    if len(class_name_str) == 1:
        return class_name_str.lower()
    return class_name_str[0].lower() + class_name_str[1:]


# Examples
print(f"'MyClassName' -> '{pascal_to_camel_case('MyClassName')}'")
print(f"'AnotherExample' -> '{pascal_to_camel_case('AnotherExample')}'")
print(f"'HTTPRequest' -> '{pascal_to_camel_case('HTTPRequest')}'")
print(f"'A' -> '{pascal_to_camel_case('A')}'")
print(f"'' -> '{pascal_to_camel_case('')}'")
print(
    f"'alreadyCamel' -> '{pascal_to_camel_case('alreadyCamel')}'"
)  # Note: If already camelCase, it stays as is.
