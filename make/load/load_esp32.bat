echo "you might need to connect while holding down the flash button"
python -m esptool --port COM42 --chip esp32 erase_flash
python -m esptool --port COM42 --chip esp32 write_flash -z 0x1000 images/esp32.bin
#python -m esptool --port COM42 --chip esp32 write_flash -z 0x1000 images/ESP32_GENERIC-20240222-v1.22.2.bin
pause