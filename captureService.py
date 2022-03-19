from concurrent import futures

from scapy.all import *

stop_event = threading.Event()

def getAllNetInterfaces():
    return IFACES.data


class MyThread(threading.Thread):
    def __init__(self, iface, captured_callback):
        threading.Thread.__init__(self)
        self.captured_callback = captured_callback
        self.iface = iface
        self.urlhead = ''
        self.ex = futures.ThreadPoolExecutor(max_workers=5)

    def run(self):
        sniff(iface=self.iface,
              filter="tcp",#tcp and dst port 1935
              prn=self.callback,
              stop_filter=lambda data: stop_event.is_set(),
              count=0)
        self.ex.shutdown()

    def callback(self, data_packet):
        self.ex.submit(self.analysis, data_packet)

    def analysis(self, packet):
        # print(threading.current_thread().name)
        if packet["TCP"].payload:
            payload = bytes(packet["TCP"].payload)
            if b'connect' in payload and b'tcUrl' in payload:
                r = re.search(b'\x05tcUrl(.*)', payload)
                if r:
                    urls = r.group(1)
                    url_length = struct.unpack('>h', urls[1:3])[0] + 3
                    self.urlhead = urls[3:url_length].decode(encoding='utf-8')
            if b'\x02\x00\x04\x70\x6c\x61\x79' in payload:
                r = re.search(b'\x02\x00\x04\x70\x6c\x61\x79(.*)', payload)
                if r:
                    play_body = r.group(1)
                    tail_length = struct.unpack('>h', play_body[11:13])[0] + 13
                    url_tail = play_body[13:tail_length].decode(encoding='utf-8', errors="ignore")
                    self.captured_callback(self.urlhead + '/' + url_tail)


def start(iface, captured_callback):
    stop_event.clear()
    capture_thread = MyThread(iface, captured_callback)
    capture_thread.start()


def stop():
    stop_event.set()
