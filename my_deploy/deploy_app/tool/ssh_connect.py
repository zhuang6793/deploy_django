import os
import time

from paramiko.client import SSHClient, AutoAddPolicy
from paramiko import Transport, SFTPClient


class SshUpload:
    def __init__(self, hostname, username, passwd, port=22):
        # self.ip = ip
        # self.port = port
        # self.user = user
        # self.passwd = passwd
        # self.filename = filename
        # self.localpath = self._path(localpath)
        # self.remotepath = self._path(remotepath)
        # self.deppath = self._path(deppath)
        self.client = None
        self.sftp = None
        # self.local_file_size = os.path.getsize(self.localpath + self.filename)
        self.arguments = {
            'hostname': hostname,
            'port': port,
            'username': username,
            'password': passwd
        }

    def ssh_client(self):
        if self.client is not None:
            return self.client
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(**self.arguments)
        return self.client

    def exec_command_raw(self, command, environment=None):
        channel = self.client.get_transport().open_session()
        if environment:
            channel.update_environment(environment)
        channel.set_combine_stderr(True)
        channel.exec_command(command)
        code, output = channel.recu_exit_status(), channel.recv(-1)
        return code, self._decode(output)

    def _path(self, path):
        if path.split('/')[-1] != '':
            path = path + '/'

        return path

    def put_file(self, local_path, remote_path, callback=None):

        sftp = self._get_sftp()
        sftp.put(local_path, remote_path, callback=callback, confirm=False)

    def put_file_by_fl(self, file, remote_path, callback=None):
        sftp = self._get_sftp()
        sftp.putfo(fl=file, remotepath=remote_path, callback=callback, confirm=False)

    def _decode(self, content):
        try:
            content = content.decode()
        except UnicodeDecodeError:
            content = content.decode(encoding='GBK', errors='ignore')
        return content

    def _get_sftp(self):
        if self.sftp:
            return self.sftp

        tran = Transport((self.arguments.get('hostname'), int(self.arguments.get('port'))))
        try:
            tran.connect(username=self.arguments.get('username'), password=self.arguments.get('password'))
        except Exception as err:
            return err
        self.sftp = SFTPClient.from_transport(tran)

        return self.sftp

    def callback(self, current, total):
        progress = min(int(current / self.local_file_size * 100), 100)
        print('上传进度：{}'.format(progress))

    def run_command(self, command, sudo_password):
        channel = self.sshClient.invoke_shell()
        channel.send(command)

        while not channel.recv_ready():
            time.sleep(0.1)

        output = channel.recv(1024).decode('utf-8')
        print(output)
        if 'password' in output.lower():
            channel.send(sudo_password)

        while not channel.recv_ready():
            time.sleep(0.1)

        output = channel.recv(1024).decode('utf-8')

        print(output)

        self.sshClient.close()

        return output

    def run(self):
        remot_file_name = self.filename.replace(" ", "")
        time_tuple = time.localtime(time.time())
        info_list = []
        beifen_command = f"mv  {self.deppath}{self.filename}  {self.deppath}{remot_file_name}{time_tuple[0]}-{time_tuple[1]}-{time_tuple[2]}.zip"
        path_command = f"[ -d {self.deppath}{remot_file_name.split('.')[0]} ] && echo OK"
        file_command = f"[ -f {self.deppath}{self.filename} ] && echo OK"
        qianyi_command = f"mv  {self.remotepath}{self.filename}  {self.deppath}{remot_file_name.split('.')[0]}"
        bushu_commadn = f"sudo unzip -o {self.deppath}{remot_file_name.split('.')[0]}/{remot_file_name}"
        if self.filename.split('.')[-1] != 'zip':
            return "只支持zip格式的文件"
        else:
            # self.sftp_client().put(localpath=self.localpath + self.filename,
            #                        remotepath=self.remotepath + remot_file_name, callback=self.callback)
            stdin, stdout, stderr = self.sshClient.exec_command(
                'echo {} | sudo -S {}'.format(self.passwd, beifen_command))
            if stderr != '':
                return stderr.readline()

            info_list.append(stdout.readline())
            stdin, stdout, stderr = self.sshClient.exec_command(
                'echo {} | sudo -S {}'.format(self.passwd, qianyi_command))
            if stderr != '':
                return stderr.readline()

            info_list.append(stdout.readline())
            stdin, stdout, stderr = self.sshClient.exec_command(
                'echo {} | sudo -S {}'.format(self.passwd, bushu_commadn))

            if stderr != '':
                return stderr.readline()

            info_list.append(stdout.readline())
            return info_list

    def __enter__(self):
        self.ssh_client()
        transport = self.sftp.get_transport()
        if 'windows' in transport.remote_version.lower():
            pass
            # self.exec_command = self.exec_command_raw
            # self.exec_command_with_stream = self._win_exec_command_with_stream
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        self.client = None
