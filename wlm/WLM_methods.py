import ctypes

import numpy as np

import wlmData
import wlmConst
import time
import matplotlib.pyplot as plt
import math

# constant that shows the dependency between PID and frequency
# that constant passes to the parameters of functions that make PID regulation
cDependFrequencyPID = -2.23e-06*1.5225

# Gets the exposition. Parameter is the channel to use. Param can be set in separate scroll or else in UI
# Return value can be shown in text form in UI
def get_exposure1(chan: int):
    '''
        Function to get the exposition time from the 1st ccd array in ms

        Errors: 1 - The Wavelength Meter is not active
                2 - The specified channel or array index is not available for this Wavelength
                    Meter version
        :param chan: channel number
        :return: the value of exposition or error code
    '''
    answer = wlmData.dll.GetExposureNum(chan,1,0)
    if(answer == wlmConst.ErrWlmMissing):
        return 1
    elif(answer == wlmConst.ErrNotAvailable):
        return 2
    else:
        return answer

# in UI there can be a checkbox to turn that on or off.
def built_in_laser_regulation(mode: bool):
    '''
        Sets a regulation mode. Whether mode is true we use built-in laser regulation. If false - we don't use any.

        :param chan: channel to use
        :param mode: the parameter to turn regulation of laser on or off
        :return: 0 or error
    '''
    return wlmData.dll.SetDeviationMode(mode)
# in UI there can be a checkbox to turn that on or off.
def autoexposure(chan: int, setting: bool):
    '''
        Sets an exposure mode. Whether setting is true we use auto mode. If false - than manual.

        :param chan: channel to use
        :param setting: the parameter to turn auto mode on or off
        :return: 0 or error
    '''
    return wlmData.dll.SetExposureModeNum(chan, setting)

# Sets the exposition. Parameter is the channel to use. Param can be set in separate scroll or else in UI
# Value to be set can be shown in text form in UI
def set_exposure1(chan: int, value):
    '''
    Sets exposure for the 1st ccd array in ms
    :param chan: channel to use
    :param value: value to be set
    :return: 0 or set_error, -40 - value out of range
    '''
    if((wlmData.dll.GetExposureRange(wlmConst.cExpoMin) <= value) and (wlmData.dll.GetExposureRange(wlmConst.cExpoMax) >= value)):
        return wlmData.dll.SetExposureNum(chan, 1, value)
    else:
        return -40
# This can be used for the feedback with user if some setting went wrong.
def return_set_errors(switcher_error) -> str:
    '''
        The function represents errors of setters

        :param switcher_error: the result of set function (contains error code)
        Comment: if everything is ok set function will return 0
        :return: error string
    '''
    if (switcher_error == wlmConst.ResERR_WlmMissing):
        return "The WLM isn't instantiated"
    elif (switcher_error == wlmConst.ResERR_CouldNotSet):
        return "The value hasn't been set"
    elif (switcher_error == wlmConst.ResERR_ParmOutOfRange):
        return "Parameters are out of range"
    elif (switcher_error == wlmConst.ResERR_WlmOutOfResources):
        return "WLM is out of resources"
    elif (switcher_error == wlmConst.ResERR_WlmInternalError):
        return "WLM internal error"
    elif (switcher_error == wlmConst.ResERR_NotAvailable):
        return "The specified channel or array index is not available for this Wavelength Meter version"
    elif (switcher_error == wlmConst.ResERR_WlmBusy):
        return "WLM is busy"

    elif (switcher_error == wlmConst.ResERR_NotInMeasurementMode):
        return "WLM isn't in measurement mode"
    elif (switcher_error == wlmConst.ResERR_OnlyInMeasurementMode):
        return "WLM is only in measurement mode"
    elif (switcher_error == wlmConst.ResERR_ChannelNotAvailable):
        return "The channel isn't available"
    elif (switcher_error == wlmConst.ResERR_ChannelTemporarilyNotAvailable):
        return "The channel is temporarily not available"
    elif (switcher_error == wlmConst.ResERR_CalOptionNotAvailable):
        return "Calibration option isn't available"
    elif (switcher_error == wlmConst.ResERR_CalWavelengthOutOfRange):
        return "Calibration wavelength is out of range"

    elif (switcher_error == wlmConst.ResERR_BadCalibrationSignal):
        return "Bad calibration signal"
    elif (switcher_error == wlmConst.ResERR_UnitNotAvailable):
        return "Unit isn't available"
    elif (switcher_error == wlmConst.ResERR_FileNotFound):
        return "File not found"
    elif (switcher_error == wlmConst.ResERR_FileCreation):
        return "File creation error"
    elif (switcher_error == wlmConst.ResERR_TriggerPending):
        return "Trigger pending error"
    elif (switcher_error == wlmConst.ResERR_TriggerWaiting):
        return "Trigger waiting error"

    elif (switcher_error == wlmConst.ResERR_NoLegitimation):
        return "No legitimation error"
    elif (switcher_error == wlmConst.ResERR_NoTCPLegitimation):
        return "No TCP legitimation error"
    elif (switcher_error == wlmConst.ResERR_NotInPulseMode):
        return "WLM isn't in pulse mode"
    elif (switcher_error == wlmConst.ResERR_OnlyInPulseMode):
        return "WLM is only in pulse mode"
    elif (switcher_error == wlmConst.ResERR_NotInSwitchMode):
        return "WLM isn't in switch mode"
    elif (switcher_error == wlmConst.ResERR_OnlyInSwitchMode):
        return "WLM is only in switch mode"
    elif (switcher_error == wlmConst.ResERR_TCPErr):
        return "TCP error"
    elif (switcher_error == wlmConst.ResERR_StringTooLong):
        return "String too long"
    elif (switcher_error == wlmConst.ResERR_InterruptedByUser):
        return "Interrupted by user"

