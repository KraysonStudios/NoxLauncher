import sys
import os
import subprocess
import shutil
import platform

if __name__ == "__main__":

    def optimize_linux() -> None:

        if os.path.exists("linux/NoxLauncher"): 

            process: subprocess.Popen = subprocess.Popen(f"""
upx --best linux/NoxLauncher/_internal/pydantic_core/_pydantic_core.cpython-312-x86_64-linux-gnu.so &&
upx --best linux/NoxLauncher/_internal/uvloop/loop.cpython-312-x86_64-linux-gnu.so
            """, shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)

            if process.wait(): 
                print(process.stderr.read()) 
                exit(1)

    def build_for_linux() -> None:

        if os.path.exists("linux/NoxLauncher"): shutil.rmtree("linux/NoxLauncher", ignore_errors= True)
        if os.path.exists("NoxLauncher.spec"): os.remove("NoxLauncher.spec")

        process: subprocess.Popen = subprocess.Popen(f'pyinstaller --clean --name="NoxLauncher" --optimize=2 --strip --nowindowed --noconsole --target-architecture=x86_64 --workpath="./work" --distpath="./linux" "../main.py"', shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)

        if process.wait(): 
            print(process.stderr.read()) 
            return

        optimize_linux()

        print("Build successful for Linux")

    def build_for_windows() -> None: 

        if os.path.exists("windows/NoxLauncher"): shutil.rmtree("windows/NoxLauncher", ignore_errors= True)
        if os.path.exists("NoxLauncher.spec"): os.remove("NoxLauncher.spec")

        process = subprocess.run(f'pyinstaller --onedir --noconsole --name="NoxLauncher" --optimize=2 --icon="../assets/icon.ico" --workpath="./work" --distpath="./windows" "../main.py"', shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE, stdin= subprocess.PIPE, text= True)
        
        if process.returncode != 0:
            print(process.stderr)
            return
        
        print("Build successful for Windows")

    if len(sys.argv) == 1: 
        print("Expected OS flag for build")
        exit(1)

    match sys.argv[1]:

        case "linux": build_for_linux() if platform.system() == "Linux" else print("Expected a Linux Host Machine to build for Linux")
        case "windows": build_for_windows() if platform.system() == "Windows" else print("Expected a Windows Host Machine to build for Windows")
        case _: print("Expected valid OS flag for build")

