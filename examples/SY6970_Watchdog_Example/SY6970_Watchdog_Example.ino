/**
 * @file      SY6970_Watchdog_Example.ino
 * @author    Lewis He (lewishe@outlook.com)
 * @license   MIT
 * @copyright Copyright (c) 2023  Shenzhen Xin Yuan Electronic Technology Co., Ltd
 * @date      2023-08-31
 *
 */
#include <XPowersLib.h>

XPowersPPM PPM;


#ifndef CONFIG_PMU_SDA
#define CONFIG_PMU_SDA 15
#endif

#ifndef CONFIG_PMU_SCL
#define CONFIG_PMU_SCL 10
#endif

#ifndef CONFIG_PMU_IRQ
#define CONFIG_PMU_IRQ 28
#endif

const uint8_t i2c_sda = CONFIG_PMU_SDA;
const uint8_t i2c_scl = CONFIG_PMU_SCL;
const uint8_t pmu_irq_pin = CONFIG_PMU_IRQ;
uint32_t cycleInterval;

void setup()
{
    Serial.begin(115200);
    while (!Serial);


    // Begin SY6970 PPM , Default disable watchdog timer
    bool result =  PPM.init(Wire, i2c_sda, i2c_scl, SY6970_SLAVE_ADDRESS);

    if (result == false) {
        while (1) {
            Serial.println("PPM is not online...");
            delay(50);
        }
    }

    // Disable battery charge function
    PPM.disableCharge();

    /*
    * Example:
    *   PPM.enableWatchdog( SY6970_WDT_TIMEROUT_40SEC );
    * Optional parameters:
    *   SY6970_WDT_TIMEROUT_40SEC,      //40 Second
    *   SY6970_WDT_TIMEROUT_80SEC,      //80 Second
    *   SY6970_WDT_TIMEROUT_160SEC,     //160 Second
    * * */
    // Enable SY6970 PPM watchdog function ,default timer out 40 second
    PPM.enableWatchdog();

}



void loop()
{
    // Feed watchdog , If the dog is not fed, the PPM will restart after a timeout, and all PPM settings will be restored to their default values
    Serial.print(millis() / 1000); Serial.println(" Second");
    PPM.feedWatchdog();
    delay(1000);
}





