import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QListWidget, QVBoxLayout, QGridLayout, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from core.git_manager import GitManager  # Подключаем модуль для работы с Git

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
        self.btn_new.clicked.connect(self.connect_new_repository)  # Обработчик кнопки
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

        # Логика работы с Git
        self.git_manager = GitManager()  # Экземпляр GitManager

        # Обновляем список недавих проектов
        self.update_recent_projects()

    def connect_new_repository(self):
        """Обработчик для кнопки 'Подключить новый репозиторий'"""
        # 1. Диалог выбора папки
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для подключения")
        if not folder:
            QMessageBox.warning(self, "Ошибка", "Папка для подключения не выбрана.")
            return

        # 2. Проверяем, является ли папка репозиторием
        if self.git_manager.is_git_repository(folder):
            QMessageBox.information(self, "Репозиторий подключён", f"Репозиторий в папке {folder} подключён.")
        else:
            # Предложение инициализировать новый репозиторий
            init_repo = QMessageBox.question(
                self,
                "Инициализация репозитория",
                f"Папка {folder} не является репозиторием. Создать новый репозиторий?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if init_repo == QMessageBox.StandardButton.Yes:
                self.git_manager.init_repository(folder)
                QMessageBox.information(self, "Репозиторий создан", f"Новый репозиторий в папке {folder} создан.")

        # 3. Сохранить в список недавних проектов
        self.save_recent_repository(folder)

    def save_recent_repository(self, path):
        """Сохранить путь к репозиторию и обновить список проектов"""
        print(path)
        self.git_manager.save_recent_repository(path)
        self.update_recent_projects()

    def update_recent_projects(self):
        """Обновить список 'Недавние проекты'"""
        recent_repositories = self.git_manager.get_recent_repositories()
        self.projects_list.clear()
        for repo in recent_repositories:
            self.projects_list.addItem(repo)
