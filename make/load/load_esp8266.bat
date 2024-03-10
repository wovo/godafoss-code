echo "you might need to connect while holding down the flash button"
python -m esptool --port COM42 --chip esp8266 erase_flash
python -m esptool --port COM42 --chip esp8266 write_flash --flash_size=detect 0 images/esp8266.bin
pause