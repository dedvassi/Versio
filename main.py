import sys
from PyQt6.QtWidgets import QApplication, QMessageBox

from core.git_checker import is_git_installed
from gui.dialogs import GitNotInstalledDialog


def main():
    app = QApplication(sys.argv)

    # Проверка наличия Git
    if not is_git_installed():
        dialog = GitNotInstalledDialog()
        dialog.exec()
        sys.exit()  # Завершаем приложение, если Git не установлен

    # Теперь можно импортировать GitPython
    from core.git_manager import GitManager
    from gui.main_window import MainWindow

    # Проверяем глобальные настройки Git
    git_manager = GitManager()
    if not git_manager.check_global_config():
        sys.exit()  # Завершаем, если настройки Git некорректны

    # Запуск основного окна программы
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
