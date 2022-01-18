import socket
import threading
import logging

from project.src.Coordinator import local_state_lock, remote_state_lock
from project.src.DataDeserializer import DataDeserializer


class TCPModule:
    """
    Class represents TCP module.
    """

    def __init__(self, listen_address, listen_port, buffer_size,
                 connection_close_simulation=False, additional_bytes_simulation=False, max_iterations=0):
        """
        TCPModule constructor.

        :param listen_address: address on which module listens
        :param listen_port: port on which tcp module is listening
        :param buffer_size: size of buffer for receiving messages
        :param connection_close_simulation: if true, simulation of connection close is performed
        :param additional_bytes_simulation: if true, simulation of adding additional bytes
        :param max_iterations: number of max iterations used in simulation, if connection_close_simulation is True
        """
        self.LISTEN_ADDRESS = listen_address
        self.LISTEN_PORT = listen_port
        self.BUFFER_SIZE = buffer_size
        self.listen_socket = None
        self.connection_close_simulation = connection_close_simulation
        self.additional_bytes_simulation = additional_bytes_simulation
        self.max_iterations = max_iterations

    def prepare_socket_listen(self):
        """
        Prepares socket for listening.
        :return: socket for listening
        """
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind((self.LISTEN_ADDRESS, self.LISTEN_PORT))
        listen_socket.listen(5)
        logging.info("SERVER TCP | Server listening at port " + str(self.LISTEN_PORT))
        return listen_socket

    def prepare_socket_send(self, address, port):
        """
        Prepares socket with connection to specific address and port.

        :param address: address to which socket will connect
        :param port: port to which socket will connect
        :return: connected socket
        """
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_socket.connect((address, port))
        return send_socket

    def send_data(self, socket_connection, data):
        """
        Performs send of data on specific socket.

        :param socket_connection: socket for connection
        :param data: data to send

        :return: 0 if file sent else exception object
        """
        try:
            if self.additional_bytes_simulation:
                data += b'ksiezniczkabalbinka'
            socket_connection.sendall(data)
            print("INFO | FILE SENT!")
            logging.info("SERVER TCP | FILE SENT!")
            socket_connection.close()
            return 0
        except Exception as exception:
            socket_connection.close()
            return exception

    def receive_data(self, socket_connection):
        """
        Performs receiving of data on given socket.

        :param socket_connection: socket with connection
        :return: data if got data, exception object if error
        """
        data = b''
        iteration = 0
        while True:
            if iteration == self.max_iterations and self.connection_close_simulation:
                print('Connection closed!')
                socket_connection.close()
                break
            else:
                try:
                    msg_data = socket_connection.recv(self.BUFFER_SIZE)
                except Exception as exception:
                    print("ERROR | Error while receiving file!")
                    logging.warning("SERVER TCP | Error while receiving data!")
                    socket_connection.close()
                    return exception
                if not msg_data:
                    break
                data += msg_data
                iteration += 1
        return data

    def listen_service(self, socket_connection, client_address, coordinator):
        """
        Performs listening logic.

        :param socket_connection: socket with connection
        :param client_address: address of client
        :param coordinator: coordinator object
        """
        data_decoder = DataDeserializer()
        connection_from = str(client_address[0]) + ":" + str(client_address[1])
        print(
            "INFO | Connection from "
            + connection_from
        )
        logging.info("SERVER TCP | Connection from " + connection_from)
        data = self.receive_data(socket_connection)

        if isinstance(data, Exception):
            logging.warning("SERVER TCP | Cant read data! " + str(data))
            return

        try:
            command, payload = data_decoder.deserialize_tcp(data)
        except Exception as exception:
            print(f"ERROR | Got wrong data, download abandoned!")
            logging.warning(f"SERVER TCP | {exception} - wrong hash, download abandoned!")

            socket_connection.close()
            connection_from = str(client_address[0]) + ":" + str(client_address[1])
            print(
                "INFO | SERVER TCP | Disconnection of "
                + connection_from
            )
            logging.info("SERVER TCP | Disconnection of " + connection_from)
            return

        if command == 'GETF':
            with local_state_lock:
                logging.info("SERVER TCP | GETF command received")
                if coordinator.local_state.get_local_file(payload.file_name) is None:
                    logging.warning(f"COORDINATOR | LOCAL STATE | FILE {payload.file_name} NOT FOUND, SENDING DECF!")
                    coordinator.send_decf(payload)
                else:
                    logging.info(f"COORDINATOR | LOCAL STATE | FILE {payload.file_name} FOUND, SENDING FILE!")
                    coordinator.send_file(payload)

        elif command == "FILE":
            logging.info("SERVER TCP | FILE command received")
            coordinator.save_file(payload=payload)

        elif command == "DECF":
            logging.info("SERVER TCP | DECF command received")
            coordinator.remove_node_from_file(payload=payload)
            print(f'ERROR | Can\'t download file {payload.file_name}! Try again!')
            logging.warning(f"CAN\'T DOWNLOAD FILE {payload.file_name}!")

        elif command == 'NDST':
            logging.info("SERVER TCP | NDST command received")
            with remote_state_lock:
                coordinator.remote_state.remove_node_from_others_files(payload.ip_address, payload.port)
                coordinator.add_other_files(payload)
            print(f'INFO | Got state of node with address {(payload.ip_address, payload.port)}: {payload.data}')
            logging.info(
                f"SERVER TCP | State of node with address {(payload.ip_address, payload.port)} is: {payload.data}")
        else:
            logging.warning(f"SERVER TCP | UNKNOWN COMMAND: {command}")

        socket_connection.close()
        connection_from = str(client_address[0]) + ":" + str(client_address[1])
        print(
            "INFO | Disconnection of "
            + connection_from
        )
        logging.info("SERVER TCP | Disconnection of " + connection_from)

    def start_listen(self, coordinator):
        """
        Performs start of listening.

        :param coordinator: coordinator object
        """
        self.listen_socket = self.prepare_socket_listen()
        while True:
            client_socket, client_address = self.listen_socket.accept()
            threading.Thread(
                target=self.listen_service,
                args=(
                    client_socket,
                    client_address,
                    coordinator,
                ),
                daemon=True,
            ).start()
