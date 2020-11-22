// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LOOP)
@SCREEN  // this computer has symbol SCREEN predefined as RAM addresses 16384 (0x4000)
D=A  // get the address of SCREEN, the base address of the screen memory map
@SCREEN_START_ADDRESS
M=D  // save the address value for use later
//////////////////////////////////////
(CHECK_KEYBOARD)
// "Whenever a key is pressed on the physical keyboard, its 16-bit ASCII code appears in RAM[24576] 
// When no key is pressed, the code 0 appears in this location"

@KBD  // this computer also uses symbol KBD predefined at address 24576 (0x6000)
D=M  // get the value in the keyboard RAM location 

@FILL_BLACK
D;JGT  // if any keypress (implies value >0), jumps to fill black section

@FILL_WHITE
D;JEQ // else only jumps to fill white if no keypress

//////////////////////////////////////
(FILL_BLACK)
@FILL_VALUE
M=-1  // -1 represented by 11111111111111 in 2s complement, generates 16 black pixels
@FILL_SCREEN
0;JMP  // now that we know what fill value is, go to fill screen

//////////////////////////////////////
(FILL_WHITE)
@FILL_VALUE
M=0  // 0 represention (16 0s) generates 16 white pixels
@FILL_SCREEN
0;JMP

//////////////////////////////////////
(FILL_SCREEN)
@FILL_VALUE
D=M  // store data of fill_value into data register for use below

@SCREEN_START_ADDRESS
A=M  // get address to start filling the 16 bits representing the first "word" of screen memory map
M=D  // fill with the fill_value from above

@SCREEN_START_ADDRESS
D=M+1 // get the next "word" address to see how many "words" left in calc below
M=M+1 // move on to the next "word" of the screen map, whose address is +1 from the address before it
A=M // unsure if this line is needed

@KBD
D=A-D // calc the difference between keyboard address and current screen "word" address

@FILL_SCREEN
D;JGT // if the difference is zero, screen has been filled. 
// this only works because in this computer, kbd address follows directly after screen

//////////////////////////////////////
@LOOP  // loop back to start of program
0;JMP