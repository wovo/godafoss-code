import machine

# outer pixels are not easily visible
# setting the hard SPI clock (baudrate) too high crashes
# the spiram is needed for the pixelbuffer, but it is slooow

#  5 TFT_CS
# 12 TFT_BL
# 18 TFT_SCLK
# 19 TFT_MOSI
# 27 TFT_DC
# 39 MBA423 interrupt
# 21 BMA423 I2C SDA
# 22 BMA423 I2C SCL
# 26 MAX98257A I2S BCK
# 25 MAX98357A I2S WS
# 33 MAX98357A I2S DOUT
#  4 vibration motor
# 35 AXP202 interrupt
# 21 AXP202 SDA
# 22 AXP202 SCL
# 13 IR
# 37 RTC interrupt
# 38 touch interrupt
# 23 touch I2C SDA
# 32 touch I2C SCL

if 1:
    # enable LCD power
    i0 = machine.SoftI2C(sda=machine.Pin(21),scl=machine.Pin(22))    
    power_output_control = i0.readfrom_mem(53, 0x12, 1)[0]
    power_output_control |= ( 1 << 1 ) # DCDC3 enable
    power_output_control |= ( 1 << 2 ) # LDO2 enable
    i0.writeto_mem(53, 0x12, bytes([power_output_control]))

# vibration motor / buzzer

pin_buzzer = 4
    
# touch screen i2c

pin_touch_scl = 32
pin_touch_sda = 23

touch_i2c = machine.SoftI2C(
    scl = machine.Pin( pin_touch_scl ),
    sda = machine.Pin( pin_touch_sda ),
    freq = 100_000
)
    
# axp202 mpu and bma423 acceleration sensor i2c

pin_main_scl = 22
pin_main_sda = 21

main_i2c = machine.SoftI2C(
    scl = machine.Pin( pin_main_scl ),
    sda = machine.Pin( pin_main_sda ),
    freq = 100_000
)
    
# st7789 lcd

pin_lcd_sclk = 18
pin_lcd_mosi = 19
pin_lcd_miso = 39 # dummy
pin_lcd_cs = 5
pin_lcd_dc = 27
pin_lcd_backlight = 12

lcd_spi = machine.SPI(
    1,
    baudrate = 30_000_000, # 30 MHz OK, 40 MHz crashes
    polarity = 1,
    phase = 1, 
    sck = machine.Pin( pin_lcd_sclk ),
    mosi = machine.Pin( pin_lcd_mosi ),
    miso = machine.Pin( pin_lcd_miso )
)