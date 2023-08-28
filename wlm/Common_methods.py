import wlmData
import wlmConst
from Powermeter_methods import initialise_power_meter
import time
from WLM_methods import reference_const_PID_stabilisator
from WLM_methods import time_counter


def find_max_mod(absc_list, ord_list):
    '''
        Gets the max mod in the diagram Powers/frequencies

        :param absc_list: list of frequences
        :param ord_list: list of power values from PM
        :return: (the peak meaning of the mod, the frequency corresponding, the index in list) - tuple pack
    '''
    max_mod = max(ord_list)
    freq_of_max_mod = 0.
    index = -1
    for k in range(len(absc_list)):
        if (ord_list[k] == max_mod):
            freq_of_max_mod = absc_list[k]
            index = k
            break
    return max_mod,freq_of_max_mod,index

def find_breadth_mod(absc_list, ord_list, index_mod):
    '''
        Searches the breadth of maximum mod in the diagram Powers/frequencies

        :param absc_list: list of frequences
        :param ord_list: list of power values from PM
        :param index_mod: the index of the mod passing
        :return: difference in [THz]
    '''
    size = len(absc_list)
    assert index_mod >= 0 and index_mod < size, "Error: index of mod is out of bounds. Check lists of values and index"
    k1 = index_mod
    k2 = index_mod
    barier = ord_list[index_mod] / 2
    while(ord_list[k1] >= barier):
        k1+=1
    while(ord_list[k2] >= barier):
        k2-=1
    assert k1 >= 0 and k2 < size, "Error: index is out of bounds. The mod can be cut off"
    return absc_list[k1]-absc_list[k2]
def del_mod(absc_list, ord_list, index_mod, breadth):
    '''
        Deletes the mod passing to the parameters

        :param absc_list: list of frequences
        :param ord_list: list of power values from PM
        :param index_mod: the index of the mod passing
        :param breadth: the THZ "size" of the mod to delete
        :return:
    '''
    size = len(absc_list)
    assert index_mod >= 0 and index_mod < size, "Error: index of mod is out of bounds. Check lists of values and index"
    k1 = index_mod
    k2 = index_mod
    left = absc_list[index_mod] - breadth/2
    right = absc_list[index_mod] + breadth/2
    while (absc_list[k1] <= right):
        k1+=1
    while (absc_list[k2] >= left):
        k2 -= 1
    for _ in range(k1 - k2 + 1):
        del absc_list[k2]
        del ord_list[k2]

def stepping_PID_course(mode: bool, down_reference, upper_reference, stabilisation_time,
                        PID_step_mV, time_limit):
    '''
        Makes stepping PID. We can use PID_step_mV to vary the decline of the linear function dependency
        Note that due to the laser options 2 - 4096 mV the 1mV step takes nearly 1.5 MHz step in frequency

        :param mode: Set true if you pass the references in [THz]. Set false if in [nm]
        :param down_reference: the bottom frequency
        :param upper_reference: the upper values of frequency
        :param stabilisation_time: time to stabilise the bottom value
        :param PID_step_mV: the step of PID in [mv]
        :param time_limit: limit to perform the al-m
        :return: the dictionary representing the tuples (delta_frequency, power_resonator) and its size
    '''
    assert stabilisation_time < time_limit, "Error: too short time limit"
    koef = -2.23e-06 * 1.5225
    flag = False
    d_reference = down_reference
    u_reference = upper_reference
    delta_freq = koef * PID_step_mV
    d = {}
    i = 0
    if (not mode):
        d_reference = wlmData.dll.ConvertUnit(d_reference, wlmConst.cReturnWavelengthVac,
                                              wlmConst.cReturnFrequency)
        u_reference = wlmData.dll.ConvertUnit(upper_reference, wlmConst.cReturnWavelengthVac,
                                              wlmConst.cReturnFrequency)
    max_PID_val = 4096

    power_meter = initialise_power_meter("USB0::0x1313::0x8078::P0008894::INSTR")

    time1 = time.time()
    start_PID_point = wlmData.dll.GetDeviationSignalNum(1, 0)
    reference_const_PID_stabilisator(True, d_reference, koef, max_PID_val,
                                     wlmData.dll.GetExposureNum(1, 1, 0) * 1.2, stabilisation_time, start_PID_point)
    PID_current = wlmData.dll.GetDeviationSignalNum(1, 0)

    d[i] = (abs(wlmData.dll.ConvertUnit(wlmData.dll.GetWavelengthNum(1, 0), wlmConst.cReturnWavelengthVac,
                                        wlmConst.cReturnFrequency) - d_reference), power_meter.read)
    i += 1
    while (True):
        flag = False
        PID_current = PID_current + PID_step_mV
        cur_freq = wlmData.dll.ConvertUnit(wlmData.dll.GetWavelengthNum(1, 0), wlmConst.cReturnWavelengthVac,
                                           wlmConst.cReturnFrequency)
        if (cur_freq + delta_freq > u_reference):
            percent = (u_reference-cur_freq) / delta_freq
            if( percent > 0.1 and percent <= 1. and abs(PID_step_mV*percent) >= 0.125):
                PID_current = PID_current - PID_step_mV
                PID_current = PID_current + PID_step_mV*percent
                wlmData.dll.SetDeviationSignalNum(1, PID_current)
                freq = time_counter(cur_freq)
                d[i] = (abs(freq - d_reference), power_meter.read)
                if (d[i][0] / d[i - 1][0] > 1000):
                    del d[i]
                    flag = True
                if (not flag):
                    i += 1
            break
        wlmData.dll.SetDeviationSignalNum(1, PID_current)
        freq = time_counter(cur_freq)
        d[i] = (abs(freq - d_reference), power_meter.read)
        if(d[i][0]/d[i-1][0] > 1000):
            del d[i]
            flag = True
        if(not flag):
            i += 1
        if (time.time() - time1 > time_limit):
            break
    return d, i