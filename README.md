# python-i2c-lcd
- Simple and easy-to-use scripts to control LCD with `smubs` library

## Implementation
- Referenced to [LiquidCrystal_I2C](https://github.com/johnrickman/LiquidCrystal_I2C)
- Implement an simplified version providing following functions
    ```
    'backlight', 'blink', 'clear', 'cursor', 'display', 'home', 'init_lcd', 'no_backlight', 'no_blink', 'no_cursor', 'no_display', 'print', 'send_cmd', 'send_data', 'set_cursor', 'write_lcd'
    ```

## Tested Environment
- Orange Pi 5
    `Linux 5.10.110-rockchip-rk3588 #23.02.2 SMP Fri Feb 17 23:59:20 UTC 2023 aarch64 aarch64 aarch64 GNU`
- LCD1602 with PCF8574 
### Referenced Commands
- Install requirements
    ```
    pip3 install -r requirements.txt
    ```
- Connect to I2C device and check device address
    ```
    i2cdetect -y <dev_num>
    ```
- Adjust parameters like `LCD_ADDR, DEV_NUM, LCD_WIDTH, LCD_COLS`
- Start program to test
    ```
    python3 LCD.py
    ```

## Reference
- [LiquidCrystal_I2C](https://github.com/johnrickman/LiquidCrystal_I2C)