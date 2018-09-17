from datatypes import Scale, PacketID, MotorControllerData



class Commands:
    def __init__(self):
        self.CanId = 0
        self.timeout = 0
        self.mcData = MotorControllerData()

    def process_packet(self, packet):
        if packet.get_next_number(8, Scale.NONE, True) == PacketID.GET_VALUES:


