import functools
import sys

def catch_exception_decorator(orin_func):
    @functools.wraps(orin_func)
    def func(*args, **kwargs):
        try:
            return orin_func(*args, **kwargs)
        except Exception as e:
            print(f"{orin_func.__name__}\tEXCEP: {e}")
    return func

class PCF8574:
    """LCD Command Instrctions for PCT8574"""
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    LCD_SETCGRAMADDR = 0x40
    LCD_SETDDRAMADDR = 0x80
    
    # Flags for display entry mode
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # Flags for display on/off control
    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00

    # Flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x04
    LCD_MOVELEFT = 0x00

    # Flags for function set
    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00
    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00
    
    # Backlight Control
    BACKLIGHT = 0x08
    NOBACKLIGHT = 0x00

    Bl = 0b00001000
    En = 0b00000100  # Enable bit
    Rw = 0b00000010  # Read/Write bit
    Rs = 0b00000001  # Register select bit
    

    