import pyvisa
import ThorlabsPM100

def initialise_power_meter(connection_row):
    '''
        Initialiser for Thorlabs Powermeter

        :param connection_row: the row representing connection to the specific tool
        :return: the object of powermeter connected
    '''
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource(connection_row)
    power_meter = ThorlabsPM100.ThorlabsPM100(inst=inst)
    return power_meter