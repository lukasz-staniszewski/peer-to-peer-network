import threading
import logging

from project.src.DataDeserializer import DataDeserializer
from project.src.DataSerializer import DataSerializer
from project.src.StructPreparation import StructPreparation
from project.src.LocalStateModule import LocalStateModule
from project.src.RemoteStateModule import RemoteStateModule
from project.src.FileCoordinator import FileCoordinator
from project.File import File
import random

local_state_lock = threading.Lock()
remote_state_lock = threading.Lock()


class Coordinator:
    """
    Class represents general coordinator.
    """
    def __init__(self, address, udp_port, udp_module, tcp_port, tcp_module):
        """
        Coordinator constructor.

        :param address: node address
        :param udp_port: udp broadcast listener port
        :param udp_module: udp broadcast module
        :param tcp_port: tcp transmission listener port
        :param tcp_module: tcp transmission module
        """
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.address = address
        self.local_state = LocalStateModule()
        self.remote_state = RemoteStateModule()
        self.tcp_module = tcp_module
        self.udp_module = udp_module
        self.struct_preparation = StructPreparation()

    def deserialize_udp(self, data):
        """
        Function performs deserialization of data for udp payloads.

        :param data: data to deserialize
        :return: deserialized data
        """
        data_deserializer = DataDeserializer()
        return data_deserializer.deserialize_udp(data)

    def serialize_udp(self, command, payload):
        """
        Performs serialization of udp payloads.

        :param command: sending command
        :param payload: payload to serialize
        :return: serialized data
        """
        data_serializer = DataSerializer()
        return data_serializer.serialize_udp(command, payload)

    def serialize_tcp(self, command, payload):
        """
        Performs serialization of tcp payloads.

        :param command: sending command
        :param payload: payload to serialize
        :return: serialized data
        """
        data_serializer = DataSerializer()
        return data_serializer.serialize_tcp(command, payload)

    def add_local_file(self, file_object):
        """
        Performs adding file with given name to local state.

        :param file object: object of file
        """
        with local_state_lock:
            if self.local_state.add_local_file(file_object):
                logging.info(f"COORDINATOR BROADCAST | Sending NWRS of {file_object.name}!")
                command, payload = self.struct_preparation.prepare_nwrs(self.address, self.tcp_port, file_object.name)
                data = self.serialize_udp(command, payload)
                self.udp_module.send_broadcast(data)
            else:
                print(f"ERROR | In local files there is already file {file_object.name}!")
                logging.warning(f"COORDINATOR | In local files there is already file {file_object.name}!")

    def remove_local_file(self, filename):
        """
        Performs removing file with given name from local state.

        :param filename: name of file to remove
        """
        with local_state_lock:
            if self.local_state.remove_local_file(filename):
                logging.info(f"COORDINATOR BROADCAST | Sending RMRS of {filename}!")
                command, payload = self.struct_preparation.prepare_rmrs(self.address, self.tcp_port, filename)
                data = self.serialize_udp(command, payload)
                self.udp_module.send_broadcast(data)
            else:
                print(f"ERROR | In local files there is no {filename}!")
                logging.warning(f"COORDINATOR | In local files there is no {filename}!")

    def add_other_files(self, payload):
        """
        Performs adding other node state to remote state.

        :param payload: payload with node state
        """
        for filename in payload.data:
            self.remote_state.add_to_others_files(filename, payload.ip_address, payload.port)

    def get_others_files(self):
        """
        Performs sending request for other nodes' states.
        """
        logging.info(f"COORDINATOR BROADCAST | Sending GETS!")
        command, payload = self.struct_preparation.prepare_gets(self.address, self.tcp_port)
        data = self.serialize_udp(command, payload)
        self.udp_module.send_broadcast(data)

    def perform_send(self, address, port, data):
        """
        Performs sending tcp data to specific node.

        :param address: address where to send
        :param port: port where to send
        :param data: tcp data to send
        """
        try:
            send_socket = self.tcp_module.prepare_socket_send(address, port)
            threading.Thread(
                target=self.tcp_module.send_data,
                args=(
                    send_socket,
                    data,
                ),
                daemon=True,
            ).start()

        except Exception as exception:
            print(f'ERROR | SERVER TCP | Can\'t establish a connection with {address, port}')
            logging.error(f"SERVER TCP | Can\'t establish a connection with {address, port} | {exception}")
            with remote_state_lock:
                self.remote_state.remove_node_from_others_files(address, port)

    def send_ndst(self, addr, port):
        """
        Performs sending NDST payload.

        :param addr: address where to send
        :param port: port on which to send
        """
        logging.info(f"COORDINATOR | STARTING SENDING NDST TO {addr}:{port}")
        with local_state_lock:
            ndst_data = self.local_state.get_myfiles_names()
        command, payload = self.struct_preparation.prepare_ndst(self.address, self.tcp_port, ndst_data)
        data = self.serialize_tcp(command, payload)
        self.perform_send(address=addr, port=port, data=data)

    def send_file(self, payload):
        """
        Performs sending file.

        :param payload: payload in which is file to send.
        """
        print(f"INFO | Starting sending {payload.file_name} to {payload.ip_address}:{payload.port}!")
        logging.info(f"COORDINATOR | STARTING SENDING {payload.file_name} TO {payload.ip_address}:{payload.port}")
        addr = payload.ip_address
        port = payload.port
        file = self.local_state.get_local_file(payload.file_name)
        file_coordinator = FileCoordinator()
        data = file_coordinator.get_data_from_file(file_path=file.path)
        command, payload = self.struct_preparation.prepare_file(self.address, self.tcp_port, file.name, data)
        data = self.serialize_tcp(command, payload)
        self.perform_send(address=addr, port=port, data=data)

    def send_decf(self, payload):
        """
        Performs sending DECF payload.

        :param payload: payload to send
        """
        logging.info(
            f"COORDINATOR | STARTING SENDING DECF OF {payload.file_name} TO {payload.ip_address}:{payload.port}")
        address = payload.ip_address
        port = payload.port
        command, payload = self.struct_preparation.prepare_decf(self.address, self.tcp_port, payload.file_name)
        data = self.serialize_tcp(command, payload)
        self.perform_send(address=address, port=port, data=data)

    def print_info(self):
        """
        Prints info about current node.
        """
        print(f"UDP_PORT: {self.udp_port}, TCP_PORT: {self.tcp_port}, LOCAL_ADDRESS: {self.address}")
        logging.info(f"UDP_PORT: {self.udp_port}, TCP_PORT: {self.tcp_port}, LOCAL_ADDRESS: {self.address}")

    def download_file(self, filename):
        """
        Performs download by sending GETF command.

        :param filename: name of file to download
        """
        with remote_state_lock:
            addresses = self.remote_state.get_addresses_by_filename(filename)
        #print(f"INFO | DOWNLOADING | Downloading {filename}... from {addresses}")
        logging.info(f"DOWNLOADING | Downloading {filename}... from {addresses}")
        if addresses is not None:
            send_params = random.choice(addresses)
            send_address, send_port = send_params[0], send_params[1]
            command, payload = self.struct_preparation.prepare_getf(self.address, self.tcp_port, filename)
            data = self.serialize_tcp(command, payload)
            self.perform_send(address=send_address, port=send_port, data=data)
        else:
            print('ERROR | DOWNLOADING | File doesnt exists! Cannot download such file!')
            logging.warning(f"DOWNLOADING | File {filename} doesnt exists! Cannot download such file!")

    def save_file(self, payload):
        """
        Save file to disk from given payload.

        :param payload: payload with file.
        """
        file_coordinator = FileCoordinator()
        with remote_state_lock:
            if payload.file_name not in self.local_state.get_local_files():
                print(f'INFO | Saving file {payload.file_name}...!')
                logging.info(f"COORDINATOR | Saving file {payload.file_name}...!")
                new_file_path = file_coordinator.save_to_file(file_name=payload.file_name, file_data=payload.data)
                self.add_local_file(File(payload.file_name, new_file_path))
            else:
                print(f'ERROR | Cant save file {payload.file_name} - already got it!')
                logging.warning(f"COORDINATOR | Cant save file {payload.file_name} - already got it!")

    def send_nors(self):
        """
        Performs sending NORS payload.
        """
        logging.info(f'COORDINATOR | Sending NORS!')
        command, payload = self.struct_preparation.prepare_nors(self.address, self.tcp_port)
        data = self.serialize_udp(command, payload)
        self.udp_module.send_broadcast(data)

    def remove_node_from_file(self, payload):
        """
        Performs removing node from file in remote states.

        :param payload: payload depending on which file is being removed
        """
        print(f'INFO | Removing owner of {payload.file_name}!')
        logging.info(f'COORDINATOR | REMOTE STATE | '
                     f'Removing ({payload.ip_address}:{payload.port}) from {payload.file_name} owners!')
        with remote_state_lock:
            self.remote_state.remove_from_others_files(filename=payload.file_name, address=payload.ip_address,
                                                       port=payload.port)

    def remove_all_local_files(self):
        """
        Performs removing all files from local state.
        """
        print(f'INFO | Removing all own files!')
        with local_state_lock:
            self.local_state.remove_all_files()
