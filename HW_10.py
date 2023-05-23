from collections import UserDict
import functools


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


class Field:
    def __init__(self, value=None):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break


contacts = AddressBook()


def input_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Контакт не найден"
        except ValueError:
            return "Неверный ввод. Пожалуйста, введите имя и телефон через пробел."
        except IndexError:
            return "Неверный ввод. Укажите имя."

    return wrapper


@input_error
def add_contact(name, phone):
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "Контакт успешно добавлен."


@input_error
def change_contact(name, phone):
    record = contacts.data.get(name)
    if record:
        record.edit_phone(record.phones[0].value, phone)
        return "Контакт успешно обновлен."
    raise KeyError


@input_error
def get_phone(name):
    record = contacts.data.get(name)
    if record:
        return record.phones[0].value
    raise KeyError


def show_all_contacts():
    if not contacts.data:
        return "Контакты не найдены."
    result = ""
    for record in contacts.data.values():
        result += f"{record.name.value}: "
        for phone in record.phones:
            result += f"{phone.value}, "
        result = result.rstrip(", ") + "\n"
    return result.strip()


def handle_command(command):
    if command.lower() == "hello":
        return "Могу я чем-нибудь помочь?"
    elif command.lower().startswith("add"):
        parts = command.split(" ", 2)
        if len(parts) < 3:
            raise ValueError
        name, phone = parts[1], parts[2]
        return add_contact(name, phone)
    elif command.lower().startswith("change"):
        parts = command.split(" ", 2)
        if len(parts) < 3:
            raise ValueError
        name, phone = parts[1], parts[2]
        return change_contact(name, phone)
    elif command.lower().startswith("phone"):
        parts = command.split(" ", 1)
        if len(parts) < 2:
            raise ValueError
        name = parts[1]
        return get_phone(name)
    elif command.lower() == "show all":
        return show_all_contacts()
    elif command.lower() in ["good bye", "close", "exit"]:
        return "До свидания!"
    else:
        return "Неверная команда. Пожалуйста, попробуйте еще ра."

def main():
    while True:
        command = input("Введите команду: ")
        response = handle_command(command)
        print(response)
        if response == "До свидания!":
            break

if __name__ == "__main__":
    main()

