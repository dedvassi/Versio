import os
import json
from git import Repo, InvalidGitRepositoryError, NoSuchPathError
from core.file_status import FileStatus  # Импортируем класс FileStatus

class GitManager:
    def __init__(self):
        # Путь к файлу конфигурации, где хранятся последние репозитории
        self.config_path = os.path.join("data", "config.json")
        self.ensure_config_file()
        self.repo = None  # Это будет хранить текущий репозиторий
        self.file_status = None  # Это будет хранить объект для работы с состоянием файлов

    def ensure_config_file(self):
        """Создаёт файл конфигурации, если он отсутствует или пустой."""
        if not os.path.exists(self.config_path):
            # Если файл не существует, создаём его с дефолтными значениями
            self.create_default_config_file()
        elif os.path.getsize(self.config_path) == 0:
            # Если файл пустой, создаём его заново
            self.create_default_config_file()

    def create_default_config_file(self):
        """Создаёт файл конфигурации с дефолтными значениями."""
        if not os.path.exists(os.path.dirname(self.config_path)):
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

        # Содержимое по умолчанию
        default_config = {"recent_repositories": []}

        with open(self.config_path, "w") as config_file:
            json.dump(default_config, config_file, indent=4)

    def is_git_repository(self, folder_path):
        """
        Проверяет, является ли папка Git-репозиторием.

        Args:
            folder_path (str): Путь к папке.

        Returns:
            bool: True, если папка содержит .git, иначе False.
        """
        try:
            Repo(folder_path).git_dir  # Попробуем открыть репозиторий
            return True
        except (InvalidGitRepositoryError, NoSuchPathError):
            return False

    def init_repository(self, folder_path):
        """
        Инициализирует новый Git-репозиторий в указанной папке.

        Args:
            folder_path (str): Путь к папке.
        """
        Repo.init(folder_path)

    def save_recent_repository(self, folder_path):
        """
        Сохраняет путь к репозиторию в список недавних проектов.

        Args:
            folder_path (str): Путь к папке с репозиторием.
        """
        try:
            with open(self.config_path, "r") as config_file:
                config = json.load(config_file)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            # Если файл пустой или поврежден, восстанавливаем его
            print("Ошибка: файл конфигурации поврежден или пуст.")
            self.create_default_config_file()  # Восстанавливаем файл с дефолтными значениями
            config = {"recent_repositories": []}  # Загружаем дефолтные данные

        # Удаляем дубликаты и добавляем новый путь в начало списка
        recent = config.get("recent_repositories", [])
        if folder_path in recent:
            recent.remove(folder_path)
        recent.insert(0, folder_path)

        # Ограничиваем список до 10 записей
        config["recent_repositories"] = recent[:10]

        # Сохраняем изменения
        with open(self.config_path, "w") as config_file:
            json.dump(config, config_file, indent=4)

    def get_recent_repositories(self):
        """
        Возвращает список последних репозиториев.

        Returns:
            list: Список путей к недавним репозиториям.
        """
        try:
            with open(self.config_path, "r") as config_file:
                config = json.load(config_file)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            print("Ошибка при загрузке конфигурации. Создаём новый файл.")
            self.create_default_config_file()
            config = {"recent_repositories": []}  # Возвращаем дефолтное значение

        return config.get("recent_repositories", [])

    def load_repo(self, folder_path):
        """
        Загружает репозиторий и создаёт объект для работы с состоянием файлов.

        Args:
            folder_path (str): Путь к папке с репозиторием.
        """
        if self.is_git_repository(folder_path):
            self.repo = Repo(folder_path)
            self.file_status = FileStatus(self.repo)  # Инициализируем FileStatus для текущего репозитория
        else:
            raise ValueError(f"{folder_path} не является Git-репозиторием.")

    def get_repo(self):
        """
        Возвращает текущий репозиторий.

        Returns:
            Repo: Объект репозитория Git.
        """
        if self.repo:
            return self.repo
        else:
            raise ValueError("Репозиторий не загружен. Сначала вызовите load_repo().")

    def get_file_status(self):
        """
        Получает состояние файлов в текущем репозитории.

        Returns:
            dict: Статус файлов в репозитории (modified, untracked, staged).
        """
        if self.file_status:
            return self.file_status.get_all_file_status()
        else:
            raise ValueError("Репозиторий не загружен. Сначала вызовите load_repo().")
