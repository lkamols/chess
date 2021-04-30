# chess

Building a physical chess set that plays against a human player. Human moves will be detected with magnets and the 'CPU' will move pieces against the player.

## Description

The project is being done using a raspberry pi 3 and various other components. The board being constructed is 8x12, with 8x8 for the chess board, and an extra 8x2 on each side for dead pieces. Every square has an RGB neopixel LED underneath it, so the board can be updated to any configuration. The board itself is not coloured as that will be communicated using the LEDs.

## Code

Currently I have implemented a chess engine that can run a game (located in Code), with a framework for the important functions for the game display and movement which will come further down the line. This contains some functions currently being used to debug the constructed circuit.

## Chess Board Construction

The chess board is being 3D printed, made up of 24 components, laid out as below. 

<img src="https://user-images.githubusercontent.com/30397441/116361985-ea796980-a844-11eb-8eb4-53a6e09a23e4.png" width=700>

Each of these pieces was designed using Autodesk Inventor (files in Board/Pieces)[detection_schematic.pdf](https://github.com/lkamols/chess/files/6402259/detection_schematic.pdf)
 and was then 3D printed, they look like this. 

<img src="https://user-images.githubusercontent.com/30397441/116362643-9cb13100-a845-11eb-9ae9-30a46c50e769.jpg" width=700>

These then interlock to form the whole board, there are holes throughout which have metal rods to provide structural support.

<img src="https://user-images.githubusercontent.com/30397441/116362816-d124ed00-a845-11eb-9d2b-ba4e45a0c55c.jpg" width=700>

## Piece Detection

A circuit schematic for the piece detection circuit is shown below. This makes use of decoders and multiplexers to reduce the number of pins on the Raspberry Pi that are required to 8. To detect any particular square, one of the input (horizontal) lines is driven high (all others low) and then reading any of the output (vertical) lines gives whether or not there is a piece (magnet) at any particular square. At each square there is a reed switch (one I designed myself, discussed later) which will act as a switch that is connected when there is a magnet nearby.

<img src="https://user-images.githubusercontent.com/30397441/116632597-e2cbd900-a99a-11eb-8930-4a36639e8b1c.png" width=1000>

## Reed Switches
I originally bought some reed switches for piece detection, but these don't work for what I need. The reason for this is the magnetic field orientation required. To move the pieces later with an electromagnet, they need to have the north/south poles vertically. But the only way to reliably execute this with a reed switch is to orient them vertically, which would make the board thick and I didn't want to do that, so I designed my own reed switches, shown below. These reed switches are contained in the same compartment as the neopixel LED to save space.

<img src="https://user-images.githubusercontent.com/30397441/116365038-324dc000-a848-11eb-8a7f-823a1e1ac13c.jpg">

The small long component is a strip of iron I got from pulling apart an old transformer with a piece of copper tape on one side. This is placed in the other compartment next to the LED (but cannot ever touch the LED because of its shape). This is then glued to the bottom of the other, flatter piece as shown below.

<img src="https://user-images.githubusercontent.com/30397441/116365683-d5063e80-a848-11eb-90e3-92ca4236f523.jpg">

This is then placed into the chess board facing the opposite way. When a magnet is placed on the top surface, the metal strip is attracted to it, and completes the circuit, allowing current to flow through. If there is no magnet nearby the piece of iron strip falls back down with gravity and disconnects the circuit. In practice this has been very reliable, and does not depend at all on the orientation of the magnet, which fixes the problem with an existing reed switch.

## LED circuitry
Each square has a Neopixel RGB LED in it so that the board can change colours at any time. The Neopixel LEDs are connected to GPIO18 on the Raspberry pi. The neopixel library is used to send signals for controlling the colours displayed, it uses PWM and DMA to ensure the signals are correct even with the Pi's operating system running. There is a level shifter to convert from the 3.3V of the Raspberry Pi to the 5V required for the neopixels. Capacitors are included close to the neopixel to help avoid any damage caused by spikes. The wiring is shown below, with 96 LEDs being repeated, one for each square.

<img src="https://user-images.githubusercontent.com/30397441/116632938-9a60eb00-a99b-11eb-884e-2563c8292189.png" width=600>

## Putting it all together
The reed switch and LED are placed in the same compartment for each square, shown above. These then have wires soldered to the copper tape which is then fed through the holes in the chess board, and wired to copper tape on the underside of the chess board. A picture of the underside of the board is shown below.

<img src="https://user-images.githubusercontent.com/30397441/116633156-2115c800-a99c-11eb-8cb2-b4592f88c528.jpg">

This soldering process is about one third complete, life has taken over which has pushed this further down the priority list unfortunately.

## Moving Pieces
I intend on building a 3D printer style movement system under the board which moves an electromagnet. To move a piece, the electromagnet would be moved underneath the piece, turned on, moved to the destination, and the electromagnet turned off. Currently I have been doing some experiments with electromagnets to determine the strength of electromagnet I would need to effectively move one piece (but not more). I have been doing this by constructing an electromagnet myself, pulling apart an old transistor to salvage iron pieces for the iron core and the wiring. I have made two electromagnets so far, shown below.

<img src="https://user-images.githubusercontent.com/30397441/116634108-8cf93000-a99e-11eb-9876-f1ad2309ea21.jpg" width=600>

## Chess Pieces
Using Autodesk Inventor I have designed my own chess pieces, I went for a quite minimalistic theme, they are shown below and can be found in Board/Chess-Pieces.

<img src="https://user-images.githubusercontent.com/30397441/116634884-abf8c180-a9a0-11eb-9d69-ee920af4fe73.png">

They each have a small compartment at the bottom to insert a magnet, the magnets being used are rectangular floristry magnets.

## How Will the Knight Move?
Everyone's favourite question, the board is quite large, for this particular problem, with the pieces being on the smaller side. The horse will then be able to travel between two pieces, moving through the corners of the squares
