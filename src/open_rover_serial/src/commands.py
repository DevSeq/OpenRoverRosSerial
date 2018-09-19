from datatypes import Scale, PacketID, MotorControllerData, FaultCode



class Commands:
    def __init__(self):
        self.CanId = 0
        self.timeout = 0
        self.mcData = MotorControllerData()

    def process_packet(self, packet):
        if packet.get_next_number(8, Scale.NONE, True) == PacketID.GET_VALUES:
            self.mcData.temp_mos           = float(packet.get_next_number(16, Scale.E1))
            self.mcData.temp_motor         = float(packet.get_next_number(16, Scale.E1))
            self.mcData.current_motor      = float(packet.get_next_number(32, Scale.E2))
            self.mcData.current_in         = float(packet.get_next_number(32, Scale.E2))
            self.mcData.id                 = float(packet.get_next_number(32, Scale.E2))
            self.mcData.iq                 = float(packet.get_next_number(32, Scale.E2))
            self.mcData.duty_now           = float(packet.get_next_number(16, Scale.E3))
            self.mcData.rpm                = float(packet.get_next_number(32, Scale.NONE))
            self.mcData.v_in               = float(packet.get_next_number(16, Scale.E1))
            self.mcData.amp_hours          = float(packet.get_next_number(32, Scale.E4))
            self.mcData.amp_hours_charged  = float(packet.get_next_number(32, Scale.E4))
            self.mcData.watt_hours         = float(packet.get_next_number(32, Scale.E4))
            self.mcData.watt_hours_charged = float(packet.get_next_number(32, Scale.E4))
            self.mcData.tachometer         = int(packet.get_next_number(32, Scale.NONE))
            self.mcData.tachometer_abs     = int(packet.get_next_number(32, Scale.NONE))
            self.mcData.fault_code         = FaultCode(int(packet.get_next_number(8, Scale.NONE)))

            if packet.length_left() >= 4:
                self.mcData.position = float(packet.get_next_number(32, Scale.E6))
            else:
                self.mcData.position = -1.0

            if packet.length_left() >= 1:
                self.mcData.vesc_id = int(packet.get_next_number(8, Scale.NONE))
            else:
                self.mcData.vesc_id = 255

            self.mcData.fault_str = ""

