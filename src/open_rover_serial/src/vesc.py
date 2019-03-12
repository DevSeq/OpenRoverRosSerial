"""
This file is a sending/receiving script to the VESC 6

"""
import serial, sys, glob
from time import sleep

from packets import Packet
from commands import Commands
from datatypes import Scale, PacketID


class Vesc:
    def __init__(self):
        self.left_back = None
        self.right_back = None

        self.commands = Commands()
        self.generalpacket = Packet()
        self.get_data = Packet(8, PacketID.GET_VALUES, Scale.NONE)
        self.alive = Packet(8, PacketID.ALIVE, Scale.NONE)

    def print_mc_data(self):
        print "PWM:", self.commands.mcData.duty_now
        print "RPM:", self.commands.mcData.rpm

    def setandmonitorPWM(self, leftduty, rightduty):
        Packet(8, PacketID.SET_DUTY, Scale.NONE, 32, leftduty,  Scale.E5).send(self.left_back)
        Packet(8, PacketID.SET_DUTY, Scale.NONE, 32, -rightduty, Scale.E5).send(self.right_back)
        '''
        sleep(0.05)
        self.get_data.send(self.left_back)
        sleep(0.05)
        if self.left_back.in_waiting > 5:
            converted = [int(elem.encode("hex"), 16) for elem in self.left_back.read_all()]
            if self.generalpacket.process_buffer(converted):
                self.commands.process_packet(self.generalpacket.goodpacket)
                self.print_mc_data()

        self.get_data.send(self.right_back)
        sleep(0.05)
        if self.right_back.in_waiting > 5:
            converted = [int(elem.encode("hex"), 16) for elem in self.right_back.read_all()]
            if self.generalpacket.process_buffer(converted):
                self.commands.process_packet(self.generalpacket.goodpacket)
                self.print_mc_data()

        '''
    def findandmapcontrollers(self):
        left_back_port = ""
        right_back_port = ""
        get_data = Packet(8, PacketID.GET_VALUES, Scale.NONE)
        if sys.platform.startswith ('linux'):
            temp_list = glob.glob('/dev/tty[A]*')

            for a_port in temp_list:

                try:
                    vesc_usb = serial.Serial(a_port, 115200, timeout=0.1)
                    vesc_usb.flush()
                    sleep(2)
                    get_data.send(vesc_usb)
                    sleep(0.5)
                    if vesc_usb.in_waiting > 5:
                        buffer = Packet()
                        converted = [int(elem.encode("hex"), 16) for elem in vesc_usb.read_all()]
                        if buffer.process_buffer(converted):
                            self.commands.process_packet(buffer.goodpacket)
                            if self.commands.mcData.vesc_id == 100:
                                left_back_port = a_port
                                print "Found left wheel.\n"
                            elif self.commands.mcData.vesc_id == 200:
                                print "Found right wheel.\n"
                                right_back_port = a_port

                    vesc_usb.close()
                except serial.SerialException:
                    pass

        if len(left_back_port) > 0  and len(right_back_port) > 0:
            self.left_back  = serial.Serial(left_back_port,  115200, timeout=0.1)
            self.right_back = serial.Serial(right_back_port, 115200, timeout=0.1)
            self.left_back.flush()
            self.right_back.flush()

#data = [2, 59, 4, 1, 100, 252, 188, 255, 255, 255, 238, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 244, 0, 0, 7, 128, 1, 109, 0, 0, 0, 156, 0, 0, 0, 0, 0, 0, 22, 44, 0, 0, 0, 24, 0, 1, 14, 20, 0, 1, 48, 94, 0, 0, 0, 0, 0, 100, 38, 197, 3]
'''
if __name__ == '__main__':
    print "Test!!"
    vesc = Vesc()
    vesc.findandmapcontrollers()

    while True:
        vesc.setandmonitorPWM(0.5, 0.5)
    
'''

