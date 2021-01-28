import adafruit_rfm9x
import board
import busio
import digitalio as dio
import argparse

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
    tx_lora = adafruit_rfm9x.RFM9x(**{x: SPI0[x] for x in ['spi', 'cs', 'reset', 'frequency']})
    rx_lora = adafruit_rfm9x.RFM9x(**{x: SPI1[x] for x in ['spi', 'cs', 'reset', 'frequency']})

    print('RFM95w found on SPI0: {}, SPI1: {}'.format(tx_lora, rx_lora))
