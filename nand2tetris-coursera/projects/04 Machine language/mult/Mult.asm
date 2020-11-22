// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

   @i  // set i=1 for i variable (in some memory location)
   M=1
   @R2 // set R2=0
   M=0

(LOOP)
   @i
   D=M  // set data register to value of i
   @R0
   D=D-M  // calculate (data of value i) minus R0
   @END
   D;JGT  // if i minus R0 is >0, jump to END (loop is over)
   
   @R1
   D=M  // set data register to value of R1
   @R2
   M=M+D  // increase R2 by value of D, which is R1

   @i
   M=M+1  // increase i
   
   @LOOP
   0;JMP  // repeat the loop

(END)  // infinite loop that keeps jumping to @END (itself)
   @END
   0; JMP