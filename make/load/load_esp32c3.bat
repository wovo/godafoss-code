echo "you might need to connect while holding down the flash button"
python -m esptool --port COM42 --chip esp32c3 erase_flash
python -m esptool --port COM42 --chip esp32c3 write_flash -z 0x0 ../godafoss/images/esp32c3.bin
pause