import os
import socket
from time import sleep

import paramiko


DANGEROUS_COMMANDS = ["rm -rf /", "rm -rf .", "rm -rf *", ":(){:|:&};:"]


def send_command(host, cmd):
    results = {}
    client = paramiko.SSHClient()
    username = os.getenv("USERNAME_HOST")
    password = os.getenv("PASSWORD_HOST")
    key_filename = os.getenv("KEY_PATH")
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=username, password=password, key_filename=key_filename, timeout=10)
    except Exception as e:
        return f"Error {e} Invalid Ip {host}"

    if cmd in DANGEROUS_COMMANDS:
        return "Inputed command blocked by developers"
    stdin, stdout, stderr = client.exec_command(cmd)

    result = stdout.channel.recv_exit_status()
    results[host] = result
    client.close()
    stdin.close()
    stdout.close()
    stderr.close()
    return results
