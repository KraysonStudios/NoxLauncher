from concurrent.futures import ThreadPoolExecutor

NOXLAUNCHER_THREADPOOL: ThreadPoolExecutor = ThreadPoolExecutor(max_workers= 5, thread_name_prefix= "NoxLauncher Background")