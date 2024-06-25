/**
 * @file      BQ25896_Example.ino
 * @author    Lewis He (lewishe@outlook.com)
 * @license   MIT
 * @copyright Copyright (c) 2024  Shenzhen Xin Yuan Electronic Technology Co., Ltd
 * @date      2024-06-04
 *
 */
#include <XPowersLib.h>

PowersSY6970 PMU;


#ifndef CONFIG_PMU_SDA
#define CONFIG_PMU_SDA 0
#endif

#ifndef CONFIG_PMU_SCL
#define CONFIG_PMU_SCL 1
#endif

#ifndef CONFIG_PMU_IRQ
#define CONFIG_PMU_IRQ 28
#endif

const uint8_t i2c_sda = CONFIG_PMU_SDA;
const uint8_t i2c_scl = CONFIG_PMU_SCL;
const uint8_t pmu_irq_pin = CONFIG_PMU_IRQ;
uint32_t cycleInterval;
bool pmu_irq = false;

void setup()
{
    Serial.begin(115200);
    while (!Serial);


    bool result =  PMU.init(Wire, i2c_sda, i2c_scl, BQ25896_SLAVE_ADDRESS);

    if (result == false) {
        while (1) {
            Serial.println("PMU is not online...");
            delay(50);
        }
    }

    // Set the minimum operating voltage. Below this voltage, the PMU will protect
    PMU.setSysPowerDownVoltage(3300);

    // Set input current limit, default is 500mA
    PMU.setInputCurrentLimit(3250);

    Serial.printf("getInputCurrentLimit: %d mA\n", PMU.getInputCurrentLimit());

    // Disable current limit pin
    PMU.disableCurrentLimitPin();

    // Set the charging target voltage, Range:3840 ~ 4608mV ,step:16 mV
    PMU.setChargeTargetVoltage(4208);

    // Set the precharge current , Range: 64mA ~ 1024mA ,step:64mA
    PMU.setPrechargeCurr(64);

    // The premise is that Limit Pin is disabled, or it will only follow the maximum charging current set by Limi tPin.
    // Set the charging current , Range:0~5056mA ,step:64mA
    PMU.setChargerConstantCurr(1024);

    // Get the set charging current
    PMU.getChargerConstantCurr();
    Serial.printf("getChargerConstantCurr: %d mA\n", PMU.getChargerConstantCurr());


    // To obtain voltage data, the ADC must be enabled first
    PMU.enableADCMeasure();

    // Turn on charging function
    // If there is no battery connected, do not turn on the charging function
    PMU.enableCharge();

    // Turn off charging function
    // If USB is used as the only power input, it is best to turn off the charging function,
    // otherwise the VSYS power supply will have a sawtooth wave, affecting the discharge output capability.
    // PMU.disableCharge();


    // The OTG function needs to enable OTG, and set the OTG control pin to HIGH
    // After OTG is enabled, if an external power supply is plugged in, OTG will be turned off

    // PMU.enableOTG();
    // PMU.disableOTG();
    // pinMode(OTG_ENABLE_PIN, OUTPUT);
    // digitalWrite(OTG_ENABLE_PIN, HIGH);

    pinMode(pmu_irq_pin, INPUT_PULLUP);
    attachInterrupt(pmu_irq_pin, []() {
        pmu_irq = true;
    }, FALLING);

}


void loop()
{
    if (pmu_irq) {
        pmu_irq = false;

        // Get PMU interrupt status
        PMU.getIrqStatus();

        Serial.print("-> [");
        Serial.print(millis() / 1000);
        Serial.print("] ");

        if (PMU.isWatchdogFault()) {

            Serial.println("Watchdog Fault");

        } else if (PMU.isBoostFault()) {

            Serial.println("Boost Fault");

        } else if (PMU.isChargeFault()) {

            Serial.println("Charge Fault");

        } else if (PMU.isBatteryFault()) {

            Serial.println("Batter Fault");

        } else if (PMU.isNTCFault()) {

            Serial.print("NTC Fault:");
            Serial.print(PMU.getNTCStatusString());
            Serial.print(" Percentage:");
            Serial.print(PMU.getNTCPercentage()); Serial.println("%");
        }
        // The battery may be disconnected or damaged.
        else if (PMU.isVsysLowVoltageWarning()) {

            Serial.println("In VSYSMIN regulation (BAT<VSYSMIN)");

        } else {
            /*
            * When the battery is removed, INT will send an interrupt every 100ms. If the battery is not connected,
            * you can use PMU.disableCharge() to turn off the charging function.
            * */
            // PMU.disableCharge();

            Serial.println("Battery remove");
        }
    }

    /*
    * Obtaining the battery voltage and battery charging status does not directly read the register, 
    * but determines whether the charging current register is normal. 
    * If read directly, the reading will be inaccurate.
    * The premise for obtaining these two states is that the NTC temperature measurement circuit is normal.
    * If the NTC detection is abnormal, it will return 0
    * * */
    if (millis() > cycleInterval) {
        Serial.printf("CHG TARGET VOLTAGE :%04dmV CURRENT:%04dmA PER_CHARGE_CUR %04dmA\n",
                      PMU.getChargeTargetVoltage(), PMU.getChargerConstantCurr(), PMU.getPrechargeCurr());
        Serial.printf("VBUS:%s %04dmV VBAT:%04dmV VSYS:%04dmV\n", PMU.isVbusIn() ? "Connected" : "Disconnect",
                      PMU.getVbusVoltage(),
                      PMU.getBattVoltage(),
                      PMU.getSystemVoltage());
        Serial.printf("BUS STATE:%d STR:%s\n", PMU.getBusStatus(), PMU.getBusStatusString());
        Serial.printf("CHG STATE:%d STR:%s CURRENT:%04dmA\n", PMU.chargeStatus(), PMU.getChargeStatusString(), PMU.getChargeCurrent());
        Serial.printf("[%lu]", millis() / 1000);
        Serial.println("----------------------------------------------------------------------------------");
        cycleInterval = millis() + 1000;
    }

}





