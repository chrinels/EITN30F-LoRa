import signal
import sys
from socket import gethostname
from logging import getLogger, getLevelName, Formatter, StreamHandler, log

import adafruit_rfm9x
import board
import busio
import digitalio as dio
import argparse

import RPi.GPIO as GPIO


class LoRaNode:

    def __init__(self, spi: dict, rfm9x: dict, name: str='', loglevel: str='ERROR') -> None:
        # Initialize the logging 
        self._set_up_logging(name)
        self._set_log_level(loglevel)

        # Now the actual radio
        self._set_up_spi(spi)
        self._set_up_rfm9x()

    def _set_up_rfm9x(self) -> None:
        pass

    def _set_up_spi(self, spi: dict) -> None:
        self.log.debug('Setting up SPI bus {}'.format(spi))

        try:
            self.spi = busio.SPI(**{x: spi[x] for x in ['clock', 'MOSI', 'MISO']})
        except KeyError:
            self.log.error("The SPI dict must contain 'clock', 'MOSI', and 'MISO' keys.")
            sys.exit(-1)


    def _set_up_logging(self, name: str='') -> None:
        self.log = getLogger(name='[{}] LoRa {}'.format(gethostname(), name))
        log_formatter = Formatter("%(asctime)s [%(threadName)s][%(levelname)s]%(name)s: %(message)s ") # I am printing thread id here
        console_handler = StreamHandler()
        console_handler.setFormatter(log_formatter)
        self.log.addHandler(console_handler)

    def _set_log_level(self, level: str) -> None:
        '''
        Level name      CRITICAL    ERROR   WARNING     INFO    DEBUG   NOTSET
        Numeric value   50          40      30          20      10      0    
        '''
        self.log.setLevel(getLevelName(level))
        self.log.debug('LogLevel -> "{}"'.format(level))


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
            #'MISO':board.D19,
            'clock':board.D21,
            'cs':dio.DigitalInOut(board.D17),
            }

    node = LoRaNode(RXSPI, RXRFM96, name='Rx', loglevel='ERROR')
