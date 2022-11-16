import paramiko
from bashstreams import BashStreams


class LinuxSSH:
    def __init__(self, host, require_password=False, **kwargs):
        """refer to paramiko.connect() documention for **kwarg options"""
        self.host = host
        self.connect_kwargs = kwargs
        self.require_password = require_password
        if require_password and "password" not in self.connect_kwargs:
            raise Exception(
                "Must provide a password as arg or kwarg if require_password is set"
            )
        self.session = paramiko.SSHClient()
        self.session.set_missing_host_key_policy()

    def __del__(self):
        self.close()

    def close(self):
        if self.session:
            self.session.close()
            self.session = None

    @property
    def connected(self):
        return self.session.get_transport().is_active()

    def connect(self):
        self.session.connect(self.host, **self.connect_kwargs)

    def check_connection(self):
        if not self.connected:
            self.connect()

    def run(self, command):
        self.check_connection()
        _stdin, stdout, stderr = self.session.exec_command(command)
        return BashStreams(stdout, stderr, stdout.channel.recv_exit_status())

    def sudo(self, command):
        self.check_connection()
        command = f"sudo -S -p '' {command}"
        stdin, stdout, stderr = self.session.exec_command(command)
        if (
            self.require_password
        ):  # Enters password if password is expected in order to run sudo command
            stdin.write(self.connect_kwargs["password"] + "\n")
            stdin.flush()
        return BashStreams(stdout, stderr, stdout.channel.recv_exit_status())
