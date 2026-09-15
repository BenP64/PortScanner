try:
    import sys
    from modules import scanner, settings
except KeyboardInterrupt:
    print("Exiting...")
    sys.exit(0)
except Exception:
    print("Error importing, Please ensure dependencies are installed.")
    sys.exit(1)


def launch_menu():
    print("""
----- Scanner -----
[1] Port Scanner
[2] Settings
[3] Exit""")

    try:
        menu_input = input("> ")
        return int(menu_input)
    except ValueError:
        return print(f'"{menu_input}" is not a valid input.')
    except KeyboardInterrupt:
        print("\nExiting program...")
        sys.exit(0)


if __name__ == "__main__":
    file_found = settings.check_config()
    if not file_found:
        settings.reset_config()

    user_input = launch_menu()

    while user_input != 3:

        if user_input == 1:
            scanner.port_scanner()
        elif user_input == 2:
            settings.main()
        else:
            ...
        user_input = launch_menu()

    print("Exiting...")