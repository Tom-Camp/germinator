import gc
import machine
import network
import ntptime
import time


gc.enable()


class Connect:
    def __init__(self, ssid: str, password: str, hostname: str):
        self.ssid = ssid
        self.password = password
        self.status: bool = False
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.hostname = network.hostname(hostname)

    def connect(self):
        self.wlan.connect(self.ssid, self.password)
        max_wait = 10
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            time.sleep(1)

        if self.wlan.status() != 3:
            machine.reset()
        else:
            print('connected')
            status = self.wlan.ifconfig()
            print('ip = ' + status[0])
            ntptime.settime()
            time.sleep(2)
            rtc = machine.RTC()
            print(rtc.datetime())
            gc.collect()
