/*
MIT License

Copyright (c) 2026 lewis he

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
*/

/*
! WARN:
Please do not run the example without knowing the external load voltage of the PMU,
it may burn your external load, please check the voltage setting before running the example,
if there is any loss, please bear it by yourself
*/
#ifndef XPOWERS_NO_ERROR
#error "Running this example is known to not damage the device! Please go and uncomment this!"
#endif

// Defined using AXP2102
#define XPOWERS_CHIP_AXP2101

#include <Wire.h>
#include <Arduino.h>
#include "XPowersLib.h"

#ifndef CONFIG_PMU_SDA
#define CONFIG_PMU_SDA 21
#endif

#ifndef CONFIG_PMU_SCL
#define CONFIG_PMU_SCL 22
#endif

#ifndef CONFIG_PMU_IRQ
#define CONFIG_PMU_IRQ 35
#endif

bool  pmu_flag = 0;
XPowersPMU power;

const uint8_t i2c_sda = CONFIG_PMU_SDA;
const uint8_t i2c_scl = CONFIG_PMU_SCL;
const uint8_t pmu_irq_pin = CONFIG_PMU_IRQ;

void setFlag(void)
{
    pmu_flag = true;
}


void setup()
{
    Serial.begin(115200);

    bool result = power.begin(Wire, AXP2101_SLAVE_ADDRESS, i2c_sda, i2c_scl);

    if (result == false) {
        Serial.println("power is not online...");
        while (1)delay(50);
    }

    Serial.printf("getID:0x%x\n", power.getChipID());

    Serial.println("DCDC=======================================================================");
    Serial.printf("DC1  : %s   Voltage:%u mV \n",  power.isEnableDC1()  ? "+" : "-", power.getDC1Voltage());
    Serial.printf("DC2  : %s   Voltage:%u mV \n",  power.isEnableDC2()  ? "+" : "-", power.getDC2Voltage());
    Serial.printf("DC3  : %s   Voltage:%u mV \n",  power.isEnableDC3()  ? "+" : "-", power.getDC3Voltage());
    Serial.printf("DC4  : %s   Voltage:%u mV \n",  power.isEnableDC4()  ? "+" : "-", power.getDC4Voltage());
    Serial.printf("DC5  : %s   Voltage:%u mV \n",  power.isEnableDC5()  ? "+" : "-", power.getDC5Voltage());
    Serial.println("ALDO=======================================================================");
    Serial.printf("ALDO1: %s   Voltage:%u mV\n",  power.isEnableALDO1()  ? "+" : "-", power.getALDO1Voltage());
    Serial.printf("ALDO2: %s   Voltage:%u mV\n",  power.isEnableALDO2()  ? "+" : "-", power.getALDO2Voltage());
    Serial.printf("ALDO3: %s   Voltage:%u mV\n",  power.isEnableALDO3()  ? "+" : "-", power.getALDO3Voltage());
    Serial.printf("ALDO4: %s   Voltage:%u mV\n",  power.isEnableALDO4()  ? "+" : "-", power.getALDO4Voltage());
    Serial.println("BLDO=======================================================================");
    Serial.printf("BLDO1: %s   Voltage:%u mV\n",  power.isEnableBLDO1()  ? "+" : "-", power.getBLDO1Voltage());
    Serial.printf("BLDO2: %s   Voltage:%u mV\n",  power.isEnableBLDO2()  ? "+" : "-", power.getBLDO2Voltage());
    Serial.println("CPUSLDO====================================================================");
    Serial.printf("CPUSLDO: %s Voltage:%u mV\n",  power.isEnableCPUSLDO() ? "+" : "-", power.getCPUSLDOVoltage());
    Serial.println("DLDO=======================================================================");
    Serial.printf("DLDO1: %s   Voltage:%u mV\n",  power.isEnableDLDO1()  ? "+" : "-", power.getDLDO1Voltage());
    Serial.printf("DLDO2: %s   Voltage:%u mV\n",  power.isEnableDLDO2()  ? "+" : "-", power.getDLDO2Voltage());
    Serial.println("===========================================================================");



    /*
      The default setting is CHGLED is automatically controlled by the PMU.
    - XPOWERS_CHG_LED_OFF,
    - XPOWERS_CHG_LED_BLINK_1HZ,
    - XPOWERS_CHG_LED_BLINK_4HZ,
    - XPOWERS_CHG_LED_ON,
    - XPOWERS_CHG_LED_CTRL_CHG,
    * */
    power.setChargingLedMode(XPOWERS_CHG_LED_ON);


    // Force add pull-up
    pinMode(pmu_irq_pin, INPUT_PULLUP);
    attachInterrupt(pmu_irq_pin, setFlag, FALLING);


    // Disable all interrupts
    power.disableIRQ(XPOWERS_AXP2101_ALL_IRQ);
    // Clear all interrupt flags
    power.clearIrqStatus();
    // Enable the required interrupt function
    power.enableIRQ(
        XPOWERS_AXP2101_PKEY_SHORT_IRQ    | XPOWERS_AXP2101_PKEY_LONG_IRQ  //POWER KEY
    );

}


void loop()
{

    if (pmu_flag) {

        pmu_flag = false;

        // Get PMU Interrupt Status Register
        uint32_t status = power.getIrqStatus();
        Serial.print("STATUS => HEX:");
        Serial.print(status, HEX);
        Serial.print(" BIN:");
        Serial.println(status, BIN);

        if (power.isPekeyLongPressIrq()) {
            Serial.println("BATTERY FET DISABLED");

            // Disable internal ADC detection
            power.disableTemperatureMeasure();
            power.disableBattDetection();
            power.disableVbusVoltageMeasure();
            power.disableBattVoltageMeasure();
            power.disableSystemVoltageMeasure();

            // Significantly reduce shutdown current
            power.disableBATFET();

            power.shutdown();
        }
        // Clear PMU Interrupt Status Register
        power.clearIrqStatus();

    }
    delay(10);
}

