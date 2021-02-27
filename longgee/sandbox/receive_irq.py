import signal
import sys

from logging import getLogger, getLevelName, Formatter, StreamHandler

import adafruit_rfm9x
import board
import busio
import digitalio as dio
import argparse

import RPi.GPIO as GPIO


log = getLogger()
log.setLevel(getLevelName('INFO'))
log_formatter = Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s [%(threadName)s] [%(thread)d]") # I am printing thread id here


console_handler = StreamHandler()
console_handler.setFormatter(log_formatter)
log.addHandler(console_handler)

RADIO_FREQ_MHZ = 868.0

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def rx_irq_callback(radio):
    log.info('Radio {}\tRSSI = {} dBm'.format(radio, radio.rssi))
    packet = radio.receive(timeout=5.0)
    # radio.receive()

SPI1 = {
        'MOSI':board.D20,
        'MISO':board.D19,
        'frequency':RADIO_FREQ_MHZ,
        'clock':board.D21,
        'cs':dio.DigitalInOut(board.D17),
        'reset':dio.DigitalInOut(board.D4)
        }

if __name__ == '__main__':


    # Initialize SPI bus.
    SPI1['spi'] = busio.SPI(**{x: SPI1[x] for x in ['clock', 'MOSI', 'MISO']})

    # Initialze RFM radio: (spi, cs, reset, frequency, *, preamble_length=8, high_power=True, baudrate=5000000)
    rx_lora = adafruit_rfm9x.RFM9x(**{x: SPI1[x] for x in ['spi', 'cs', 'reset', 'frequency']})
    rx_lora.node = 2

    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(6, GPIO.RISING, callback=lambda x: rx_irq_callback(rx_lora))

    rx_lora.receive()

    print('RFM95w found on SPI0: {}, SPI1: {}'.format(0, rx_lora))
    print('Press Ctrl+c to quit.')

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
