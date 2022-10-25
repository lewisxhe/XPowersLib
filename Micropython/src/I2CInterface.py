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

@file      I2CInterface.py
@author    Lewis He (lewishe@outlook.com)
@date      2022-10-20

'''

from sys import implementation
from struct import unpack

if implementation.name == 'micropython':
    from machine import Pin, I2C
if implementation.name == 'circuitpython':
    import digitalio
    import busio
    from time import sleep, monotonic_ns
    from adafruit_bus_device import i2c_device


class I2CInterface:

    def __init__(self, i2c_bus:I2C,addr):

        if implementation.name == 'micropython':
            print('micropython')
            self._bus = i2c_bus
        if implementation.name == 'circuitpython':
            print('circuitpython')
            self._bus = i2c_device.I2CDevice(i2c_bus, addr)

        self._address = addr
        self._buffer = bytearray(8)
        self._bytebuf = memoryview(self._buffer[0:1])

    def _BV(self, bit):
        return (1 << bit)

    def _IS_BIT_SET(self, val, mask):
        return bool((((val) & (mask)) == (mask)))

    def writeRegister(self, reg: int, val: int):
        if implementation.name == 'micropython':
            self._bytebuf[0] = val
            self._bus.writeto_mem(self._address, reg, self._bytebuf)
        elif implementation.name == 'circuitpython':
            self._buffer[0] = reg & 0xFF
            self._buffer[1] = val & 0xFF
            with self._bus as i2c:
                i2c.write(self._buffer, start=0, end=2)

    def readRegister(self, reg: int) -> int:
        if implementation.name == 'micropython':
            self._bus.readfrom_mem_into(self._address, reg, self._bytebuf)
            return self._bytebuf[0]
        elif implementation.name == 'circuitpython':
            self._buffer[0] = reg & 0xFF
            with self._bus as i2c:
                i2c.write(self._buffer, start=0, end=1)
                i2c.readinto(self._buffer, start=0, end=1)
                return unpack("<b", self._buffer[0:1])[0]

    def getRegisterBit(self, reg, bit)->bool:
        val = self.readRegister(reg)
        return val & self._BV(bit)

    def setRegisterBit(self, reg : int , bit: int ):
        val = self.readRegister(reg)
        self.writeRegister(reg, (val | (self._BV(bit))))

    def clrRegisterBit(self, reg: int , bit: int ):
        val = self.readRegister(reg)
        self.writeRegister(reg, (val & (~self._BV(bit))))

    def readRegisterH8L4(self, highReg, lowReg) -> int:
        h8 = self.readRegister(highReg)
        l4 = self.readRegister(lowReg)
        return (h8 << 4) | (l4 & 0x0F)

    def readRegisterH8L5(self, highReg, lowReg) -> int:
        h8 = self.readRegister(highReg)
        l5 = self.readRegister(lowReg)
        return (h8 << 5) | (l5 & 0x1F)

    def readRegisterH6L8(self, highReg, lowReg) -> int:
        h6 = self.readRegister(highReg)
        l8 = self.readRegister(lowReg)
        return ((h6 & 0x3F) << 8) | l8

    def readRegisterH5L8(self, highReg, lowReg) -> int:
        h5 = self.readRegister(highReg)
        l8 = self.readRegister(lowReg)
        return ((h5 & 0x1F) << 8) | l8
