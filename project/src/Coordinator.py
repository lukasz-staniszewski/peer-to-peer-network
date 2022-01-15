import threading

from .DataDeserializer import DataDeserializer
from .DataSerializer import DataSerializer
from .StructPreparation import StructPreparation
from .LocalStateModule import LocalStateModule
from .RemoteStateModule import RemoteStateModule
from .FileCoordinator import FileCoordinator
from project.File import File
import random


class Coordinator:

    def __init__(self, addr, udp_port, udp_module, tcp_port, tcp_module):
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.address = addr
        self.local_state = LocalStateModule()
        self.remote_state = RemoteStateModule()
        self.tcp_module = tcp_module
        self.udp_module = udp_module
        self.struct_preparation = StructPreparation()

    def deserialize(self, data):
        data_deserializer = DataDeserializer()
        return data_deserializer.deserialize(data)

    def serialize(self, command, payload):
        data_serializer = DataSerializer()
        return data_serializer.serialize_msg(command, payload)

    def add_local_file(self, filename):
        if self.local_state.add_local_file(filename):
            print(f"INFO | COORDINATOR BROADCAST | Sending NWRS of {filename}!")
            command, payload = self.struct_preparation.prepare_nwrs(self.address, self.tcp_port, filename)
            data = self.serialize(command, payload)
            self.udp_module.send_broadcast(data)
        else:
            print(f"ERROR | COORDINATOR | In local files there is already file {filename}!")

    def remove_local_file(self, filename):
        if self.local_state.remove_local_file(filename):
            print(f"INFO | COORDINATOR BROADCAST | Sending RMRS of {filename}!")
            command, payload = self.struct_preparation.prepare_rmrs(self.address, self.tcp_port, filename)
            data = self.serialize(command, payload)
            self.udp_module.send_broadcast(data)
        else:
            print(f"ERROR | COORDINATOR | In local files there is no {filename}!")

    def add_other_files(self, payload):
        for filename in payload.data:
            self.remote_state.add_to_others_files(filename, payload.ip_address, payload.port)

    def get_others_files(self):
        print(f"INFO | COORDINATOR BROADCAST | Sending GETS!")
        command, payload = self.struct_preparation.prepare_gets(self.address, self.tcp_port)
        data = self.serialize(command, payload)
        self.udp_module.send_broadcast(data)

    def perform_send(self, address, port, data):
        send_socket = self.tcp_module.prepare_socket_send(address, port)
        threading.Thread(
            target=self.tcp_module.send_data,
            args=(
                send_socket,
                data,
            ),
            daemon=True,
        ).start()

    def send_ndst(self, addr, port):
        print(f"INFO | COORDINATOR | STARTING SENDING NDST TO {addr}:{port}")
        ndst_data = self.local_state.get_local_files()
        command, payload = self.struct_preparation.prepare_ndst(self.address, self.tcp_port, ndst_data)
        data = self.serialize(command, payload)
        self.perform_send(address=addr, port=port, data=data)

    def send_file(self, payload):
        print(f"INFO | COORDINATOR | STARTING SENDING {payload.file_name} TO {payload.ip_address}:{payload.port}")
        addr = payload.ip_address
        port = payload.port
        file = self.local_state.get_local_file(payload.file_name)
        file_coordinator = FileCoordinator()
        data = file_coordinator.get_data_from_file(file_path=file.path)
        command, payload = self.struct_preparation.prepare_file(self.address, self.tcp_port, file.name, data)
        data = self.serialize(command, payload)
        self.perform_send(address=addr, port=port, data=data)

    def send_decf(self, payload):
        print(f"INFO | COORDINATOR | STARTING SENDING DECF OF {payload.file_name} TO {payload.ip_address}:{payload.port}")
        addr = payload.ip_address
        port = payload.port
        command, payload = self.struct_preparation.prepare_decf(self.address, self.tcp_port, payload.file_name)
        data = self.serialize(command, payload)
        self.perform_send(address=addr, port=port, data=data)


    def print_info(self):
        print(f"UDP_PORT: {self.udp_port}, TCP_PORT: {self.tcp_port}, LOCAL_ADDRESS: {self.address}")

    def download_file(self, filename):
        addresses = self.remote_state.get_addresses_by_filename(filename)
        print(f"INFO | DOWNLOADING | Downloading {filename}... from {addresses}")
        if addresses is not None:
            send_params = random.choice(addresses)
            send_address, send_port = send_params[0], send_params[1]
            command, payload = self.struct_preparation.prepare_getf(self.address, self.tcp_port, filename)
            data = self.serialize(command, payload)
            self.perform_send(address=send_address, port=send_port, data=data)
        else:
            print('ERROR | DOWNLOADING | File doesnt exists! Cannot download such file!')

    def save_file(self, payload):
        print(f'INFO | COORDINATOR | Saving file {payload.file_name}!')
        file_coordinator = FileCoordinator()
        new_file_path = file_coordinator.save_to_file(file_name=payload.file_name, file_data=payload.data)
        self.add_local_file(File(payload.file_name, new_file_path))

    def send_nors(self):
        print(f'INFO | COORDINATOR | Sending NORS!')
        command, payload = self.struct_preparation.prepare_nors(self.address, self.tcp_port)
        data = self.serialize(command, payload)
        self.udp_module.send_broadcast(data)

    def remove_node_from_file(self, payload):
        print(f'INFO | COORDINATOR | REMOTE STATE | '
              f'Removing ({payload.ip_address}:{payload.port}) from {payload.file_name} owners!')
        self.remote_state.remove_from_others_files(filename=payload.file_name, address=payload.ip_address,
                                                   port=payload.port)