# This can be used for the feedback with user if getwavelength or getfrequency went wrong
# for ex. if GetWavelengthNum returns wlmConst.ErrWlmMissing val we can inform user with dialog
def get_wavelength_frequency_errors(switcher_error) -> str:
    '''
        The function represents errors of GetWavelength and GetFrequency

        :param switcher_error: the result of set function (contains error code)
        Comment: if everything is ok set function will return 0
        :return: error string
    '''
    if (switcher_error == wlmConst.ErrWlmMissing):
        return "The Wavelength Meter is not active"
    elif (switcher_error == wlmConst.ErrNotAvailable):
        return "The specified channel or array index is not available for this Wavelength Meter version"
    elif (switcher_error == wlmConst.ErrNoValue):
        return "No value"
    elif (switcher_error == wlmConst.ErrNoSignal):
        return "The Wavelength Meter has not detected any signal."
    elif (switcher_error == wlmConst.ErrBadSignal):
        return "The Wavelength Meter has not detected a calculable signal."
    elif (switcher_error == wlmConst.ErrLowSignal):
        return "The signal is too small to be calculated properly."
    elif (switcher_error == wlmConst.ErrBigSignal):
        return "The signal is too large to be calculated properly, this can happen if the amplitude of the signal is electronically cut caused by stack overflow."
    elif (switcher_error == wlmConst.ErrNoPulse):
        return "The detected signal could not be divided into separated pulses."

# Gets the frequency. Parameter is the channel to use. Param can be set in separate scroll or else in UI
# Return value can be shown in text form in UI
def get_frequency(chan: int):
    '''
        Function to get current frequency

        :param chan: the channel to be used
        :return: Frequency in THz or error
    '''
    return wlmData.dll.GetFrequencyNum(chan, 0)
# the same as previous
def get_wavelength(chan: int):
    '''
        Function to get current wavelength

        :param chan: the channel to be used
        :return: Wavelength in nm or error
    '''
    return wlmData.dll.GetWavelengthNum(chan, 0)

# This gets PID in mV. UI can show the result value. Parameter is the channel to use - that should be specified by user
# The result depends on the timing that is set in ScanMeasurement method. We can make checkbox whether to show or not the
# PID in separate field
def get_current_PID(chan: int):
    '''
        Returns the analog output voltage of a specified DAC channel in
        Wavelength Meter versions with Deviation output or PID regulation function.

        :param chan: channel number
        :return: the value of output WLM DAC channel PID in mV
    '''
    answer = wlmData.dll.GetDeviationSignalNum(chan, 0)
    return answer

# this function sets the PID but doesn't "hold" it
# the gui is pretty same: we need field to enter value and channel
# and we can show error if something went wrong
# errors for set methods were listed earlier
def set_PID_const(chan: int, value: float):
    '''
        Sets the PID laser control manually in mV with constant val

        :param chan: channel to use
        :param value: value to set
        :return: 0 if ok and error code if something wrong
        Comment: set errors were described separately
    '''
    return wlmData.dll.SetDeviationSignalNum(chan, value)

