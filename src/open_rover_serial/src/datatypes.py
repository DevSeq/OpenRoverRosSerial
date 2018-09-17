from enum import Enum


class PacketID(Enum):
    FW_VERSION = 0
    JUMP_TO_BOOTLOADER = 1
    ERASE_NEW_APP = 2
    WRITE_NEW_APP_DATA = 3
    GET_VALUES = 4
    SET_DUTY = 5
    SET_CURRENT = 6
    SET_CURRENT_BRAKE = 7
    SET_RPM = 8
    SET_POS = 9
    SET_HANDBRAKE = 10
    SET_DETECT = 11
    SET_SERVO_POS = 12
    SET_MCCONF = 13
    GET_MCCONF = 14
    GET_MCCONF_DEFAULT = 15
    SET_APPCONF = 16
    GET_APPCONF = 17
    GET_APPCONF_DEFAULT = 18
    SAMPLE_PRINT = 19
    TERMINAL_CMD = 20
    PRINT = 21
    ROTOR_POSITION = 22
    EXPERIMENT_SAMPLE = 23
    DETECT_MOTOR_PARAM = 24
    DETECT_MOTOR_R_L = 25
    DETECT_MOTOR_FLUX_LINKAGE = 126
    DETECT_ENCODER = 26
    DETECT_HALL_FOC = 28
    REBOOT = 29
    ALIVE = 30
    GET_DECODED_PPM = 31
    GET_DECODED_ADC = 32
    GET_DECODED_CHUK = 33
    FORWARD_CAN = 34
    SET_CHUCK_DATA = 35
    CUSTOM_APP_DATA = 36
    NRF_START_PAIRING = 37
    
    
class FaultCode(Enum):
    NONE = 0
    OVER_VOLTAGE = 1
    UNDER_VOLTAGE = 2
    DRV = 3
    ABS_OVER_CURRENT = 4
    OVER_TEMP_FET = 5
    OVER_TEMP_MOTOR = 6


class Scale(Enum):
    NONE = 1
    E1   = 1e1
    E2   = 1e2
    E3   = 1e3
    E4   = 1e4
    E5   = 1e5
    E6   = 1e6


class MotorControllerData:
    def __init__(self):
        v_in = 0.0
        temp_mos = 0.0
        temp_motor = 0.0
        current_motor = 0.0
        current_in = 0.0
        id = 0.0
        iq = 0.0
        rpm = 0.0
        duty_now = 0.0
        amp_hours = 0.0
        amp_hours_charged = 0.0
        watt_hours = 0.0
        watt_hours_charged = 0.0
        tachometer = 0
        tachometer_abs = 0
        position = 0.0
        fault_code = FaultCode.NONE
        vesc_id = 0
        fault_str = ""

