echo "you might need to connect while holding down the flash button"
python -m esptool --port COM42 --chip esp32 --baud 19200 erase_flash
python -m esptool --port COM42 --chip esp32 --baud 19200 write_flash -z 0x1000 ../godafoss/images/esp32-%1.bin
pause