# The function represents PID regulation of constant type
# In GUI it can be used to set constant frequency or wavelength and "hold" it until terminate process
# In gui could be setting of channel (chan), choosing the units (mode) i.e. nm/THZ, timer to wait after each setting of PID (time_pause),
# start point for PID and channel to use.
# the method should be made as a separate process
def reference_const_PID_stabilisator(mode: bool,  reference_wl: float, koef: float, max_PID_val: int, time_pause: int,  start_PID_point = 4096/2, chan = 1):
    '''
        The function stabilises the reference value of frequency
        2nd version of algorithm

        :param mode: True - reference_wl should be frequency
        :param reference_wl: frequency or wavelength (no matter in fact, unless you didn't set the right mode. We use frequencies inside algorithm anyway)
        :param koef: koef of dependency between PID mV and frequency
        :param max_PID_val: max val in mV for PID
        :param time_pause: pause after setting value needed
        :param start_PID_point: starting point of PID setting.
        :param chan: shows the channel to use
        :return: nothing or -42 (PID is out of range)
    '''
    stabilised = False
    PID_step = 0
    PID_current = start_PID_point
    reference = reference_wl
    if(not mode):
        reference = wlmData.dll.ConvertUnit(reference, wlmConst.cReturnWavelengthVac,
                                wlmConst.cReturnFrequency)
    while(True):
        if(not stabilised):
            PID_current = PID_current + PID_step
            wlmData.dll.SetDeviationSignalNum(chan, PID_current)
            time.sleep(time_pause / 1000)
        wave_current = wlmData.dll.ConvertUnit(wlmData.dll.GetWavelengthNum(chan, 0), wlmConst.cReturnWavelengthVac,
                                       wlmConst.cReturnFrequency)
        delta = reference - wave_current
        abs_dev = abs(delta)
        # 0.125 changes in 180 kHz. it's the 7th from point int THz view of freq
        if(abs_dev >= 10e-07 and abs_dev <= 5*10e-07):
            if (delta > 0):
                PID_step = -0.125
            elif (delta < 0):
                PID_step = 0.125
        elif (abs_dev > 5*10e-07 and abs_dev <= 10e-06):
            if (delta > 0):
                PID_step = -0.625
            elif (delta < 0):
                PID_step = 0.625
        elif (abs_dev > 10e-06 and abs_dev <= 5*10e-06):
            if (delta > 0):
                PID_step = -3.125
            elif (delta < 0):
                PID_step = 3.125
        elif (abs_dev > 5*10e-06 and abs_dev <= 10e-05):
            if (delta > 0):
                PID_step = -15.625
            elif (delta < 0):
                PID_step = 15.625
        elif (abs_dev > 10e-05 and abs_dev <= 10e-04):
            if (delta > 0):
                PID_step = -156.25
            elif (delta < 0):
                PID_step = 156.25
        elif(abs_dev > 10e-04 ):
            PID_step = delta / koef
        if(( PID_current + PID_step ) > max_PID_val or ( PID_current + PID_step ) < 0):
            return -42
        if(round(delta,7) == 0.0000000):
            stabilised = True
        elif(stabilised):
            stabilised = False

# this method could be called with some timing as a separate process
# In UI could've been made Timing field, field that shows the result that refreshes every "timing" ms
# then an interface unit like scroller or else could make reset of units of measurement.  "chan" is also specified by user
# There also could be some action to start and terminate this process from user
def scan_measurement(unit: int, chan: int):
    '''

    :param unit: a unit to get the result: 0 - nm; 1 - THz
    :param chan: channel to scan
    :return: current result or set_error or set_unit_error (-41)
    Comment: set_errors have been described separately
    '''
    if(unit == 0):
        return get_wavelength(chan)
    elif(unit == 1):
        return get_frequency(chan)
    else:
        return -41

