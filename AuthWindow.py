from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from Database import Database


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Шелкопряд - Авторизация")
        self.setFixedSize(400, 300)

        # Логотип и заголовок
        header_layout = QHBoxLayout()

        # Логотип
        self.logo_label = QLabel(self)
        try:
            pixmap = QPixmap("logo.jpeg").scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio)
            self.logo_label.setPixmap(pixmap)
        except:
            self.logo_label.setText("Логотип")

        # Название приложения
        title_label = QLabel("Шелкопряд\nУчет заказов")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        header_layout.addWidget(self.logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Поля ввода
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Кнопки
        login_btn = QPushButton("Войти")
        login_btn.clicked.connect(self.authenticate)

        # Основной лейаут
        main_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.email_input)
        main_layout.addWidget(self.password_input)
        main_layout.addWidget(login_btn)

        self.setLayout(main_layout)

    def authenticate(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        # Проверка учетных данных
        user = self.db.get_user(email, password)
        if not user:
            QMessageBox.warning(self, "Ошибка", "Неверный email или пароль")
            return

        # Определение роли
        role = user[0]['role']
        QMessageBox.information(self, "Успех",
                                f"Добро пожаловать!\nРоль: {role.capitalize()}")

        # Закрываем окно авторизации
        self.close()

        # Здесь будет открытие соответствующего интерфейса
        # if role == 'customer':
        #     self.customer_window = CustomerWindow()
        #     self.customer_window.show()
        # elif role == 'manager':
        #     self.manager_window = ManagerWindow()
        #     self.manager_window.show()