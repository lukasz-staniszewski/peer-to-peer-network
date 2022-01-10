from .DataDeserializer import DataDeserializer
from .DataSerializer import DataSerializer
from .TCPModule import TCPModule
from .StructPreparation import StructPreparation
from .LocalStateModule import LocalStateModule
from .RemoteStateModule import RemoteStateModule
from .UDPModule import UDPModule


class Coordinator:

    def __init__(self, addr, udp_port, tcp_port):
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.address = addr
        self.local_state = LocalStateModule()
        self.remote_state = RemoteStateModule()

    def deserialize(self, data):
        data_deserializer = DataDeserializer()
        return data_deserializer.deserialize(data)

    def serialize(self, command, payload):
        data_serializer = DataSerializer()
        return data_serializer.serialize_msg(command, payload)

    def add_local_file(self, filename):
        udp_module = UDPModule()
        struct_preparation = StructPreparation()
        self.local_state.add_local_file(filename)
        command, payload = struct_preparation.prepare_nwrs(self.address, self.tcp_port, filename)
        data = self.serialize(command, payload)
        udp_module.send_broadcast(data)

    def remove_local_file(self, filename):
        udp_module = UDPModule()
        struct_preparation = StructPreparation()
        self.local_state.remove_local_file(filename)
        command, payload = struct_preparation.prepare_rmrs(self.address, self.tcp_port, filename)
        data = self.serialize(command, payload)
        udp_module.send_broadcast(data)

    def get_others_files(self):
        udp_module = UDPModule()
        struct_preparation = StructPreparation()
        command, payload = struct_preparation.prepare_gets(self.address, self.tcp_port)
        data = self.serialize(command, payload)
        udp_module.send_broadcast(data)

    def send_ndst(self, addr, port):
        tcp_module = TCPModule()
        struct_preparation = StructPreparation()
        ndst_data = self.local_state.get_local_files()
        command, payload = struct_preparation.prepare_ndst(self.address, self.tcp_port, ndst_data)
        data = self.serialize(command, payload)
        send_socket = tcp_module.prepare_socket_send(addr, port)
        tcp_module.send_ndst(send_socket, data)
