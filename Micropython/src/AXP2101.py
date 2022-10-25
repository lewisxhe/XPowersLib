'''
@license MIT License

Copyright (c) 2022 lewis he

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

@file      AXP2101.py
@author    Lewis He (lewishe@outlook.com)
@date      2022-10-20

'''

from I2CInterface import *
from AXP2101Constants import *

class AXP2101(I2CInterface):
    def __init__(self, i2c_bus, addr=AXP2101_SLAVE_ADDRESS) -> None:
        super().__init__(i2c_bus,addr)
        print('AXP2101 __init__')
        self.statusRegister = [0] * XPOWERS_AXP2101_INTSTS_CNT
        self.intRegister = [0] * XPOWERS_AXP2101_INTSTS_CNT
        
        if self.getChipID() != XPOWERS_AXP2101_CHIP_ID:
            raise RuntimeError(
                "Failed to find %s - check your wiring!" % self.__class__.__name__
            )


    #  PMU status functions
    def isVbusGood(self) ->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_STATUS1, 5))

    def getBatfetState(self) ->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_STATUS1, 4))

    # getBatPresentState
    def isBatteryConnect(self) ->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_STATUS1, 3))

    def isBatInActiveModeState(self) ->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_STATUS1, 3))

    def getThermalRegulationStatus(self) ->bool:
        return super().getRegisterBit(XPOWERS_AXP2101_STATUS1, 2)

    def getCurrnetLimitStatus(self) ->bool:
        return super().getRegisterBit(XPOWERS_AXP2101_STATUS1, 1)

    def isCharging(self) ->bool:
        return (super().readRegister(XPOWERS_AXP2101_STATUS2) >> 5) == 0x01

    def isDischarge(self) ->bool:
        return (super().readRegister(XPOWERS_AXP2101_STATUS2) >> 5) == 0x02

    def isStandby(self) ->bool:
        return (super().readRegister(XPOWERS_AXP2101_STATUS2) >> 5) == 0x00

    def isPowerOn(self) ->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_STATUS2, 4))

    def isPowerOff(self) ->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_STATUS2, 4))

    def isVbusIn(self) ->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_STATUS2, 3) == 0)

    def getChargerStatus(self):
        return super().readRegister(XPOWERS_AXP2101_THE_REGU_THRES_SET) & 0x07

    # Data Buffer
    def writeDataBuffer(self, data,  size):
        if (size > XPOWERS_AXP2101_DATA_BUFFER_SIZE):
            return False
        for i in range(0, size):
            super().writeRegister(XPOWERS_AXP2101_DATA_BUFFER1 + i, data[i])
        return True

    def readDataBuffer(self, size):
        if (size > XPOWERS_AXP2101_DATA_BUFFER_SIZE):
            return None
        buf = [0] * size
        for i in range(0, size):
            buf[i] = super().readRegister(XPOWERS_AXP2101_DATA_BUFFER1 + i)
        return buf

    # PMU common configuration
    # @brief   Internal off-discharge enable for DCDC & LDO & SWITCH
    def enableInternalDischarge(self):
        super().setRegisterBit(XPOWERS_AXP2101_COMMON_CONFIG, 5)

    def disableInternalDischarge(self):
        super().clrRegisterBit(XPOWERS_AXP2101_COMMON_CONFIG, 5)

    # @brief   PWROK PIN pull low to Restart
    def enablePwrOkPinPullLow(self):
        super().setRegisterBit(XPOWERS_AXP2101_COMMON_CONFIG, 3)

    def disablePwrOkPinPullLow(self):
        super().clrRegisterBit(XPOWERS_AXP2101_COMMON_CONFIG, 3)

    def enablePwronShutPMIC(self):
        super().setRegisterBit(XPOWERS_AXP2101_COMMON_CONFIG, 2)

    def disablePwronShutPMIC(self):
        super().clrRegisterBit(XPOWERS_AXP2101_COMMON_CONFIG, 2)

    # @brief  Restart the SoC System, POWOFF/POWON and reset the related registers
    def reset(self):
        super().setRegisterBit(XPOWERS_AXP2101_COMMON_CONFIG, 1)

    # @brief  Set shutdown, calling shutdown will turn off all power channels,
    # only VRTC belongs to normal power supply
    def shutdown(self):
        super().setRegisterBit(XPOWERS_AXP2101_COMMON_CONFIG, 0)

    # @brief  BATFET control / REG 12H
    # @note   DIE Over Temperature Protection Level1 Configuration
    # @param   opt: 0:115 , 1:125 , 2:135
    def setBatfetDieOverTempLevel1(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_BATFET_CTRL)
        val &= 0xF9
        super().writeRegister(XPOWERS_AXP2101_BATFET_CTRL, val | (opt << 1))

    def getBatfetDieOverTempLevel1(self):
        return (super().readRegister(XPOWERS_AXP2101_BATFET_CTRL) & 0x06)

    def enableBatfetDieOverTempDetect(self):
        super().setRegisterBit(XPOWERS_AXP2101_BATFET_CTRL, 0)

    def disableBatfetDieOverTempDetect(self):
        super().setRegisterBit(XPOWERS_AXP2101_BATFET_CTRL, 0)

    # @param   opt: 0:115 , 1:125 , 2:135
    def setDieOverTempLevel1(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_DIE_TEMP_CTRL)
        val &= 0xF9
        super().writeRegister(XPOWERS_AXP2101_DIE_TEMP_CTRL, val | (opt << 1))

    def getDieOverTempLevel1(self):
        return (super().readRegister(XPOWERS_AXP2101_DIE_TEMP_CTRL) & 0x06)

    def enableDieOverTempDetect(self):
        super().setRegisterBit(XPOWERS_AXP2101_DIE_TEMP_CTRL, 0)

    def disableDieOverTempDetect(self):
        super().setRegisterBit(XPOWERS_AXP2101_DIE_TEMP_CTRL, 0)

    # Linear Charger Vsys voltage dpm
    def setLinearChargerVsysDpm(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_MIN_SYS_VOL_CTRL)
        val &= 0x8F
        super().writeRegister(XPOWERS_AXP2101_MIN_SYS_VOL_CTRL, val | (opt << 4))

    def getLinearChargerVsysDpm(self):
        val = super().readRegister(XPOWERS_AXP2101_MIN_SYS_VOL_CTRL)
        val &= 0x70
        return (val & 0x70) >> 4

    # Set the minimum common working voltage of the PMU VBUS input,
    # below this value will turn off the PMU
    def setVbusVoltageLimit(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_INPUT_VOL_LIMIT_CTRL)
        val &= 0xF0
        super().writeRegister(XPOWERS_AXP2101_INPUT_VOL_LIMIT_CTRL, val | (opt & 0x0F))

    def getVbusVoltageLimit(self):
        return (super().readRegister(XPOWERS_AXP2101_INPUT_VOL_LIMIT_CTRL) & 0x0F)

    # @brief  Set VBUS Current Input Limit.
    # @param   opt: View the related chip type xpowers_axp2101_vbus_cur_limit_t enumeration parameters in "XPowersParams.hpp"
    def setVbusCurrentLimit(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_INPUT_CUR_LIMIT_CTRL)
        val &= 0xF8
        super().writeRegister(XPOWERS_AXP2101_INPUT_CUR_LIMIT_CTRL, val | (opt & 0x07))

     # @brief  Get VBUS Current Input Limit.
     # @retval View the related chip type xpowers_axp2101_vbus_cur_limit_t enumeration parameters in "XPowersParams.hpp"
    def getVbusCurrentLimit(self):
        return (super().readRegister(XPOWERS_AXP2101_INPUT_CUR_LIMIT_CTRL) & 0x07)

    # @brief  Reset the fuel gauge
    def resetGauge(self):
        super().setRegisterBit(XPOWERS_AXP2101_RESET_FUEL_GAUGE, 3)

    # @brief   reset the gauge besides reset
    def resetGaugeBesides(self):
        super().setRegisterBit(XPOWERS_AXP2101_RESET_FUEL_GAUGE, 2)

    # @brief Gauge Module
    def enableGauge(self):
        super().setRegisterBit(XPOWERS_AXP2101_CHARGE_GAUGE_WDT_CTRL, 3)

    def disableGauge(self):
        super().clrRegisterBit(XPOWERS_AXP2101_CHARGE_GAUGE_WDT_CTRL, 3)

    # @brief  Button Battery charge
    def enableButtonBatteryCharge(self):
        super().setRegisterBit(XPOWERS_AXP2101_CHARGE_GAUGE_WDT_CTRL, 2)

    def disableButtonBatteryCharge(self):
        super().clrRegisterBit(XPOWERS_AXP2101_CHARGE_GAUGE_WDT_CTRL, 2)

    def isEanbleButtonBatteryCharge(self)->bool:
        return super().getRegisterBit(XPOWERS_AXP2101_CHARGE_GAUGE_WDT_CTRL, 2)

    # Button battery charge termination voltage setting
    def setButtonBatteryChargeVoltage(self, millivolt:int)->bool:
        if (millivolt % XPOWERS_AXP2101_BTN_VOL_STEPS):
            print("Mistake ! Button battery charging step voltage is %u mV" %
                  XPOWERS_AXP2101_BTN_VOL_STEPS)
            return False
        if (millivolt < XPOWERS_AXP2101_BTN_VOL_MIN):
            print("Mistake ! The minimum charge termination voltage of the coin cell battery is %u mV" %
                  XPOWERS_AXP2101_BTN_VOL_MIN)
            return False
        elif (millivolt > XPOWERS_AXP2101_BTN_VOL_MAX):
            print("Mistake ! The minimum charge termination voltage of the coin cell battery is %u mV" %
                  XPOWERS_AXP2101_BTN_VOL_MAX)
            return False
        val = super().readRegister(XPOWERS_AXP2101_BTN_BAT_CHG_VOL_SET)
        val &= 0xF8
        val |= (int)(millivolt - XPOWERS_AXP2101_BTN_VOL_MIN) / \
            XPOWERS_AXP2101_BTN_VOL_STEPS
        super().writeRegister(XPOWERS_AXP2101_BTN_BAT_CHG_VOL_SET, val)
        return True

    def getButtonBatteryVoltage(self):
        val = super().readRegister(XPOWERS_AXP2101_BTN_BAT_CHG_VOL_SET)
        return (val & 0x07) * XPOWERS_AXP2101_BTN_VOL_STEPS + XPOWERS_AXP2101_BTN_VOL_MIN

    # @brief Cell Battery charge
    def enableCellbatteryCharge(self):
        super().setRegisterBit(XPOWERS_AXP2101_CHARGE_GAUGE_WDT_CTRL, 1)

    def disableCellbatteryCharge(self):
        super().clrRegisterBit(XPOWERS_AXP2101_CHARGE_GAUGE_WDT_CTRL, 1)

    # @brief  Watchdog Module
    def enableWatchdog(self):
        super().setRegisterBit(XPOWERS_AXP2101_CHARGE_GAUGE_WDT_CTRL, 0)
        self.enableIRQ(XPOWERS_AXP2101_WDT_EXPIRE_IRQ)

    def disableWatchdog(self):
        self.disableIRQ(XPOWERS_AXP2101_WDT_EXPIRE_IRQ)
        super().clrRegisterBit(XPOWERS_AXP2101_CHARGE_GAUGE_WDT_CTRL, 0)

    # @brief Watchdog Config
    # @param   opt: 0: IRQ Only 1: IRQ and System reset  2: IRQ, System Reset and Pull down PWROK 1s  3: IRQ, System Reset, DCDC/LDO PWROFF & PWRON
    def setWatchdogConfig(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_WDT_CTRL)
        val &= 0xCF
        super().writeRegister(XPOWERS_AXP2101_WDT_CTRL, val | (opt << 4))

    def getWatchConfig(self):
        return (super().readRegister(XPOWERS_AXP2101_WDT_CTRL) & 0x30) >> 4

    def clrWatchdog(self):
        super().setRegisterBit(XPOWERS_AXP2101_WDT_CTRL, 3)

    def setWatchdogTimeout(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_WDT_CTRL)
        val &= 0xF8
        super().writeRegister(XPOWERS_AXP2101_WDT_CTRL, val | opt)

    def getWatchdogTimerout(self):
        return super().readRegister(XPOWERS_AXP2101_WDT_CTRL) & 0x07

    # @brief Low battery warning threshold 5-20%, 1% per step
    def setLowBatWarnThreshold(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_LOW_BAT_WARN_SET)
        val &= 0x0F
        super().writeRegister(XPOWERS_AXP2101_LOW_BAT_WARN_SET, val | (opt << 4))

    def getLowBatWarnThreshold(self):
        return (super().readRegister(XPOWERS_AXP2101_LOW_BAT_WARN_SET) & 0xF0) >> 4

    # @brief Low battery shutdown threshold 0-15%, 1% per step
    def setLowBatShutdownThreshold(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_LOW_BAT_WARN_SET)
        val &= 0xF0
        super().writeRegister(XPOWERS_AXP2101_LOW_BAT_WARN_SET, val | opt)

    def getLowBatShutdownThreshold(self):
        return (super().readRegister(XPOWERS_AXP2101_LOW_BAT_WARN_SET) & 0x0F)

    #!  PWRON statu  20
    # POWERON always high when EN Mode as POWERON Source
    def isPoweronAlwaysHighSource(self)->bool:
        return super().getRegisterBit(XPOWERS_AXP2101_PWRON_STATUS, 5)

    # Battery Insert and Good as POWERON Source
    def isBattInsertOnSource(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_PWRON_STATUS, 4))

    # Battery Voltage > 3.3V when Charged as Source
    def isBattNormalOnSource(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_PWRON_STATUS, 3))

    # Vbus Insert and Good as POWERON Source
    def isVbusInsertOnSource(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_PWRON_STATUS, 2))

    # IRQ PIN Pull-down as POWERON Source
    def isIrqLowOnSource(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_PWRON_STATUS, 1))

    # POWERON low for on level when POWERON Mode as POWERON Source
    def isPwronLowOnSource(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_PWRON_STATUS, 0))

    def getPowerOnSource(self):
        return super().readRegister(XPOWERS_AXP2101_PWRON_STATUS)

    #!  PWROFF status  21
    # Die Over Temperature as POWEROFF Source
    def isOverTemperatureOffSource(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_PWROFF_STATUS, 7))

    # DCDC Over Voltage as POWEROFF Source
    def isDcOverVoltageOffSource(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_PWROFF_STATUS, 6))

    # DCDC Under Voltage as POWEROFF Source
    def isDcUnderVoltageOffSource(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_PWROFF_STATUS, 5))

    # VBUS Over Voltage as POWEROFF Source
    def isVbusOverVoltageOffSource(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_PWROFF_STATUS, 4))

    # Vsys Under Voltage as POWEROFF Source
    def isVsysUnderVoltageOffSource(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_PWROFF_STATUS, 3))

    # POWERON always low when EN Mode as POWEROFF Source
    def isPwronAlwaysLowOffSource(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_PWROFF_STATUS, 2))

    # Software configuration as POWEROFF Source
    def isSwConfigOffSource(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_PWROFF_STATUS, 1))

    # POWERON Pull down for off level when POWERON Mode as POWEROFF Source
    def isPwrSourcePullDown(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_PWROFF_STATUS, 0))

    def getPowerOffSource(self):
        return super().readRegister(XPOWERS_AXP2101_PWROFF_STATUS)

    #!REG 22H
    def enableOverTemperatureLevel2PowerOff(self):
        super().setRegisterBit(XPOWERS_AXP2101_PWROFF_EN, 2)

    def disableOverTemperaturePowerOff(self):
        super().clrRegisterBit(XPOWERS_AXP2101_PWROFF_EN, 2)

    def enablePwrOnOverVolOffLevelPowerOff(self):
        super().setRegisterBit(XPOWERS_AXP2101_PWROFF_EN, 1)

    def disablePwrOnOverVolOffLevelPowerOff(self):
        super().clrRegisterBit(XPOWERS_AXP2101_PWROFF_EN, 1)

    def enablePwrOffSelectFunction(self):
        super().setRegisterBit(XPOWERS_AXP2101_PWROFF_EN, 0)

    def disablePwrOffSelectFunction(self):
        super().clrRegisterBit(XPOWERS_AXP2101_PWROFF_EN, 0)

    #!REG 23H
    # DCDC 120%(130%) high voltage turn off PMIC function
    def enableDCHighVoltageTurnOff(self):
        super().setRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 5)

    def disableDCHighVoltageTurnOff(self):
        super().clrRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 5)

    # DCDC5 85% low voltage turn Off PMIC function
    def enableDC5LowVoltageTurnOff(self):
        super().setRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 4)

    def disableDC5LowVoltageTurnOff(self):
        super().clrRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 4)

    # DCDC4 85% low voltage turn Off PMIC function
    def enableDC4LowVoltageTurnOff(self):
        super().setRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 3)

    def disableDC4LowVoltageTurnOff(self):
        super().clrRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 3)

    # DCDC3 85% low voltage turn Off PMIC function
    def enableDC3LowVoltageTurnOff(self):
        super().setRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 2)

    def disableDC3LowVoltageTurnOff(self):
        super().clrRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 2)

    # DCDC2 85% low voltage turn Off PMIC function
    def enableDC2LowVoltageTurnOff(self):
        super().setRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 1)

    def disableDC2LowVoltageTurnOff(self):
        super().clrRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 1)

    # DCDC1 85% low voltage turn Off PMIC function
    def enableDC1LowVoltageTurnOff(self):
        super().setRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 0)

    def disableDC1LowVoltageTurnOff(self):
        super().clrRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 0)

    # Set the minimum system operating voltage inside the PMU,
    # below this value will shut down the PMU,Adjustment range 2600mV~3300mV
    def setSysPowerDownVoltage(self, millivolt:int)->bool:
        if (millivolt % XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_STEPS):
            print("Mistake ! The steps is must %u mV" %
                  XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_STEPS)
            return False

        if (millivolt < XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_MIN):
            print("Mistake ! The minimum settable voltage of VSYS is %u mV" %
                  XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_MIN)
            return False
        elif (millivolt > XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_MAX):
            print("Mistake ! The maximum settable voltage of VSYS is %u mV" %
                  XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_MAX)
            return False

        val = super().readRegister(XPOWERS_AXP2101_VOFF_SET)
        val &= 0xF8
        super().writeRegister(XPOWERS_AXP2101_VOFF_SET, val | (int)((millivolt -
                                                                     XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_MIN) / XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_STEPS))
        return True

    def getSysPowerDownVoltage(self):
        val = super().readRegister(XPOWERS_AXP2101_VOFF_SET)
        return (val & 0x07) * XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_STEPS + XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_MIN

    # PWROK setting and PWROFF sequence control 25.
    # Check the PWROK Pin enable after all dcdc/ldo output valid 128ms
    def enablePwrOk(self):
        super().setRegisterBit(XPOWERS_AXP2101_PWROK_SEQU_CTRL, 4)

    def disablePwrOk(self):
        super().clrRegisterBit(XPOWERS_AXP2101_PWROK_SEQU_CTRL, 4)

    # POWEROFF Delay 4ms after PWROK enable
    def eanblePowerOffDelay(self):
        super().setRegisterBit(XPOWERS_AXP2101_PWROK_SEQU_CTRL, 3)

    # POWEROFF Delay 4ms after PWROK disable
    def disablePowerOffDelay(self):
        super().clrRegisterBit(XPOWERS_AXP2101_PWROK_SEQU_CTRL, 3)

    # POWEROFF Sequence Control the reverse of the Startup
    def eanblePowerSequence(self):
        super().setRegisterBit(XPOWERS_AXP2101_PWROK_SEQU_CTRL, 2)

    # POWEROFF Sequence Control at the same time
    def disablePowerSequence(self):
        super().clrRegisterBit(XPOWERS_AXP2101_PWROK_SEQU_CTRL, 2)

    # Delay of PWROK after all power output good
    def setPwrOkDelay(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_PWROK_SEQU_CTRL)
        val &= 0xFC
        super().writeRegister(XPOWERS_AXP2101_PWROK_SEQU_CTRL, val | opt)

    def getPwrOkDelay(self):
        return (super().readRegister(XPOWERS_AXP2101_PWROK_SEQU_CTRL) & 0x03)

    #  Sleep and 26
    def wakeupControl(self, opt, enable):
        val = super().readRegister(XPOWERS_AXP2101_SLEEP_WAKEUP_CTRL)
        if enable:
            val |= opt
        else:
            val &= (~opt)
        super().writeRegister(XPOWERS_AXP2101_SLEEP_WAKEUP_CTRL, val | opt)

    def enableWakeup(self):
        super().setRegisterBit(XPOWERS_AXP2101_SLEEP_WAKEUP_CTRL, 1)

    def disableWakeup(self):
        super().clrRegisterBit(XPOWERS_AXP2101_SLEEP_WAKEUP_CTRL, 1)

    def enableSleep(self):
        super().setRegisterBit(XPOWERS_AXP2101_SLEEP_WAKEUP_CTRL, 0)

    def disableSleep(self):
        super().clrRegisterBit(XPOWERS_AXP2101_SLEEP_WAKEUP_CTRL, 0)

    #  RQLEVEL/OFFLEVEL/ONLEVEL setting 27
    # @brief  IRQLEVEL configur
    # @param   opt: 0:1s  1:1.5s  2:2s 3:2.5s
    def setIrqLevel(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL)
        val &= 0xFC
        super().writeRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL, val | (opt << 4))

    # @brief  OFFLEVEL configuration
    # @param   opt:  0:4s 1:6s 2:8s 3:10s
    def setOffLevel(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL)
        super().writeRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL, val | (opt << 2))

    # @brief  ONLEVEL configuration
    # @param   opt: 0:128ms 1:512ms 2:1s  3:2s
    def setOnLevel(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL)
        super().writeRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL, val | opt)

    # Fast pwron setting 0  28
    # Fast Power On Start Sequence
    def setDc4FastStartSequence(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET0)
        super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET0, val | ((opt & 0x3) << 6))

    def setDc3FastStartSequence(self,  opt:int):
        val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET0)
        super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET0, val | ((opt & 0x3) << 4))

    def setDc2FastStartSequence(self,  opt:int):
        val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET0)
        super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET0, val | ((opt & 0x3) << 2))

    def setDc1FastStartSequence(self,  opt:int):
        val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET0)
        super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET0, val | (opt & 0x3))

    #  Fast pwron setting 1  29
    def setAldo3FastStartSequence(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET1)
        super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET1, val | ((opt & 0x3) << 6))

    def setAldo2FastStartSequence(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET1)
        super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET1, val | ((opt & 0x3) << 4))

    def setAldo1FastStartSequence(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET1)
        super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET1, val | ((opt & 0x3) << 2))

    def setDc5FastStartSequence(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET1)
        super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET1, val | (opt & 0x3))

    #  Fast pwron setting 2  2A
    def setCpuldoFastStartSequence(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET2)
        super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET2, val | ((opt & 0x3) << 6))

    def setBldo2FastStartSequence(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET2)
        super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET2, val | ((opt & 0x3) << 4))

    def setBldo1FastStartSequence(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET2)
        super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET2, val | ((opt & 0x3) << 2))

    def setAldo4FastStartSequence(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET2)
        super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET2, val | (opt & 0x3))

    #  Fast pwron setting 3  2B
    def setDldo2FastStartSequence(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_CTRL)
        super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_CTRL, val | ((opt & 0x3) << 2))

    def setDldo1FastStartSequence(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_CTRL)
        super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_CTRL, val | (opt & 0x3))

    # @brief   Setting Fast Power On Start Sequence
    def setFastPowerOnLevel(self, opt, seq_level):
        val = 0
        if opt == XPOWERS_AXP2101_FAST_DCDC1:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET0)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET0, val | seq_level)
        elif opt == XPOWERS_AXP2101_FAST_DCDC2:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET0)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET0, val | (seq_level << 2))
        elif opt == XPOWERS_AXP2101_FAST_DCDC3:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET0)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET0, val | (seq_level << 4))
        elif opt == XPOWERS_AXP2101_FAST_DCDC4:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET0)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET0, val | (seq_level << 6))
        elif opt == XPOWERS_AXP2101_FAST_DCDC5:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET1)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET1, val | seq_level)
        elif opt == XPOWERS_AXP2101_FAST_ALDO1:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET1)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET1, val | (seq_level << 2))
        elif opt == XPOWERS_AXP2101_FAST_ALDO2:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET1)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET1, val | (seq_level << 4))
        elif opt == XPOWERS_AXP2101_FAST_ALDO3:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET1)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET1, val | (seq_level << 6))
        elif opt == XPOWERS_AXP2101_FAST_ALDO4:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET2)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET2, val | seq_level)
        elif opt == XPOWERS_AXP2101_FAST_BLDO1:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET2)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET2, val | (seq_level << 2))
        elif opt == XPOWERS_AXP2101_FAST_BLDO2:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET2)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET2, val | (seq_level << 4))
        elif opt == XPOWERS_AXP2101_FAST_CPUSLDO:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET2)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET2, val | (seq_level << 6))
        elif opt == XPOWERS_AXP2101_FAST_DLDO1:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_CTRL)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_CTRL, val | seq_level)
        elif opt == XPOWERS_AXP2101_FAST_DLDO2:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_CTRL)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_CTRL, val | (seq_level << 2))

    def disableFastPowerOn(self, opt:int):
        val = 0
        if opt == XPOWERS_AXP2101_FAST_DCDC1:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET0)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET0, val & 0xFC)
        elif opt == XPOWERS_AXP2101_FAST_DCDC2:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET0)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET0, val & 0xF3)
        elif opt == XPOWERS_AXP2101_FAST_DCDC3:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET0)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET0, val & 0xCF)
        elif opt == XPOWERS_AXP2101_FAST_DCDC4:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET0)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET0, val & 0x3F)
        elif opt == XPOWERS_AXP2101_FAST_DCDC5:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET1)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET1, val & 0xFC)
        elif opt == XPOWERS_AXP2101_FAST_ALDO1:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET1)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET1, val & 0xF3)
        elif opt == XPOWERS_AXP2101_FAST_ALDO2:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET1)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET1, val & 0xCF)
        elif opt == XPOWERS_AXP2101_FAST_ALDO3:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET1)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET1, val & 0x3F)
        elif opt == XPOWERS_AXP2101_FAST_ALDO4:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET2)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET2, val & 0xFC)
        elif opt == XPOWERS_AXP2101_FAST_BLDO1:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET2)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET2, val & 0xF3)
        elif opt == XPOWERS_AXP2101_FAST_BLDO2:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET2)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET2, val & 0xCF)
        elif opt == XPOWERS_AXP2101_FAST_CPUSLDO:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_SET2)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_SET2, val & 0x3F)
        elif opt == XPOWERS_AXP2101_FAST_DLDO1:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_CTRL)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_CTRL, val & 0xFC)
        elif opt == XPOWERS_AXP2101_FAST_DLDO2:
            val = super().readRegister(XPOWERS_AXP2101_FAST_PWRON_CTRL)
            super().writeRegister(XPOWERS_AXP2101_FAST_PWRON_CTRL, val & 0xF3)

    def enableFastPowerOnCtrl(self):
        super().setRegisterBit(XPOWERS_AXP2101_FAST_PWRON_CTRL, 7)

    def disableFastPowerOnCtrl(self):
        super().clrRegisterBit(XPOWERS_AXP2101_FAST_PWRON_CTRL, 7)

    def enableFastWakeup(self):
        super().setRegisterBit(XPOWERS_AXP2101_FAST_PWRON_CTRL, 6)

    def disableFastWakeup(self):
        super().clrRegisterBit(XPOWERS_AXP2101_FAST_PWRON_CTRL, 6)

    # DCDC 120%(130%) high voltage turn off PMIC function
    def setDCHighVoltagePowerDowm(self, en):
        if en:
            super().setRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 5)
        else:
            super().clrRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 5)

    def getDCHighVoltagePowerDowmEn(self):
        return bool(super().getRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 5))

    # DCDCS force PWM control
    def setDcUVPDebounceTime(self,opt:int):
        val = super().readRegister(XPOWERS_AXP2101_DC_FORCE_PWM_CTRL)
        val &= 0xFC
        super().writeRegister(XPOWERS_AXP2101_DC_FORCE_PWM_CTRL,val|opt)

    def settDC1WorkModeToPwm(self,enable):
        if enable:
            super().setRegisterBit(XPOWERS_AXP2101_DC_FORCE_PWM_CTRL, 2)
        else:
            super().clrRegisterBit(XPOWERS_AXP2101_DC_FORCE_PWM_CTRL, 2)

    def settDC2WorkModeToPwm(self,enable):
        if enable:
            super().setRegisterBit(XPOWERS_AXP2101_DC_FORCE_PWM_CTRL, 3)
        else:
            super().clrRegisterBit(XPOWERS_AXP2101_DC_FORCE_PWM_CTRL, 3)

    def settDC3WorkModeToPwm(self,enable):
        if enable:
            super().setRegisterBit(XPOWERS_AXP2101_DC_FORCE_PWM_CTRL, 4)
        else:
            super().clrRegisterBit(XPOWERS_AXP2101_DC_FORCE_PWM_CTRL, 4)

    def settDC4WorkModeToPwm(self,enable):
        if enable:
            super().setRegisterBit(XPOWERS_AXP2101_DC_FORCE_PWM_CTRL, 5)
        else:
            super().clrRegisterBit(XPOWERS_AXP2101_DC_FORCE_PWM_CTRL, 5)

    #1 = 100khz 0=50khz
    def setDCFreqSpreadRange(self, opt:int):
        if opt:
            super().setRegisterBit(XPOWERS_AXP2101_DC_FORCE_PWM_CTRL, 6)
        else:  
            super().clrRegisterBit(XPOWERS_AXP2101_DC_FORCE_PWM_CTRL, 6)

    def setDCFreqSpreadRangeEn(self, en):
        if en:
            super().setRegisterBit(XPOWERS_AXP2101_DC_FORCE_PWM_CTRL, 7)
        else:  
            super().clrRegisterBit(XPOWERS_AXP2101_DC_FORCE_PWM_CTRL, 7)

    # Power control DCDC1 functions
    def isEnableDC1(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 0))

    def enableDC1(self):
        super().setRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 0)

    def disableDC1(self):
        super().clrRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 0)

    def setDC1Voltage(self, millivolt:int)->bool:
        if (millivolt % XPOWERS_AXP2101_DCDC1_VOL_STEPS):
            print("Mistake ! The steps is must %u mV" %
                  XPOWERS_AXP2101_DCDC1_VOL_STEPS)
            return False
        if (millivolt < XPOWERS_AXP2101_DCDC1_VOL_MIN):
            print("Mistake ! DC1 minimum voltage is %u mV" %
                  XPOWERS_AXP2101_DCDC1_VOL_MIN)
            return False
        elif (millivolt > XPOWERS_AXP2101_DCDC1_VOL_MAX):
            print("Mistake ! DC1 maximum voltage is %u mV" %
                  XPOWERS_AXP2101_DCDC1_VOL_MAX)
            return False
        super().writeRegister(XPOWERS_AXP2101_DC_VOL0_CTRL, (int)((millivolt -
                                                                  XPOWERS_AXP2101_DCDC1_VOL_MIN) / XPOWERS_AXP2101_DCDC1_VOL_STEPS))
        return True

    def getDC1Voltage(self):
        return (super().readRegister(XPOWERS_AXP2101_DC_VOL0_CTRL) & 0x1F) * XPOWERS_AXP2101_DCDC1_VOL_STEPS + XPOWERS_AXP2101_DCDC1_VOL_MIN

    # DCDC1 85% low voltage turn off PMIC function
    def setDC1LowVoltagePowerDowm(self, en):
        if en:
            super().setRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 0)
        else:
            super().clrRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 0)

    def getDC1LowVoltagePowerDowmEn(self):
        return bool(super().getRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 0))

    # Power control DCDC2 functions
    def isEnableDC2(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 1))

    def enableDC2(self):
        super().setRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 1)

    def disableDC2(self):
        super().clrRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 1)

    def setDC2Voltage(self, millivolt:int)->bool:
        val = super().readRegister(XPOWERS_AXP2101_DC_VOL1_CTRL)
        val &= 0x80
        if (millivolt >= XPOWERS_AXP2101_DCDC2_VOL1_MIN and millivolt <= XPOWERS_AXP2101_DCDC2_VOL1_MAX):
            if (millivolt % XPOWERS_AXP2101_DCDC2_VOL_STEPS1):
                print("Mistake !  The steps is must %umV" %
                      XPOWERS_AXP2101_DCDC2_VOL_STEPS1)
                return False

            super().writeRegister(XPOWERS_AXP2101_DC_VOL1_CTRL, val | (int)((millivolt -
                                                                            XPOWERS_AXP2101_DCDC2_VOL1_MIN) / XPOWERS_AXP2101_DCDC2_VOL_STEPS1))
            return True
        elif (millivolt >= XPOWERS_AXP2101_DCDC2_VOL2_MIN and millivolt <= XPOWERS_AXP2101_DCDC2_VOL2_MAX):
            if (millivolt % XPOWERS_AXP2101_DCDC2_VOL_STEPS2):
                print("Mistake !  The steps is must %umV" %
                      XPOWERS_AXP2101_DCDC2_VOL_STEPS2)
                return False
            val |= (int)((((millivolt - XPOWERS_AXP2101_DCDC2_VOL2_MIN) /
                          XPOWERS_AXP2101_DCDC2_VOL_STEPS2) + XPOWERS_AXP2101_DCDC2_VOL_STEPS2_BASE))
            super().writeRegister(XPOWERS_AXP2101_DC_VOL1_CTRL, val)
            return True
        return False

    def getDC2Voltage(self):
        val = super().readRegister(XPOWERS_AXP2101_DC_VOL1_CTRL)
        val &= 0x7F
        if (val < XPOWERS_AXP2101_DCDC2_VOL_STEPS2_BASE):
            return (val * XPOWERS_AXP2101_DCDC2_VOL_STEPS1) + XPOWERS_AXP2101_DCDC2_VOL1_MIN
        return (val * XPOWERS_AXP2101_DCDC2_VOL_STEPS2) - 200

    def getDC2WorkMode(self):
        return super().getRegisterBit(XPOWERS_AXP2101_DCDC2_VOL_STEPS2, 7)

    def setDC2LowVoltagePowerDowm(self, en):
        if en:
            super().setRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 1)
        else:
            super().clrRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 1)

    def getDC2LowVoltagePowerDowmEn(self):
        return bool(super().getRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 1))

    # Power control DCDC3 functions
    def isEnableDC3(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 2))

    def enableDC3(self):
        super().setRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 2)

    def disableDC3(self):
        super().clrRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 2)

    # 0.5~1.2V,10mV/step,71steps
    # 1.22~1.54V,20mV/step,17steps
    # 1.6~3.4V,100mV/step,19steps
    def setDC3Voltage(self, millivolt:int)->bool:
        val = super().readRegister(XPOWERS_AXP2101_DC_VOL2_CTRL)
        val &= 0x80
        if (millivolt >= XPOWERS_AXP2101_DCDC3_VOL1_MIN and millivolt <= XPOWERS_AXP2101_DCDC3_VOL1_MAX):
            if (millivolt % XPOWERS_AXP2101_DCDC3_VOL_STEPS1):
                print("Mistake ! The steps is must %umV" %
                      XPOWERS_AXP2101_DCDC3_VOL_STEPS1)
                return False

            super().writeRegister(XPOWERS_AXP2101_DC_VOL2_CTRL, val | (int)((millivolt -
                                                                            XPOWERS_AXP2101_DCDC3_VOL_MIN) / XPOWERS_AXP2101_DCDC3_VOL_STEPS1))
            return True
        elif (millivolt >= XPOWERS_AXP2101_DCDC3_VOL2_MIN and millivolt <= XPOWERS_AXP2101_DCDC3_VOL2_MAX):
            if (millivolt % XPOWERS_AXP2101_DCDC3_VOL_STEPS2):
                print("Mistake ! The steps is must %umV" %
                      XPOWERS_AXP2101_DCDC3_VOL_STEPS2)
                return False

            val |= (int)(((millivolt - XPOWERS_AXP2101_DCDC3_VOL2_MIN) /
                          XPOWERS_AXP2101_DCDC3_VOL_STEPS2) + XPOWERS_AXP2101_DCDC3_VOL_STEPS2_BASE)
            return 0 == super().writeRegister(XPOWERS_AXP2101_DC_VOL2_CTRL, val)
        elif (millivolt >= XPOWERS_AXP2101_DCDC3_VOL3_MIN and millivolt <= XPOWERS_AXP2101_DCDC3_VOL3_MAX):
            if (millivolt % XPOWERS_AXP2101_DCDC3_VOL_STEPS3):
                print("Mistake ! The steps is must %umV" %
                      XPOWERS_AXP2101_DCDC3_VOL_STEPS3)
                return False

            val |= (int)(((millivolt - XPOWERS_AXP2101_DCDC3_VOL3_MIN) /
                          XPOWERS_AXP2101_DCDC3_VOL_STEPS3) + XPOWERS_AXP2101_DCDC3_VOL_STEPS3_BASE)
            super().writeRegister(XPOWERS_AXP2101_DC_VOL2_CTRL, val)
            return True
        return False

    def getDC3Voltage(self):
        val = super().readRegister(XPOWERS_AXP2101_DC_VOL2_CTRL) & 0x7F
        if (val < XPOWERS_AXP2101_DCDC3_VOL_STEPS2_BASE):
            return (val * XPOWERS_AXP2101_DCDC3_VOL_STEPS1) + XPOWERS_AXP2101_DCDC3_VOL_MIN
        elif (val >= XPOWERS_AXP2101_DCDC3_VOL_STEPS2_BASE and val < XPOWERS_AXP2101_DCDC3_VOL_STEPS3_BASE):
            return (val * XPOWERS_AXP2101_DCDC3_VOL_STEPS2) - 200
        return (val * XPOWERS_AXP2101_DCDC3_VOL_STEPS3) - 7200

    def getDC3WorkMode(self):
        return super().getRegisterBit(XPOWERS_AXP2101_DC_VOL2_CTRL, 7)

    # DCDC3 85% low voltage turn off PMIC function
    def setDC3LowVoltagePowerDowm(self, en):
        if en:
            super().setRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 2)
        else:
            super().clrRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 2)

    def getDC3LowVoltagePowerDowmEn(self):
        return bool(super().getRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 2))


    # Power control DCDC4 functions
    # 0.5~1.2V,10mV/step,71steps
    # 1.22~1.84V,20mV/step,32steps
    def isEnableDC4(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 3))

    def enableDC4(self):
        super().setRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 3)

    def disableDC4(self):
        super().clrRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 3)

    def setDC4Voltage(self, millivolt:int)->bool:
        val = super().readRegister(XPOWERS_AXP2101_DC_VOL3_CTRL)
        val &= 0x80
        if (millivolt >= XPOWERS_AXP2101_DCDC4_VOL1_MIN and millivolt <= XPOWERS_AXP2101_DCDC4_VOL1_MAX):
            if (millivolt % XPOWERS_AXP2101_DCDC4_VOL_STEPS1):
                print("Mistake ! The steps is must %umV" %
                      XPOWERS_AXP2101_DCDC4_VOL_STEPS1)
                return False
            super().writeRegister(XPOWERS_AXP2101_DC_VOL3_CTRL, val | (int)((millivolt -
                                                                            XPOWERS_AXP2101_DCDC4_VOL1_MIN) / XPOWERS_AXP2101_DCDC4_VOL_STEPS1))
            return True
        elif (millivolt >= XPOWERS_AXP2101_DCDC4_VOL2_MIN and millivolt <= XPOWERS_AXP2101_DCDC4_VOL2_MAX):
            if (millivolt % XPOWERS_AXP2101_DCDC4_VOL_STEPS2):
                print("Mistake ! The steps is must %umV" %
                      XPOWERS_AXP2101_DCDC4_VOL_STEPS2)
                return False
            val |= (int)(((millivolt - XPOWERS_AXP2101_DCDC4_VOL2_MIN) /
                          XPOWERS_AXP2101_DCDC4_VOL_STEPS2) + XPOWERS_AXP2101_DCDC4_VOL_STEPS2_BASE)
            super().writeRegister(XPOWERS_AXP2101_DC_VOL3_CTRL, val)
            return True
        return False

    def getDC4Voltage(self):
        val = super().readRegister(XPOWERS_AXP2101_DC_VOL3_CTRL)
        val &= 0x7F
        if (val < XPOWERS_AXP2101_DCDC4_VOL_STEPS2_BASE):
            return (val * XPOWERS_AXP2101_DCDC4_VOL_STEPS1) + XPOWERS_AXP2101_DCDC4_VOL1_MIN
        return (val * XPOWERS_AXP2101_DCDC4_VOL_STEPS2) - 200

    # DCDC4 85% low voltage turn off PMIC function
    def setDC4LowVoltagePowerDowm(self, en):
        if en:
            super().setRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 3)
        else:
            super().clrRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 3)

    def getDC4LowVoltagePowerDowmEn(self):
        return bool(super().getRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 3))

    # Power control DCDC5 functions,Output to gpio pin
    def isEnableDC5(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 4))

    def enableDC5(self):
        super().setRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 4)

    def disableDC5(self):
        super().clrRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 4)

    def setDC5Voltage(self, millivolt:int)->bool:
        if (millivolt % XPOWERS_AXP2101_DCDC5_VOL_STEPS):
            print("Mistake ! The steps is must %u mV" %
                  XPOWERS_AXP2101_DCDC5_VOL_STEPS)
            return False

        if (millivolt != XPOWERS_AXP2101_DCDC5_VOL_1200MV and millivolt < XPOWERS_AXP2101_DCDC5_VOL_MIN):
            print("Mistake ! DC5 minimum voltage is %umV ,%umV" %
                  XPOWERS_AXP2101_DCDC5_VOL_1200MV, XPOWERS_AXP2101_DCDC5_VOL_MIN)
            return False
        elif (millivolt > XPOWERS_AXP2101_DCDC5_VOL_MAX):
            print("Mistake ! DC5 maximum voltage is %umV" %
                  XPOWERS_AXP2101_DCDC5_VOL_MAX)
            return False
        return True

        val = super().readRegister(XPOWERS_AXP2101_DC_VOL4_CTRL)
        val &= 0xE0
        if (millivolt == XPOWERS_AXP2101_DCDC5_VOL_1200MV):
            super().writeRegister(XPOWERS_AXP2101_DC_VOL4_CTRL,
                                  val | XPOWERS_AXP2101_DCDC5_VOL_VAL)
        val |= (int)((millivolt - XPOWERS_AXP2101_DCDC5_VOL_MIN) /
                     XPOWERS_AXP2101_DCDC5_VOL_STEPS)
        super().writeRegister(XPOWERS_AXP2101_DC_VOL4_CTRL, val)

    def getDC5Voltage(self):
        val = super().readRegister(XPOWERS_AXP2101_DC_VOL4_CTRL)
        val &= 0x1F
        if (val == XPOWERS_AXP2101_DCDC5_VOL_VAL):
            return XPOWERS_AXP2101_DCDC5_VOL_1200MV
        return (val * XPOWERS_AXP2101_DCDC5_VOL_STEPS) + XPOWERS_AXP2101_DCDC5_VOL_MIN

    def isDC5FreqCompensationEn(self)->bool:
        return super().getRegisterBit(XPOWERS_AXP2101_DC_VOL4_CTRL, 5)

    def enableDC5FreqCompensation(self):
        super().setRegisterBit(XPOWERS_AXP2101_DC_VOL4_CTRL, 5)

    def disableFreqCompensation(self):
        super().clrRegisterBit(XPOWERS_AXP2101_DC_VOL4_CTRL, 5)

    # DCDC4 85% low voltage turn off PMIC function
    def setDC5LowVoltagePowerDowm(self, en):
        if en:
            super().setRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 4)
        else:
            super().clrRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 4)

    def getDC5LowVoltagePowerDowmEn(self):
        return bool(super().getRegisterBit(XPOWERS_AXP2101_DC_OVP_UVP_CTRL, 4))


    # Power control ALDO1 functions
    def isEnableALDO1(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 0))

    def enableALDO1(self):

        super().setRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 0)

    def disableALDO1(self):

        super().clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 0)

    def setALDO1Voltage(self, millivolt:int)->bool:
        if (millivolt % XPOWERS_AXP2101_ALDO1_VOL_STEPS):
            print("Mistake ! The steps is must %u mV" %
                  XPOWERS_AXP2101_ALDO1_VOL_STEPS)
            return False
        if (millivolt < XPOWERS_AXP2101_ALDO1_VOL_MIN):
            print("Mistake ! ALDO1 minimum output voltage is  %umV" %
                  XPOWERS_AXP2101_ALDO1_VOL_MIN)
            return False
        elif (millivolt > XPOWERS_AXP2101_ALDO1_VOL_MAX):
            print("Mistake ! ALDO1 maximum output voltage is  %umV" %
                  XPOWERS_AXP2101_ALDO1_VOL_MAX)
            return False

        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL0_CTRL) & 0xE0
        val |= (int)((millivolt - XPOWERS_AXP2101_ALDO1_VOL_MIN) /
                     XPOWERS_AXP2101_ALDO1_VOL_STEPS)
        super().writeRegister(XPOWERS_AXP2101_LDO_VOL0_CTRL, val)
        return True

    def getALDO1Voltage(self):
        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL0_CTRL) & 0x1F
        return val * XPOWERS_AXP2101_ALDO1_VOL_STEPS + XPOWERS_AXP2101_ALDO1_VOL_MIN

    # Power control ALDO2 functions
    def isEnableALDO2(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 1))

    def enableALDO2(self):
        super().setRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 1)

    def disableALDO2(self):
        super().clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 1)

    def setALDO2Voltage(self, millivolt:int)->bool:
        if (millivolt % XPOWERS_AXP2101_ALDO2_VOL_STEPS):
            print("Mistake ! The steps is must %u mV" %
                  XPOWERS_AXP2101_ALDO2_VOL_STEPS)
            return False

        if (millivolt < XPOWERS_AXP2101_ALDO2_VOL_MIN):
            print("Mistake ! ALDO2 minimum output voltage is  %umV" %
                  XPOWERS_AXP2101_ALDO2_VOL_MIN)
            return False
        elif (millivolt > XPOWERS_AXP2101_ALDO2_VOL_MAX):
            print("Mistake ! ALDO2 maximum output voltage is  %umV" %
                  XPOWERS_AXP2101_ALDO2_VOL_MAX)
            return False

        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL1_CTRL) & 0xE0
        val |= (int)((millivolt - XPOWERS_AXP2101_ALDO2_VOL_MIN) /
                     XPOWERS_AXP2101_ALDO2_VOL_STEPS)
        super().writeRegister(XPOWERS_AXP2101_LDO_VOL1_CTRL, val)
        return True

    def getALDO2Voltage(self):
        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL1_CTRL) & 0x1F
        return val * XPOWERS_AXP2101_ALDO2_VOL_STEPS + XPOWERS_AXP2101_ALDO2_VOL_MIN

    # Power control ALDO3 functions
    def isEnableALDO3(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 2))

    def enableALDO3(self):
        super().setRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 2)

    def disableALDO3(self):
        super().clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 2)

    def setALDO3Voltage(self, millivolt:int)->bool:
        if (millivolt % XPOWERS_AXP2101_ALDO3_VOL_STEPS):
            print("Mistake ! The steps is must %u mV" %
                  XPOWERS_AXP2101_ALDO3_VOL_STEPS)
            return False

        if (millivolt < XPOWERS_AXP2101_ALDO3_VOL_MIN):
            print("Mistake ! ALDO3 minimum output voltage is  %umV" %
                  XPOWERS_AXP2101_ALDO3_VOL_MIN)
            return False
        elif (millivolt > XPOWERS_AXP2101_ALDO3_VOL_MAX):
            print("Mistake ! ALDO3 maximum output voltage is  %umV" %
                  XPOWERS_AXP2101_ALDO3_VOL_MAX)
            return False

        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL2_CTRL) & 0xE0
        val |= (int)((millivolt - XPOWERS_AXP2101_ALDO3_VOL_MIN) /
                     XPOWERS_AXP2101_ALDO3_VOL_STEPS)
        super().writeRegister(XPOWERS_AXP2101_LDO_VOL2_CTRL, val)
        return True

    def getALDO3Voltage(self):
        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL2_CTRL) & 0x1F
        return val * XPOWERS_AXP2101_ALDO3_VOL_STEPS + XPOWERS_AXP2101_ALDO3_VOL_MIN

    # Power control ALDO4 functions
    def isEnableALDO4(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 3))

    def enableALDO4(self):
        super().setRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 3)

    def disableALDO4(self):
        super().clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 3)

    def setALDO4Voltage(self, millivolt:int)->bool:
        if (millivolt % XPOWERS_AXP2101_ALDO4_VOL_STEPS):
            print("Mistake ! The steps is must %u mV" %
                  XPOWERS_AXP2101_ALDO4_VOL_STEPS)
            return False
        if (millivolt < XPOWERS_AXP2101_ALDO4_VOL_MIN):
            print("Mistake ! ALDO4 minimum output voltage is  %umV" %
                  XPOWERS_AXP2101_ALDO4_VOL_MIN)
            return False
        elif (millivolt > XPOWERS_AXP2101_ALDO4_VOL_MAX):
            print("Mistake ! ALDO4 maximum output voltage is  %umV" %
                  XPOWERS_AXP2101_ALDO4_VOL_MAX)
            return False
        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL3_CTRL) & 0xE0
        val |= (int)((millivolt - XPOWERS_AXP2101_ALDO4_VOL_MIN) /
                     XPOWERS_AXP2101_ALDO4_VOL_STEPS)
        super().writeRegister(XPOWERS_AXP2101_LDO_VOL3_CTRL, val)
        return True

    def getALDO4Voltage(self):
        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL3_CTRL) & 0x1F
        return val * XPOWERS_AXP2101_ALDO4_VOL_STEPS + XPOWERS_AXP2101_ALDO4_VOL_MIN

    # Power control BLDO1 functions
    def isEnableBLDO1(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 4))

    def enableBLDO1(self):
        super().setRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 4)

    def disableBLDO1(self):
        super().clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 4)

    def setBLDO1Voltage(self, millivolt:int)->bool:
        if (millivolt % XPOWERS_AXP2101_BLDO1_VOL_STEPS):
            print("Mistake ! The steps is must %u mV" %
                  XPOWERS_AXP2101_BLDO1_VOL_STEPS)
            return False
        if (millivolt < XPOWERS_AXP2101_BLDO1_VOL_MIN):
            print("Mistake ! BLDO1 minimum output voltage is  %umV" %
                  XPOWERS_AXP2101_BLDO1_VOL_MIN)
            return False
        elif (millivolt > XPOWERS_AXP2101_BLDO1_VOL_MAX):
            print("Mistake ! BLDO1 maximum output voltage is  %umV" %
                  XPOWERS_AXP2101_BLDO1_VOL_MAX)
            return False
        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL4_CTRL)
        val &= 0xE0
        val |= (int)((millivolt - XPOWERS_AXP2101_BLDO1_VOL_MIN) /
                     XPOWERS_AXP2101_BLDO1_VOL_STEPS)
        super().writeRegister(XPOWERS_AXP2101_LDO_VOL4_CTRL, val)
        return True

    def getBLDO1Voltage(self):
        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL4_CTRL)
        val &= 0x1F
        return val * XPOWERS_AXP2101_BLDO1_VOL_STEPS + XPOWERS_AXP2101_BLDO1_VOL_MIN

    # Power control BLDO2 functions
    def isEnableBLDO2(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 5))

    def enableBLDO2(self):
        super().setRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 5)

    def disableBLDO2(self):
        super().clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 5)

    def setBLDO2Voltage(self, millivolt:int)->bool:
        if (millivolt % XPOWERS_AXP2101_BLDO2_VOL_STEPS):
            print("Mistake ! The steps is must %u mV" %
                  XPOWERS_AXP2101_BLDO2_VOL_STEPS)
            return False
        if (millivolt < XPOWERS_AXP2101_BLDO2_VOL_MIN):
            print("Mistake ! BLDO2 minimum output voltage is  %umV" %
                  XPOWERS_AXP2101_BLDO2_VOL_MIN)
            return False
        elif (millivolt > XPOWERS_AXP2101_BLDO2_VOL_MAX):
            print("Mistake ! BLDO2 maximum output voltage is  %umV" %
                  XPOWERS_AXP2101_BLDO2_VOL_MAX)
            return False
        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL5_CTRL) & 0xE0
        val |= (int)((millivolt - XPOWERS_AXP2101_BLDO2_VOL_MIN) /
                     XPOWERS_AXP2101_BLDO2_VOL_STEPS)
        super().writeRegister(XPOWERS_AXP2101_LDO_VOL5_CTRL, val)
        return True

    def getBLDO2Voltage(self):
        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL5_CTRL)
        val &= 0x1F
        return val * XPOWERS_AXP2101_BLDO2_VOL_STEPS + XPOWERS_AXP2101_BLDO2_VOL_MIN

    # Power control CPUSLDO functions
    def isEnableCPUSLDO(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 6))

    def enableCPUSLDO(self):
        super().setRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 6)

    def disableCPUSLDO(self):
        super().clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 6)

    def setCPUSLDOVoltage(self, millivolt:int)->bool:
        if (millivolt % XPOWERS_AXP2101_CPUSLDO_VOL_STEPS):
            print("Mistake ! The steps is must %u mV" %
                  XPOWERS_AXP2101_CPUSLDO_VOL_STEPS)
            return False

        if (millivolt < XPOWERS_AXP2101_CPUSLDO_VOL_MIN):
            print("Mistake ! CPULDO minimum output voltage is  %umV" %
                  XPOWERS_AXP2101_CPUSLDO_VOL_MIN)
            return False
        elif (millivolt > XPOWERS_AXP2101_CPUSLDO_VOL_MAX):
            print("Mistake ! CPULDO maximum output voltage is  %umV" %
                  XPOWERS_AXP2101_CPUSLDO_VOL_MAX)
            return False
        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL6_CTRL) & 0xE0
        val |= (int)((millivolt - XPOWERS_AXP2101_CPUSLDO_VOL_MIN) /
                     XPOWERS_AXP2101_CPUSLDO_VOL_STEPS)
        super().writeRegister(XPOWERS_AXP2101_LDO_VOL6_CTRL, val)
        return True

    def getCPUSLDOVoltage(self):
        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL6_CTRL)
        val &= 0x1F
        return val * XPOWERS_AXP2101_CPUSLDO_VOL_STEPS + XPOWERS_AXP2101_CPUSLDO_VOL_MIN

    # Power control DLDO1 functions
    def isEnableDLDO1(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 7))

    def enableDLDO1(self):
        super().setRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 7)

    def disableDLDO1(self):
        super().clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 7)

    def setDLDO1Voltage(self, millivolt:int)->bool:
        if (millivolt % XPOWERS_AXP2101_DLDO1_VOL_STEPS):
            print("Mistake ! The steps is must %u mV" %
                  XPOWERS_AXP2101_DLDO1_VOL_STEPS)
            return False
        if (millivolt < XPOWERS_AXP2101_DLDO1_VOL_MIN):
            print("Mistake ! DLDO1 minimum output voltage is  %umV" %
                  XPOWERS_AXP2101_DLDO1_VOL_MIN)
            return False
        elif (millivolt > XPOWERS_AXP2101_DLDO1_VOL_MAX):
            print("Mistake ! DLDO1 maximum output voltage is  %umV" %
                  XPOWERS_AXP2101_DLDO1_VOL_MAX)
            return False
        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL7_CTRL) & 0xE0
        val |= (int)((millivolt - XPOWERS_AXP2101_DLDO1_VOL_MIN) /
                     XPOWERS_AXP2101_DLDO1_VOL_STEPS)
        super().writeRegister(XPOWERS_AXP2101_LDO_VOL7_CTRL, val)
        return True

    def getDLDO1Voltage(self):
        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL7_CTRL)
        val &= 0x1F
        return val * XPOWERS_AXP2101_DLDO1_VOL_STEPS + XPOWERS_AXP2101_DLDO1_VOL_MIN

    # Power control DLDO2 functions
    def isEnableDLDO2(self)->bool:
        return bool(super().getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL1, 0))

    def enableDLDO2(self):
        super().setRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL1, 0)

    def disableDLDO2(self):
        super().clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL1, 0)

    def setDLDO2Voltage(self, millivolt:int)->bool:
        if (millivolt % XPOWERS_AXP2101_DLDO2_VOL_STEPS):
            print("Mistake ! The steps is must %u mV" %
                  XPOWERS_AXP2101_DLDO2_VOL_STEPS)
            return False
        if (millivolt < XPOWERS_AXP2101_DLDO2_VOL_MIN):
            print("Mistake ! DLDO2 minimum output voltage is  %umV" %
                  XPOWERS_AXP2101_DLDO2_VOL_MIN)
            return False
        elif (millivolt > XPOWERS_AXP2101_DLDO2_VOL_MAX):
            print("Mistake ! DLDO2 maximum output voltage is  %umV" %
                  XPOWERS_AXP2101_DLDO2_VOL_MAX)
            return False
        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL8_CTRL) & 0xE0
        val |= (int)((millivolt - XPOWERS_AXP2101_DLDO2_VOL_MIN) /
                     XPOWERS_AXP2101_DLDO2_VOL_STEPS)
        super().writeRegister(XPOWERS_AXP2101_LDO_VOL8_CTRL, val)
        return True

    def getDLDO2Voltage(self):
        val = super().readRegister(XPOWERS_AXP2101_LDO_VOL8_CTRL)
        val &= 0x1F
        return val * XPOWERS_AXP2101_DLDO2_VOL_STEPS + XPOWERS_AXP2101_DLDO2_VOL_MIN

    #  Power ON OFF IRQ TIMMING Control method
    def setIrqLevelTime(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL)
        val &= 0xCF
        super().writeRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL, val | (opt << 4))

    def getIrqLevelTime(self):
        return ((super().readRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL) & 0x30) >> 4)

    # @brief Set the PEKEY power-on long press time.
    # @param  opt: See xpowers_press_on_time_t enum for details.
    def setPowerKeyPressOnTime(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL)
        val &= 0xFC
        super().writeRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL, val | opt)

    # @brief Get the PEKEY power-on long press time.
    # @retval See xpowers_press_on_time_t enum for details.
    def getPowerKeyPressOnTime(self):
        val = super().readRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL)
        return (val & 0x03)

    # @brief Set the PEKEY power-off long press time.
    # @param  opt: See xpowers_press_off_time_t enum for details.
    # @retval
    def setPowerKeyPressOffTime(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL)
        val &= 0xF3
        super().writeRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL, val | (opt << 2))

    # @brief Get the PEKEY power-off long press time.
    # @retval See xpowers_press_off_time_t enum for details.
    def getPowerKeyPressOffTime(self):
        return ((super().readRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL) & 0x0C) >> 2)

    #  ADC Control method
    def enableGeneralAdcChannel(self):
        super().setRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 5)

    def disableGeneralAdcChannel(self):
        super().clrRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 5)

    def enableTemperatureMeasure(self):
        super().setRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 4)

    def disableTemperatureMeasure(self):
        super().clrRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 4)

    def getTemperature(self):
        #!FIXME
        return super().readRegisterH6L8(XPOWERS_AXP2101_ADC_DATA_RELUST8, XPOWERS_AXP2101_ADC_DATA_RELUST9)

    def enableSystemVoltageMeasure(self):
        super().setRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 3)

    def disableSystemVoltageMeasure(self):
        super().clrRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 3)

    def getSystemVoltage(self):
        return super().readRegisterH6L8(XPOWERS_AXP2101_ADC_DATA_RELUST6, XPOWERS_AXP2101_ADC_DATA_RELUST7)

    def enableVbusVoltageMeasure(self):
        super().setRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 2)

    def disableVbusVoltageMeasure(self):
        super().clrRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 2)

    def getVbusVoltage(self):
        return super().readRegisterH6L8(XPOWERS_AXP2101_ADC_DATA_RELUST4, XPOWERS_AXP2101_ADC_DATA_RELUST5)

    def enableTSPinMeasure(self):
        super().setRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 1)

    def disableTSPinMeasure(self):
        super().clrRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 1)

    def enableTSPinLowFreqSample(self):
        super().setRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 7)

    def disableTSPinLowFreqSample(self):
        super().clrRegisterBit(XPOWERS_AXP2101_ADC_DATA_RELUST2, 7)

    def getTsTemperature(self):
        return super().readRegisterH6L8(XPOWERS_AXP2101_ADC_DATA_RELUST2, XPOWERS_AXP2101_ADC_DATA_RELUST3)

    def enableBattVoltageMeasure(self):
        super().setRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 0)

    def disableBattVoltageMeasure(self):
        super().clrRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 0)

    def enableBattDetection(self):
        super().setRegisterBit(XPOWERS_AXP2101_BAT_DET_CTRL, 0)

    def disableBattDetection(self):
        super().clrRegisterBit(XPOWERS_AXP2101_BAT_DET_CTRL, 0)

    def getBattVoltage(self) -> int:
        if not self.isBatteryConnect():
            return 0
        return super().readRegisterH5L8(XPOWERS_AXP2101_ADC_DATA_RELUST0, XPOWERS_AXP2101_ADC_DATA_RELUST1)

    def getBatteryPercent(self) -> int:
        if not self.isBatteryConnect():
            return -1
        return super().readRegister(XPOWERS_AXP2101_BAT_PERCENT_DATA)

    # CHG LED setting and control

    # def enableChargingLed(self):
    #     super().setRegisterBit(XPOWERS_AXP2101_CHGLED_SET_CTRL, 0)
    #

    # def disableChargingLed(self):
    #     super().clrRegisterBit(XPOWERS_AXP2101_CHGLED_SET_CTRL, 0)
    #

     # @brief Set charging led mode.
     # @retval See xpowers_chg_led_mode_t enum for details.

    def setChargingLedMode(self, mode:int):
        range = [XPOWERS_CHG_LED_OFF, XPOWERS_CHG_LED_BLINK_1HZ,
                 XPOWERS_CHG_LED_BLINK_4HZ, XPOWERS_CHG_LED_ON]
        val = 0
        if mode in range:
            val = super().readRegister(XPOWERS_AXP2101_CHGLED_SET_CTRL)
            val &= 0xC8
            val |= 0x05  # use manual ctrl
            val |= (mode << 4)
            super().writeRegister(XPOWERS_AXP2101_CHGLED_SET_CTRL, val)
        else:
            val = super().readRegister(XPOWERS_AXP2101_CHGLED_SET_CTRL)
            val &= 0xF9
            super().writeRegister(XPOWERS_AXP2101_CHGLED_SET_CTRL, val | 0x01)  # use type A mode

    def getChargingLedMode(self):
        val = super().readRegister(XPOWERS_AXP2101_CHGLED_SET_CTRL)
        val >>= 1
        if (val & 0x02) == 0x02:
            val >>= 4
            return val & 0x03
        return XPOWERS_CHG_LED_CTRL_CHG

    # @brief 预充电充电电流限制
    # @note  Precharge current limit 25N mA
    # @param   opt: 25  opt
    # # @retval None
    def setPrechargeCurr(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_IPRECHG_SET)
        val &= 0xFC
        super().writeRegister(XPOWERS_AXP2101_IPRECHG_SET, val | opt)

    def getPrechargeCurr(self):
        return (super().readRegister(XPOWERS_AXP2101_IPRECHG_SET) & 0x03)

     # @brief Set charge current.
     # @param   opt: See xpowers_axp2101_chg_curr_t enum for details.
     # @retval
    def setChargerConstantCurr(self, opt:int):
        if (opt > XPOWERS_AXP2101_CHG_CUR_1000MA):
            return False
        val = super().readRegister(XPOWERS_AXP2101_ICC_CHG_SET)
        val &= 0xE0
        super().writeRegister(XPOWERS_AXP2101_ICC_CHG_SET, val | opt)

    # @brief Get charge current settings.
    # @retval See xpowers_axp2101_chg_curr_t enum for details.

    def getChargerConstantCurr(self):
        return (super().readRegister(XPOWERS_AXP2101_ICC_CHG_SET) & 0x1F)

    # @brief  充电终止电流限制
    # @note   Charging termination of current limit

    def setChargerTerminationCurr(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_ITERM_CHG_SET_CTRL)
        val &= 0xF0
        super().writeRegister(XPOWERS_AXP2101_ICC_CHG_SET, val | opt)

    def getChargerTerminationCurr(self):
        return (super().readRegister(XPOWERS_AXP2101_ITERM_CHG_SET_CTRL) & 0x0F)

    def enableChargerTerminationLimit(self):
        val = super().readRegister(XPOWERS_AXP2101_ITERM_CHG_SET_CTRL)
        super().writeRegister(XPOWERS_AXP2101_ITERM_CHG_SET_CTRL, val | 0x10)

    def disableChargerTerminationLimit(self):
        val = super().readRegister(XPOWERS_AXP2101_ITERM_CHG_SET_CTRL)
        super().writeRegister(XPOWERS_AXP2101_ITERM_CHG_SET_CTRL, val & 0xEF)

    def isChargerTerminationLimit(self)->bool:
        return super().getRegisterBit(XPOWERS_AXP2101_ITERM_CHG_SET_CTRL, 4)

    # @brief Set charge target voltage.
    # @param   opt: See xpowers_axp2101_chg_vol_t enum for details.

    def setChargeTargetVoltage(self, opt:int):
        if (opt >= XPOWERS_AXP2101_CHG_VOL_MAX):
            return False
        val = super().readRegister(XPOWERS_AXP2101_CV_CHG_VOL_SET)
        val &= 0xFC
        super().writeRegister(XPOWERS_AXP2101_CV_CHG_VOL_SET, val | opt)

    # @brief Get charge target voltage settings.
    # @retval See xpowers_axp2101_chg_vol_t enum for details.

    def getChargeTargetVoltage(self):
        return (super().readRegister(XPOWERS_AXP2101_CV_CHG_VOL_SET) & 0x03)

    # @brief  设定热阈值
    # @note   Thermal regulation threshold setting
    def setThermaThreshold(self, opt:int):
        val = super().readRegister(XPOWERS_AXP2101_THE_REGU_THRES_SET)
        val &= 0xFC
        super().writeRegister(XPOWERS_AXP2101_THE_REGU_THRES_SET, val | opt)

    def getThermaThreshold(self):
        return (super().readRegister(XPOWERS_AXP2101_THE_REGU_THRES_SET) & 0x03)

    def getBatteryParameter(self):
        return super().readRegister(XPOWERS_AXP2101_BAT_PARAME)

    #  Interrupt status/control functions
    # @brief  Get the interrupt controller mask value.
    # @retval   Mask value corresponds to xpowers_axp2101_irq_t ,
    def getIrqStatus(self):
        self.statusRegister[0] = super().readRegister(XPOWERS_AXP2101_INTSTS1)
        self.statusRegister[1] = super().readRegister(XPOWERS_AXP2101_INTSTS2)
        self.statusRegister[2] = super().readRegister(XPOWERS_AXP2101_INTSTS3)
        return (self.statusRegister[0] << 16) | (self.statusRegister[1] << 8) | (self.statusRegister[2])

    # @brief  Clear interrupt controller state.

    def clearIrqStatus(self):
        for i in range(0, XPOWERS_AXP2101_INTSTS_CNT):
            super().writeRegister(XPOWERS_AXP2101_INTSTS1 + i, 0xFF)
            self.statusRegister[i] = 0

    # @brief  Eanble PMU interrupt control mask .
    # @param   opt: View the related chip type xpowers_axp2101_irq_t enumeration parameters in "XPowersParams.hpp"

    def enableIRQ(self, opt:int, debug=False):
        self.setInterruptImpl(opt, True, debug)

    # @brief  Disable PMU interrupt control mask .
    # @param   opt: View the related chip type xpowers_axp2101_irq_t enumeration parameters in "XPowersParams.hpp"
    def disableIRQ(self, opt:int, debug=False):
        self.setInterruptImpl(opt, False, debug)

    # IRQ STATUS 0
    def isDropWarningLevel2Irq(self)->bool:
        mask = XPOWERS_AXP2101_WARNING_LEVEL2_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False

    def isDropWarningLevel1Irq(self)->bool:
        mask = XPOWERS_AXP2101_WARNING_LEVEL1_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False

    def isGaugeWdtTimeoutIrq(self)->bool:
        mask = XPOWERS_AXP2101_WDT_TIMEOUT_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False

    def isBatChargerOverTemperatureIrq(self)->bool:
        mask = XPOWERS_AXP2101_BAT_CHG_OVER_TEMP_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False

    def isBatChargerUnderTemperatureIrq(self)->bool:
        mask = XPOWERS_AXP2101_BAT_CHG_UNDER_TEMP_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False
            
    def isBatWorkOverTemperatureIrq(self)->bool:
        mask = XPOWERS_AXP2101_BAT_NOR_OVER_TEMP_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False
            
    def isBatWorkUnderTemperatureIrq(self)->bool:
        mask = XPOWERS_AXP2101_BAT_NOR_UNDER_TEMP_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False
            
    # IRQ STATUS 1
    def isVbusInsertIrq(self)->bool:
        mask = XPOWERS_AXP2101_VBUS_INSERT_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isVbusRemoveIrq(self)->bool:
        mask = XPOWERS_AXP2101_VBUS_REMOVE_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isBatInsertIrq(self)->bool:
        mask = XPOWERS_AXP2101_BAT_INSERT_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isBatRemoveIrq(self)->bool:
        mask = XPOWERS_AXP2101_BAT_REMOVE_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isPekeyShortPressIrq(self)->bool:
        mask = XPOWERS_AXP2101_PKEY_SHORT_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isPekeyLongPressIrq(self)->bool:
        mask = XPOWERS_AXP2101_PKEY_LONG_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isPekeyNegativeIrq(self)->bool:
        mask = XPOWERS_AXP2101_PKEY_NEGATIVE_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isPekeyPositiveIrq(self)->bool:
        mask = XPOWERS_AXP2101_PKEY_POSITIVE_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    # IRQ STATUS 2
    def isWdtExpireIrq(self)->bool:
        mask = XPOWERS_AXP2101_WDT_EXPIRE_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isLdoOverCurrentIrq(self)->bool:
        mask = XPOWERS_AXP2101_LDO_OVER_CURR_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isBatfetOverCurrentIrq(self)->bool:
        mask = XPOWERS_AXP2101_BATFET_OVER_CURR_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isBatChagerDoneIrq(self)->bool:
        mask = XPOWERS_AXP2101_BAT_CHG_DONE_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isBatChagerStartIrq(self)->bool:
        mask = XPOWERS_AXP2101_BAT_CHG_START_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isBatDieOverTemperatureIrq(self)->bool:
        mask = XPOWERS_AXP2101_DIE_OVER_TEMP_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isChagerOverTimeoutIrq(self)->bool:
        mask = XPOWERS_AXP2101_CHAGER_TIMER_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isBatOverVoltageIrq(self)->bool:
        mask = XPOWERS_AXP2101_BAT_OVER_VOL_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def getChipID(self):
        return super().readRegister(XPOWERS_AXP2101_IC_TYPE)

    def __to_bin(self, value, num):
        bin_chars = ""
        tmp = value
        for i in range(num):
            bin_char = bin(tmp % 2)[-1]
            tmp = tmp // 2
            bin_chars = bin_char + bin_chars
        return bin_chars.upper()

    def setInterruptImpl(self, opts:int, enable:bool, debug:bool):
        if debug:
            print(("DISABLE", "ENABLE ")[enable], end='')
            print(': HEX:{:#08X}'.format(opts), end='')
            print(' BIN:', end='')
            print(self.__to_bin(opts, 64))
        if (opts & 0x0000FF):
            value = opts & 0xFF
            if debug:
                print('write in ints0 0b{0}'.format(self.__to_bin(value, 8)))
            data = super().readRegister(XPOWERS_AXP2101_INTEN1)
            self.intRegister[0] = ((data & (~value)), (data | value))[enable]
            super().writeRegister(XPOWERS_AXP2101_INTEN1,self.intRegister[0])
        if (opts & 0x00FF00):
            value = opts >> 8
            if debug:
                print('write in ints1 0b{0}'.format(self.__to_bin(value, 8)))
            data = super().readRegister(XPOWERS_AXP2101_INTEN2)
            self.intRegister[1] = ((data & (~value)), (data | value))[enable]
            super().writeRegister(XPOWERS_AXP2101_INTEN2,self.intRegister[1])
        if (opts & 0xFF0000):
            value = opts >> 16
            if debug:
                print('write in ints2 0b{0}'.format(self.__to_bin(value, 8)))
            data = super().readRegister(XPOWERS_AXP2101_INTEN3)
            self.intRegister[2] = ((data & (~value)), (data | value))[enable]
            super().writeRegister(XPOWERS_AXP2101_INTEN3,self.intRegister[2])
    
    def printIntRegister(self):
        for i in range(0, XPOWERS_AXP2101_INTSTS_CNT):
            val = super().readRegister(XPOWERS_AXP2101_INTEN1+i)
            print('[{0}]HEX={1} BIN={2}'.format(
                i, hex(val), self.__to_bin(val, 8)))