# The method represents the PID regulation of type "Stairs"
# GUI can be as for const PID regulation except the parameters
# There also could be scrolls to choose units (mode); fields for the bottom (down_reference)
# and upper (upper_reference) values of frequencies or wavelengths
# for stabilisation time in ms (stabilisation_time) and for PID increase every step (PID_step_mV)
def triangle_PID_course(mode: bool, down_reference: float, upper_reference: float, stabilisation_time: int, PID_step_mV: float):
    '''
        The function makes triangle PID stepping

        :param mode: Set true if you pass the references in [THz]. Set false if in [nm]
        :param down_reference: the bottom frequency
        :param upper_reference: the upper values of frequency
        :param stabilisation_time: time to stabilise the bottom value
        :param PID_step_mV: the step of PID in [mv]
        :return:
    '''
    koef = -2.23e-06*1.5225
    d_reference = down_reference
    u_reference = upper_reference
    delta_freq = koef*PID_step_mV
    d = {}
    i = 0
    if(not mode):
        d_reference = wlmData.dll.ConvertUnit(d_reference, wlmConst.cReturnWavelengthVac,
                                wlmConst.cReturnFrequency)
        u_reference = wlmData.dll.ConvertUnit(upper_reference, wlmConst.cReturnWavelengthVac,
                                wlmConst.cReturnFrequency)
    max_PID_val = 4096
    while(True):
        start_PID_point = wlmData.dll.GetDeviationSignalNum(1, 0)
        reference_const_PID_stabilisator(True, d_reference, koef, max_PID_val,
                                                     wlmData.dll.GetExposureNum(1, 1, 0) * 1.2, stabilisation_time, start_PID_point)
        PID_current = wlmData.dll.GetDeviationSignalNum(1, 0)
        while(True):
            PID_current = PID_current + PID_step_mV
            cur_freq = wlmData.dll.ConvertUnit(wlmData.dll.GetWavelengthNum(1,0), wlmConst.cReturnWavelengthVac,
                                               wlmConst.cReturnFrequency)
            if(cur_freq + delta_freq > u_reference):
                break
            wlmData.dll.SetDeviationSignalNum(1, PID_current)
            time_counter(cur_freq)

#________________________________________________________________________________________________________________________

def set_wl(amount):
    '''
    The function can set PID_course of every type, not only constant
    we can place here some law, e.g. sin or cos but there is some style of doing
    this that is said in manual to WLM

    :param amount: the set of PID course
    :return:
    '''
    new_b = bytes('= ' + str(amount), encoding='utf-8')
    new_PIDC = ctypes.create_string_buffer(new_b)
    print(new_PIDC.value.decode())
    if (wlmData.dll.SetPIDCourseNum(1, new_PIDC) == wlmConst.ResERR_NoErr):
        print("Successful write-in %s" % new_PIDC.value.decode())

def set_wl2(amount):
    '''
    The same as set_wl but without feedback

    :param amount: the set of PID course
    :return:
    '''
    new_b = bytes('= ' + str(amount), encoding='utf-8')
    new_PIDC = ctypes.create_string_buffer(new_b)
    wlmData.dll.SetPIDCourseNum(1, new_PIDC)

def wavelength_regulation(cycle_steps, initial_wave, delta_wave, time_pause_set, time_pause_getpwr, wl_precision):
    ''' Definition:
        _________________________________________________________________
        The function makes needed steps of 'set - measure' wavelength
        in WLM with explicit interruptions and wavelength step setting
        _________________________________________________________________
        Parameters:
        ________________________________________________________________
        cycle_steps - how many cycles of 'set - measure' do we need
        initial_wave - current wavelength, set in WLM
        delta_wave - step of wavelength to change WLM initial wavelength
        time_pause_set - time to wait after setting wavelength of WLM in ms
        time_pause_getpwr - time to wait after getting power of measurement shot in WLM of al-m in ms
        wl_precision - precision of wavelength in number of digits
        _________________________________________________________________
        Return:
        _________________________________________________________________
        A dictionary of tuples that consist of 4 parts.
        1 - time between set_wl and the moment after last pause including all pauses
        2 - wavelength that was set
        3 - wavelength that was got after set to check whether it was set right
        4 - power of the measurement shot
        _________________________________________________________________
        Comment:
        _________________________________________________________________
        The function uses SetPIDCourse, hence we need PID regulator on when use
        it.
    '''
    d = {}
    i = 1
    while(i <= cycle_steps):
        wl_set = round(initial_wave + i*delta_wave, wl_precision)
        time1 = time.time()
        set_wl2(wl_set)
        time.sleep(time_pause_set*0.001)
        wavelength1 = round(wlmData.dll.GetWavelengthNum(1, 0), wl_precision)
        power1 = round(wlmData.dll.GetPowerNum(1,0),2)
        time.sleep(time_pause_getpwr * 0.001)
        time2 = time.time()
        d[i] = (round((time2-time1)*1000,2), wl_set, wavelength1, power1)
        i+=1
    return d

