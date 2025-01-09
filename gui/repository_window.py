import os
from PyQt6 import QtCore, QtGui, QtWidgets
from git import Repo

class RepositoryWindowUi(object):
    def __init__(self, git_manager):
        self.git_manager = git_manager  # Добавляем GitManager для работы с репозиториями

        # На всякий случай сохраним путь к текущему проекту тут
        self.project_path = self.git_manager.get_recent_repositories()[0]
        self.project_name = os.path.basename(self.project_path)

    def setupUi(self, MainWindow):
            MainWindow.setObjectName("RepositoryWindow")
            MainWindow.resize(800, 657)
            MainWindow.setAnimated(True)

            # Определяем путь к файлу стилей относительно текущего файла
            current_dir = os.path.dirname(os.path.abspath(__file__))  # Папка gui/
            style_path = os.path.join(current_dir, "styles.qss")

            # Применяем стили
            with open(style_path, "r") as file:
                MainWindow.setStyleSheet(file.read())

            self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
            self.gridLayout.setObjectName("gridLayout")

            # Таблица для отображения состояния репозитория
            self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Expanding)
            self.tableWidget.setSizePolicy(sizePolicy)
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setObjectName("tableWidget")
            self.tableWidget.setRowCount(0)

            # Настройка заголовков столбцов
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(0, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(1, item)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(2, item)
            self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
            self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
            self.tableWidget.horizontalHeader().setStretchLastSection(False)

            # Устанавливаем равную ширину колонок
            self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

            self.gridLayout.addWidget(self.tableWidget, 0, 1, 1, 1)

            # Блок кнопок управления
            self.verticalLayout = QtWidgets.QVBoxLayout()
            self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
            self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
            self.verticalLayout.setObjectName("verticalLayout")

            # Кнопка Commit Changes
            self.btn_commit = QtWidgets.QPushButton(parent=self.centralwidget)
            self.btn_commit.setObjectName("btn_commit")
            self.verticalLayout.addWidget(self.btn_commit)

            # Кнопка Push Changes
            self.btn_push = QtWidgets.QPushButton(parent=self.centralwidget)
            self.btn_push.setObjectName("btn_push")
            self.verticalLayout.addWidget(self.btn_push)

            # Кнопка Pull Changes
            self.btn_pull = QtWidgets.QPushButton(parent=self.centralwidget)
            self.btn_pull.setObjectName("btn_pull")
            self.verticalLayout.addWidget(self.btn_pull)

            # Кнопка Stage Files
            self.btn_stage = QtWidgets.QPushButton(parent=self.centralwidget)
            self.btn_stage.setObjectName("btn_stage")
            self.verticalLayout.addWidget(self.btn_stage)

            # Кнопка Unstage Files
            self.btn_unstage = QtWidgets.QPushButton(parent=self.centralwidget)
            self.btn_unstage.setObjectName("btn_unstage")
            self.verticalLayout.addWidget(self.btn_unstage)

            # Кнопка Refresh Status
            self.btn_refresh = QtWidgets.QPushButton(parent=self.centralwidget)
            self.btn_refresh.setObjectName("btn_refresh")
            self.verticalLayout.addWidget(self.btn_refresh)

            # Кнопка Open Graph
            self.btn_open_graph = QtWidgets.QPushButton(parent=self.centralwidget)
            self.btn_open_graph.setObjectName("btn_open_graph")
            self.verticalLayout.addWidget(self.btn_open_graph)

            self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

            MainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
            self.menubar.setObjectName("menubar")
            MainWindow.setMenuBar(self.menubar)

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

            # Связываем кнопку "Обновить" с методом обновления таблицы
            self.btn_refresh.clicked.connect(self.refresh_table)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(_translate("RepositoryWindow", f"Versio 😄 - {self.project_name}"))

        # Заголовки таблицы
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("RepositoryWindow", "Modified"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("RepositoryWindow", "Untracked"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("RepositoryWindow", "Staged"))

        # Тексты кнопок
        self.btn_commit.setText(_translate("RepositoryWindow", "Commit Changes"))
        self.btn_push.setText(_translate("RepositoryWindow", "Push Changes"))
        self.btn_pull.setText(_translate("RepositoryWindow", "Pull Changes"))
        self.btn_stage.setText(_translate("RepositoryWindow", "Stage Files"))
        self.btn_unstage.setText(_translate("RepositoryWindow", "Unstage Files"))
        self.btn_refresh.setText(_translate("RepositoryWindow", "Refresh Status"))
        self.btn_open_graph.setText(_translate("RepositoryWindow", "Open Graph"))

    def refresh_table(self):
        """
        Метод для обновления таблицы в окне репозитория.
        Получает состояние репозитория и обновляет таблицу.
        """
        # Получаем состояние репозитория
        repo = self.git_manager.get_repo()  # Предположим, что get_repo возвращает объект Repo
        status = repo.git.status('-s', '--porcelain').splitlines()

        # Разделяем изменения на три категории: modified, untracked, staged
        modified_files = []
        untracked_files = []
        staged_files = []

        for file in status:
            if file.startswith(' M'):
                modified_files.append(file[2:])
            elif file.startswith('??'):
                untracked_files.append(file[3:])
            elif file.startswith('A') or file.startswith('D'):
                staged_files.append(file[2:])

        # Обновляем таблицу
        self.tableWidget.setRowCount(0)  # Очищаем таблицу перед обновлением
        max_rows = max(len(modified_files), len(untracked_files), len(staged_files))

        for row in range(max_rows):
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(modified_files[row] if row < len(modified_files) else ""))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(untracked_files[row] if row < len(untracked_files) else ""))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(staged_files[row] if row < len(staged_files) else ""))

