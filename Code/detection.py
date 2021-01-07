from gpiozero import LED, Button
import time

#decoder inputs
DEC_C = 17
DEC_B = 27
DEC_A = 22
#mux inputs
MUX_C = 23
MUX_B = 24
MUX_A = 25
#mux outputs
M1_OUT = 12 #output of multiplexer controlling columns 0-5
M2_OUT = 4 #output of multiplexer controlling columns 6-11


"""
generally set an output to a value, 0 for off, otherwise on
pin - a gpiozero LED variable
"""
def set_output(pin, value):
    if value == 0:
        pin.off()
    else:
        pin.on()

"""
read an input from a GPIO declared button, just a rename to 
make it more clear
pin - a gpiozero Button variable
"""
def read_input(pin):
    return 1 - int(pin.is_pressed) #this is opposite to intuitive

"""
set the values for a 3 bit control of a logic chip.
pin0, pin1, pin2 - the LEDs/pins to control
val - the value to write to these pins, 0 <= val <= 7
"""
def three_val_input(pin0, pin1, pin2, val):
    set_output(pin0, val & (1<<0))
    set_output(pin1, val & (1<<1))
    set_output(pin2, val & (1<<2))


class Detection:
    """
    init function, initialises the mux to zero
    """
    def __init__(self):
        self._init_mux()
        self._init_decoder()
        self._board = []
        for i in range(8):
            self._board += [[0]*12]
      
    """
    initialise the mux to be all set as outputs
    """
    def _init_mux(self):
        #declare shared MUX inputs as LEDs for on/off functionality
        self._muxC = LED(MUX_C)
        self._muxB = LED(MUX_B)
        self._muxA = LED(MUX_A)
        #declare the MUX outputs as buttons so that they can be read from
        self._m1_out = Button(M1_OUT)
        self._m2_out = Button(M2_OUT)
    
    """
    initialise the decoder inputs to be set as outputs
    """
    def _init_decoder(self):
        #declare decoder inputs as LEDs for on/off functionality
        self._decC = LED(DEC_C)
        self._decB = LED(DEC_B)
        self._decA = LED(DEC_A)

    """
    Set the mux inputs to a specific value, 0 <= val <= 7
    """
    def set_mux(self, val):
        three_val_input(self._muxA, self._muxB, self._muxC, val)

    """
    Set the decoder inputs to a specific valu, 0 <= val <= 7
    """
    def set_decoder(self, val):
        three_val_input(self._decA, self._decB, self._decC, val)

    """
    Read a specific square, for debugging purposes
    """
    def read_square(self, row, col):
        #the row is controlled by the decoder
        self.set_decoder(row)
        #the column is controlled by the muxes
        self.set_mux(col % 6)
        #then choose output based on the column
        #0-5 are on the first mux
        #6-11 are on the second mux
        if col < 6:
            return read_input(self._m1_out)
        else:
            return read_input(self._m2_out)

    """
    print the current detected board status
    """
    def print_board(self):
        for row in range(8):
            print(self._board[row])


    """
    Update the detected board storage
    """
    def update_board(self):
        global _board
        for row in range(8):
            self.set_decoder(row)
            for mux_val in range(6):
                self.set_mux(mux_val)
                self._board[row][mux_val] = read_input(self._m1_out)
                self._board[row][mux_val + 6] = read_input(self._m2_out)

if __name__ == "__main__":
    det = Detection()
    det.print_board()
    while(1):
        time.sleep(5)
        det.update_board()
        det.print_board()
  
