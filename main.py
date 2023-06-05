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


class UserInfoWidget(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        label_name = QLabel()
        label_surname = QLabel()
        label_books = QLabel()

        layout.addWidget(label_name)
        layout.addWidget(label_surname)
        layout.addWidget(label_books)

        button_logout = QPushButton("Logout")
        button_logout.clicked.connect(self.logout)
        layout.addWidget(button_logout)

        self.setLayout(layout)

        username = database.child("users").shallow().get().val()
        if username is not None:
            user_info = database.child("users").child(username).get().val()
            if user_info is not None:
                label_name.setText(f"Name: {user_info['name']}")
                label_surname.setText(f"Surname: {user_info['surname']}")
                label_books.setText(f"Books Borrowed: {user_info['books_borrowed']}")

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
