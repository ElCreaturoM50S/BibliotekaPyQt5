import sys
import pyrebase
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

# Konfiguracja połączenia z bazą danych Firebase
config = {
  "apiKey": "AIzaSyBSA3r4wQ_kf5SgzImGeX6eQxL6rjvBNsE",
  "authDomain": "bibliotekafirebase-9a68f.firebaseapp.com",
  "databaseURL": "https://bibliotekafirebase-9a68f-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "bibliotekafirebase-9a68f",
  "storageBucket": "bibliotekafirebase-9a68f.appspot.com",
  "messagingSenderId": "809928352089",
  "appId": "1:809928352089:web:9b2fef01773a58c9e72c48"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()


class LoginWidget(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        label_username = QLabel("Username:")
        self.edit_username = QLineEdit()
        layout.addWidget(label_username)
        layout.addWidget(self.edit_username)

        label_password = QLabel("Password:")
        self.edit_password = QLineEdit()
        self.edit_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_password)
        layout.addWidget(self.edit_password)

        button_login = QPushButton("Login")
        button_login.clicked.connect(self.login)
        layout.addWidget(button_login)

        self.setLayout(layout)

    def login(self):
        username = self.edit_username.text()
        password = self.edit_password.text()

        # Perform login validation logic here
        # For simplicity, let's just check if username and password are not empty
        if username and password:
            user = database.child("users").child(username).get().val()

            if user is not None and user["password"] == password:
                self.stacked_widget.setCurrentIndex(1)  # Switch to the user info page
                self.stacked_widget.currentWidget().set_username(username)  # Pass the username to UserInfoWidget


class UserInfoWidget(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.label_name = QLabel()
        self.label_surname = QLabel()
        self.label_joindate = QLabel()
        self.label_books = QLabel()

        layout.addWidget(self.label_name)
        layout.addWidget(self.label_surname)
        layout.addWidget(self.label_joindate)
        layout.addWidget(self.label_books)

        button_logout = QPushButton("Logout")
        button_logout.clicked.connect(self.logout)
        layout.addWidget(button_logout)

        self.setLayout(layout)

    def set_username(self, username):
        self.username = username
        self.load_user_info()

    def load_user_info(self):
        user_info = database.child("users").child(self.username).get().val()
        if user_info is not None:
            self.label_name.setText(f"Name: {user_info['name']}")
            self.label_surname.setText(f"Surname: {user_info['surname']}")
            self.label_joindate.setText(f"Join date: {user_info['joindate']}")
            
            books_borrowed = user_info.get('books_borrowed', [])
            books_text = "Books Borrowed:\n"

            # Pobranie informacji o książkach na podstawie ich ID
            for book_id in books_borrowed:
                books_table = database.child("books")
                booklocation = books_table.child(book_id)
                book_info = booklocation.get().val()
                print(book_id)
                print(book_info)

                if book_info is not None:
                    book_name = book_info.get('book_name', '')
                    books_text += f"ID: {book_id}, Name: {book_name}\n"

            
            self.label_books.setText(books_text)


    def logout(self):
        self.stacked_widget.setCurrentIndex(0)  # Switch back to the login page


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("StackedWidget Example")
        self.setGeometry(100, 100, 400, 300)

        self.stacked_widget = QStackedWidget(self)

        login_widget = LoginWidget(self.stacked_widget)
        user_info_widget = UserInfoWidget(self.stacked_widget)

        self.stacked_widget.addWidget(login_widget)
        self.stacked_widget.addWidget(user_info_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())