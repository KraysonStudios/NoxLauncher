from concurrent.futures import ThreadPoolExecutor

class NoxLauncherThreadPool(ThreadPoolExecutor):

    def __init__(self, max_workers: int = 5, thread_name_prefix: str = "Nox Launcher") -> None:
        super().__init__(max_workers= max_workers, thread_name_prefix= thread_name_prefix)

    def flush(self) -> None:
        self.shutdown(wait= False, cancel_futures= True)

NOXLAUNCHER_THREAD_POOL: NoxLauncherThreadPool = NoxLauncherThreadPool(max_workers= 5, thread_name_prefix= "Nox Launcher Background")