def wavelength_PID_bond(points, PID_step, PID_start, expo_time):
    '''
        Function reveals the dependency between PID and wavelength

        :param points: the number of PID points
        :param PID_step: step per each PID point
        :param PID_start: the start
        :param expo_time: exposition or any delay time
        :return: the dictionary of (PID, wavelength) tuples

        Comment: here wavelength is in [nm]
    '''
    i = 0
    d = {}
    while (i < points):
        PID = PID_start + i*PID_step
        wlmData.dll.SetDeviationSignalNum(1, PID)
        time.sleep((expo_time)/1000)
        wave = wlmData.dll.GetWavelengthNum(1, 0)
        d[i] = (PID, wave)
        i+=1
    wlmData.dll.SetDeviationSignalNum(1, PID_start)
    return d

# Don't need it really. Better to make general plotter than. To reduce code for plotting
def plot_wavelength_PID_bond(points, PID_step):
    expo_time =  wlmData.dll.GetExposureNum(1,1,0)
    start_pid = wlmData.dll.GetDeviationSignalNum(1,0)
    d = wavelength_PID_bond(points, PID_step, start_pid, expo_time).copy()
    x = [round(d[i][0],2) for i in range(points)]
    y = [round(d[i][1],7) for i in range(points)]
    fig, ax = plt.subplots(figsize=(5,3), layout='constrained')
    ax.plot(x,y)
    plt.ylim(min(y), max(y))
    plt.show()

def wl_stabilisation_after_set(wave, time_pause, precision):
    '''
        The function finds the time of stabilisation after setting PID course

        :param wave: wavelength in [nm]
        :param time_pause: time to pause between checks of correctness in [ms]
        :param precision: the precision in the digits terms e.g. 5 means 5 digits after point
        :return: the time in [ms]

        Comment: The function uses SetPIDCourse, hence we need PID regulator on when use
        it.
    '''
    i = 1
    prec_as_num = 1
    while(i <= precision):
        prec_as_num*=0.1
        i+=1
    set_wl2(wave)
    time1 = time.time()
    delta = round(abs(wave - wlmData.dll.GetWavelengthNum(1,0)),6)
    while(delta > prec_as_num):
        time.sleep(time_pause*0.001)
        delta = round(abs(wave - wlmData.dll.GetWavelengthNum(1,0)),6)
    time2 = time.time()
    return round((time2-time1)*1000,2)

# obsolete version of stabiliser
def wl_stabilisation_through_PID_const(reference_wl, koef, max_dev, time_pause, timer, start_PID_point = 1860):
    '''
        Function stabilises the wavelength on reference_val
        1st version of algorithm

        :param reference_wl: reference value in nm
        :param koef: koefficient of bond between PID in mV and wavelength as frequency
        :param max_dev: max deviation in mV
        :param time_pause: pause after setting PID inside alg-m
        :param timer: lifetime of function in sec
        :param start_PID_point: start point for al-m to change PID
        :return:
    '''
    flag = False
    flag2 = True # regulates PID_STEP if laser swims out of reference
    first_stabilisation_flag = True # regulates PID_STEP if laser isn't stabilised yet
    counter = 0
    PID_step = 0
    time2 = 0
    i = 0
    k = koef
    PID_prev = 0
    reference_wl_Thz = wlmData.dll.ConvertUnit(reference_wl, wlmConst.cReturnWavelengthVac,
                                wlmConst.cReturnFrequency)
    wlmData.dll.SetDeviationSignalNum(1, start_PID_point)
    time.sleep(time_pause/1000)
    time1 = time.time()
    wave = wlmData.dll.ConvertUnit(wlmData.dll.GetWavelengthNum(1, 0), wlmConst.cReturnWavelengthVac,
                                   wlmConst.cReturnFrequency)
    while(True):
        current = wlmData.dll.GetDeviationSignalNum(1,0)
        delta = reference_wl_Thz - wave
        if(flag2):
            if (delta > 0):
                PID_step = -0.125
            elif (delta < 0):
                PID_step = 0.125
        if(not flag and first_stabilisation_flag):
            PID_step = delta / k
        if(abs(PID_step - PID_prev) > max_dev):
            print("!")
            if(delta > 0):
                PID_step = -100
            elif(delta < 0):
                PID_step = 100
        if(round(delta,7) == 0.00000000):
            if(not flag):
                print("stabilized!")
                flag = True
                flag2 = False
                first_stabilisation_flag = False
        elif(flag):
            flag = False
            flag2 = True
        if(not flag):
            wlmData.dll.SetDeviationSignalNum(1, current + PID_step)
        time.sleep(time_pause/1000)
        wave = wlmData.dll.ConvertUnit(wlmData.dll.GetWavelengthNum(1, 0), wlmConst.cReturnWavelengthVac,
                                       wlmConst.cReturnFrequency)
        PID_prev = PID_step
        time2 = time.time()
        if((time2-time1)>timer):
            break


