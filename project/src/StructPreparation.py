from project.structures.UDP_STR_RS import UDP_STR_RS
from project.structures.UDP_STR_INFO import UDP_STR_INFO
from project.structures.TCP_STR_CONT import TCP_STR_CONT
from project.structures.TCP_STR_INFO import TCP_STR_INFO


class StructPreparation:
    """
    Class prepares structures for payloads.
    """

    def prepare_ndst(self, addr, port, ndst_data):
        return 'NDST', TCP_STR_CONT(addr, port, None, ndst_data)

    def prepare_rmrs(self, addr, port, filename):
        return 'RMRS', UDP_STR_RS(addr, port, filename)

    def prepare_nwrs(self, addr, port, filename):
        return 'NWRS', UDP_STR_RS(addr, port, filename)

    def prepare_gets(self, addr, port):
        return 'GETS', UDP_STR_INFO(addr, port)

    def prepare_file(self, addr, port, filename, data):
        return 'FILE', TCP_STR_CONT(addr, port, filename, data)

    def prepare_getf(self, addr, port, filename):
        return 'GETF', TCP_STR_INFO(addr, port, filename)

    def prepare_nors(self, addr, port):
        return 'NORS', UDP_STR_INFO(addr, port)

    def prepare_decf(self, addr, port, filename):
        return 'DECF', TCP_STR_INFO(addr, port, filename)
