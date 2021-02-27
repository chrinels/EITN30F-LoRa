import signal
import sys

from logging import getLogger, getLevelName, Formatter, StreamHandler, log

import adafruit_rfm9x
import board
import busio
import digitalio as dio
import argparse

import RPi.GPIO as GPIO


class LoRaNode:

    def __init__(self, SPI: dict, RFM9x: dict, loglevel: str='NOTSET') -> None:
        self._setUpLogging()
        self._setLogLevel(loglevel)

    def _setUpRFM9x(self) -> None:
        pass

    def _setUpSPI(self) -> None:
        pass

    def _setUpLogging(self) -> None:
        self.log = getLogger(name='LoRa')
        log_formatter = Formatter("%(asctime)s [%(threadName)s][%(levelname)s] %(name)s: %(message)s ") # I am printing thread id here
        console_handler = StreamHandler()
        console_handler.setFormatter(log_formatter)
        self.log.addHandler(console_handler)

    def _setLogLevel(self, level: str) -> None:
        '''
        Level       Numeric value
        CRITICAL    50
        ERROR       40
        WARNING     30
        INFO        20
        DEBUG       10
        NOTSET      0
        '''
        if level is None:
            level = 'NOTSET'
        self.log.setLevel(getLevelName(level))
        self.log.debug('LogLevel set to {}'.format(level))


if __name__ == '__main__':

    RADIO_FREQ_MHZ = 868.0

    RXRFM96 = {
                'address': 255,
                'frequency': RADIO_FREQ_MHZ,
                'channel': 0,
                'irqpin': None,
                'reset': dio.DigitalInOut(board.D4)

                }

    RXSPI = {
            'MOSI':board.D20,
            'MISO':board.D19,
            'clock':board.D21,
            'cs':dio.DigitalInOut(board.D17),
            }

    node = LoRaNode(loglevel='DEBUG')


