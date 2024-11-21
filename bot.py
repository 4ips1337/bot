import pickle
from abc import ABC, abstractmethod


class Contact:
    def __init__(self, name, phone, email=""):
        self.name = name
        self.phone = phone
        self.email = email

    def __repr__(self):
        return f"Contact(name={self.name}, phone={self.phone}, email={self.email})"


class AddressBook:
    def __init__(self):
        self.contacts = {}

    def add_contact(self, contact):
        self.contacts[contact.name] = contact

    def remove_contact(self, name):
        if name in self.contacts:
            del self.contacts[name]

    def find_contact(self, name):
        return self.contacts.get(name)

    def get_all_contacts(self):
        return self.contacts.values()



class UserInterface(ABC):
    @abstractmethod
    def show_menu(self):
        pass

    @abstractmethod
    def get_user_input(self, prompt):
        pass

    @abstractmethod
    def show_message(self, message):
        pass

    @abstractmethod
    def display_contacts(self, contacts):
        pass



class ConsoleInterface(UserInterface):
    def show_menu(self):
        print("\nМеню:")
        print("1. Додати контакт")
        print("2. Видалити контакт")
        print("3. Знайти контакт")
        print("4. Показати всі контакти")
        print("5. Вийти")

    def get_user_input(self, prompt):
        return input(prompt)

    def show_message(self, message):
        print(message)

    def display_contacts(self, contacts):
        if contacts:
            for contact in contacts:
                print(contact)
        else:
            print("Адресна книга порожня.")



def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()



def main(ui: UserInterface):
    ui.show_message("Завантаження адресної книги...")
    book = load_data()
    ui.show_message("Адресна книга успішно завантажена.")

    while True:
        ui.show_menu()
        choice = ui.get_user_input("Оберіть опцію: ")

        if choice == "1":
            name = ui.get_user_input("Ім'я: ")
            phone = ui.get_user_input("Телефон: ")
            email = ui.get_user_input("Email (необов'язково): ")
            contact = Contact(name, phone, email)
            book.add_contact(contact)
            ui.show_message("Контакт додано.")

        elif choice == "2":
            name = ui.get_user_input("Введіть ім'я контакту, який потрібно видалити: ")
            if book.find_contact(name):
                book.remove_contact(name)
                ui.show_message("Контакт видалено.")
            else:
                ui.show_message("Контакт не знайдено.")

        elif choice == "3":
            name = ui.get_user_input("Введіть ім'я для пошуку: ")
            contact = book.find_contact(name)
            if contact:
                ui.show_message(f"Знайдено: {contact}")
            else:
                ui.show_message("Контакт не знайдено.")

        elif choice == "4":
            ui.show_message("Всі контакти:")
            ui.display_contacts(book.get_all_contacts())

        elif choice == "5":
            ui.show_message("Збереження адресної книги...")
            save_data(book)
            ui.show_message("Дані успішно збережено. До побачення!")
            break

        else:
            ui.show_message("Невірна опція. Спробуйте ще раз.")


if __name__ == "__main__":
    console_ui = ConsoleInterface()
    main(console_ui)
