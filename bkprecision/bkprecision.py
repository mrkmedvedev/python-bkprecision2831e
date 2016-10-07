import serial
import logging
import time


class BKPrecisionMultimeter:

    """
    This class provides basic functionality to operate with a BK Precision multimeter 2831E.
    """

    baud = 38400
    ser = None
    time_resolution = 0.008

    def __init__(self, serial_port=None, time_resolution=0.008, logging_file='bkprecision.log'):
        """
        Initialize the serial port in which the multimeter is connected.
        :param serial_port: is the ID (Windows) or dev resource (Linux) which the multimeter is connected.
        :param time_resolution: is the time between measures.
        :param logging_file: optional, is the file which the log messages will be stored.
        """
        if serial_port is not None:
            self.ser = serial.Serial(port=serial_port,
                                     baudrate=self.baud,
                                     bytesize=serial.EIGHTBITS,
                                     timeout=0,
                                     parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE)
            logging.basicConfig(filename=logging_file, level=logging.DEBUG)
            self.configure_connection()
            self.time_resolution = time_resolution

    def configure_connection(self):
        """
        Configure the connection.
        :return: True if connection and configuration is successful: otherwise, return False.
        """
        if self.ser.is_open:
            logging.info('The serial port is opened.')
        else:
            logging.error('The error could not been opened! Check serial port configuration.')
            return False
        self.ser.write('*IDN?\r')
        time.sleep(0.1)
        out = self.ser.read(100)
        logging.info('BKPrecision 2831E: (%d) %s' % (len(out), out))
        self.ser.flush()
        self.ser.write(':FUNC?\r')
        time.sleep(0.1)
        out = self.ser.read(100)
        logging.info('BKPrecision 2831E: (%d) %s' % (len(out), out))
        self.ser.flush()
        return True

    def measure(self):
        """
        Query a measure command to the multimeter.
        :return: a float value representing the response from the multimeter at a given time_resolution. None if
                 conversion could not been completed.
        """
        self.ser.write(':FETC?\r')
        time.sleep(self.time_resolution)
        out = self.ser.read(20)
        self.ser.flush()
        if out is not None and out != '':
            try:
                return float(out)
            except ValueError:
                return None

    def close_connection(self):
        """
        Closes the connection with the serial port.
        :return: None.
        """
        self.ser.close()
