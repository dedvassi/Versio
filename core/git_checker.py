import shutil

def is_git_installed() -> bool:
    """Проверяет, установлен ли Git на компьютере."""
    return shutil.which("git") is not None
