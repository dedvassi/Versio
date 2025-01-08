import git

class FileStatus:
    def __init__(self, repo):
        self.repo = repo

    def get_modified_files(self):
        """Возвращает список изменённых файлов (modified)."""
        modified_files = [item.a_path for item in self.repo.index.diff(None)]
        return modified_files

    def get_untracked_files(self):
        """Возвращает список неотслеживаемых файлов (untracked)."""
        untracked_files = self.repo.untracked_files
        return untracked_files

    def get_staged_files(self):
        """Возвращает список индексированных файлов (staged)."""
        staged_files = [item.a_path for item in self.repo.index.diff("HEAD")]
        return staged_files

    def get_all_file_status(self):
        """Возвращает все данные о статусе файлов (modified, untracked, staged)."""
        return {
            "modified": self.get_modified_files(),
            "untracked": self.get_untracked_files(),
            "staged": self.get_staged_files()
        }