from .DataDeserializer import DataDeserializer
from .DataSerializer import DataSerializer
from .StructPreparation import StructPreparation
from .LocalStateModule import LocalStateModule
from .RemoteStateModule import RemoteStateModule
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
            command, payload = self.struct_preparation.prepare_nwrs(self.address, self.tcp_port, filename)
            data = self.serialize(command, payload)
            self.udp_module.send_broadcast(data)

    def remove_local_file(self, filename):
        self.local_state.remove_local_file(filename)
        command, payload = self.struct_preparation.prepare_rmrs(self.address, self.tcp_port, filename)
        data = self.serialize(command, payload)
        self.udp_module.send_broadcast(data)

    def add_other_files(self, payload):
        for filename in payload.data:
            self.remote_state.add_to_others_files(filename, payload.ip_address, payload.port)

    def get_others_files(self):
        command, payload = self.struct_preparation.prepare_gets(self.address, self.tcp_port)
        data = self.serialize(command, payload)
        self.udp_module.send_broadcast(data)

    def send_ndst(self, addr, port):
        ndst_data = self.local_state.get_local_files()
        command, payload = self.struct_preparation.prepare_ndst(self.address, self.tcp_port, ndst_data)
        data = self.serialize(command, payload)
        send_socket = self.tcp_module.prepare_socket_send(addr, port)
        self.tcp_module.send_ndst(send_socket, data)

    def send_file(self, send_socket, payload):
        print(payload.file_name)
        file = self.local_state.get_local_file(payload.file_name)
        command, payload = self.struct_preparation.prepare_file(self.address, self.tcp_port, file.name, file.data)
        data = self.serialize(command, payload)
        print(file.name)
        return self.tcp_module.send_data(send_socket, data)

    def print_info(self):
        print(f"UDP_PORT: {self.udp_port}, TCP_PORT: {self.tcp_port}, LOCAL_ADDRESS: {self.address}")

    def download_file(self, filename):
        addresses = self.remote_state.get_addresses_by_filename(filename)
        print(filename)
        print(addresses)
        if addresses is not None:
            send_params = random.choice(addresses)
            send_address, send_port = send_params[0], send_params[1]
            command, payload = self.struct_preparation.prepare_getf(self.address, self.tcp_port, filename)
            data = self.serialize(command, payload)
            send_socket = self.tcp_module.prepare_socket_send(send_address, send_port)
            received_data = self.tcp_module.send_getf(send_socket, data)
            command, payload = self.deserialize(received_data)
            self.add_local_file(File(payload.file_name, payload.data))
        else:
            print('FILE DOESNT EXIST! CANNOT DOWNLOAD THAT FILE')

    def send_nors(self):
        command, payload = self.struct_preparation.prepare_nors(self.address, self.tcp_port)
        data = self.serialize(command, payload)
        self.udp_module.send_broadcast(data)


