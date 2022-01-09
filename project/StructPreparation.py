from structures.UDP_STR_RS import UDP_STR_RS
from structures.UDP_STR_INFO import UDP_STR_INFO
from structures.TCP_STR_CONT import TCP_STR_CONT
from structures.TCP_STR_INFO import TCP_STR_INFO


class StructPreparation:

    def prepare_ndst(self, addr, port, ndst_data):
        return 'NDST', TCP_STR_CONT(addr, port, None, ndst_data)
