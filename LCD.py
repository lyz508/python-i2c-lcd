import smbus2
import logging
import time
from utils import PCF8574, catch_exception_decorator
        
class LCD:
    """For 1602"""
    def __init__(self, debug_level = logging.INFO, 
                bl = True, frame_buf = False, dev_num = 1,
                lcd_addr = 0x27, lcd_width = 16, lcd_cols = 16, lcd_rows = 2,
                ) -> None:
        # params 
        self.LCD_ADDR = lcd_addr
        self.LCD_WIDTH = lcd_width
        self.LCD_BACKLIGHT = PCF8574.BACKLIGHT if bl else PCF8574.NOBACKLIGHT
        self.LCD_COLS = lcd_cols
        self.LCD_ROWS = lcd_rows
        self.DEV_NUM = dev_num
        self.DEBUG_LEVEL = debug_level
        self.DISPLAYFUNC = PCF8574.LCD_DISPLAYON | PCF8574.LCD_CURSOROFF | PCF8574.LCD_BLINKOFF
        self.CURSOR = (0, 0) # (col, row)
        if frame_buf: 
            self.frame_buf = [(lambda row: list([col//100 for col in range(self.LCD_COLS)]))(row) for row in range(self.LCD_ROWS)]
            print(self.frame_buf)
        else:
            self.frame_buf = None
        # bus
        self.lcd_bus = smbus2.SMBus(self.DEV_NUM)
        # debug
        logging.basicConfig(
            level=self.DEBUG_LEVEL,
            format="[%(levelname)s]> %(message)s"
        )
        # init LCD
        self.init_lcd()
    
    @catch_exception_decorator
    def _move_cursor(self, pos_cursor: tuple):
        col, row = pos_cursor
        row = self.LCD_ROWS-1 if row > self.LCD_ROWS else row
        col = self.LCD_COLS-1 if col > self.LCD_COLS else col
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        pos = PCF8574.LCD_SETDDRAMADDR + row_offsets[row] + col
        self.send_cmd(pos) # set cursor
        logging.debug(f"Cursor move ({col}, {row})")
    
    def _get_parsed_str(self, msg: str, lpad = 0, rpad = 0):
        msg = msg.rjust(len(msg)+lpad, " ").ljust(len(msg)+lpad+rpad, " ")
        if len(msg) < self.LCD_WIDTH:
            msg = msg.ljust(self.LCD_WIDTH, " ")
        return msg[0: self.LCD_WIDTH]
    
    @catch_exception_decorator
    def send_cmd(self, cmd):
        logging.debug(f"CMD:\t{hex(cmd)}({bin(cmd)})")
        # first bits
        buf = cmd & 0xF0 | self.LCD_BACKLIGHT | PCF8574.En 
        self.lcd_bus.write_byte(self.LCD_ADDR, buf) 
        time.sleep(0.002)
        buf &= 0xFB
        self.lcd_bus.write_byte(self.LCD_ADDR, buf)
        # second bits
        buf = ((cmd & 0x0F) << 4) | self.LCD_BACKLIGHT | PCF8574.En
        self.lcd_bus.write_byte(self.LCD_ADDR, buf)
        time.sleep(0.002)
        buf &= 0xFB
        self.lcd_bus.write_byte(self.LCD_ADDR, buf)

    @catch_exception_decorator
    def send_data(self, data):
        logging.debug(f"DATA:\t{hex(data)}({chr(data)})")
        # first bits
        buf = data & 0xF0 | self.LCD_BACKLIGHT | PCF8574.En | PCF8574.Rs
        self.lcd_bus.write_byte(self.LCD_ADDR, buf) 
        time.sleep(0.002)
        buf &= 0xFB
        self.lcd_bus.write_byte(self.LCD_ADDR, buf)
        # second bits
        buf = ((data & 0x0F) << 4) | self.LCD_BACKLIGHT | PCF8574.En | PCF8574.Rs
        self.lcd_bus.write_byte(self.LCD_ADDR, buf)
        time.sleep(0.002)
        buf &= 0xFB
        self.lcd_bus.write_byte(self.LCD_ADDR, buf)
        
    def init_lcd(self, Bl = True):
        try:
            self.send_cmd(0x33) # Must initialize to 8-line mode at first
            time.sleep(0.005)
            self.send_cmd(0x32) # Then initialize to 4-line mode
            time.sleep(0.005)
            self.send_cmd(0x06) # Cursor move direction
            time.sleep(0.005)
            self.send_cmd(PCF8574.LCD_DISPLAYCONTROL | self.DISPLAYFUNC) # Enable display without cursor
            time.sleep(0.005)
            self.send_cmd(0x28) # 2 Lines & 5*7 dots
            time.sleep(0.005)
            self.send_cmd(0x01) # Clear Display
            time.sleep(0.005)
        except:
            logging.debug("Init LCD failed.")
            return False
        finally:
            logging.debug("Init LCD.")
            self.lcd_bus.write_byte(self.LCD_ADDR, self.LCD_BACKLIGHT)
            logging.debug("Backlight done.")
            self.lcd_bus.write_byte(self.LCD_ADDR, PCF8574.LCD_CLEARDISPLAY)
            return True

    def set_cursor(self, col, row):
        self.CURSOR = (col, row)
        self._move_cursor(self.CURSOR)
    
    def clear(self):
        self.send_cmd(PCF8574.LCD_CLEARDISPLAY)
        time.sleep(0.002)
        
    def home(self):
        self.send_cmd(PCF8574.LCD_RETURNHOME)
        time.sleep(0.002)
        
    def backlight(self):
        self.LCD_BACKLIGHT = PCF8574.BACKLIGHT
        self.send_cmd(0x00)
        time.sleep(0.002)
    
    def no_backlight(self):
        self.LCD_BACKLIGHT = PCF8574.NOBACKLIGHT
        self.send_cmd(0x00)
        time.sleep(0.002)
        
    def cursor(self):
        self.DISPLAYFUNC |= PCF8574.LCD_CURSORON
        self.send_cmd(PCF8574.LCD_DISPLAYCONTROL | self.DISPLAYFUNC)
        logging.debug(f"DISPLAYFUNC:\t{format(self.DISPLAYFUNC, '#010b')}")
        time.sleep(0.002)
        
    def no_cursor(self):
        self.DISPLAYFUNC &= ~PCF8574.LCD_CURSORON # as mask
        self.send_cmd(PCF8574.LCD_DISPLAYCONTROL | self.DISPLAYFUNC)
        logging.debug(f"DISPLAYFUNC:\t{format(self.DISPLAYFUNC, '#010b')}")
        time.sleep(0.002)
        
    def blink(self):
        self.DISPLAYFUNC |= PCF8574.LCD_BLINKON
        self.send_cmd(PCF8574.LCD_DISPLAYCONTROL | self.DISPLAYFUNC)
        logging.debug(f"DISPLAYFUNC:\t{format(self.DISPLAYFUNC, '#010b')}")
        time.sleep(0.002)
        
    def no_blink(self):
        self.DISPLAYFUNC &= ~PCF8574.LCD_BLINKON
        self.send_cmd(PCF8574.LCD_DISPLAYCONTROL | self.DISPLAYFUNC)
        logging.debug(f"DISPLAYFUNC:\t{format(self.DISPLAYFUNC, '#010b')}")
        time.sleep(0.002)
        
    def display(self):
        self.DISPLAYFUNC |= PCF8574.LCD_DISPLAYON
        self.send_cmd(PCF8574.LCD_DISPLAYCONTROL | self.DISPLAYFUNC)
        logging.debug(f"DISPLAYFUNC:\t{format(self.DISPLAYFUNC, '#010b')}")
        time.sleep(0.002)
    
    def no_display(self):
        self.DISPLAYFUNC &= ~PCF8574.LCD_DISPLAYON
        self.send_cmd(PCF8574.LCD_DISPLAYCONTROL | self.DISPLAYFUNC)
        logging.debug(f"DISPLAYFUNC:\t{format(self.DISPLAYFUNC, '#010b')}")
        time.sleep(0.002)
        
    def print(self, msg):
        """print toward carsor"""
        self._get_parsed_str(msg)
        for i, c in enumerate(msg):
            if i + self.CURSOR[0] >= self.LCD_WIDTH:
                break
            self.send_data(ord(c))
            
    def write_lcd(self, col, row, msg: str = ""):
        # string parse
        msg = self._get_parsed_str(msg, 0, 0)
        self._move_cursor((col, row))
        for i, c in enumerate(msg):
            if i + col >= self.LCD_WIDTH:
                break
            self.send_data(ord(c))

    
def check_funcs(lcd: LCD):
    """check LCD functions work properly"""
    print("Start Checking Funcs...")
    lcd.set_cursor(0, 0)
    lcd.print("Checking FUNCs")
    time.sleep(3)
    lcd.clear()
    
    print("LCD Line 1 + Line 2")
    lcd.write_lcd(0, 0, str("--LINE 1 OK").ljust(16, "-"))
    lcd.write_lcd(0, 1, str("--LINE 2 OK").ljust(16, "-"))
    time.sleep(3)
    lcd.clear()
    
    print("Blinking Test")
    lcd.set_cursor(0, 0)
    lcd.print("Blinking Test")
    lcd.blink()
    time.sleep(3)
    lcd.clear()
    lcd.no_blink()
    
    print("Cursor Test")
    lcd.set_cursor(0, 0)
    lcd.print("Cursor Test")
    lcd.cursor()
    time.sleep(3)
    lcd.clear()
    
    print("Return Home")
    lcd.write_lcd(0, 1, "Return Home")
    lcd.blink()
    lcd.home()
    time.sleep(3)
    lcd.clear()
    
    print("Backlight")
    lcd.write_lcd(0, 0, "Backlight")
    lcd.backlight()
    time.sleep(1)
    lcd.no_backlight()
    time.sleep(2)
    lcd.backlight()
    time.sleep(1)
    lcd.clear()
    
    print(str("End").ljust(16, "="))
    lcd.write_lcd(0, 0, "End")
    time.sleep(3)
    lcd.no_display()
    
    
def main():
    lcd = LCD(debug_level=logging.DEBUG)
    check_funcs(lcd)

    
if __name__ == "__main__":
    main()
    