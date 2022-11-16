class BashStreams:
    """ Struct to return object with stdout, stderr and the exit status of each command """
    def __init__(self, stdout, stderr, exit_status):
        self.stdout = stdout.read().decode()
        self.stderr = stderr.read().decode()
        self.exit_status = exit_status
 