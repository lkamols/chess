# chess

Building a physical chess set that plays against a human player. Human moves will be detected with magnets and the 'CPU' will move pieces against the player.

## Description

The project is being done using a raspberry pi 3 and various other components. The board being constructed is 8x12, with 8x8 for the chess board, and an extra 8x2 on each side for dead pieces. Every square has an RGB neopixel LED underneath it, so the board can be updated to any configuration. The board itself is not coloured as that will be communicated using the LEDs.

## Code

Currently I have implemented a chess engine that can run a game (located in Code), with a framework for the important functions for the game display and movement which will come further down the line. This contains some functions currently being used to debug the constructed circuit.

## Chess Board Construction

The chess board is being 3D printed, made up of 24 components, laid out as below. ![piece-layout](https://user-images.githubusercontent.com/30397441/116361985-ea796980-a844-11eb-8eb4-53a6e09a23e4.png)

Each of these pieces was designed using Autodesk Inventor and was then 3D printed, they look like this. ![179560527_483279189684561_8732139022125843091_n](https://user-images.githubusercontent.com/30397441/116362643-9cb13100-a845-11eb-9ae9-30a46c50e769.jpg)

These then interlock to form the whole board, there are holes throughout which have metal rods to provide structural support.
![177470531_576113653351113_729673815005825239_n](https://user-images.githubusercontent.com/30397441/116362816-d124ed00-a845-11eb-9d2b-ba4e45a0c55c.jpg)

## Piece Detection

A circuit schematic for the piece detection circuit is shown below. This makes use of decoders and multiplexers to reduce the number of pins on the Raspberry Pi that are required to 8. To detect any particular square, one of the input (horizontal) lines is driven high (all others low) and then reading any of the output (vertical) lines gives whether or not there is a piece (magnet) at any particular square. At each square there is a reed switch (one I designed myself, discussed later) which will act as a switch that is connected when there is a magnet nearby.
