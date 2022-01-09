from DataDeserializer import DataDeserializer
from DataSerializer import DataSerializer
from TCPModule import TCPModule
from StructPreparation import StructPreparation


class Coordinator:

    def deserialize(self, data):
        data_deserializer = DataDeserializer()
        return data_deserializer.deserialize(data)

    def serialize(self, command, payload):
        data_serializer = DataSerializer()
        return data_serializer.serialize_msg(command, payload)

    def send_ndst(self, addr, port):
        tcp_module = TCPModule()
        struct_preparation = StructPreparation()
        ndst_data = ['elo.txt', 'abc.asm', 'google.jpg']
        command, payload = struct_preparation.prepare_ndst(addr, port, ndst_data)
        data = self.serialize(command, payload)
        send_socket = tcp_module.prepare_socket_send(addr, port)
        tcp_module.send_ndst(send_socket, data)
