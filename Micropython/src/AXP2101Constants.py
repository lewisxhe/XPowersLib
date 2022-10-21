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

@file      AXP2101Constants.py
@author    Lewis He (lewishe@outlook.com)
@date      2022-10-20

'''

AXP2101_SLAVE_ADDRESS                            = const(0x34)

XPOWERS_AXP2101_CHIP_ID                          = const(0x4A)

XPOWERS_AXP2101_STATUS1                          = const(0x00)
XPOWERS_AXP2101_STATUS2                          = const(0x01)
XPOWERS_AXP2101_IC_TYPE                          = const(0x03)


XPOWERS_AXP2101_DATA_BUFFER1                     = const(0x04)
XPOWERS_AXP2101_DATA_BUFFER2                     = const(0x05)
XPOWERS_AXP2101_DATA_BUFFER3                     = const(0x06)
XPOWERS_AXP2101_DATA_BUFFER4                     = const(0x07)
XPOWERS_AXP2101_DATA_BUFFER_SIZE                 = const(4)

XPOWERS_AXP2101_COMMON_CONFIG                    = const(0x10)
XPOWERS_AXP2101_BATFET_CTRL                      = const(0x12)
XPOWERS_AXP2101_DIE_TEMP_CTRL                    = const(0x13)
XPOWERS_AXP2101_MIN_SYS_VOL_CTRL                 = const(0x14)
XPOWERS_AXP2101_INPUT_VOL_LIMIT_CTRL             = const(0x15)
XPOWERS_AXP2101_INPUT_CUR_LIMIT_CTRL             = const(0x16)
XPOWERS_AXP2101_RESET_FUEL_GAUGE                 = const(0x17)
XPOWERS_AXP2101_CHARGE_GAUGE_WDT_CTRL            = const(0x18)


XPOWERS_AXP2101_WDT_CTRL                         = const(0x19)
XPOWERS_AXP2101_LOW_BAT_WARN_SET                 = const(0x1A)


XPOWERS_AXP2101_PWRON_STATUS                     = const(0x20)
XPOWERS_AXP2101_PWROFF_STATUS                    = const(0x21)
XPOWERS_AXP2101_PWROFF_EN                        = const(0x22)
XPOWERS_AXP2101_DC_OVP_UVP_CTRL                  = const(0x23)
XPOWERS_AXP2101_VOFF_SET                         = const(0x24)
XPOWERS_AXP2101_PWROK_SEQU_CTRL                  = const(0x25)
XPOWERS_AXP2101_SLEEP_WAKEUP_CTRL                = const(0x26)
XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL            = const(0x27)

XPOWERS_AXP2101_FAST_PWRON_SET0                  = const(0x28)
XPOWERS_AXP2101_FAST_PWRON_SET1                  = const(0x29)
XPOWERS_AXP2101_FAST_PWRON_SET2                  = const(0x2A)
XPOWERS_AXP2101_FAST_PWRON_CTRL                  = const(0x2B)

XPOWERS_AXP2101_ADC_CHANNEL_CTRL                 = const(0x30)
XPOWERS_AXP2101_ADC_DATA_RELUST0                 = const(0x34)
XPOWERS_AXP2101_ADC_DATA_RELUST1                 = const(0x35)
XPOWERS_AXP2101_ADC_DATA_RELUST2                 = const(0x36)
XPOWERS_AXP2101_ADC_DATA_RELUST3                 = const(0x37)
XPOWERS_AXP2101_ADC_DATA_RELUST4                 = const(0x38)
XPOWERS_AXP2101_ADC_DATA_RELUST5                 = const(0x39)
XPOWERS_AXP2101_ADC_DATA_RELUST6                 = const(0x3A)
XPOWERS_AXP2101_ADC_DATA_RELUST7                 = const(0x3B)
XPOWERS_AXP2101_ADC_DATA_RELUST8                 = const(0x3C)
XPOWERS_AXP2101_ADC_DATA_RELUST9                 = const(0x3D)


#XPOWERS INTERRUPT REGISTER
XPOWERS_AXP2101_INTEN1                           = const(0x40)
XPOWERS_AXP2101_INTEN2                           = const(0x41)
XPOWERS_AXP2101_INTEN3                           = const(0x42)


#XPOWERS INTERRUPT STATUS REGISTER
XPOWERS_AXP2101_INTSTS1                          = const(0x48)
XPOWERS_AXP2101_INTSTS2                          = const(0x49)
XPOWERS_AXP2101_INTSTS3                          = const(0x4A)
XPOWERS_AXP2101_INTSTS_CNT                       = const(3)

XPOWERS_AXP2101_TS_PIN_CTRL                      = const(0x50)
XPOWERS_AXP2101_TS_HYSL2H_SET                    = const(0x52)
XPOWERS_AXP2101_TS_LYSL2H_SET                    = const(0x53)


XPOWERS_AXP2101_VLTF_CHG_SET                     = const(0x54)
XPOWERS_AXP2101_VHLTF_CHG_SET                    = const(0x55)
XPOWERS_AXP2101_VLTF_WORK_SET                    = const(0x56)
XPOWERS_AXP2101_VHLTF_WORK_SET                   = const(0x57)


XPOWERS_AXP2101_JIETA_EN_CTRL                    = const(0x58)
XPOWERS_AXP2101_JIETA_SET0                       = const(0x59)
XPOWERS_AXP2101_JIETA_SET1                       = const(0x5A)
XPOWERS_AXP2101_JIETA_SET2                       = const(0x5B)


XPOWERS_AXP2101_IPRECHG_SET                      = const(0x61)
XPOWERS_AXP2101_ICC_CHG_SET                      = const(0x62)
XPOWERS_AXP2101_ITERM_CHG_SET_CTRL               = const(0x63)

XPOWERS_AXP2101_CV_CHG_VOL_SET                   = const(0x64)

XPOWERS_AXP2101_THE_REGU_THRES_SET               = const(0x65)
XPOWERS_AXP2101_CHG_TIMEOUT_SET_CTRL             = const(0x67)

XPOWERS_AXP2101_BAT_DET_CTRL                     = const(0x68)
XPOWERS_AXP2101_CHGLED_SET_CTRL                  = const(0x69)

XPOWERS_AXP2101_BTN_VOL_MIN                      = const(2600)
XPOWERS_AXP2101_BTN_VOL_MAX                      = const(3300)
XPOWERS_AXP2101_BTN_VOL_STEPS                    = const(100)


XPOWERS_AXP2101_BTN_BAT_CHG_VOL_SET              = const(0x6A)


XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL                = const(0x80)
XPOWERS_AXP2101_DC_FORCE_PWM_CTRL                = const(0x81)
XPOWERS_AXP2101_DC_VOL0_CTRL                     = const(0x82)
XPOWERS_AXP2101_DC_VOL1_CTRL                     = const(0x83)
XPOWERS_AXP2101_DC_VOL2_CTRL                     = const(0x84)
XPOWERS_AXP2101_DC_VOL3_CTRL                     = const(0x85)
XPOWERS_AXP2101_DC_VOL4_CTRL                     = const(0x86)


XPOWERS_AXP2101_LDO_ONOFF_CTRL0                  = const(0x90)
XPOWERS_AXP2101_LDO_ONOFF_CTRL1                  = const(0x91)
XPOWERS_AXP2101_LDO_VOL0_CTRL                    = const(0x92)
XPOWERS_AXP2101_LDO_VOL1_CTRL                    = const(0x93)
XPOWERS_AXP2101_LDO_VOL2_CTRL                    = const(0x94)
XPOWERS_AXP2101_LDO_VOL3_CTRL                    = const(0x95)
XPOWERS_AXP2101_LDO_VOL4_CTRL                    = const(0x96)
XPOWERS_AXP2101_LDO_VOL5_CTRL                    = const(0x97)
XPOWERS_AXP2101_LDO_VOL6_CTRL                    = const(0x98)
XPOWERS_AXP2101_LDO_VOL7_CTRL                    = const(0x99)
XPOWERS_AXP2101_LDO_VOL8_CTRL                    = const(0x9A)


XPOWERS_AXP2101_BAT_PARAME                       = const(0xA1)
XPOWERS_AXP2101_FUEL_GAUGE_CTRL                  = const(0xA2)
XPOWERS_AXP2101_BAT_PERCENT_DATA                 = const(0xA4)

# DCDC 1~5
XPOWERS_AXP2101_DCDC1_VOL_MIN                    = const(1500)
XPOWERS_AXP2101_DCDC1_VOL_MAX                    = const(3400)
XPOWERS_AXP2101_DCDC1_VOL_STEPS                  = const(100)

XPOWERS_AXP2101_DCDC2_VOL1_MIN                  = const(500)
XPOWERS_AXP2101_DCDC2_VOL1_MAX                  = const(1200)
XPOWERS_AXP2101_DCDC2_VOL2_MIN                  = const(1220)
XPOWERS_AXP2101_DCDC2_VOL2_MAX                  = const(1540)

XPOWERS_AXP2101_DCDC2_VOL_STEPS1                 = const(10)
XPOWERS_AXP2101_DCDC2_VOL_STEPS2                 = const(20)

XPOWERS_AXP2101_DCDC2_VOL_STEPS1_BASE            = const(0)
XPOWERS_AXP2101_DCDC2_VOL_STEPS2_BASE            = const(71)


XPOWERS_AXP2101_DCDC3_VOL1_MIN                  = const(500)
XPOWERS_AXP2101_DCDC3_VOL1_MAX                  = const(1200)
XPOWERS_AXP2101_DCDC3_VOL2_MIN                  = const(1220)
XPOWERS_AXP2101_DCDC3_VOL2_MAX                  = const(1540)
XPOWERS_AXP2101_DCDC3_VOL3_MIN                  = const(1600)
XPOWERS_AXP2101_DCDC3_VOL3_MAX                  = const(3400)

XPOWERS_AXP2101_DCDC3_VOL_MIN                    = const(500)
XPOWERS_AXP2101_DCDC3_VOL_MAX                    = const(3400)

XPOWERS_AXP2101_DCDC3_VOL_STEPS1                 = const(10)
XPOWERS_AXP2101_DCDC3_VOL_STEPS2                 = const(20)
XPOWERS_AXP2101_DCDC3_VOL_STEPS3                 = const(100)

XPOWERS_AXP2101_DCDC3_VOL_STEPS1_BASE            = const(0)
XPOWERS_AXP2101_DCDC3_VOL_STEPS2_BASE            = const(71)
XPOWERS_AXP2101_DCDC3_VOL_STEPS3_BASE            = const(88)



XPOWERS_AXP2101_DCDC4_VOL1_MIN                  = const(500)
XPOWERS_AXP2101_DCDC4_VOL1_MAX                  = const(1200)
XPOWERS_AXP2101_DCDC4_VOL2_MIN                  = const(1220)
XPOWERS_AXP2101_DCDC4_VOL2_MAX                  = const(1840)

XPOWERS_AXP2101_DCDC4_VOL_STEPS1                 = const(10)
XPOWERS_AXP2101_DCDC4_VOL_STEPS2                 = const(20)

XPOWERS_AXP2101_DCDC4_VOL_STEPS1_BASE            = const(0)
XPOWERS_AXP2101_DCDC4_VOL_STEPS2_BASE            = const(71)



XPOWERS_AXP2101_DCDC5_VOL_1200MV                 = const(1200)
XPOWERS_AXP2101_DCDC5_VOL_VAL                    = const(0x19)
XPOWERS_AXP2101_DCDC5_VOL_MIN                    = const(1400)
XPOWERS_AXP2101_DCDC5_VOL_MAX                    = const(3700)
XPOWERS_AXP2101_DCDC5_VOL_STEPS                  = const(100)

XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_MIN          = const(2600)
XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_MAX          = const(3300)
XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_STEPS        = const(100)

# ALDO 1~4

XPOWERS_AXP2101_ALDO1_VOL_MIN                    = const(500)
XPOWERS_AXP2101_ALDO1_VOL_MAX                    = const(3500)
XPOWERS_AXP2101_ALDO1_VOL_STEPS                  = const(100)

XPOWERS_AXP2101_ALDO2_VOL_MIN                    = const(500)
XPOWERS_AXP2101_ALDO2_VOL_MAX                    = const(3500)
XPOWERS_AXP2101_ALDO2_VOL_STEPS                  = const(100)


XPOWERS_AXP2101_ALDO3_VOL_MIN                    = const(500)
XPOWERS_AXP2101_ALDO3_VOL_MAX                    = const(3500)
XPOWERS_AXP2101_ALDO3_VOL_STEPS                  = const(100)


XPOWERS_AXP2101_ALDO4_VOL_MIN                    = const(500)
XPOWERS_AXP2101_ALDO4_VOL_MAX                    = const(3500)
XPOWERS_AXP2101_ALDO4_VOL_STEPS                  = const(100)

# BLDO 1~2

XPOWERS_AXP2101_BLDO1_VOL_MIN                    = const(500)
XPOWERS_AXP2101_BLDO1_VOL_MAX                    = const(3500)
XPOWERS_AXP2101_BLDO1_VOL_STEPS                  = const(100)

XPOWERS_AXP2101_BLDO2_VOL_MIN                    = const(500)
XPOWERS_AXP2101_BLDO2_VOL_MAX                    = const(3500)
XPOWERS_AXP2101_BLDO2_VOL_STEPS                  = const(100)

# CPUSLDO

XPOWERS_AXP2101_CPUSLDO_VOL_MIN                  = const(500)
XPOWERS_AXP2101_CPUSLDO_VOL_MAX                  = const(1400)
XPOWERS_AXP2101_CPUSLDO_VOL_STEPS                = const(50)


# DLDO 1~2
XPOWERS_AXP2101_DLDO1_VOL_MIN                  = const(500)
XPOWERS_AXP2101_DLDO1_VOL_MAX                  = const(3400)
XPOWERS_AXP2101_DLDO1_VOL_STEPS                = const(100)

XPOWERS_AXP2101_DLDO2_VOL_MIN                  = const(500)
XPOWERS_AXP2101_DLDO2_VOL_MAX                  = const(3400)
XPOWERS_AXP2101_DLDO2_VOL_STEPS                = const(100)



# ARGS ARGS ARGS ARGS ARGS ARGS ARGS ARGS ARGS

XPOWERS_AXP2101_IRQ_TIME_1S                    = const(0) 
XPOWERS_AXP2101_IRQ_TIME_1S5                   = const(1)     
XPOWERS_AXP2101_IRQ_TIME_2S                    = const(2) 
XPOWERS_AXP2101_PRESSOFF_2S5                   = const(3)     


XPOWERS_AXP2101_PRECHARGE_0MA                   = const(0)
XPOWERS_AXP2101_PRECHARGE_25MA                  = const(1)
XPOWERS_AXP2101_PRECHARGE_50MA                  = const(2)
XPOWERS_AXP2101_PRECHARGE_75MA                  = const(3)
XPOWERS_AXP2101_PRECHARGE_100MA                 = const(4)
XPOWERS_AXP2101_PRECHARGE_125MA                 = const(5)
XPOWERS_AXP2101_PRECHARGE_150MA                 = const(6)
XPOWERS_AXP2101_PRECHARGE_175MA                 = const(7)
XPOWERS_AXP2101_PRECHARGE_200MA                 = const(8)


XPOWERS_AXP2101_CHG_ITERM_0MA                   = const(0)
XPOWERS_AXP2101_CHG_ITERM_25MA                  = const(1)
XPOWERS_AXP2101_CHG_ITERM_50MA                  = const(2)
XPOWERS_AXP2101_CHG_ITERM_75MA                  = const(3)
XPOWERS_AXP2101_CHG_ITERM_100MA                 = const(4)
XPOWERS_AXP2101_CHG_ITERM_125MA                 = const(5)
XPOWERS_AXP2101_CHG_ITERM_150MA                 = const(6)
XPOWERS_AXP2101_CHG_ITERM_175MA                 = const(7)
XPOWERS_AXP2101_CHG_ITERM_200MA                 = const(8)



XPOWERS_AXP2101_THREMAL_60DEG                   = const(0)
XPOWERS_AXP2101_THREMAL_80DEG                   = const(1)
XPOWERS_AXP2101_THREMAL_100DEG                  = const(2)
XPOWERS_AXP2101_THREMAL_120DEG                  = const(3)


XPOWERS_AXP2101_CHG_TRI_STATE                   = const(0)  #tri_charge
XPOWERS_AXP2101_CHG_PRE_STATE                   = const(1)  #pre_charge
XPOWERS_AXP2101_CHG_CC_STATE                    = const(2)  #constant charge
XPOWERS_AXP2101_CHG_CV_STATE                    = const(3)  #constant voltage
XPOWERS_AXP2101_CHG_DONE_STATE                  = const(4)  #charge done
XPOWERS_AXP2101_CHG_STOP_STATE                  = const(5)  #not chargin


XPOWERS_AXP2101_WAKEUP_IRQ_PIN_TO_LOW           = const(1<<4)
XPOWERS_AXP2101_WAKEUP_PWROK_TO_LOW             = const(1<<3)
XPOWERS_AXP2101_WAKEUP_DC_DLO_SELECT            = const(1<<2)


XPOWERS_AXP2101_FAST_DCDC1                      = const(0)
XPOWERS_AXP2101_FAST_DCDC2                      = const(1)
XPOWERS_AXP2101_FAST_DCDC3                      = const(2)
XPOWERS_AXP2101_FAST_DCDC4                      = const(3)
XPOWERS_AXP2101_FAST_DCDC5                      = const(4)
XPOWERS_AXP2101_FAST_ALDO1                      = const(5)
XPOWERS_AXP2101_FAST_ALDO2                      = const(6)
XPOWERS_AXP2101_FAST_ALDO3                      = const(7)
XPOWERS_AXP2101_FAST_ALDO4                      = const(8)
XPOWERS_AXP2101_FAST_BLDO1                      = const(9)
XPOWERS_AXP2101_FAST_BLDO2                      = const(10)
XPOWERS_AXP2101_FAST_CPUSLDO                    = const(11)    
XPOWERS_AXP2101_FAST_DLDO1                      = const(12)
XPOWERS_AXP2101_FAST_DLDO2                      = const(13)



XPOWERS_AXP2101_SEQUENCE_LEVEL_0                = const(0)
XPOWERS_AXP2101_SEQUENCE_LEVEL_1                = const(1)
XPOWERS_AXP2101_SEQUENCE_LEVEL_2                = const(2)
XPOWERS_AXP2101_SEQUENCE_DISABLE                = const(3)


XPOWERS_AXP2101_WDT_IRQ_TO_PIN                  = const(0)#Just interrupt to pin
XPOWERS_AXP2101_WDT_IRQ_AND_RSET                = const(1)#IRQ to pin and reset pmu system
XPOWERS_AXP2101_WDT_IRQ_AND_RSET_PD_PWROK       = const(2)#IRQ to pin and reset pmu systempull down pwrok
XPOWERS_AXP2101_WDT_IRQ_AND_RSET_ALL_OFF        = const(3)#IRQ to pin and reset pmu systemturn off dcdc & ldo pull down pwrok


XPOWERS_AXP2101_WDT_TIMEOUT_1S                  = const(0)
XPOWERS_AXP2101_WDT_TIMEOUT_2S                  = const(1)
XPOWERS_AXP2101_WDT_TIMEOUT_4S                  = const(2)
XPOWERS_AXP2101_WDT_TIMEOUT_8S                  = const(3)
XPOWERS_AXP2101_WDT_TIMEOUT_16S                 = const(4)
XPOWERS_AXP2101_WDT_TIMEOUT_32S                 = const(5)
XPOWERS_AXP2101_WDT_TIMEOUT_64S                 = const(6)
XPOWERS_AXP2101_WDT_TIMEOUT_128S                = const(7)    




XPOWERS_AXP2101_VBUS_VOL_LIM_3V88               = const(0)
XPOWERS_AXP2101_VBUS_VOL_LIM_3V96               = const(1)
XPOWERS_AXP2101_VBUS_VOL_LIM_4V04               = const(2)
XPOWERS_AXP2101_VBUS_VOL_LIM_4V12               = const(3)
XPOWERS_AXP2101_VBUS_VOL_LIM_4V20               = const(4)
XPOWERS_AXP2101_VBUS_VOL_LIM_4V28               = const(5)
XPOWERS_AXP2101_VBUS_VOL_LIM_4V36               = const(6)
XPOWERS_AXP2101_VBUS_VOL_LIM_4V44               = const(7)
XPOWERS_AXP2101_VBUS_VOL_LIM_4V52               = const(8)
XPOWERS_AXP2101_VBUS_VOL_LIM_4V60               = const(9)
XPOWERS_AXP2101_VBUS_VOL_LIM_4V68               = const(10)
XPOWERS_AXP2101_VBUS_VOL_LIM_4V76               = const(11)
XPOWERS_AXP2101_VBUS_VOL_LIM_4V84               = const(12)
XPOWERS_AXP2101_VBUS_VOL_LIM_4V92               = const(13)
XPOWERS_AXP2101_VBUS_VOL_LIM_5V                 = const(14)
XPOWERS_AXP2101_VBUS_VOL_LIM_5V08               = const(15)


XPOWERS_AXP2101_VSYS_VOL_4V1                    = const(0)
XPOWERS_AXP2101_VSYS_VOL_4V2                    = const(1)
XPOWERS_AXP2101_VSYS_VOL_4V3                    = const(2)
XPOWERS_AXP2101_VSYS_VOL_4V4                    = const(3)
XPOWERS_AXP2101_VSYS_VOL_4V5                    = const(4)
XPOWERS_AXP2101_VSYS_VOL_4V6                    = const(5)
XPOWERS_AXP2101_VSYS_VOL_4V7                    = const(6)
XPOWERS_AXP2101_VSYS_VOL_4V8                    = const(7)


XPOWER_POWERON_SRC_POWERON_LOW                  = const(0)                    #POWERON low for on level when POWERON Mode as POWERON Source
XPOWER_POWERON_SRC_IRQ_LOW                      = const(1)                    #IRQ PIN Pull-down as POWERON Source
XPOWER_POWERON_SRC_VBUS_INSERT                  = const(2)                    #Vbus Insert and Good as POWERON Source
XPOWER_POWERON_SRC_BAT_CHARGE                   = const(3)                    #Vbus Insert and Good as POWERON Source
XPOWER_POWERON_SRC_BAT_INSERT                   = const(4)                    #Battery Insert and Good as POWERON Source
XPOWER_POWERON_SRC_ENMODE                       = const(5)                    #POWERON always high when EN Mode as POWERON Source
XPOWER_POWERON_SRC_UNKONW                       = const(6)                    #Unkonw


XPOWER_POWEROFF_SRC_PWEKEY_PULLDOWN             = const(0)#POWERON Pull down for off level when POWERON Mode as POWEROFF Source
XPOWER_POWEROFF_SRC_SOFT_OFF                    = const(1)#Software configuration as POWEROFF Source
XPOWER_POWEROFF_SRC_PWEKEY_LOW                  = const(2)#POWERON always low when EN Mode as POWEROFF Source
XPOWER_POWEROFF_SRC_UNDER_VSYS                  = const(3)#Vsys Under Voltage as POWEROFF Source
XPOWER_POWEROFF_SRC_OVER_VBUS                   = const(4)#VBUS Over Voltage as POWEROFF Source
XPOWER_POWEROFF_SRC_UNDER_VOL                   = const(5)#DCDC Under Voltage as POWEROFF Source
XPOWER_POWEROFF_SRC_OVER_VOL                    = const(6)#DCDC Over Voltage as POWEROFF Source
XPOWER_POWEROFF_SRC_OVER_TEMP                   = const(7)#Die Over Temperature as POWEROFF Source
XPOWER_POWEROFF_SRC_UNKONW                      = const(8)#Unkonw


XPOWER_PWROK_DELAY_8MS                          = const(0)
XPOWER_PWROK_DELAY_16MS                         = const(1)
XPOWER_PWROK_DELAY_32MS                         = const(2)
XPOWER_PWROK_DELAY_64MS                         = const(3)


XPOWERS_POWEROFF_4S                             = const(0)        
XPOWERS_POWEROFF_6S                             = const(1)        
XPOWERS_POWEROFF_8S                             = const(2)        
XPOWERS_POWEROFF_10S                            = const(3)         


XPOWERS_POWERON_128MS                           = const(0)            
XPOWERS_POWERON_512MS                           = const(1)            
XPOWERS_POWERON_1S                              = const(2)        
XPOWERS_POWERON_2S                              = const(3)        


POWERS_CHG_LED_OFF                              = const(0)     
POWERS_CHG_LED_BLINK_1HZ                        = const(1)             
POWERS_CHG_LED_BLINK_4HZ                        = const(2)             
POWERS_CHG_LED_ON                               = const(3)     
POWERS_CHG_LED_CTRL_CHG                         = const(4)         

XPOWERS_AXP2101_CHG_VOL_4V                      = const(1)   
XPOWERS_AXP2101_CHG_VOL_4V1                     = const(2)   
XPOWERS_AXP2101_CHG_VOL_4V2                     = const(3)   
XPOWERS_AXP2101_CHG_VOL_4V35                    = const(4)       
XPOWERS_AXP2101_CHG_VOL_4V4                     = const(5)   
XPOWERS_AXP2101_CHG_VOL_MAX                     = const(6)   
# @brief axp2101 charge currnet voltage parameters.
XPOWERS_AXP2101_CHG_CUR_0MA                     = const(0)    
XPOWERS_AXP2101_CHG_CUR_100MA                   = const(4)            
XPOWERS_AXP2101_CHG_CUR_125MA                   = const(5)        
XPOWERS_AXP2101_CHG_CUR_150MA                   = const(6)        
XPOWERS_AXP2101_CHG_CUR_175MA                   = const(7)        
XPOWERS_AXP2101_CHG_CUR_200MA                   = const(8)        
XPOWERS_AXP2101_CHG_CUR_300MA                   = const(9)        
XPOWERS_AXP2101_CHG_CUR_400MA                   = const(10)        
XPOWERS_AXP2101_CHG_CUR_500MA                   = const(11)        
XPOWERS_AXP2101_CHG_CUR_600MA                   = const(12)        
XPOWERS_AXP2101_CHG_CUR_700MA                   = const(13)        
XPOWERS_AXP2101_CHG_CUR_800MA                   = const(14)        
XPOWERS_AXP2101_CHG_CUR_900MA                   = const(15)        
XPOWERS_AXP2101_CHG_CUR_1000MA                  = const(16)        

# @brief axp2101 vbus currnet limit parameters.
XPOWERS_AXP2101_VBUS_CUR_LIM_100MA      = const(0)
XPOWERS_AXP2101_VBUS_CUR_LIM_500MA      = const(1)
XPOWERS_AXP2101_VBUS_CUR_LIM_900MA      = const(2)
XPOWERS_AXP2101_VBUS_CUR_LIM_1000MA     = const(3)
XPOWERS_AXP2101_VBUS_CUR_LIM_1500MA     = const(4)
XPOWERS_AXP2101_VBUS_CUR_LIM_2000MA     = const(5)

# @brief axp2101 interrupt control mask parameters.

#! IRQ1 REG 40H
XPOWERS_AXP2101_BAT_NOR_UNDER_TEMP_IRQ   = const(1<<0)   # Battery Under Temperature in Work
XPOWERS_AXP2101_BAT_NOR_OVER_TEMP_IRQ    = const(1<<1)   # Battery Over Temperature in Work mode
XPOWERS_AXP2101_BAT_CHG_UNDER_TEMP_IRQ   = const(1<<2)   # Battery Under Temperature in Charge mode IRQ(bcut_irq)
XPOWERS_AXP2101_BAT_CHG_OVER_TEMP_IRQ    = const(1<<3)   # Battery Over Temperature in Charge mode IRQ(bcot_irq) enable
XPOWERS_AXP2101_GAUGE_NEW_SOC_IRQ        = const(1<<4)   # Gauge New SOC IRQ(lowsoc_irq) enable ???
XPOWERS_AXP2101_WDT_TIMEOUT_IRQ          = const(1<<5)   # Gauge Watchdog Timeout IRQ(gwdt_irq) enable
XPOWERS_AXP2101_WARNING_LEVEL1_IRQ       = const(1<<6)   # SOC drop to Warning Level1 IRQ(socwl1_irq) enable
XPOWERS_AXP2101_WARNING_LEVEL2_IRQ       = const(1<<7)   # SOC drop to Warning Level2 IRQ(socwl2_irq) enable

#! IRQ2 REG 41H
XPOWERS_AXP2101_PKEY_POSITIVE_IRQ        = const(1<<8)   # POWERON Positive Edge IRQ(ponpe_irq_en) enable
XPOWERS_AXP2101_PKEY_NEGATIVE_IRQ        = const(1<<9)   # POWERON Negative Edge IRQ(ponne_irq_en) enable
XPOWERS_AXP2101_PKEY_LONG_IRQ            = const(1<<10)  # POWERON Long PRESS IRQ(ponlp_irq) enable
XPOWERS_AXP2101_PKEY_SHORT_IRQ           = const(1<<11)  # POWERON Short PRESS IRQ(ponsp_irq_en) enable
XPOWERS_AXP2101_BAT_REMOVE_IRQ           = const(1<<12)  # Battery Remove IRQ(bremove_irq) enable
XPOWERS_AXP2101_BAT_INSERT_IRQ           = const(1<<13)  # Battery Insert IRQ(binsert_irq) enabl
XPOWERS_AXP2101_VBUS_REMOVE_IRQ          = const(1<<14)  # VBUS Remove IRQ(vremove_irq) enabl
XPOWERS_AXP2101_VBUS_INSERT_IRQ          = const(1<<15)  # VBUS Insert IRQ(vinsert_irq) enable

#! IRQ3 REG 42H
XPOWERS_AXP2101_BAT_OVER_VOL_IRQ         = const(1<<16)  # Battery Over Voltage Protection IRQ(bovp_irq) enable
XPOWERS_AXP2101_CHAGER_TIMER_IRQ         = const(1<<17)  # Charger Safety Timer1/2 expire IRQ(chgte_irq) enable
XPOWERS_AXP2101_DIE_OVER_TEMP_IRQ        = const(1<<18)  # DIE Over Temperature level1 IRQ(dotl1_irq) enable
XPOWERS_AXP2101_BAT_CHG_START_IRQ        = const(1<<19)  # Charger start IRQ(chgst_irq) enable
XPOWERS_AXP2101_BAT_CHG_DONE_IRQ         = const(1<<20)  # Battery charge done IRQ(chgdn_irq) enable
XPOWERS_AXP2101_BATFET_OVER_CURR_IRQ     = const(1<<21)  # BATFET Over Current Protection IRQ(bocp_irq) enable
XPOWERS_AXP2101_LDO_OVER_CURR_IRQ        = const(1<<22)  # LDO Over Current IRQ(ldooc_irq) enable
XPOWERS_AXP2101_WDT_EXPIRE_IRQ           = const(1<<23)  # Watchdog Expire IRQ(wdexp_irq) enable

XPOWERS_AXP2101_ALL_IRQ                  = const(0xFFFFFFFF)


XPOWERS_CHG_LED_OFF                     = const(0)
XPOWERS_CHG_LED_BLINK_1HZ               = const(1)
XPOWERS_CHG_LED_BLINK_4HZ               = const(2)
XPOWERS_CHG_LED_ON                      = const(3)
XPOWERS_CHG_LED_CTRL_CHG                = const(4)
