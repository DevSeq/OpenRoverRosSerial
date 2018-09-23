"""
This file is a sending/receiving script to the VESC 6

"""
import serial, sys, glob
from time import sleep

from packets import Packet
from commands import Commands
from datatypes import Scale, PacketID
import packets


'''
def test():
    phase = 0
    payload = bytearray()
    length = 0
    crc = 0
    
    time.sleep(1)  # give the connection a second to settle

    current_control = Packet(8, CURRENT_CONTROL_ID, NO_SCALE, 32, 0.3, CURRENT_CONTROL_ACCURACY)
    current_control_high = Packet(8, CURRENT_CONTROL_ID, NO_SCALE, 32, 0.5, CURRENT_CONTROL_ACCURACY)
    duty_control = Packet(8, DUTY_CONTROL_ID, NO_SCALE, 32, 0.1, DUTY_CONTROL_ACCURACY)
    alive = Packet(8, ALIVE_ID, NO_SCALE)
    reboot = Packet(8, REBOOT_ID, NO_SCALE)
    stop = Packet(8, 6, 1, 32, 0, CURRENT_CONTROL_ACCURACY)
    get_rt_data = Packet(8, GET_VALUES_ID, NO_SCALE)

    get_rt_data.send(vesc_usb)
    data = [[] for x in range(20)]
    counter = 0
    data_counter = 0
    wait_until = time.time() + 1
    data_req_sent = False
    while True:
        alive.send(vesc_usb)
        if process_buffer(vesc_usb.read(10)):
            data_counter += 1
            data_req_sent = False
            if data_counter > 10:
                counter += 1
                data_counter = 0
                Packet(8, DUTY_CONTROL_ID, NO_SCALE, 32, get_duty_for_counter(counter), DUTY_CONTROL_ACCURACY).send(vesc_usb)
                time.sleep(0.3)
                alive.send(vesc_usb)
                time.sleep(0.3)
            get_rt_data.send(vesc_usb)
        if counter > 19:
            break
    stop.send(vesc_usb)
    text_file = open("Output.txt", "w")
    print(data)
    text_file.writelines("%s\n" % numpy.average(item) for item in data)
    text_file.close()

'''
result = dict()
left_key = "left"
right_key = "right"
commands = Commands()

def setandmonitorPWM():
    get_data = Packet(8, PacketID.GET_VALUES, Scale.NONE)
    alive = Packet(8, PacketID.ALIVE, Scale.NONE)

    counter = 30
    if left_key in result:
        vesc_usb = serial.Serial(result[left_key], 115200, timeout=0.1)
        vesc_usb.flush()
        sleep(2)

        while(counter > 0):
            sleep(0.2)
            counter -= 1
            Packet(8, PacketID.SET_DUTY, Scale.NONE, 32, 0.50, Scale.E5).send(vesc_usb)
            sleep(0.3)
            #alive.send(vesc_usb)
            #sleep(0.3)
            get_data.send(vesc_usb)
            sleep(0.5)
            if vesc_usb.in_waiting > 5:
                buffer = Packet()
                converted = [int(elem.encode("hex"), 16) for elem in vesc_usb.read_all()]
                if buffer.process_buffer(converted):
                    commands.process_packet(buffer.goodpacket)
                    print "PWM:", commands.mcData.duty_now
                    print "RPM:",commands.mcData.rpm
                    print "Counter", counter

    vesc_usb.close()


''' values from spinning motor
[2, 59, 4, 1, 100, 252, 188, 255, 255, 255, 238, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 244, 0, 0, 7, 128, 1, 109, 0, 0, 0, 156, 0, 0, 0, 0, 0, 0, 22, 44, 0, 0, 0, 24, 0, 1, 14, 20, 0, 1, 48, 94, 0, 0, 0, 0, 0, 100, 38, 197, 3]
'''

def findandmapcontrollers():

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
                        commands.process_packet(buffer.goodpacket)
                        if commands.mcData.vesc_id == 100:
                            result[left_key] = a_port
                        elif commands.mcData.vesc_id == 200:
                            result[right_key] = a_port

                vesc_usb.close()
            except serial.SerialException:
                pass

    return result

if __name__ == '__main__':
    print "Test!!"
    findandmapcontrollers()
    setandmonitorPWM()
