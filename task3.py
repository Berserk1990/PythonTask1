def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "User not found"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Enter user name"
    return wrapper


@input_error
def add_contact(data, contacts):
    name, phone = data
    contacts[name] = phone
    return "Contact"+name+" added"


@input_error
def change_contact(data, contacts):
    name, phone = data
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact "+name+"changed"


@input_error
def phone_contact(data, contacts):
    name = data[0]
    if name not in contacts:
        raise KeyError
    return contacts[name]


@input_error
def show_all(contacts):
    if not contacts:
        return "No contacts saved"

    result = ""
    for name, phone in contacts.items():
        result += name+": "+phone+"\n"
    return result.strip()


def parser(user_input):
    user_input = user_input.strip()
    command = user_input.lower()

    if command in ["good bye", "close", "exit"]:
        return "exit", []
    elif command == "hello":
        return "hello", []
    elif command == "show all":
        return "show all", []
    elif command.startswith("add "):
        return "add", user_input[4:].split()
    elif command.startswith("change "):
        return "change", user_input[7:].split()
    elif command.startswith("phone "):
        return "phone", user_input[6:].split()
    else:
        return "unknown", []


contacts = {}

while True:
    user_input = input(">>> ")
    command, data = parser(user_input)

    if command == "hello":
        print("How can I help you?")
    elif command == "add":
         print(add_contact(data, contacts))
    elif command == "change":
        print(change_contact(data, contacts))
    elif command == "phone":
        print(phone_contact(data, contacts))
    elif command == "show all":
        print(show_all(contacts))
    elif command == "exit":
        print("Good bye!")
        break
    else:
        print("Unknown command")
