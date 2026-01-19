#include <stdio.h>
#include <cstring>
#include "sdkconfig.h"
#include "esp_log.h"
#include "esp_err.h"

#ifdef CONFIG_PPM_BQ25896

#define XPOWERS_CHIP_BQ25896
#include "XPowersLib.h"
static const char *TAG = "BQ25896";

XPowersPPM power;

extern int pmu_register_read(uint8_t devAddr, uint8_t regAddr, uint8_t *data, uint8_t len);
extern int pmu_register_write_byte(uint8_t devAddr, uint8_t regAddr, uint8_t *data, uint8_t len);


esp_err_t pmu_init()
{
    //* Implemented using read and write callback methods, applicable to other platforms
#if CONFIG_I2C_COMMUNICATION_METHOD_CALLBACK_RW
    ESP_LOGI(TAG, "Implemented using read and write callback methods");
    if (power.begin(BQ25896_SLAVE_ADDRESS, pmu_register_read, pmu_register_write_byte)) {
        ESP_LOGI(TAG, "Init PMU SUCCESS!");
    } else {
        ESP_LOGE(TAG, "Init PMU FAILED!");
        return ESP_FAIL;
    }
#endif

    //* Use the built-in esp-idf communication method
#if CONFIG_I2C_COMMUNICATION_METHOD_BUILTIN_RW
#if (ESP_IDF_VERSION >= ESP_IDF_VERSION_VAL(5,0,0)) && defined(CONFIG_XPOWERS_ESP_IDF_NEW_API)

    ESP_LOGI(TAG, "Implemented using built-in read and write methods (Use higher version >= 5.0 API)");
    // * Using the new API of esp-idf 5.x, you need to pass the I2C BUS handle,
    // * which is useful when the bus shares multiple devices.
    extern i2c_master_bus_handle_t bus_handle;

    if (power.begin(bus_handle, BQ25896_SLAVE_ADDRESS)) {
        ESP_LOGI(TAG, "Init PMU SUCCESS!");
    } else {
        ESP_LOGE(TAG, "Init PMU FAILED!");
        return false;
    }
#else

    ESP_LOGI(TAG, "Implemented using built-in read and write methods (Use lower version < 5.0 API)");

    if (power.begin((i2c_port_t)CONFIG_I2C_MASTER_PORT_NUM, BQ25896_SLAVE_ADDRESS, CONFIG_PMU_I2C_SDA, CONFIG_PMU_I2C_SCL)) {
        ESP_LOGI(TAG, "Init PMU SUCCESS!");
    } else {
        ESP_LOGE(TAG, "Init PMU FAILED!");
        return false;
    }
#endif //ESP_IDF_VERSION >= ESP_IDF_VERSION_VAL(5,0,0)
#endif //CONFIG_I2C_COMMUNICATION_METHOD_BUILTIN_RW

    ESP_LOGI(TAG, "getID:0x%x", power.getChipID());

    // Set the minimum operating voltage. Below this voltage, the power will protect
    power.setSysPowerDownVoltage(3300);

    // Set input current limit, default is 500mA
    power.setInputCurrentLimit(3250);

    ESP_LOGI(TAG, "getInputCurrentLimit: %d mA", power.getInputCurrentLimit());

    // Disable current limit pin
    power.disableCurrentLimitPin();

    // Set the charging target voltage, Range:3840 ~ 4608mV ,step:16 mV
    power.setChargeTargetVoltage(4208);

    // Set the precharge current , Range: 64mA ~ 1024mA ,step:64mA
    power.setPrechargeCurr(64);

    // The premise is that Limit Pin is disabled, or it will only follow the maximum charging current set by Limi tPin.
    // Set the charging current , Range:0~5056mA ,step:64mA
    power.setChargerConstantCurr(1024);

    // Get the set charging current
    power.getChargerConstantCurr();
    ESP_LOGI(TAG, "getChargerConstantCurr: %d mA\n", power.getChargerConstantCurr());


    // To obtain voltage data, the ADC must be enabled first
    power.enableMeasure();

    // Turn on charging function
    // If there is no battery connected, do not turn on the charging function
    power.enableCharge();


    /*
    * Obtaining the battery voltage and battery charging status does not directly read the register,
    * but determines whether the charging current register is normal.
    * If read directly, the reading will be inaccurate.
    * The premise for obtaining these two states is that the NTC temperature measurement circuit is normal.
    * If the NTC detection is abnormal, it will return 0
    * * */
    ESP_LOGI(TAG, "CHG TARGET VOLTAGE :%04dmV CURRENT:%04dmA PER_CHARGE_CUR %04dmA",
             power.getChargeTargetVoltage(), power.getChargerConstantCurr(), power.getPrechargeCurr());
    ESP_LOGI(TAG, "VBUS:%s %04dmV VBAT:%04dmV VSYS:%04dmV", power.isVbusIn() ? "Connected" : "Disconnect",
             power.getVbusVoltage(),
             power.getBattVoltage(),
             power.getSystemVoltage());
    ESP_LOGI(TAG, "BUS STATE:%d STR:%s", power.getBusStatus(), power.getBusStatusString());
    ESP_LOGI(TAG, "CHG STATE:%d STR:%s CURRENT:%04dmA", power.chargeStatus(), power.getChargeStatusString(), power.getChargeCurrent());
    return ESP_OK;
}


void pmu_isr_handler()
{

    // Get power interrupt status
    power.getFaultStatus();

    if (power.isWatchdogFault()) {

        ESP_LOGI(TAG, "Watchdog Fault");

    } else if (power.isBoostFault()) {

        ESP_LOGI(TAG, "Boost Fault");

    } else if (power.isChargeFault()) {

        ESP_LOGI(TAG, "Charge Fault");

    } else if (power.isBatteryFault()) {

        ESP_LOGI(TAG, "Battery Fault");

    } else if (power.isNTCFault()) {

        ESP_LOGI(TAG, "NTC Fault: %s", power.getNTCStatusString());
        ESP_LOGI(TAG, " Percentage: %d%%", power.getNTCPercentage());
    } else {
        /*
        * When the battery is removed, INT will send an interrupt every 100ms. If the battery is not connected,
        * you can use power.disableCharge() to turn off the charging function.
        * */
        // power.disableCharge();

        ESP_LOGI(TAG, "Battery remove");
    }
}
#endif /*CONFIG_XPOWERS_AXP192_CHIP_AXP192*/


