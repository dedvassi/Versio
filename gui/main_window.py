import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QListWidget, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Versio 😄 by dedvassi")
        self.resize(340, 450)

        # Определяем путь к файлу стилей относительно текущего файла
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Папка gui/
        style_path = os.path.join(current_dir, "styles.qss")

        # Применяем стили
        with open(style_path, "r") as file:
            self.setStyleSheet(file.read())

        # Центральный виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Главный макет
        main_layout = QGridLayout(central_widget)

        # Верхняя часть: заголовки
        header_layout = QVBoxLayout()
        self.name_lbl = QLabel("Versio 😄", alignment=Qt.AlignmentFlag.AlignCenter)
        self.name_lbl.setObjectName("name_lbl")
        self.sl_lbl = QLabel("Управлять версиями проектов легко и просто!", alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.name_lbl)
        header_layout.addWidget(self.sl_lbl)

        # Средняя часть: кнопки
        btn_layout = QVBoxLayout()
        self.btn_open_existing = QPushButton("Открыть существующий репозиторий")
        self.btn_new = QPushButton("Подключить новый репозиторий")
        btn_layout.addWidget(self.btn_open_existing)
        btn_layout.addWidget(self.btn_new)

        # Список проектов
        project_layout = QVBoxLayout()
        self.projects_lbl = QLabel("Недавние проекты")
        self.projects_list = QListWidget()
        project_layout.addWidget(self.projects_lbl)
        project_layout.addWidget(self.projects_list)

        # Нижняя часть: кнопка настроек
        self.settings_btn = QPushButton("Настройки")

        # Добавляем все в основной макет
        main_layout.addLayout(header_layout, 0, 0)
        main_layout.addLayout(btn_layout, 1, 0)
        main_layout.addLayout(project_layout, 2, 0)
        main_layout.addWidget(self.settings_btn, 3, 0)


