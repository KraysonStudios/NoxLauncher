import sys
import os
import subprocess
import shutil
import platform
import getpass

if __name__ == "__main__":

    def optimize_linux(path: str) -> None:

        if not os.path.exists(path): return

        for name in os.listdir(path):
            if os.path.isfile(os.path.join(path, name)) and os.path.join(path, name).endswith(".so"): os.system(f"upx --best {os.path.join(path, name)}")
            if os.path.isdir(os.path.join(path, name)): optimize_linux(os.path.join(path, name))

    def build_for_linux() -> None:

        if os.path.exists("linux/NoxLauncher"): shutil.rmtree("linux/NoxLauncher", ignore_errors= True)
        if os.path.exists("NoxLauncher.spec"): os.remove("NoxLauncher.spec")

        pyinstaller_process: subprocess.Popen = subprocess.Popen(f'pyinstaller --clean --name="NoxLauncher" --optimize=2 --strip --upx-dir="/usr/bin/upx" --nowindowed --noconsole --target-architecture=x86_64 --workpath="./work" --distpath="./linux" "../main.py"', shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)
        updater_process: subprocess.Popen = subprocess.Popen(f'cargo build --release --manifest-path="{os.path.dirname(os.getcwd().replace("\\", "/"))}/updater/Cargo.toml" && upx --best "{os.path.dirname(os.getcwd().replace("\\", "/"))}/updater/target/release/updater"', shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)

        if pyinstaller_process.wait(): 
            print(pyinstaller_process.stderr.read()) 
            return
        
        if updater_process.wait():
            print(updater_process.stderr.read()) 
            return

        optimize_linux("linux/NoxLauncher")

        print("Build successful for Linux")

    def build_for_windows() -> None: 

        if os.path.exists("windows/NoxLauncher"): shutil.rmtree("windows/NoxLauncher", ignore_errors= True)
        if os.path.exists("NoxLauncher.spec"): os.remove("NoxLauncher.spec")

        pyinstaller_process = subprocess.run(f'pyinstaller --onedir --noconsole --name="NoxLauncher" --optimize=2 --icon="../assets/icon.ico" --workpath="./work" --distpath="./windows" "../main.py"', shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)
        updater_process = subprocess.run(f'cargo build --release --manifest-path="{os.path.dirname(os.getcwd().replace("\\", "/"))}/updater/Cargo.toml" && "C:/Users/{getpass.getuser()}/Documents/upx-4.2.4-win64/upx.exe" --best "{os.path.dirname(os.getcwd().replace("\\", "/"))}/updater/target/release/updater.exe"', shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)
        
        if pyinstaller_process.returncode != 0:
            print(pyinstaller_process.stderr)
            return
        
        if updater_process.returncode != 0:
            print(updater_process.stderr)
            return
        
        print("Build successful for Windows")

    if len(sys.argv) == 1: 
        print("Expected OS flag for build")
        exit(1)

    match sys.argv[1]:

        case "linux": build_for_linux() if platform.system() == "Linux" else print("Expected a Linux Host Machine to build for Linux")
        case "windows": build_for_windows() if platform.system() == "Windows" else print("Expected a Windows Host Machine to build for Windows")
        case _: print("Expected valid OS flag for build")

