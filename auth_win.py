from PyQt6 import QtCore, QtGui, QtWidgets
from Database import Database


class AuthWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setup_ui()
        self.setup_events()

    def setup_ui(self):
        self.setObjectName("AuthWindow")
        self.resize(500, 400)
        self.setWindowTitle("Авторизация")

        # Иконка окна
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("silkweb/logo.jpeg"))
        self.setWindowIcon(icon)

        # Логотип
        self.logo = QtWidgets.QLabel(self)
        self.logo.setGeometry(QtCore.QRect(10, 10, 80, 80))
        self.logo.setPixmap(QtGui.QPixmap("silkweb/logo.jpeg"))
        self.logo.setScaledContents(True)

        # Заголовок
        self.title = QtWidgets.QLabel(self)
        self.title.setGeometry(QtCore.QRect(100, 10, 380, 80))
        self.title.setFont(QtGui.QFont("Arial", 14))
        self.title.setText("Введите ваши учетные данные\nдля авторизации в системе:")

        # Центральный виджет с полями ввода
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setGeometry(QtCore.QRect(50, 120, 400, 200))

        # Вертикальный layout
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Поле логина
        self.login_input = QtWidgets.QLineEdit()
        self.login_input.setPlaceholderText("Ваш email")
        self.login_input.setFont(QtGui.QFont("Arial", 12))
        self.login_input.setMinimumHeight(40)
        self.layout.addWidget(self.login_input)

        # Поле пароля
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Ваш пароль")
        self.password_input.setFont(QtGui.QFont("Arial", 12))
        self.password_input.setMinimumHeight(40)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)

        # Кнопка входа
        self.auth_button = QtWidgets.QPushButton("Войти")
        self.auth_button.setFont(QtGui.QFont("Arial", 14))
        self.auth_button.setMinimumHeight(50)
        self.auth_button.setStyleSheet("background-color: #00aaff; color: white;")
        self.layout.addWidget(self.auth_button)

    def setup_events(self):
        self.auth_button.clicked.connect(self.authenticate)

    def authenticate(self):
        login = self.login_input.text()
        password = self.password_input.text()

        if not login or not password:
            self.show_message("Ошибка", "Все поля должны быть заполнены")
            return

        user = self.db.check_credentials(login, password)

        if user:
            self.show_message("Успех", f"Добро пожаловать, {user['email']}!\nВаша роль: {user['role']}")
            # Здесь будет переход к соответствующему интерфейсу
        else:
            self.show_message("Ошибка", "Неверные учетные данные")

    def show_message(self, title, message):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()