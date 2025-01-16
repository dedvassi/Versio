import sys
from PyQt6.QtWidgets import QApplication, QMessageBox, QDialog

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
    git_manager = GitManager()
    # Проверяем глобальные настройки Git
    if not git_manager.check_global_config():
        from gui.dialogs import GitConfigDialog
        dialog = GitConfigDialog()

        # Показываем диалог и проверяем результат
        if dialog.exec() == QDialog.rejected:
            sys.exit()  # Завершаем приложение, если пользователь закрыл окно

        # Получаем введенные значения
        username, useremail = dialog.get_values()

        # Проверяем, что данные введены
        if not username or not useremail:
            dialog.warning_save_data()
            sys.exit()  # Завершаем приложение, если данные не введены

        # Сохраняем конфигурацию
        git_manager.set_global_config(username, useremail)

    # Запуск основного окна программы
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
