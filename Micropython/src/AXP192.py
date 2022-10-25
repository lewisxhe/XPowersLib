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

@file      AXP192.py
@author    Lewis He (lewishe@outlook.com)
@date      2022-10-20

'''

from I2CInterface import *
from AXP192Constants import *
import math

class PMU_Gpio:
    def __init__(self) -> None:
        self.mode = 0
        self.val = 0

class AXP192(I2CInterface):
    def __init__(self, i2c_bus:I2C, addr=AXP192_SLAVE_ADDRESS) -> None:
        super().__init__(i2c_bus,addr)
        print('AXP192 __init__')
        self.statusRegister = [0] * XPOWERS_AXP192_INTSTS_CNT
        self.intRegister = [0] * XPOWERS_AXP192_INTSTS_CNT
        self.gpio = [PMU_Gpio(),PMU_Gpio(),PMU_Gpio(),PMU_Gpio(),PMU_Gpio(),PMU_Gpio()] 

        if self.getChipID() != XPOWERS_AXP192_CHIP_ID:
            raise RuntimeError(
                "Failed to find %s - check your wiring!" % self.__class__.__name__
            )
        

    def isAcinVbusStart(self) -> bool:
        return bool(super().getRegisterBit(XPOWERS_AXP192_STATUS, 0))

    def isDischarge(self) -> bool:
        return not bool(super().getRegisterBit(XPOWERS_AXP192_STATUS, 2))

    def isVbusIn(void) -> bool:
        return bool(super().getRegisterBit(XPOWERS_AXP192_STATUS, 5))

    def isAcinEfficient(self) -> bool:
        return bool(super().getRegisterBit(XPOWERS_AXP192_STATUS, 6))

    def isAcinIn(self) -> bool:
        return bool(super().getRegisterBit(XPOWERS_AXP192_STATUS, 7))

    def isOverTemperature(self) -> bool:
        return bool(super().getRegisterBit(XPOWERS_AXP192_MODE_CHGSTATUS, 7))

    def isCharging(self) -> bool:
        return bool(super().getRegisterBit(XPOWERS_AXP192_MODE_CHGSTATUS, 6))

    def isBatteryConnect(self) -> bool:
        return bool(super().getRegisterBit(XPOWERS_AXP192_MODE_CHGSTATUS, 5))

    def isBattInActiveMode(self) -> bool:
        return bool(super().getRegisterBit(XPOWERS_AXP192_MODE_CHGSTATUS, 3))

    def isChargeCurrLessPreset(self) -> bool:
        return bool(super().getRegisterBit(XPOWERS_AXP192_MODE_CHGSTATUS, 2))

    def enableVbusVoltageLimit(self):
        super().setRegisterBit(XPOWERS_AXP192_IPS_SET, 6)

    def disableVbusVoltageLimit(self):
        super().clrRegisterBit(XPOWERS_AXP192_IPS_SET, 6)

    def setVbusVoltageLimit(self, opt: int):
        val = super().readRegister(XPOWERS_AXP192_IPS_SET)
        val &= 0xC7
        super().writeRegister(XPOWERS_AXP192_IPS_SET, val | (opt << 3))

    # @brief  Set VBUS Current Input Limit.
    # @param  opt: View the related chip type xpowers_axp192_vbus_cur_limit_t enumeration
    #              parameters in "XPowersParams.hpp"

    def setVbusCurrentLimit(self, opt: int):
        if opt == XPOWERS_AXP192_VBUS_CUR_LIM_500MA:
            super().setRegisterBit(XPOWERS_AXP192_IPS_SET, 1)
            super().clrRegisterBit(XPOWERS_AXP192_IPS_SET, 0)
        elif opt == XPOWERS_AXP192_VBUS_CUR_LIM_100MA:
            super().setRegisterBit(XPOWERS_AXP192_IPS_SET, 1)
            super().setRegisterBit(XPOWERS_AXP192_IPS_SET, 0)
        elif opt == XPOWERS_AXP192_VBUS_CUR_LIM_OFF:
            super().clrRegisterBit(XPOWERS_AXP192_IPS_SET, 1)

    # @brief  Get VBUS Current Input Limit.
    # @retval View the related chip type xpowers_axp192_vbus_cur_limit_t enumeration
    #              parameters in "XPowersParams.hpp"
    def getVbusCurrentLimit(self) -> int:
        if super().getRegisterBit(XPOWERS_AXP192_IPS_SET, 1) == 0:
            return XPOWERS_AXP192_VBUS_CUR_LIM_OFF
        if super().getRegisterBit(XPOWERS_AXP192_IPS_SET, 0):
            return XPOWERS_AXP192_VBUS_CUR_LIM_100MA
        return XPOWERS_AXP192_VBUS_CUR_LIM_500MA

    # Set the minimum system operating voltage inside the PMU,
    # below this value will shut down the PMU,Adjustment range 2600mV ~ 3300mV
    def setSysPowerDownVoltage(self, millivolt: int) -> bool:
        if millivolt % XPOWERS_AXP192_SYS_VOL_STEPS:
            print("Mistake ! The steps is must %u mV"%
                  XPOWERS_AXP192_SYS_VOL_STEPS)
            return False
        if millivolt < XPOWERS_AXP192_VOFF_VOL_MIN:
            print("Mistake ! SYS minimum output voltage is  %umV"%
                  XPOWERS_AXP192_VOFF_VOL_MIN)
            return False
        elif millivolt > XPOWERS_AXP192_VOFF_VOL_MAX:
            print("Mistake ! SYS maximum output voltage is  %umV"%
                  XPOWERS_AXP192_VOFF_VOL_MAX)
            return False
        val = super().readRegister(XPOWERS_AXP192_VOFF_SET)
        val &= 0xF8
        val |= (int)((millivolt - XPOWERS_AXP192_VOFF_VOL_MIN) / XPOWERS_AXP192_SYS_VOL_STEPS)
        super().writeRegister(XPOWERS_AXP192_VOFF_SET, val)
        return True

    def getSysPowerDownVoltage(self) -> int:
        val = super().readRegister(XPOWERS_AXP192_VOFF_SET)
        val &= 0x07
        return (val * XPOWERS_AXP192_SYS_VOL_STEPS) + XPOWERS_AXP192_VOFF_VOL_MIN

    # @brief  Set shutdown, calling shutdown will turn off all power channels,
    #         only VRTC belongs to normal power supply
    def shutdown(self):
        super().setRegisterBit(XPOWERS_AXP192_OFF_CTL, 7)

    # Charge setting
    def enableCharge(self):
        super().setRegisterBit(XPOWERS_AXP192_CHARGE1, 7)

    def disableCharge(self):
        super().clrRegisterBit(XPOWERS_AXP192_CHARGE1, 7)

    # @brief Set charge target voltage.
    # @param  opt: See xpowers_axp192_chg_vol_t enum for details.
    def setChargeTargetVoltage(self, opt: int):
        if opt >= XPOWERS_AXP192_CHG_VOL_MAX:
            return False
        val = super().readRegister(XPOWERS_AXP192_CHARGE1)
        val &= 0x9F
        super().writeRegister(XPOWERS_AXP192_CHARGE1, val | (opt << 5))

     # @brief Get charge target voltage settings.
     # @retval See xpowers_axp192_chg_vol_t enum for details.
    def getChargeTargetVoltage(self) -> int:
        val = super().readRegister(XPOWERS_AXP192_CHARGE1)
        return (val & 0x60) >> 5

    # @brief Set charge current settings.
    # @retval See xpowers_axp192_chg_curr_t enum for details.

    def setChargerConstantCurr(self, opt: int) -> bool:
        if opt > 0x0F:
            return False
        val = super().readRegister(XPOWERS_AXP192_CHARGE1)
        val &= 0xF0
        super().writeRegister(XPOWERS_AXP192_CHARGE1, val | opt)
        return True

    # @brief Get charge current settings.
    # @retval See xpowers_axp192_chg_curr_t enum for details.
    def getChargerConstantCurr(self):
        val = super().readRegister(XPOWERS_AXP192_CHARGE1) & 0x0F
        return val

    def setChargerTerminationCurr(self, opt: int):
        if opt == XPOWERS_AXP192_CHG_ITERM_LESS_10_PERCENT:
            super().clrRegisterBit(XPOWERS_AXP192_CHARGE1, 0)
        elif opt == XPOWERS_AXP192_CHG_ITERM_LESS_15_PERCENT:
            super().setRegisterBit(XPOWERS_AXP192_CHARGE1, 0)

    def getChargerTerminationCurr(self) -> int:
        return super().getRegisterBit(XPOWERS_AXP192_CHARGE1, 4)

    def setPrechargeTimeout(self, opt: int):
        val = super().readRegister(XPOWERS_AXP192_CHARGE2)
        val &= 0x3F
        super().writeRegister(XPOWERS_AXP192_CHARGE2, val | (opt << 6))

    #  External channel charge current setting,Range:300~1000mA
    def setChargerExternChannelCurr(self, milliampere: int) -> bool:
        if milliampere % XPOWERS_AXP192_CHG_EXT_CURR_STEP:
            print("Mistake ! The steps is must %u mV"%
                  XPOWERS_AXP192_CHG_EXT_CURR_STEP)
            return False
        if milliampere < XPOWERS_AXP192_CHG_EXT_CURR_MIN:
            print("Mistake ! The minimum external path charge current setting is:  %umA"%
                  XPOWERS_AXP192_CHG_EXT_CURR_MIN)
            return False
        elif milliampere > XPOWERS_AXP192_CHG_EXT_CURR_MAX:
            print("Mistake ! The maximum external channel charge current setting is:  %umA"%
                  XPOWERS_AXP192_CHG_EXT_CURR_MAX)
            return False
        val = super().readRegister(XPOWERS_AXP192_CHARGE2)
        val &= 0xC7
        val |= (int)((milliampere - XPOWERS_AXP192_CHG_EXT_CURR_MIN) / XPOWERS_AXP192_CHG_EXT_CURR_STEP)
        super().writeRegister(XPOWERS_AXP192_CHARGE2, val)
        return True

    def enableChargerExternChannel(self):
        super().setRegisterBit(XPOWERS_AXP192_CHARGE2, 2)

    def disableChargerExternChannel(self):
        super().clrRegisterBit(XPOWERS_AXP192_CHARGE2, 2)

    #  Timeout setting in constant current mode
    def setChargerConstantTimeout(self, opt:int):
        val = super().readRegister(XPOWERS_AXP192_CHARGE2)
        val &= 0xFC
        super().writeRegister(XPOWERS_AXP192_CHARGE2, val | opt)

    def enableBackupBattCharger(self):
        super().setRegisterBit(XPOWERS_AXP192_BACKUP_CHG, 7)

    def disableBackupBattCharger(self):
        super().clrRegisterBit(XPOWERS_AXP192_BACKUP_CHG, 7)

    def isEanbleBackupCharger(self) -> bool:
        return bool(super().getRegisterBit(XPOWERS_AXP192_BACKUP_CHG, 7))

    def setBackupBattChargerVoltage(self, opt: int) -> int:
        val = super().readRegister(XPOWERS_AXP192_BACKUP_CHG)
        val &= 0x9F
        super().writeRegister(XPOWERS_AXP192_BACKUP_CHG, val | (opt << 5))

    def setBackupBattChargerCurr(self, opt: int):
        val = super().readRegister(XPOWERS_AXP192_BACKUP_CHG)
        val &= 0xFC
        super().writeRegister(XPOWERS_AXP192_BACKUP_CHG, val | opt)

    # Temperature
    def getTemperature(self) -> float:
        return super().readRegisterH8L4(XPOWERS_AXP192_INTERNAL_TEMP_H8, XPOWERS_AXP192_INTERNAL_TEMP_L4) * XPOWERS_AXP192_INTERNAL_TEMP_STEP - XPOWERS_AXP192_INERNAL_TEMP_OFFSET

    def enableTemperatureMeasure(self):
        super().setRegisterBit(XPOWERS_AXP192_ADC_EN2, 7)

    def disableTemperatureMeasure(self):
        super().clrRegisterBit(XPOWERS_AXP192_ADC_EN2, 7)

    # Power control LDOio functions
    def isEnableLDOio(self) -> bool:
        val = super().readRegister(XPOWERS_AXP192_GPIO0_CTL)
        return bool(val & 0x02)

    def enableLDOio(self):
        val = super().readRegister(XPOWERS_AXP192_GPIO0_CTL) & 0xF8
        super().writeRegister(XPOWERS_AXP192_GPIO0_CTL, val | 0x02)

    def disableLDOio(self):
        val = super().readRegister(XPOWERS_AXP192_GPIO0_CTL) & 0xF8
        super().writeRegister(XPOWERS_AXP192_GPIO0_CTL, val)

    def setLDOioVoltage(self, millivolt: int) -> bool:
        if millivolt % XPOWERS_AXP192_LDOIO_VOL_STEPS:
            print("Mistake ! The steps is must %u mV"%
                  XPOWERS_AXP192_LDOIO_VOL_STEPS)
            return False
        if millivolt < XPOWERS_AXP192_LDOIO_VOL_MIN:
            print("Mistake ! LDOIO minimum output voltage is  %umV"%
                  XPOWERS_AXP192_LDOIO_VOL_MIN)
            return False
        elif millivolt > XPOWERS_AXP192_LDOIO_VOL_MAX:
            print("Mistake ! LDOIO maximum output voltage is  %umV"%
                  XPOWERS_AXP192_LDOIO_VOL_MAX)
            return False

        val = super().readRegister(XPOWERS_AXP192_GPIO0_VOL)
        val |= ((int)((millivolt - XPOWERS_AXP192_LDOIO_VOL_MIN) / XPOWERS_AXP192_LDOIO_VOL_STEPS) << 4)
        super().writeRegister(XPOWERS_AXP192_GPIO0_VOL, val)
        return True

    def getLDOioVoltage(self) -> int:
        val = super().readRegister(XPOWERS_AXP192_GPIO0_VOL)
        val >>= 4
        val *= XPOWERS_AXP192_LDOIO_VOL_STEPS
        val += XPOWERS_AXP192_LDOIO_VOL_MIN
        return val

    # Power control LDO2 functions
    def isEnableLDO2(self) -> bool:
        return bool(super().getRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 2))

    def enableLDO2(self):
        super().setRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 2)

    def disableLDO2(self):
        super().clrRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 2)

    def setLDO2Voltage(self, millivolt: int) -> int:
        if millivolt % XPOWERS_AXP192_LDO2_VOL_STEPS:
            print("Mistake ! The steps is must %u mV"%
                  XPOWERS_AXP192_LDO2_VOL_STEPS)
            return False
        if millivolt < XPOWERS_AXP192_LDO2_VOL_MIN:
            print("Mistake ! LDO2 minimum output voltage is  %umV"%
                  XPOWERS_AXP192_LDO2_VOL_MIN)
            return False
        elif millivolt > XPOWERS_AXP192_LDO2_VOL_MAX:
            print("Mistake ! LDO2 maximum output voltage is  %umV"%
                  XPOWERS_AXP192_LDO2_VOL_MAX)
            return False
        val = super().readRegister(XPOWERS_AXP192_LDO23OUT_VOL)
        val &= 0x0F
        super().writeRegister(XPOWERS_AXP192_LDO23OUT_VOL, val | ((int)((millivolt - XPOWERS_AXP192_LDO2_VOL_MIN) / XPOWERS_AXP192_LDO2_VOL_STEPS) << XPOWERS_AXP192_LDO2_VOL_BIT_MASK))
        return True

    def getLDO2Voltage(self) -> int:
        val = super().readRegister(XPOWERS_AXP192_LDO23OUT_VOL) & 0xF0
        return (val >> XPOWERS_AXP192_LDO2_VOL_BIT_MASK) * XPOWERS_AXP192_LDO2_VOL_STEPS + XPOWERS_AXP192_LDO2_VOL_MIN

    # Power control LDO3 functions

    def isEnableLDO3(self) -> bool:
        return bool(super().getRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 3))

    def enableLDO3(self):
        super().setRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 3)

    def disableLDO3(self):
        super().clrRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 3)

    def setLDO3Voltage(self, millivolt: int):
        if millivolt % XPOWERS_AXP192_LDO3_VOL_STEPS:
            print("Mistake ! The steps is must %u mV"%
                  XPOWERS_AXP192_LDO3_VOL_STEPS)
            return False
        if millivolt < XPOWERS_AXP192_LDO3_VOL_MIN:
            print("Mistake ! LDO3 minimum output voltage is  %umV"%
                  XPOWERS_AXP192_LDO3_VOL_MIN)
            return False
        elif millivolt > XPOWERS_AXP192_LDO3_VOL_MAX:
            print("Mistake ! LDO3 maximum output voltage is  %umV"%
                  XPOWERS_AXP192_LDO3_VOL_MAX)
            return False

        val = super().readRegister(XPOWERS_AXP192_LDO23OUT_VOL) & 0xF0
        super().writeRegister(XPOWERS_AXP192_LDO23OUT_VOL, val | (int)((millivolt - XPOWERS_AXP192_LDO3_VOL_MIN) / XPOWERS_AXP192_LDO3_VOL_STEPS))
        return True

    def getLDO3Voltage(self) -> int:
        val = super().readRegister(XPOWERS_AXP192_LDO23OUT_VOL)
        val &= 0x0F
        return (val * XPOWERS_AXP192_LDO3_VOL_STEPS) + XPOWERS_AXP192_LDO3_VOL_MIN

    # Power control DCDC1 functions
    def setDC1PwmMode(self):
        val = super().readRegister(XPOWERS_AXP192_DCDC_MODESET) & 0xF7
        super().writeRegister(XPOWERS_AXP192_DCDC_MODESET, val | 0x08)

    def setDC1AutoMode(self):
        val = super().readRegister(XPOWERS_AXP192_DCDC_MODESET) & 0xF7
        super().writeRegister(XPOWERS_AXP192_DCDC_MODESET, val)

    def isEnableDC1(self) -> bool:
        return bool(super().getRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 0))

    def enableDC1(self):
        super().setRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 0)

    def disableDC1(self):
        super().clrRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 0)

    def setDC1Voltage(self, millivolt) -> bool:
        if millivolt % XPOWERS_AXP192_DC1_VOL_STEPS:
            print("Mistake ! The steps is must %u mV"%
                  XPOWERS_AXP192_DC1_VOL_STEPS)
            return False
        if millivolt < XPOWERS_AXP192_DC1_VOL_STEPS:
            print("Mistake ! DCDC1 minimum output voltage is  %umV"%
                  XPOWERS_AXP192_DC1_VOL_STEPS)
            return False
        elif millivolt > XPOWERS_AXP192_DC1_VOL_MAX:
            print("Mistake ! DCDC1 maximum output voltage is  %umV"%
                  XPOWERS_AXP192_DC1_VOL_MAX)
            return False
        val = super().readRegister(XPOWERS_AXP192_DC1_VLOTAGE)
        val &= 0x80
        val |= (int)((millivolt - XPOWERS_AXP192_DC1_VOL_MIN) /  XPOWERS_AXP192_DC1_VOL_STEPS)
        super().writeRegister(XPOWERS_AXP192_DC1_VLOTAGE, val)
        return True

    def getDC1Voltage(self) -> int:
        val = super().readRegister(XPOWERS_AXP192_DC1_VLOTAGE) & 0x7F
        return val * XPOWERS_AXP192_DC1_VOL_STEPS + XPOWERS_AXP192_DC1_VOL_MIN

    # Power control DCDC2 functions

    def setDC2PwmMode(self):
        val = super().readRegister(XPOWERS_AXP192_DCDC_MODESET) & 0xFB
        super().writeRegister(XPOWERS_AXP192_DCDC_MODESET, val | 0x04)

    def setDC2AutoMode(self):
        val = super().readRegister(XPOWERS_AXP192_DCDC_MODESET) & 0xFB
        super().writeRegister(XPOWERS_AXP192_DCDC_MODESET, val)

    def enableDC2VRC(self):
        val = super().readRegister(XPOWERS_AXP192_DC2_DVM)
        super().writeRegister(XPOWERS_AXP192_DC2_DVM, val | 0x04)

    def disableDC2VRC(self):
        val = super().readRegister(XPOWERS_AXP192_DC2_DVM)
        super().writeRegister(XPOWERS_AXP192_DC2_DVM, val & 0xFB)

    def setDC2VRC(self, opts: int) -> bool:
        if opts > 1:
            return False
        val = super().readRegister(XPOWERS_AXP192_DC2_DVM) & 0xFE
        super().writeRegister(XPOWERS_AXP192_DC2_DVM, val | opts)
        return True

    def isEanbleDC2VRC(self) -> bool:
        return (super().readRegister(XPOWERS_AXP192_DC2_DVM) & 0x04) == 0x04

    def isEnableDC2(self) -> bool:
        return bool(super().getRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 4))

    def enableDC2(self):
        super().setRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 4)

    def disableDC2(self):
        super().clrRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 4)

    def setDC2Voltage(self, millivolt: int) -> bool:
        if millivolt % XPOWERS_AXP192_DC2_VOL_STEPS:
            print("Mistake ! The steps is must %u mV"%XPOWERS_AXP192_DC2_VOL_STEPS)
            return False

        if millivolt < XPOWERS_AXP192_DC2_VOL_MIN:
            print("Mistake ! DCDC2 minimum output voltage is  %umV"%
                  XPOWERS_AXP192_DC2_VOL_MIN)
            return False
        elif millivolt > XPOWERS_AXP192_DC2_VOL_MAX:
            print("Mistake ! DCDC2 maximum output voltage is  %umV"% 
                  XPOWERS_AXP192_DC2_VOL_MAX)
            return False
        val = super().readRegister(XPOWERS_AXP192_DC2OUT_VOL)
        val &= 0x80
        val |= (int)((millivolt - XPOWERS_AXP192_DC2_VOL_MIN) /  XPOWERS_AXP192_DC2_VOL_STEPS)
        super().writeRegister(XPOWERS_AXP192_DC2OUT_VOL, val)
        return True

    def getDC2Voltage(self) -> int:
        val = super().readRegister(XPOWERS_AXP192_DC2OUT_VOL)
        return (val * XPOWERS_AXP192_DC2_VOL_STEPS) + XPOWERS_AXP192_DC2_VOL_MIN

    # Power control DCDC3 functions

    def setDC3PwmMode(self):
        val = super().readRegister(XPOWERS_AXP192_DCDC_MODESET) & 0xFD
        super().writeRegister(XPOWERS_AXP192_DCDC_MODESET, val | 0x02)

    def setDC3AutoMode(self):
        val = super().readRegister(XPOWERS_AXP192_DCDC_MODESET) & 0xFD
        super().writeRegister(XPOWERS_AXP192_DCDC_MODESET, val)

    def isEnableDC3(self) -> bool:
        return bool(super().getRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 1))

    def enableDC3(self):
        super().setRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 1)

    def disableDC3(self):
        super().clrRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 1)

    def setDC3Voltage(self, millivolt: int) -> bool:
        if millivolt % XPOWERS_AXP192_DC3_VOL_STEPS:
            print("Mistake ! The steps is must %u mV"%
                  XPOWERS_AXP192_DC3_VOL_STEPS)
            return False
        if millivolt < XPOWERS_AXP192_DC3_VOL_MIN:
            print("Mistake ! DCDC3 minimum output voltage is  %umV"%
                  XPOWERS_AXP192_DC3_VOL_MIN)
            return False
        elif millivolt > XPOWERS_AXP192_DC3_VOL_MAX:
            print("Mistake ! DCDC3 maximum output voltage is  %umV"%
                  XPOWERS_AXP192_DC3_VOL_MAX)
            return False
        super().writeRegister(XPOWERS_AXP192_DC3OUT_VOL, (int)((millivolt - XPOWERS_AXP192_DC3_VOL_MIN) / XPOWERS_AXP192_DC3_VOL_STEPS))
        return True

    def getDC3Voltage(self) -> int:
        val = super().readRegister(XPOWERS_AXP192_DC3OUT_VOL)
        return (val * XPOWERS_AXP192_DC3_VOL_STEPS) + XPOWERS_AXP192_DC3_VOL_MIN

    # Power control EXTEN functions

    def enableExternalPin(self):
        super().setRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 6)

    def disableExternalPin(self):
        super().clrRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 6)

    def isEnableExternalPin(self) -> bool:
        return bool(super().getRegisterBit(XPOWERS_AXP192_LDO23_DC123_EXT_CTL, 6))

    # Interrupt status functions
    # @brief  Get the interrupt controller mask value.
    # @retval   Mask value corresponds to xpowers_axp192_irq_t ,

    def getIrqStatus(self):
        self.statusRegister[0] = super().readRegister(XPOWERS_AXP192_INTSTS1)
        self.statusRegister[1] = super().readRegister(XPOWERS_AXP192_INTSTS2)
        self.statusRegister[2] = super().readRegister(XPOWERS_AXP192_INTSTS3)
        self.statusRegister[3] = super().readRegister(XPOWERS_AXP192_INTSTS4)
        self.statusRegister[4] = super().readRegister(XPOWERS_AXP192_INTSTS5)
        return (self.statusRegister[4]) << 32 |\
               (self.statusRegister[3]) << 24 |\
               (self.statusRegister[2]) << 16 |\
               (self.statusRegister[1]) << 8 |\
               (self.statusRegister[0])

     # @brief  Clear interrupt controller state.
    def clearIrqStatus(self):
        for i in range(XPOWERS_AXP192_INTSTS_CNT-1):
            super().writeRegister(XPOWERS_AXP192_INTSTS1 + i, 0xFF)
        super().writeRegister(XPOWERS_AXP192_INTSTS5, 0xFF)

     # @brief  Eanble PMU interrupt control mask .
     # @ param  opt: View the related chip type xpowers_axp192_irq_t enumeration
     # parameters in "XPowersParams.hpp"
     # @retval

    def enableIRQ(self, opt:int):
        self.setInterruptImpl(opt, True)

     # @brief  Disable PMU interrupt control mask .
     # @ param  opt: View the related chip type xpowers_axp192_irq_t enumeration
     # parameters in "XPowersParams.hpp"
     # @retval

    def disableIRQ(self, opt:int):
        self.setInterruptImpl(opt, False)

    # IRQ STATUS 0
    def isAcinOverVoltageIrq(self) -> bool:
        mask = XPOWERS_AXP192_ACIN_OVER_VOL_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False

    def isAcinInserIrq(self) -> bool:
        mask = XPOWERS_AXP192_ACIN_CONNECT_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False

    def isAcinRemoveIrq(self) -> bool:
        mask = XPOWERS_AXP192_ACIN_REMOVED_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False

    def isVbusOverVoltageIrq(self) -> bool:
        mask = XPOWERS_AXP192_VBUS_OVER_VOL_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False

    def isVbusInsertIrq(self) -> bool:
        mask = XPOWERS_AXP192_VBUS_INSERT_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False

    def isVbusRemoveIrq(self) -> bool:
        mask = XPOWERS_AXP192_VBUS_REMOVE_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False

    def isVbusLowVholdIrq(self) -> bool:
        mask = XPOWERS_AXP192_VBUS_VHOLD_LOW_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False


    # IRQ STATUS 1
    def isBatInsertIrq(self) -> bool:
        mask = XPOWERS_AXP192_BAT_INSERT_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isBatRemoveIrq(self) -> bool:
        mask = XPOWERS_AXP192_BAT_REMOVE_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isBattEnterActivateIrq(self) -> bool:
        mask = XPOWERS_AXP192_BATT_ACTIVATE_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isBattExitActivateIrq(self) -> bool:
        mask = XPOWERS_AXP192_BATT_EXIT_ACTIVATE_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isBatChagerStartIrq(self) -> bool:
        mask = XPOWERS_AXP192_BAT_CHG_START_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isBatChagerDoneIrq(self) -> bool:
        mask = XPOWERS_AXP192_BAT_CHG_DONE_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isBattTempHighIrq(self) -> bool:
        mask = XPOWERS_AXP192_BATT_OVER_TEMP_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isBattTempLowIrq(self) -> bool:
        mask = XPOWERS_AXP192_BATT_LOW_TEMP_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    # IRQ STATUS 2
    def isChipOverTemperatureIrq(self) -> bool:
        mask = XPOWERS_AXP192_CHIP_TEMP_HIGH_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isChargingCurrentLessIrq(self) -> bool:
        mask = XPOWERS_AXP192_CHARGE_LOW_CUR_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isDC1VoltageLessIrq(self) -> bool:
        mask = XPOWERS_AXP192_DC1_LOW_VOL_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isDC2VoltageLessIrq(self) -> bool:
        mask = XPOWERS_AXP192_DC2_LOW_VOL_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isDC3VoltageLessIrq(self) -> bool:
        mask = XPOWERS_AXP192_DC3_LOW_VOL_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isPekeyShortPressIrq(self) -> bool:
        mask = XPOWERS_AXP192_PKEY_SHORT_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isPekeyLongPressIrq(self) -> bool:
        mask = XPOWERS_AXP192_PKEY_LONG_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False


    # IRQ STATUS 3
    def isNOEPowerOnIrq(self) -> bool:
        mask = XPOWERS_AXP192_NOE_ON_IRQ >> 24
        if self.intRegister[3] & mask:
            return super()._IS_BIT_SET(self.statusRegister[3], mask)
        else:
            return False

    def isNOEPowerDownIrq(self) -> bool:
        mask = XPOWERS_AXP192_NOE_OFF_IRQ >> 24
        if self.intRegister[3] & mask:
            return super()._IS_BIT_SET(self.statusRegister[3], mask)
        else:
            return False

    def isVbusEffectiveIrq(self) -> bool:
        mask = XPOWERS_AXP192_VBUS_VAILD_IRQ >> 24
        if self.intRegister[3] & mask:
            return super()._IS_BIT_SET(self.statusRegister[3], mask)
        else:
            return False

    def isVbusInvalidIrq(self) -> bool:
        mask = XPOWERS_AXP192_VBUS_INVALID_IRQ >> 24
        if self.intRegister[3] & mask:
            return super()._IS_BIT_SET(self.statusRegister[3], mask)
        else:
            return False

    def isVbusSessionIrq(self) -> bool:
        mask = XPOWERS_AXP192_VBUS_SESSION_AB_IRQ >> 24
        if self.intRegister[3] & mask:
            return super()._IS_BIT_SET(self.statusRegister[3], mask)
        else:
            return False

    def isVbusSessionEndIrq(self) -> bool:
        mask = XPOWERS_AXP192_VBUS_SESSION_END_IRQ >> 24
        if self.intRegister[3] & mask:
            return super()._IS_BIT_SET(self.statusRegister[3], mask)
        else:
            return False

    def isLowVoltageLevel2Irq(self) -> bool:
        mask = XPOWERS_AXP192_APS_LOW_VOL_LEVEL_IRQ >> 24
        if self.intRegister[3] & mask:
            return super()._IS_BIT_SET(self.statusRegister[3], mask)
        else:
            return False

    # IRQ STATUS 4
    def isWdtExpireIrq(self) -> bool:
        mask = XPOWERS_AXP192_TIMER_TIMEOUT_IRQ >> 32
        if self.intRegister[4] & mask:
            return super()._IS_BIT_SET(self.statusRegister[4], mask)
        else:
            return False

    def isGpio2EdgeTriggerIrq(self) -> bool:
        mask = XPOWERS_AXP192_GPIO2_EDGE_TRIGGER_IRQ >> 32
        if self.intRegister[4] & mask:
            return super()._IS_BIT_SET(self.statusRegister[4], mask)
        else:
            return False

    def isGpio1EdgeTriggerIrq(self) -> bool:
        mask = XPOWERS_AXP192_GPIO1_EDGE_TRIGGER_IRQ >> 32
        if self.intRegister[4] & mask:
            return super()._IS_BIT_SET(self.statusRegister[4], mask)
        else:
            return False

    def isGpio0EdgeTriggerIrq(self) -> bool:
        mask = XPOWERS_AXP192_GPIO0_EDGE_TRIGGER_IRQ >> 32
        if self.intRegister[4] & mask:
            return super()._IS_BIT_SET(self.statusRegister[4], mask)
        else:
            return False

    #   ADC Functions
    def enableBattDetection(self) -> bool:
        super().setRegisterBit(XPOWERS_AXP192_OFF_CTL, 6)

    def disableBattDetection(self) -> bool:
        super().clrRegisterBit(XPOWERS_AXP192_OFF_CTL, 6)

    def enableVbusVoltageMeasure(self) -> bool:
        self.setSignalCaptureImpl(MONITOR_USB_CURRENT | MONITOR_USB_VOLTAGE, True)

    def disableVbusVoltageMeasure(self) -> bool:
        self.setSignalCaptureImpl(MONITOR_USB_CURRENT | MONITOR_USB_VOLTAGE, False)

    def enableBattVoltageMeasure(self) -> bool:
        self.setSignalCaptureImpl(MONITOR_BAT_CURRENT | MONITOR_BAT_VOLTAGE, True)

    def disableBattVoltageMeasure(self) -> bool:
        self.setSignalCaptureImpl(MONITOR_BAT_CURRENT | MONITOR_BAT_VOLTAGE, False)

    def enableSystemVoltageMeasure(self) -> bool:
        self.setSignalCaptureImpl(MONITOR_APS_VOLTAGE, True)

    def disableSystemVoltageMeasure(self) -> bool:
        self.setSignalCaptureImpl(MONITOR_APS_VOLTAGE, False)

    def enableTSPinMeasure(self) -> bool:
        self.setSignalCaptureImpl(MONITOR_TS_PIN, True)

    def disableTSPinMeasure(self) -> bool:
        self.setSignalCaptureImpl(MONITOR_TS_PIN, False)

    def enableAdcChannel(self, opts: int):
        self.setSignalCaptureImpl(opts, True)

    def disableAdcChannel(self, opts: int):
        self.setSignalCaptureImpl(opts, False)

    def getVbusVoltage(self) -> int:
        if not self.isVbusIn():
            return 0
        return super().readRegisterH8L4(XPOWERS_AXP192_VBUS_VOL_H8,
                                XPOWERS_AXP192_VBUS_VOL_L4
                                ) * XPOWERS_AXP192_VBUS_VOLTAGE_STEP

    def getVbusCurrent(self) -> float:
        if not self.isVbusIn():
            return 0
        return super().readRegisterH8L4(XPOWERS_AXP192_VBUS_CUR_H8,
                                XPOWERS_AXP192_VBUS_CUR_L4
                                ) * XPOWERS_AXP192_VBUS_CUR_STEP

    def getBattVoltage(self) -> float:
        if not self.isBatteryConnect():
            return 0
        return super().readRegisterH8L4(XPOWERS_AXP192_BAT_AVERVOL_H8,
                                XPOWERS_AXP192_BAT_AVERVOL_L4
                                ) * XPOWERS_AXP192_BATT_VOLTAGE_STEP

    def getBattDischargeCurrent(self) -> float:
        if not self.isBatteryConnect():
            return 0
        return super().readRegisterH8L5(XPOWERS_AXP192_BAT_AVERDISCHGCUR_H8,
                                XPOWERS_AXP192_BAT_AVERDISCHGCUR_L5) * XPOWERS_AXP192_BATT_DISCHARGE_CUR_STEP

    def getAcinVoltage(self) -> float:
        if not self.isAcinIn():
            return 0
        return super().readRegisterH8L4(XPOWERS_AXP192_ACIN_VOL_H8, XPOWERS_AXP192_ACIN_VOL_L4) * XPOWERS_AXP192_ACIN_VOLTAGE_STEP

    def getAcinCurrent(self) -> float:
        if not self.isAcinIn():
            return 0
        return super().readRegisterH8L4(XPOWERS_AXP192_ACIN_CUR_H8, XPOWERS_AXP192_ACIN_CUR_L4) * XPOWERS_AXP192_ACIN_CUR_STEP

    def getSystemVoltage(self) -> float:
        return super().readRegisterH8L4(XPOWERS_AXP192_APS_AVERVOL_H8, XPOWERS_AXP192_APS_AVERVOL_L4) * XPOWERS_AXP192_APS_VOLTAGE_STEP

    # Timer Control
    def setTimerout(self, minute: int):
        super().writeRegister(XPOWERS_AXP192_TIMER_CTL, 0x80 | minute)

    def disableTimer(self):
        super().writeRegister(XPOWERS_AXP192_TIMER_CTL, 0x80)

    def clearTimerFlag(self):
        super().setRegisterBit(XPOWERS_AXP192_TIMER_CTL, 7)

    # Data Buffer
    def writeDataBuffer(self, data,  size: int):
        if size > XPOWERS_AXP192_DATA_BUFFER_SIZE:
            print('Out of range!')
            return
        for i in range(size):
            super().writeRegister(XPOWERS_AXP192_DATA_BUFFER1 + i, data[i])

    def readDataBuffer(self, size: int):
        if size > XPOWERS_AXP192_DATA_BUFFER_SIZE:
            print('Out of range!')
            return
        data = [0]*size
        for i in range(size):
            data[i] = super().readRegister(XPOWERS_AXP192_DATA_BUFFER1 + i)
        return data

    # Charge led functions
    # @brief Set charging led mode.
    # @retval See xpowers_chg_led_mode_t enum for details.
    def setChargingLedMode(self, mode: int):
        range = [XPOWERS_CHG_LED_OFF, XPOWERS_CHG_LED_BLINK_1HZ,
                 XPOWERS_CHG_LED_BLINK_4HZ, XPOWERS_CHG_LED_ON]
        if mode in range:
            val = super().readRegister(XPOWERS_AXP192_OFF_CTL)
            val &= 0xC7
            val |= 0x08      # use manual ctrl
            val |= (mode << 4)
            super().writeRegister(XPOWERS_AXP192_OFF_CTL, val)
        else:
            super().clrRegisterBit(XPOWERS_AXP192_OFF_CTL, 3)

    def getChargingLedMode(self) -> int:
        if not bool(super().getRegisterBit(XPOWERS_AXP192_OFF_CTL, 3)):
            return XPOWERS_CHG_LED_CTRL_CHG
        val = super().readRegister(XPOWERS_AXP192_OFF_CTL)
        val &= 0x30
        return val >> 4

    # Coulomb counter control

    def enableCoulomb(self):
        super().setRegisterBit(XPOWERS_AXP192_COULOMB_CTL, 7)

    def disableCoulomb(self):
        super().clrRegisterBit(XPOWERS_AXP192_COULOMB_CTL, 7)

    def stopCoulomb(self):
        super().setRegisterBit(XPOWERS_AXP192_COULOMB_CTL, 6)

    def clearCoulomb(self):
        super().setRegisterBit(XPOWERS_AXP192_COULOMB_CTL, 5)

    def getBattChargeCoulomb(self) -> int:
        data = [0]*4
        data[0] = super().readRegister(XPOWERS_AXP192_BAT_CHGCOULOMB3)
        data[1] = super().readRegister(XPOWERS_AXP192_BAT_CHGCOULOMB2)
        data[2] = super().readRegister(XPOWERS_AXP192_BAT_CHGCOULOMB1)
        data[3] = super().readRegister(XPOWERS_AXP192_BAT_CHGCOULOMB0)
        return (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]

    def getBattDischargeCoulomb(self) -> int:
        data = [0]*4
        data[0] = super().readRegister(XPOWERS_AXP192_BAT_DISCHGCOULOMB3)
        data[1] = super().readRegister(XPOWERS_AXP192_BAT_DISCHGCOULOMB2)
        data[2] = super().readRegister(XPOWERS_AXP192_BAT_DISCHGCOULOMB1)
        data[3] = super().readRegister(XPOWERS_AXP192_BAT_DISCHGCOULOMB0)
        return (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]

    def getAdcSamplingRate(self) -> int:
        val = super().readRegister(XPOWERS_AXP192_ADC_SPEED)
        return 25 * math.pow(2, (val & 0xC0) >> 6)

    def getCoulombData(self) -> float:
        charge = self.getBattChargeCoulomb()
        discharge = self.getBattDischargeCoulomb()
        rate = self.getAdcSamplingRate()
        return 65536.0 * 0.5 * (charge - discharge) / 3600.0 / rate

    # GPIO control functions
    def getBatteryChargeCurrent(self) -> float:
        return super().readRegisterH8L5(
            XPOWERS_AXP192_BAT_AVERCHGCUR_H8,
            XPOWERS_AXP192_BAT_AVERCHGCUR_L5
        ) * XPOWERS_AXP192_BATT_CHARGE_CUR_STEP

    def getGpio0Voltage(self) -> int:
        return super().readRegisterH8L4(XPOWERS_AXP192_GPIO0_VOL_ADC_H8, XPOWERS_AXP192_GPIO0_VOL_ADC_L4) * XPOWERS_AXP192_GPIO0_STEP * 1000

    def getGpio1Voltage(self) -> int:
        return super().readRegisterH8L4(XPOWERS_AXP192_GPIO1_VOL_ADC_H8, XPOWERS_AXP192_GPIO1_VOL_ADC_L4) * XPOWERS_AXP192_GPIO1_STEP * 1000

    def pwmSetup(self, channel: int,  freq: int, duty: int):
        #  PWM输出频率 = 2.25MHz / (X+1) / Y1
        #  PWM输出占空比 = Y2 / Y1
        if channel == 0:
            super().writeRegister(XPOWERS_AXP192_PWM1_FREQ_SET,  freq)
            super().writeRegister(XPOWERS_AXP192_PWM1_DUTY_SET1, duty >> 8)
            super().writeRegister(XPOWERS_AXP192_PWM1_DUTY_SET2, duty & 0xFF)
        elif channel == 1:
            super().writeRegister(XPOWERS_AXP192_PWM2_FREQ_SET,  freq)
            super().writeRegister(XPOWERS_AXP192_PWM2_DUTY_SET1, duty >> 8)
            super().writeRegister(XPOWERS_AXP192_PWM2_DUTY_SET2, duty & 0xFF)

    def pwmEnable(self, channel):
        if channel == 0:
            val = super().readRegister(XPOWERS_AXP192_GPIO1_CTL) & 0xF8
            super().writeRegister(XPOWERS_AXP192_GPIO1_CTL, val | 0x02)
        elif channel == 1:
            val = super().readRegister(XPOWERS_AXP192_GPIO2_CTL) & 0xF8
            super().writeRegister(XPOWERS_AXP192_GPIO2_CTL, val | 0x02)

    def getBatteryPercent(self) -> int:
        if not self.isBatteryConnect():
            return -1
        table = [3000, 3650, 3700, 3740, 3760, 3795,
                     3840, 3910, 3980, 4070, 4150]
        voltage = self.getBattVoltage()
        if voltage < table[0]:
            return 0
        for i in range(11):
            if voltage < table[i]:
                return i * 10 - (10 * (int)(table[i] - voltage)) / (int)(table[i] - table[i - 1])
        return 100

    def getChipID(self) -> int:
        return super().readRegister(XPOWERS_AXP192_IC_TYPE)


    # GPIO setting
    def pinMode(self, pin: int,  mode: int):
        if pin == PMU_GPIO0:
            '''
            * 000: NMOS open-drain output
            * 001: Universal input function
            * 010: Low noise LDO
            * 011: reserved
            * 100: ADC input
            * 101: Low output
            * 11X: Floating
            '''
            if mode == INPUT or mode == INPUT_PULLDOWN:
                if self.gpio[pin].mode != INPUT:
                    self.gpio[pin].mode = INPUT
                val = super().readRegister(XPOWERS_AXP192_GPIO0_CTL) & 0xF8
                super().writeRegister(XPOWERS_AXP192_GPIO0_CTL, val | 0x01)
                # Set pull-down mode
                val = super().readRegister(XPOWERS_AXP192_GPIO012_PULLDOWN) & 0xFE
                if mode == INPUT_PULLDOWN:
                    super().writeRegister(XPOWERS_AXP192_GPIO012_PULLDOWN, val | 0x01)
                else:
                    super().writeRegister(XPOWERS_AXP192_GPIO012_PULLDOWN, val)

        elif pin == PMU_GPIO1:
            '''
            * 000: NMOS open-drain output
            * 001: Universal input function
            * 010: PWM1 output, high level is VINT, not Can add less than 100K pull-down resistance
            * 011: reserved
            * 100: ADC input
            * 101: Low output
            * 11X: Floating
            '''
            if mode == INPUT or mode == INPUT_PULLDOWN:
                if self.gpio[pin].mode != INPUT:
                    self.gpio[pin].mode = INPUT
                val = super().readRegister(XPOWERS_AXP192_GPIO1_CTL) & 0xF8
                super().writeRegister(XPOWERS_AXP192_GPIO1_CTL, val | 0x01)
                # Set pull-down mode
                val = super().readRegister(XPOWERS_AXP192_GPIO012_PULLDOWN) & 0xFD
                if mode == INPUT_PULLDOWN:
                    super().writeRegister(XPOWERS_AXP192_GPIO012_PULLDOWN, val | 0x02)
                else:
                    super().writeRegister(XPOWERS_AXP192_GPIO012_PULLDOWN, val)

        elif pin == PMU_GPIO2:
            '''
            * 000: NMOS open-drain output
            * 001: Universal input function
            * 010: PWM2 output, high level is VINT, not Can add less than 100K pull-down resistance
            * 011: reserved
            * 100: ADC input
            * 101: Low output
            * 11X: Floating
            '''
            if mode == INPUT or mode == INPUT_PULLDOWN:
                if self.gpio[pin].mode != INPUT:
                    self.gpio[pin].mode = INPUT
                val = super().readRegister(XPOWERS_AXP192_GPIO2_CTL) & 0xF8
                super().writeRegister(XPOWERS_AXP192_GPIO2_CTL, val | 0x01)

                # Set pull-down mode
                val = super().readRegister(XPOWERS_AXP192_GPIO012_PULLDOWN) & 0xFB
                if mode == INPUT_PULLDOWN:
                    super().writeRegister(XPOWERS_AXP192_GPIO012_PULLDOWN, val | 0x04)
                else:
                    super().writeRegister(XPOWERS_AXP192_GPIO012_PULLDOWN, val)
        elif pin == PMU_GPIO3:
            '''
            * 00: External charging control
            * 01: NMOS open-drain output port 3
            * 10: Universal input port 3
            * 11: ADC input
            '''
            if mode == INPUT:
                if self.gpio[pin].mode != INPUT:
                    self.gpio[pin].mode = INPUT
                val = super().readRegister(XPOWERS_AXP192_GPIO34_CTL) & 0xFC
                super().writeRegister(XPOWERS_AXP192_GPIO34_CTL, val | 0x82)

        elif pin == PMU_GPIO4:
            '''
            * 00: External charging control
            * 01: NMOS open-drain output port 4
            * 10: Universal input port 4
            * 11: undefined
            '''
            if mode == INPUT:
                if self.gpio[pin].mode != INPUT:
                    self.gpio[pin].mode = INPUT
                val = super().readRegister(XPOWERS_AXP192_GPIO34_CTL) & 0xF3
                super().writeRegister(XPOWERS_AXP192_GPIO34_CTL, val | 0x88)

        elif pin == PMU_GPIO5:
            if mode == INPUT:
                if self.gpio[pin].mode != INPUT:
                    self.gpio[pin].mode = INPUT

                val = super().readRegister(XPOWERS_AXP192_GPIO5_CTL) & 0xBF
                super().writeRegister(XPOWERS_AXP192_GPIO5_CTL, val | 0x40)
        else:
            print('gpio is invalid')

    def digitalRead(self, pin: int) -> bool:
        if pin == PMU_GPIO0:
            return bool(super().getRegisterBit(XPOWERS_AXP192_GPIO012_SIGNAL, 4))
        elif pin == PMU_GPIO1:
            return bool(super().getRegisterBit(XPOWERS_AXP192_GPIO012_SIGNAL, 5))
        elif pin == PMU_GPIO2:
            return bool(super().getRegisterBit(XPOWERS_AXP192_GPIO012_SIGNAL, 6))
        elif pin == PMU_GPIO3:
            return bool(super().getRegisterBit(XPOWERS_AXP192_GPIO34_SIGNAL, 4))
        elif pin == PMU_GPIO4:
            return bool(super().getRegisterBit(XPOWERS_AXP192_GPIO34_SIGNAL, 5))
        elif pin == PMU_GPIO5:
            return bool(super().getRegisterBit(XPOWERS_AXP192_GPIO5_CTL, 4))
        else:
            print('gpio is invalid')
        return 0

    def digitalWrite(self, pin: int, val: int):
        if pin == PMU_GPIO0:
            if self.gpio[pin].mode != OUTPUT:
                self.gpio[pin].mode = OUTPUT
            reg = super().readRegister(XPOWERS_AXP192_GPIO0_CTL) & 0xF8
            val = (reg,(reg | 0x05))[val]
            print(bin(val))
            super().writeRegister(XPOWERS_AXP192_GPIO0_CTL,  val)

        elif pin == PMU_GPIO1:
            if self.gpio[pin].mode != OUTPUT:
                self.gpio[pin].mode = OUTPUT
            reg = super().readRegister(XPOWERS_AXP192_GPIO1_CTL) & 0xF8
            val = (reg,(reg | 0x05))[val]
            super().writeRegister(XPOWERS_AXP192_GPIO1_CTL,  val)

        elif pin == PMU_GPIO2:
            if self.gpio[pin].mode != OUTPUT:
                self.gpio[pin].mode = OUTPUT
            reg = super().readRegister(XPOWERS_AXP192_GPIO2_CTL) & 0xF8
            val = (reg,(reg | 0x05))[val]
            super().writeRegister(XPOWERS_AXP192_GPIO2_CTL,  val)

        elif pin == PMU_GPIO3:
            if self.gpio[pin].mode != OUTPUT:
                self.gpio[pin].mode = OUTPUT
                reg = super().readRegister(XPOWERS_AXP192_GPIO34_CTL) & 0xFC
                super().writeRegister(XPOWERS_AXP192_GPIO34_CTL,   reg | 0x01)

            reg = super().readRegister(XPOWERS_AXP192_GPIO34_SIGNAL) & 0xF7
            val = (reg,(reg | 0x01))[val]
            super().writeRegister(XPOWERS_AXP192_GPIO34_SIGNAL,   val)

        elif pin == PMU_GPIO4:
            if self.gpio[pin].mode != OUTPUT:
                self.gpio[pin].mode = OUTPUT
                reg = super().readRegister(XPOWERS_AXP192_GPIO34_CTL) & 0xF3
                super().writeRegister(XPOWERS_AXP192_GPIO34_CTL,  reg | 0x04)

            reg = super().readRegister(XPOWERS_AXP192_GPIO34_SIGNAL) & 0xEF
            val = (reg,(reg | 0x01))[val]
            super().writeRegister(XPOWERS_AXP192_GPIO34_SIGNAL,   val)

        elif pin == PMU_GPIO5:
            if self.gpio[pin].mode != OUTPUT:
                self.gpio[pin].mode = OUTPUT
                reg = super().readRegister(XPOWERS_AXP192_GPIO5_CTL) & 0xBF
                super().writeRegister(XPOWERS_AXP192_GPIO5_CTL,  reg)

            reg = super().readRegister(XPOWERS_AXP192_GPIO5_CTL) & 0xDF
            val = (reg,(reg | 0x01))[val]
            super().writeRegister(XPOWERS_AXP192_GPIO5_CTL, val)
        else:
            print('gpio is invalid')

    #  ! Need FIX
    def analogRead(self, pin: int) -> int:
        if pin == PMU_GPIO0:
            if self.gpio[pin].mode != ANALOG:
                #  Enable GPIO ADC Function
                val = super().readRegister(XPOWERS_AXP192_GPIO0_CTL) & 0xF8
                super().writeRegister(XPOWERS_AXP192_GPIO0_CTL, val | 0x04)

                # Enable ADC2 / GPIO0
                #  val = super().readRegister(XPOWERS_AXP192_ADC_EN2) | 0x08
                #  super().writeRegister(XPOWERS_AXP192_ADC_EN2, val )
                super().setRegisterBit(XPOWERS_AXP192_ADC_EN2, 3)

                #  Set adc input range 0~2.0475V
                super().clrRegisterBit(XPOWERS_AXP192_ADC_INPUTRANGE,0)
                self.gpio[pin].mode = ANALOG

            return super().readRegisterH8L4(XPOWERS_AXP192_GPIO0_VOL_ADC_H8, XPOWERS_AXP192_GPIO0_VOL_ADC_L4)

        elif pin == PMU_GPIO1:
            if self.gpio[pin].mode != ANALOG:
                #  Enable GPIO ADC Function
                val = super().readRegister(XPOWERS_AXP192_GPIO1_CTL) & 0xF8
                super().writeRegister(XPOWERS_AXP192_GPIO1_CTL, val | 0x04)

                # Enable ADC2 / GPIO1
                #  val = super().readRegister(XPOWERS_AXP192_ADC_EN2) | 0x04
                #  super().writeRegister(XPOWERS_AXP192_ADC_EN2, val )
                super().setRegisterBit(XPOWERS_AXP192_ADC_EN2, 2)

                #  Set adc input range 0~2.0475V
                super().clrRegisterBit(XPOWERS_AXP192_ADC_INPUTRANGE,1)
                self.gpio[pin].mode = ANALOG

            return super().readRegisterH8L4(XPOWERS_AXP192_GPIO1_VOL_ADC_H8, XPOWERS_AXP192_GPIO1_VOL_ADC_L4)

        elif pin == PMU_GPIO2:
            if self.gpio[pin].mode != ANALOG:
                #  Enable GPIO ADC Function
                val = super().readRegister(XPOWERS_AXP192_GPIO1_CTL) & 0xF8
                super().writeRegister(XPOWERS_AXP192_GPIO1_CTL, val | 0x04)
                # Enable ADC2 / GPIO1
                #  val = super().readRegister(XPOWERS_AXP192_ADC_EN2) | 0x02
                #  super().writeRegister(XPOWERS_AXP192_ADC_EN2, val )
                super().setRegisterBit(XPOWERS_AXP192_ADC_EN2, 1)

                #  Set adc input range 0~2.0475V
                super().clrRegisterBit(XPOWERS_AXP192_ADC_INPUTRANGE,2)
                self.gpio[pin].mode = ANALOG

            return super().readRegisterH8L4(XPOWERS_AXP192_GPIO2_VOL_ADC_H8, XPOWERS_AXP192_GPIO2_VOL_ADC_L4)

        elif pin == PMU_GPIO3:
            if self.gpio[pin].mode != ANALOG:
                #  Enable GPIO ADC Function
                val = super().readRegister(XPOWERS_AXP192_GPIO1_CTL) & 0xF8
                super().writeRegister(XPOWERS_AXP192_GPIO1_CTL, val | 0x04)

                # Enable ADC2 / GPIO1
                super().setRegisterBit(XPOWERS_AXP192_ADC_EN2, 0)

                #  Set adc input range 0~2.0475V
                super().clrRegisterBit(XPOWERS_AXP192_ADC_INPUTRANGE,3)
                self.gpio[pin].mode = ANALOG

            return super().readRegisterH8L4(XPOWERS_AXP192_GPIO3_VOL_ADC_H8, XPOWERS_AXP192_GPIO3_VOL_ADC_L4)

        elif pin == PMU_TS_PIN:
            if self.gpio[pin].mode != ANALOG:
                #  Enable TS PIN ADC Function
                super().setRegisterBit(XPOWERS_AXP192_ADC_SPEED, 2)
                #  val = super().readRegister(XPOWERS_AXP192_ADC_SPEED) & 0xFB
                #  super().writeRegister(XPOWERS_AXP192_ADC_SPEED, val | 0x04)
                self.gpio[pin].mode = ANALOG

            return super().readRegisterH8L4(XPOWERS_AXP192_TS_IN_H8, XPOWERS_AXP192_TS_IN_L4)
        else:
            print('gpio is invalid')

        return 0


    # Sleep function
    def enableSleep(self):
        super().setRegisterBit(XPOWERS_AXP192_VOFF_SET, 3)

    # Pekey function
    # @brief Set the PEKEY power-on long press time.
    # @param opt: See xpowers_press_on_time_t enum for details.
    def setPowerKeyPressOnTime(self, opt: int):
        val = super().readRegister(XPOWERS_AXP192_POK_SET)
        super().writeRegister(XPOWERS_AXP192_POK_SET, (val & 0x3F) | (opt << 6))

    # @brief Get the PEKEY power-on long press time.
    # @retval See xpowers_press_on_time_t enum for details.

    def getPowerKeyPressOnTime(self):
        val = super().readRegister(XPOWERS_AXP192_POK_SET)
        return (val & 0xC0) >> 6

    # @brief Set the PEKEY power-off long press time.
    # @ param opt: See xpowers_press_off_time_t enum for details.

    def setPowerKeyPressOffTime(self, opt: int):
        val = super().readRegister(XPOWERS_AXP192_POK_SET)
        super().writeRegister(XPOWERS_AXP192_POK_SET, (val & 0xFC) | opt)

    # @brief Get the PEKEY power-off long press time.
    # @retval See xpowers_press_off_time_t enum for details.
    def getPowerKeyPressOffTime(self) -> int:
        val = super().readRegister(XPOWERS_AXP192_POK_SET)
        return (val & 0x03)

    def setPowerKeyLongPressOnTime(self, opt: int):
        val = super().readRegister(XPOWERS_AXP192_POK_SET)
        super().writeRegister(XPOWERS_AXP192_POK_SET, (val & 0xCF) | (opt << 4))

    def enablePowerKeyLongPressPowerOff(self):
        super().setRegisterBit(XPOWERS_AXP192_POK_SET, 3)

    def disablePowerKeyLongPressPowerOff(self):
        super().clrRegisterBit(XPOWERS_AXP192_POK_SET, 3)

    # Interrupt control functions
    def setInterruptImpl(self, opts: int, enable: bool):
        # log_d("%s %s - 0x%llx\n", __func__, enable ? "ENABLE": "DISABLE", opts)
        if opts & 0xFF:
            value = opts & 0xFF
            data = super().readRegister(XPOWERS_AXP192_INTEN1)
            self.intRegister[0] =  ((data & (~value)),(data | value))[enable]
            super().writeRegister(XPOWERS_AXP192_INTEN1, self.intRegister[0])

        if opts & 0xFF00:
            value = opts >> 8
            data = super().readRegister(XPOWERS_AXP192_INTEN2)
            self.intRegister[1] =  ((data & (~value)),(data | value))[enable]
            super().writeRegister(XPOWERS_AXP192_INTEN2, self.intRegister[1])

        if opts & 0xFF0000:
            value = opts >> 16
            data = super().readRegister(XPOWERS_AXP192_INTEN3)
            self.intRegister[2] =  ((data & (~value)),(data | value))[enable]
            super().writeRegister(XPOWERS_AXP192_INTEN3, self.intRegister[2])

        if opts & 0xFF000000:
            value = opts >> 24
            data = super().readRegister(XPOWERS_AXP192_INTEN4)
            self.intRegister[3] =  ((data & (~value)),(data | value))[enable]
            super().writeRegister(XPOWERS_AXP192_INTEN4, self.intRegister[3])

        if opts & 0xFF00000000:
            value = opts >> 32
            data = super().readRegister(XPOWERS_AXP192_INTEN5)
            self.intRegister[4] =  ((data & (~value)),(data | value))[enable]
            super().writeRegister(XPOWERS_AXP192_INTEN5, self.intRegister[4])

    # Signal Capture control functions
    def setSignalCaptureImpl(self, opts: int,  enable: bool):
        if opts & 0xFF:
            value = super().readRegister(XPOWERS_AXP192_ADC_EN1)
            value = ((value & (~opts)),(value | opts))[enable]
            super().writeRegister(XPOWERS_AXP192_ADC_EN1, value)

        if opts & 0xFF00:
            opts >>= 8
            value = super().readRegister(XPOWERS_AXP192_ADC_EN2)
            value = ((value & (~opts)),(value | opts))[enable]
            super().writeRegister(XPOWERS_AXP192_ADC_EN2, value)
