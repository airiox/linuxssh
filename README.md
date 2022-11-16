# linuxssh
Lightweight Python SSH interface for Linux built around paramiko. Provides with stdout, stderr and the exist status of the process. Also allows for sudo access. 

Example: 

    ssh = LinuxSSH("hostname.example.com", username="user1", password="S0m3PASSword!", require_password=True)
    with ssh:
        ssh.run("hostname -f")
        network_table = ssh.sudo("ss -tunap")
        if network_table.exit_status == 0:
            print(network_table.stdout)