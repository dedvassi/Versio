from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

import webbrowser

class GitConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройка Git")
        self.setLayout(QVBoxLayout())

        self.layout().addWidget(QLabel("Введите ваше имя пользователя:"))
        self.username_input = QLineEdit(self)
        self.layout().addWidget(self.username_input)

        self.layout().addWidget(QLabel("Введите вашу электронную почту:"))
        self.email_input = QLineEdit(self)
        self.layout().addWidget(self.email_input)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.layout().addWidget(self.ok_button)

    def warning_save_data(self):
        QMessageBox.critical(None, "Ошибка", "Для корректной работы необходимо ввести и сохранить свои данные.\n"
                                             "Для повторной попытки перезапустите программу\n"
                                             "Эти данные необходимы для идентификации вас как конкретного модератора проектов\n"
                                             "Они не используются для авторизации")

    def get_values(self):
        """
        Возвращает введённые имя пользователя и почту.
        """
        return self.username_input.text(), self.email_input.text()


class GitNotInstalledDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Git не установлен")
        self.setMinimumSize(300, 150)

        # Текст с предупреждением
        label = QLabel("Git не найден на вашем компьютере. Установите Git, чтобы продолжить.")
        label.setWordWrap(True)

        # Кнопка для перехода на сайт установки Git
        download_button = QPushButton("Скачать Git")
        download_button.clicked.connect(self.open_git_download_page)

        # Кнопка выхода
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(download_button)
        layout.addWidget(close_button)
        self.setLayout(layout)

    def open_git_download_page(self):
        webbrowser.open("https://git-scm.com/downloads")