# to tell the truth the find_k_i were not very useful. Finally we got the value of k and just use it. It's up tp the resource laser / WLM
def find_k(points, PID_step, PID_start, time_pause):
    '''
      Finds the coefficient in dependency PID / frequency
      Uses the average in set of delta_frequency_k/delta_PID_k

      :param points: number of steps
      :param PID_step: the value of PID step in mV
      :param PID_start: start PID value
      :param time_pause: time to pause after setting PID
      :return: the coefficient in dependency PID / frequency
      '''
    assert points > 2, "Error: 2 or more points needed"
    i = 0
    d = {}
    while (i < points):
        PID = PID_start + i * PID_step
        # wave = wlmData.dll.ConvertUnit(wlmData.dll.GetWavelengthNum(1, 0), wlmConst.cReturnWavelengthVac,
        #                                wlmConst.cReturnFrequency)
        wlmData.dll.SetDeviationSignalNum(1, PID)
        time.sleep(time_pause/1000)
        wave2 = wlmData.dll.ConvertUnit(wlmData.dll.GetWavelengthNum(1, 0), wlmConst.cReturnWavelengthVac,
                                       wlmConst.cReturnFrequency)
        d[i] = (PID, wave2)
        i += 1
    wlmData.dll.SetDeviationSignalNum(1, PID_start)
    k = 1
    koefs_list = []
    while(k < points):
        koefs_list.append((d[k][1]-d[k-1][1])/PID_step)
        k+=1
    return np.average(koefs_list)

def find_k2(points, PID_step, PID_start):
    '''
      Finds the coefficient in dependency PID / frequency
      Uses the average in set of delta_max-k/delta_PID_max-k, k < points/2
      In other words we take simply the last and the first item and find the coeff than prelast and first item etc.

      :param points: number of steps
      :param PID_step: the value of PID step in mV
      :param PID_start: start PID value
      :param time_pause: time to pause after setting PID
      :return: the coefficient in dependency PID / frequency
      '''
    assert points > 2, "Error: 2 or more points needed"
    assert (points%2) == 0, "Error: even points number needed"
    i = 0
    d = {}
    while (i < points):
        PID = PID_start + i * PID_step
        wave = wlmData.dll.ConvertUnit(wlmData.dll.GetWavelengthNum(1, 0), wlmConst.cReturnWavelengthVac,
                                       wlmConst.cReturnFrequency)
        wlmData.dll.SetDeviationSignalNum(1, PID)
        d[i] = (PID, time_counter(wave))
        i += 1
    wlmData.dll.SetDeviationSignalNum(1, PID_start)
    k = 0
    koefs_list = []
    index_max = points-1
    while(k < points/2):
        koefs_list.append((d[index_max - k][1]-d[k][1])/(d[index_max - k][0]-d[k][0]))
        k+=1
    return np.average(koefs_list)

def time_counter(ref_frequency):
    '''
    Counts time until we get new measure
    We can use this function to get new frequency of measurement with more accurate time difference
    Remark: we can get the previous frequency even if the delay is exposition time

    :param ref_frequency: it's previous frequency meaning
    :return: new frequency
    '''
    cur_freq = wlmData.dll.ConvertUnit(wlmData.dll.GetWavelengthNum(1, 0), wlmConst.cReturnWavelengthVac,
                                       wlmConst.cReturnFrequency)
    while((cur_freq - ref_frequency) == 0.00000000):
        cur_freq = wlmData.dll.ConvertUnit(wlmData.dll.GetWavelengthNum(1, 0), wlmConst.cReturnWavelengthVac,
                                        wlmConst.cReturnFrequency)
    return cur_freq




