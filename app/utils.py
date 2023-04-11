import socket

import paramiko


def send_command(hosts, cmd):
    for host in hosts:
        client = paramiko.SSHClient()

        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(host, username='root', password='marat', key_filename="/home/daniil/.ssh/id_rsa", timeout=10)
        except Exception as e:
            return f"Error {e} Invalid Ip {host}"

        stdin, stdout, stderr = client.exec_command(cmd)

        result = stdout.channel.recv_exit_status()
        client.close()
        return result
