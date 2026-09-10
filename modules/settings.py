def settings_menu():
    print("""
------- SETTINGS -------
[1] Adjust max_workers""")

    try:
        user_input = int(input("> "))
        return user_input
    except ValueError:
        return None
