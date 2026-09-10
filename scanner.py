
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
[1] Port Scanner
[2] Settings
[3] Exit""")

    try:
        menu_input = input("> ")
        return  int(menu_input)
    except ValueError as e:
        print(f'"{e}" is not a valid input.')
        return None
    except KeyboardInterrupt:
        print("\nExiting program...")
        return None


if __name__ == "__main__":
    user_input = launch_menu()

    while user_input != 3:

        if user_input == 1:
            scanner.port_scanner()
        elif user_input == 2:
            settings.settings_menu()
        else:
            print("Invalid input.")

        user_input = launch_menu()

    print("Exiting...")