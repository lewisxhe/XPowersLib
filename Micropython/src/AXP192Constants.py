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

@file      AXP192Constants.py
@author    Lewis He (lewishe@outlook.com)
@date      2022-10-20

'''

AXP192_SLAVE_ADDRESS                            = const(0x34)

XPOWERS_AXP192_CHIP_ID                          = const(0x03)

XPOWERS_AXP192_STATUS                           = const(0x00)
XPOWERS_AXP192_MODE_CHGSTATUS                   = const(0x01)
XPOWERS_AXP192_OTG_STATUS                       = const(0x02)
XPOWERS_AXP192_IC_TYPE                          = const(0x03)

XPOWERS_AXP192_DATA_BUFFER1                     = const(0x06)
XPOWERS_AXP192_DATA_BUFFER2                     = const(0x07)
XPOWERS_AXP192_DATA_BUFFER3                     = const(0x08)
XPOWERS_AXP192_DATA_BUFFER4                     = const(0x09)
XPOWERS_AXP192_DATA_BUFFER5                     = const(0x0A)
XPOWERS_AXP192_DATA_BUFFER6                     = const(0x0B)
XPOWERS_AXP192_DATA_BUFFER_SIZE                 = const(6)


XPOWERS_AXP192_LDO23_DC123_EXT_CTL              = const(0x12)
XPOWERS_AXP192_DC2OUT_VOL                       = const(0x23)
XPOWERS_AXP192_DC2_DVM                          = const(0x25)
XPOWERS_AXP192_DC3OUT_VOL                       = const(0x27)
XPOWERS_AXP192_LDO24OUT_VOL                     = const(0x28)
XPOWERS_AXP192_LDO3OUT_VOL                      = const(0x29)
XPOWERS_AXP192_IPS_SET                          = const(0x30)
XPOWERS_AXP192_VOFF_SET                         = const(0x31)
XPOWERS_AXP192_OFF_CTL                          = const(0x32)
XPOWERS_AXP192_CHARGE1                          = const(0x33)
XPOWERS_AXP192_CHARGE2                          = const(0x34)
XPOWERS_AXP192_BACKUP_CHG                       = const(0x35)
XPOWERS_AXP192_POK_SET                          = const(0x36)
XPOWERS_AXP192_DCDC_FREQSET                     = const(0x37)
XPOWERS_AXP192_VLTF_CHGSET                      = const(0x38)
XPOWERS_AXP192_VHTF_CHGSET                      = const(0x39)
XPOWERS_AXP192_APS_WARNING1                     = const(0x3A)
XPOWERS_AXP192_APS_WARNING2                     = const(0x3B)
XPOWERS_AXP192_TLTF_DISCHGSET                   = const(0x3C)
XPOWERS_AXP192_THTF_DISCHGSET                   = const(0x3D)
XPOWERS_AXP192_DCDC_MODESET                     = const(0x80)
XPOWERS_AXP192_ADC_EN1                          = const(0x82)
XPOWERS_AXP192_ADC_EN2                          = const(0x83)
XPOWERS_AXP192_ADC_SPEED                        = const(0x84)
XPOWERS_AXP192_ADC_INPUTRANGE                   = const(0x85)
XPOWERS_AXP192_ADC_IRQ_RETFSET                  = const(0x86)
XPOWERS_AXP192_ADC_IRQ_FETFSET                  = const(0x87)
XPOWERS_AXP192_TIMER_CTL                        = const(0x8A)
XPOWERS_AXP192_VBUS_DET_SRP                     = const(0x8B)
XPOWERS_AXP192_HOTOVER_CTL                      = const(0x8F)

XPOWERS_AXP192_PWM1_FREQ_SET                    = const(0x98)
XPOWERS_AXP192_PWM1_DUTY_SET1                   = const(0x99)
XPOWERS_AXP192_PWM1_DUTY_SET2                   = const(0x9A)

XPOWERS_AXP192_PWM2_FREQ_SET                    = const(0x9B)
XPOWERS_AXP192_PWM2_DUTY_SET1                   = const(0x9C)
XPOWERS_AXP192_PWM2_DUTY_SET2                   = const(0x9D)


# INTERRUPT REGISTER
XPOWERS_AXP192_INTEN1                           = const(0x40)
XPOWERS_AXP192_INTEN2                           = const(0x41)
XPOWERS_AXP192_INTEN3                           = const(0x42)
XPOWERS_AXP192_INTEN4                           = const(0x43)
XPOWERS_AXP192_INTEN5                           = const(0x4A)

# INTERRUPT STATUS REGISTER
XPOWERS_AXP192_INTSTS1                          = const(0x44)
XPOWERS_AXP192_INTSTS2                          = const(0x45)
XPOWERS_AXP192_INTSTS3                          = const(0x46)
XPOWERS_AXP192_INTSTS4                          = const(0x47)
XPOWERS_AXP192_INTSTS5                          = const(0x4D)
XPOWERS_AXP192_INTSTS_CNT                       = const(5)

XPOWERS_AXP192_DC1_VLOTAGE                      = const(0x26)
XPOWERS_AXP192_LDO23OUT_VOL                     = const(0x28)
XPOWERS_AXP192_GPIO0_CTL                        = const(0x90)
XPOWERS_AXP192_GPIO0_VOL                        = const(0x91)
XPOWERS_AXP192_GPIO1_CTL                        = const(0X92)
XPOWERS_AXP192_GPIO2_CTL                        = const(0x93)
XPOWERS_AXP192_GPIO012_SIGNAL                   = const(0x94)
XPOWERS_AXP192_GPIO34_CTL                       = const(0x95)
XPOWERS_AXP192_GPIO34_SIGNAL                    = const(0x96)
XPOWERS_AXP192_GPIO012_PULLDOWN                 = const(0x97)
XPOWERS_AXP192_GPIO5_CTL                        = const(0x9E)

XPOWERS_AXP192_GPIO0_VOL_ADC_H8                 = const(0x64)
XPOWERS_AXP192_GPIO0_VOL_ADC_L4                 = const(0x65)
XPOWERS_AXP192_GPIO1_VOL_ADC_H8                 = const(0x66)
XPOWERS_AXP192_GPIO1_VOL_ADC_L4                 = const(0x67)
XPOWERS_AXP192_GPIO2_VOL_ADC_H8                 = const(0x68)
XPOWERS_AXP192_GPIO2_VOL_ADC_L4                 = const(0x69)
XPOWERS_AXP192_GPIO3_VOL_ADC_H8                 = const(0x6A)
XPOWERS_AXP192_GPIO3_VOL_ADC_L4                 = const(0x6B)

XPOWERS_AXP192_GPIO0_STEP                       = const(0.5F)
XPOWERS_AXP192_GPIO1_STEP                       = const(0.5F)
XPOWERS_AXP192_TS_IN_H8                         = const(0x62)
XPOWERS_AXP192_TS_IN_L4                         = const(0x63)

XPOWERS_AXP192_BAT_AVERCHGCUR_H8                = const(0x7A)
XPOWERS_AXP192_BAT_AVERCHGCUR_L5                = const(0x7B)


XPOWERS_AXP192_ACIN_VOL_H8                      = const(0x56)
XPOWERS_AXP192_ACIN_VOL_L4                      = const(0x57)
XPOWERS_AXP192_ACIN_CUR_H8                      = const(0x58)
XPOWERS_AXP192_ACIN_CUR_L4                      = const(0x59)
XPOWERS_AXP192_VBUS_VOL_H8                      = const(0x5A)
XPOWERS_AXP192_VBUS_VOL_L4                      = const(0x5B)
XPOWERS_AXP192_VBUS_CUR_H8                      = const(0x5C)
XPOWERS_AXP192_VBUS_CUR_L4                      = const(0x5D)

XPOWERS_AXP192_BAT_AVERDISCHGCUR_H8             = const(0x7C)
XPOWERS_AXP192_BAT_AVERDISCHGCUR_L5             = const(0x7D)
XPOWERS_AXP192_APS_AVERVOL_H8                   = const(0x7E)
XPOWERS_AXP192_APS_AVERVOL_L4                   = const(0x7F)
XPOWERS_AXP192_BAT_AVERVOL_H8                   = const(0x78)
XPOWERS_AXP192_BAT_AVERVOL_L4                   = const(0x79)

XPOWERS_AXP192_BAT_CHGCOULOMB3                  = const(0xB0)
XPOWERS_AXP192_BAT_CHGCOULOMB2                  = const(0xB1)
XPOWERS_AXP192_BAT_CHGCOULOMB1                  = const(0xB2)
XPOWERS_AXP192_BAT_CHGCOULOMB0                  = const(0xB3)
XPOWERS_AXP192_BAT_DISCHGCOULOMB3               = const(0xB4)
XPOWERS_AXP192_BAT_DISCHGCOULOMB2               = const(0xB5)
XPOWERS_AXP192_BAT_DISCHGCOULOMB1               = const(0xB6)
XPOWERS_AXP192_BAT_DISCHGCOULOMB0               = const(0xB7)
XPOWERS_AXP192_COULOMB_CTL                      = const(0xB8)


XPOWERS_AXP192_BATT_VOLTAGE_STEP                = const(1.1F)
XPOWERS_AXP192_BATT_DISCHARGE_CUR_STEP          = const(0.5F)
XPOWERS_AXP192_BATT_CHARGE_CUR_STEP             = const(0.5F)
XPOWERS_AXP192_ACIN_VOLTAGE_STEP                = const(1.7F)
XPOWERS_AXP192_ACIN_CUR_STEP                    = const(0.625F)
XPOWERS_AXP192_VBUS_VOLTAGE_STEP                = const(1.7F)
XPOWERS_AXP192_VBUS_CUR_STEP                    = const(0.375F)
XPOWERS_AXP192_INTERNAL_TEMP_STEP               = const(0.1F)
XPOWERS_AXP192_APS_VOLTAGE_STEP                 = const(1.4F)
XPOWERS_AXP192_TS_PIN_OUT_STEP                  = const(0.8F)


XPOWERS_AXP192_LDO2_VOL_MIN                     = const(1800)
XPOWERS_AXP192_LDO2_VOL_MAX                     = const(3300)
XPOWERS_AXP192_LDO2_VOL_STEPS                   = const(100)
XPOWERS_AXP192_LDO2_VOL_BIT_MASK                = const(4)

XPOWERS_AXP192_LDO3_VOL_MIN                     = const(1800)
XPOWERS_AXP192_LDO3_VOL_MAX                     = const(3300)
XPOWERS_AXP192_LDO3_VOL_STEPS                   = const(100)


XPOWERS_AXP192_DC1_VOL_STEPS                    = const(25)
XPOWERS_AXP192_DC1_VOL_MIN                      = const(700)
XPOWERS_AXP192_DC1_VOL_MAX                      = const(3500)

XPOWERS_AXP192_DC2_VOL_STEPS                    = const(25)
XPOWERS_AXP192_DC2_VOL_MIN                      = const(700)
XPOWERS_AXP192_DC2_VOL_MAX                      = const(3500)

XPOWERS_AXP192_DC3_VOL_STEPS                    = const(25)
XPOWERS_AXP192_DC3_VOL_MIN                      = const(700)
XPOWERS_AXP192_DC3_VOL_MAX                      = const(3500)

XPOWERS_AXP192_LDOIO_VOL_STEPS                  = const(100)
XPOWERS_AXP192_LDOIO_VOL_MIN                    = const(1800)
XPOWERS_AXP192_LDOIO_VOL_MAX                    = const(3300)

XPOWERS_AXP192_SYS_VOL_STEPS                    = const(100)
XPOWERS_AXP192_VOFF_VOL_MIN                     = const(2600)
XPOWERS_AXP192_VOFF_VOL_MAX                     = const(3300)

XPOWERS_AXP192_CHG_EXT_CURR_MIN                 = const(300)
XPOWERS_AXP192_CHG_EXT_CURR_MAX                 = const(1000)
XPOWERS_AXP192_CHG_EXT_CURR_STEP                = const(100)


XPOWERS_AXP192_INTERNAL_TEMP_H8                 = const(0x5E)
XPOWERS_AXP192_INTERNAL_TEMP_L4                 = const(0x5F)
XPOWERS_AXP192_INTERNAL_TEMP_STEP               = const(0.1F)
XPOWERS_AXP192_INERNAL_TEMP_OFFSET              = const(144.7)


