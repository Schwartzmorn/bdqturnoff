import re
import time
import urllib2

class AVReceiver:
    _POWER_CMD = 'formiPhoneAppPower.xml?1+Power'
    _POWER_RE = re.compile('<Power><value>([^<]+)</value></Power>')
    _SOURCE_CMD = 'formiPhoneAppDirect.xml?SI'
    _SOURCE_RE = 'AUXB'
    _STATUS_CMD = 'formMainZone_MainZoneXmlStatus.xml'
    _STATUS_RE = re.compile('<InputFuncSelect><value>([^<]+)</value></InputFuncSelect>')

    # TODO don't hardcode the ip adress...
    def __init__(self, ip='192.168.1.13'):
        self.baseurl = 'http://{}/goform/'.format(ip)

    def _send_command(self, command):
        return urllib2.urlopen(self.baseurl + command, timeout=5)

    def _get_status(self):
        res = self._send_command(AVReceiver._STATUS_CMD)
        if res and res.getcode() == 200:
            power = None
            source = None
            for line in res:
                match = AVReceiver._STATUS_RE.search(line)
                if match:
                    source = match.group(1)
                match = AVReceiver._POWER_RE.search(line)
                if match:
                    power = match.group(1) == 'ON'

            return power, source
        return None, None

    def shut_down(self):
        power, source = self._get_status()
        if power and source == AVReceiver._SOURCE_RE:
            self._send_command(AVReceiver._POWER_CMD + 'Standby')

    def turn_on(self):
        power, source = self._get_status()
        if not power:
            self._send_command(AVReceiver._POWER_CMD + 'On')
        count = 4
        # cannot change the source during startup, so we try several times
        while source != AVReceiver._SOURCE_RE and count > 0:
            time.sleep(1)
            self._send_command(AVReceiver._SOURCE_CMD + AVReceiver._SOURCE_RE)
            count -= 1
            _, source = self._get_status()

if __name__ == '__main__':
    av = AVReceiver()
    av.shut_down()
