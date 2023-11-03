import sys
sys.path.insert(1, '../')
from LCD import LCD
import socket
import struct, time


class NTPClient:
    def __init__(self, ntpserv = "time.google.com", port = 123) -> None:
        self.ntpserv = ntpserv
        self.addr = (self.ntpserv, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.req_msg = '\x1b' + 47 * '\0'
        self.ntp_time: time.struct_time
        
    def get_time(self):
        while True:
            try:
                self.sock.sendto(self.req_msg.encode('utf-8'), self.addr)
                self.sock.settimeout(2)
                msg, addr = self.sock.recvfrom(1024)
            except socket.timeout:
                print("timeout")
                continue
            break
        t = struct.unpack( "!12I", msg )[10]
        t -= 2208988800 
        self.ntp_time = time.localtime(t)    
        return self.ntp_time
        
        
def main():
    ntpclient = NTPClient('tock.stdtime.gov.tw')
    lcd = LCD()
    print("Clock Start")
    cur_time: time.struct_time
    while True:
        cur_time = ntpclient.get_time()
        # lcd.clear()
        lcd.set_cursor(0, 0)
        lcd.print(time.strftime("%b.%d %A", cur_time))
        lcd.set_cursor(0, 1)
        lcd.print(time.strftime("%H:%M:%S"))
        time.sleep(0.3)
    

if __name__ == "__main__":
    main()
    
