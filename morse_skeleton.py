'''This file provides a few of the 'tricky' elements of the Morse Code project: those
involving setting up and reading from the serial port.'''

import arduino_connect  # This is the key import so that you can access the serial port.
import sys


# Codes for the 5 signals sent to this level from the Arduino

_dot = 1
_dash = 2
_symbol_pause = 3
_word_pause = 4
_reset = 5
_exit = 6


# Morse Code Class
class mocoder():
    current_symbol = ''
    current_word = ''
    morse_codes = {'01':'a','1000':'b','1010':'c','100':'d','0':'e','0010':'f','110':'g','0000':'h','00':'i','0111':'j',
               '101':'k','0100':'l','11':'m','10':'n','111':'o','0110':'p','1101':'q','010':'r','000':'s','1':'t',
               '001':'u','0001':'v','011':'w','1001':'x','1011':'y','1100':'z','01111':'1','00111':'2','00011':'3',
               '00001':'4','00000':'5','10000':'6','11000':'7','11100':'8','11110':'9','11111':'0'}

	# This is where you set up the connection to the serial port.
    def __init__(self,sport=True):
        if sport:
            self.serial_port = arduino_connect.pc_connect()
        self.reset()

    def reset(self):
        self.current_message = ''
        self.current_word = ''
        self.current_symbol = ''

    # This should receive an integer in range 1-4 from the Arduino via a serial port
    def read_one_signal(self,port=None):
        connection = port if port else self.serial_port
        while True:
            # Reads the input from the arduino serial connection
            data = connection.readline()
            if data:
                return data

    def update_current_symbol(self, signal):
        '''adds decoded arduino signal to current-symbol'''
        if (signal == 1):
            self.current_symbol += '0'
        elif (signal == 2):
            self.current_symbol += '1'

    def handle_symbol_end(self):
        '''when a symbol is finished, add it to the current word and resets the current symbol'''
        if(self.current_symbol in self.morse_codes):
            symbol = self.morse_codes[self.current_symbol]
            self.update_current_word(symbol)
            self.current_symbol = ''
        else:
            print('No symbol')
            self.current_symbol = ''

    def update_current_word(self, symbol):
        '''adds new symbol to current word'''
        self.current_word += symbol

    def handle_word_end(self):
        '''prints and resets the finished word'''
        self.handle_symbol_end()
        print(self.current_word, ' ')
        self.current_word = ''

    # The signal returned by the serial port is one (sometimes 2) bytes, that represent characters of a string.  So,
    # a 2 looks like this: b'2', which is one byte whose integer value is the ascii code 50 (ord('2') = 50).  The use
    # of function 'int' on the string converts it automatically.   But, due to latencies, the signal sometimes
    # consists of 2 ascii codes, hence the little for loop to cycle through each byte of the signal.

    def process_signal(self, signal):
        '''Decodes signal from the arduino and gives instructions according to what signal it is'''
        print(signal)
        #print(signal)
        if (signal == 1 or signal == 2):
            self.update_current_symbol(signal)
        elif (signal == 3):
            self.handle_symbol_end()
        elif (signal == 4):
            self.handle_word_end()
        elif (signal == 5):
            self.reset()
        elif (signal == 6):
            sys.exit()

    def decoding_loop(self):
        '''Decodes the signal from the arduino'''
        while True:
            s = self.read_one_signal(self.serial_port)
            for byte in s:
                self.process_signal(int(chr(byte)))

    
''' To test if this is working, do the following in a Python command window:

> from morse_skeleton import *
> m = mocoder()
> m.decoding_loop()

If your Arduino is currently running and hooked up to the serial port, then this
simple decoding loop will print the raw signals that the Arduino sends to
the serial port.  Each time you press (or release) your morse-code device, a signal should
appear in your Python window. In Python, these signals typically look like this:
 b'5' or b'1' or b'3', etc.
'''
