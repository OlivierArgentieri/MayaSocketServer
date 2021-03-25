class Utils:
    @staticmethod
    def is_port_is_use(host, port):
        """
        Is Port Is Use
        :param host:
        :pram port:
        :return boolean: true if port is in use, else if not
        """
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind((host, port))
            return True

        except Exception as socket_error:
            msg = "Socket Server, Failed to open port: {}".format(socket_error)
            return False

    @staticmethod
    def get_unused_ports(host, port_start, port_end):
        """
        Get Unused Ports
        :param host: host
        :param port_start: start range port
        :param port_end: end range port
        :return list: list of unused ports
        """
        available_ports = []
        ports = range(port_start, port_end)
        for i in ports:
            if (Utils.is_port_is_use(host, i)):
                available_ports.append(i)

        available_ports.sort()
        return available_ports

    @staticmethod
    def get_current_host():
        import socket
        return "127.0.0.1"  # TODO : BYPASS WSL INTERFACE
        return socket.gethostbyname(socket.gethostname())
