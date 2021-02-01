from multiprocessing import Process
import board
import busio
import digitalio as dio
import time
import struct
import argparse
from random import randint
import numpy as np

import adafruit_rfm9x

RADIO_FREQ_MHZ = 868.0

SPI0 = {
    'MOSI':board.D10,#dio.DigitalInOut(board.D10),
    'MISO':board.D9,#dio.DigitalInOut(board.D9),
    'frequency':RADIO_FREQ_MHZ,
    'clock':board.D11,#dio.DigitalInOut(board.D11),
    #'ce':dio.DigitalInOut(board.D17),
    'cs':dio.DigitalInOut(board.CE1),
    'reset':dio.DigitalInOut(board.D25)
    }
SPI1 = {
    'MOSI':board.D20,#dio.DigitalInOut(board.D20),
    'MISO':board.D19,#dio.DigitalInOut(board.D19),
    'frequency':RADIO_FREQ_MHZ,
    'clock':board.D21,#dio.DigitalInOut(board.D11),
    #'ce':dio.DigitalInOut(board.D27),
    'cs':dio.DigitalInOut(board.D17),
    'reset':dio.DigitalInOut(board.D4)
    }

# # Configure RFM9x LoRa Radio - SPI0
# CS = DigitalInOut(board.CE1)
# RESET = DigitalInOut(board.D25)
# spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
#
# # Configure RFM9x LoRa Radio - SPI1
# CS = DigitalInOut(board.D17)
# RESET = DigitalInOut(board.D4)
# spi = busio.SPI(board.D21, MOSI=board.D20, MISO=board.D19)

def tx(radio, count, size, src, dst):
    radio.destination = dst
    radio.node = src
    radio.tx_power = 23

    print('Tx RFM9x sending to address: {}'.format(radio.destination))

    status = []
    buffer = np.random.bytes(size)

    start = time.monotonic()
    while count:
        # use struct.pack to packetize your data
        # into a usable payload

        #buffer = struct.pack("<i", count)
        # 'i' means a single 4 byte int value.
        # '<' means little endian byte order. this may be optional
        #print("Sending: {} as struct: {}".format(count, buffer))
        result = radio.send(buffer)
        if not result:
            #print("send() failed or timed out")
            #print(nrf.what_happened())
            status.append(False)
        else:
            #print("send() successful")
            status.append(True)
        # print timer results despite transmission success
        count -= 1
    total_time = time.monotonic() - start

    print('{} successfull transmissions, {} failures, {} bps'.format(sum(status), len(status)-sum(status), len(buffer)*8*len(status)/total_time))

def rx(radio, count, src):
    radio.node = src

    print('Rx RFM9x started, started at address:{}'.format(radio.node))

    received = []

    start_time = None
    start = time.monotonic()
    while count and (time.monotonic() - start) < 30:
        packet = radio.receive(timeout=5.0)

        if packet:
            if start_time is None:
                start_time = time.monotonic()

            count -= 1
            received.append(len(packet))
        else:
            print(packet)

    total_time = time.monotonic() - start_time

    print('{} received, {} average, {} bps'.format(len(received), np.mean(received), np.sum(received)*8/total_time))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RFM9x test')
    parser.add_argument('--src', dest='src', type=int, default=255, help='RFM9x\'s source address', choices=range(0,255))
    parser.add_argument('--dst', dest='dst', type=int, default=255, help='RFM9x\'s destination address', choices=range(0,255))
    parser.add_argument('--count', dest='cnt', type=int, default=10, help='Number of transmissions')
    parser.add_argument('--size', dest='size', type=int, default=250, help='Packet size', choices=range(1,252))
    parser.add_argument('--txchannel', dest='txchannel', type=int, default=76, help='Tx channel', choices=range(0,125))
    parser.add_argument('--rxchannel', dest='rxchannel', type=int, default=76, help='Rx channel', choices=range(0,125))

    args = parser.parse_args()

    # Initialize SPI bus.
    SPI0['spi'] = busio.SPI(**{x: SPI0[x] for x in ['clock', 'MOSI', 'MISO']})
    SPI1['spi'] = busio.SPI(**{x: SPI1[x] for x in ['clock', 'MOSI', 'MISO']})

    # Initialze RFM radio: (spi, cs, reset, frequency, *, preamble_length=8, high_power=True, baudrate=5000000)
    rx_lora = adafruit_rfm9x.RFM9x(**{x: SPI1[x] for x in ['spi', 'cs', 'reset', 'frequency']})
    tx_lora = adafruit_rfm9x.RFM9x(**{x: SPI0[x] for x in ['spi', 'cs', 'reset', 'frequency']})

    rx_process = Process(target=rx, kwargs={'radio':rx_lora, 'count': args.cnt, 'src': args.dst})
    tx_process = Process(target=tx, kwargs={'radio':tx_lora, 'count': args.cnt, 'size': args.size, 'src': args.src, 'dst': args.dst})

    rx_process.start()
    time.sleep(1)
    tx_process.start()

    tx_process.join()
    rx_process.join()
