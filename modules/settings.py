try:
    import os
    import sys
    from configparser import ConfigParser
    from pathlib import Path
except KeyboardInterrupt:
    print("Exiting...")
    sys.exit(0)
except Exception:
    print("Error importing, Please ensure dependencies are installed.")
    sys.exit(1)


def check_config():
    """ Checks if the config file exists. """
    if os.path.isfile("settings.ini"):
        return True # File is found
    else:
        return False # File is not found


def reset_config():
    """ Rewrites the config file with default values. """
    config = ConfigParser()

    config["DEFAULT"] = {
        "max_workers": 200,
        "port_timeout": 1
    }
    with open("settings.ini", "w") as f:
        config.write(f)
        f.close()


def adjust_setting(option):
    """ Adjusts max_worker value in config file. """
    root_dir = Path(__file__).resolve().parent.parent
    ini_path = root_dir / "settings.ini"

    config = ConfigParser()
    config.read(ini_path)

    try:
        print(f"""---- Adjust {option} ----
Current value: {config["DEFAULT"][option]}""")
        user_input = input("> ")
        if option == "port_timeout":
            user_input = float(user_input)
            if not user_input >= 0.1:
                return print("Port timeout value must be larger than 0.1s ")
        else:
            user_input = int(user_input)

        config.set("DEFAULT", option, str(user_input))
        with open(ini_path, "w") as f:
            config.write(f)
            f.close()
        return print(f'Successfully updated "{option}".') # writes user input to max_worker value then returns success message.
    except ValueError:
        return print(f'"{user_input}" is not a valid input.') # Returns error message when input is not an integer
    except KeyboardInterrupt:
        print("\nExiting program...")
        sys.exit(0)


def retrieve_setting(option):
    try:
        config = ConfigParser()
        config.read("settings.ini")
        return int(config["DEFAULT"])
    except ValueError:
        return print(f'"ValueError: {option}" is not a valid value.')
    except TypeError:
        return print(f'TypeError: "{option}" is not a valid type.')

def settings_menu():
    """ Print and gets user input for settings menu. """
    print("""
------- SETTINGS -------
[1] Adjust max_workers
[2] Adjust port_timeout
[3] Revert to default settings
[4] Back
""")
    try:
        user_input = input("> ")
        return int(user_input) # returns user input as an integer
    except ValueError:
        return print(f'"{user_input}" is not a valid input.')
    except KeyboardInterrupt:
        print("\nExiting program...")
        sys.exit(0)


def main():

    user_input = settings_menu()
    while user_input != 4:
        if user_input == 1:
            adjust_setting("max_workers")
        elif user_input == 2:
            adjust_setting("port_timeout")
        elif user_input == 3:
            reset_config()
        else:
            print(f"{user_input} is not a valid input.")
        user_input = settings_menu()


if __name__ == "__main__":
    main()