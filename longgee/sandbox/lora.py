import signal
import sys
from socket import gethostname
from logging import Logger, getLogger, getLevelName, Formatter, StreamHandler, log

import adafruit_rfm9x
import board
import busio
import digitalio as dio
import argparse

import RPi.GPIO as GPIO


class LoRaNode:

    def __init__(self, spi: dict, rfm9x: dict, name: str='', loglevel: str='ERROR') -> None:
        # Initialize the logging 
        self.log = self._set_up_logging(name)
        self._set_log_level(loglevel)

        # Now the actual radio
        self.spi = self._set_up_spi(spi)
        self.radio = self._set_up_rfm9x(rfm9x)

        signal.signal(signal.SIGINT, self.default_signal_handler)

    def _set_up_logging(self, name: str='') -> Logger:
        log = getLogger(name='[{}] LoRa {}'.format(gethostname(), name))
        log_formatter = Formatter("%(asctime)s [%(levelname)s][%(threadName)s]%(name)s: %(message)s ") # I am printing thread id here
        console_handler = StreamHandler()
        console_handler.setFormatter(log_formatter)
        log.addHandler(console_handler)
        return log

    def _set_log_level(self, level: str) -> None:
        '''
        Level name      CRITICAL    ERROR   WARNING     INFO    DEBUG   NOTSET
        Numeric value   50          40      30          20      10      0    
        '''
        self.log.setLevel(getLevelName(level))
        self.log.debug('LogLevel -> "{}"'.format(level))

    def default_signal_handler(self) -> None:
        self.log.debug('SIGINT captured! Exiting ...')
        GPIO.cleanup()
        sys.exit(0)
    
    def default_irq_callback(self) -> None:
        pass

    def _set_up_rfm9x(self, rfm9x: dict) -> adafruit_rfm9x.RFM9x:
        self.log.debug('Setting up RFM9x radio {}'.format(rfm9x))

        try:
            radio = adafruit_rfm9x.RFM9x(self.spi, **{x: rfm9x[x] for x in ['cs', 'reset', 'frequency']})
        except KeyError:
            self.log.error("Missing key in the rfm9x dict. Must contain 'cs', 'reset', 'frequency'")
            sys.exit(-1)

        if 'node' in rfm9x: radio.node = rfm9x['node']
        if 'agc' in rfm9x: radio.auto_agc = rfm9x['agc']
        if 'preamble_length' in rfm9x: radio.preamble_length = rfm9x['preamble_length']
        if 'high_power' in rfm9x: radio.high_power = rfm9x['high_power']
        return radio

    def _set_up_spi(self, spi: dict) -> busio.SPI:
        self.log.debug('Setting up SPI bus {}'.format(spi))

        try:
            return busio.SPI(**{x: spi[x] for x in ['clock', 'MOSI', 'MISO']})
        except KeyError:
            self.log.error("The SPI dict must contain 'clock', 'MOSI', and 'MISO' keys.")
            sys.exit(-1)

    @property
    def coding_rate(self, rate):
        self.radio.coding_rate = rate

if __name__ == '__main__':

    RADIO_FREQ_MHZ = 868.0

    RXRFM96 = {
                'node': 255,
                'frequency': RADIO_FREQ_MHZ,
                'channel': 0,
                'irqpin': None,
                'reset': dio.DigitalInOut(board.D4),
                'cs':dio.DigitalInOut(board.D17)
                }

    RXSPI = {
            'MOSI':board.D20,
            'MISO':board.D19,
            'clock':board.D21,
            }

    node = LoRaNode(RXSPI, RXRFM96, name='Rx', loglevel='DEBUG')
