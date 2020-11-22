// push constant 0
@0 // code line 0
D=A // code line 1
@SP // code line 2
A=M // code line 3
M=D // code line 4
@SP // code line 5
M=M+1 // code line 6
// pop local 0
@LCL // code line 7
D=M // code line 8
@0 // code line 9
A=D+A // code line 10
D=A // code line 11
@R13 // code line 12
M=D // code line 13
@SP // code line 14
M=M-1 // code line 15
A=M // code line 16
D=M // code line 17
@R13 // code line 18
A=M // code line 19
M=D // code line 20
// label LOOP_START
(BasicLoop$LOOP_START)
// push argument 0
@ARG // code line 21
D=M // code line 22
@0 // code line 23
A=D+A // code line 24
D=M // code line 25
@SP // code line 26
A=M // code line 27
M=D // code line 28
@SP // code line 29
M=M+1 // code line 30
// push local 0
@LCL // code line 31
D=M // code line 32
@0 // code line 33
A=D+A // code line 34
D=M // code line 35
@SP // code line 36
A=M // code line 37
M=D // code line 38
@SP // code line 39
M=M+1 // code line 40
// add
@SP // code line 41
M=M-1 // code line 42
A=M // code line 43
D=M // code line 44
A=A-1 // code line 45
M=M+D // code line 46
// pop local 0
@LCL // code line 47
D=M // code line 48
@0 // code line 49
A=D+A // code line 50
D=A // code line 51
@R13 // code line 52
M=D // code line 53
@SP // code line 54
M=M-1 // code line 55
A=M // code line 56
D=M // code line 57
@R13 // code line 58
A=M // code line 59
M=D // code line 60
// push argument 0
@ARG // code line 61
D=M // code line 62
@0 // code line 63
A=D+A // code line 64
D=M // code line 65
@SP // code line 66
A=M // code line 67
M=D // code line 68
@SP // code line 69
M=M+1 // code line 70
// push constant 1
@1 // code line 71
D=A // code line 72
@SP // code line 73
A=M // code line 74
M=D // code line 75
@SP // code line 76
M=M+1 // code line 77
// sub
@SP // code line 78
M=M-1 // code line 79
A=M // code line 80
D=M // code line 81
A=A-1 // code line 82
M=M-D // code line 83
// pop argument 0
@ARG // code line 84
D=M // code line 85
@0 // code line 86
A=D+A // code line 87
D=A // code line 88
@R13 // code line 89
M=D // code line 90
@SP // code line 91
M=M-1 // code line 92
A=M // code line 93
D=M // code line 94
@R13 // code line 95
A=M // code line 96
M=D // code line 97
// push argument 0
@ARG // code line 98
D=M // code line 99
@0 // code line 100
A=D+A // code line 101
D=M // code line 102
@SP // code line 103
A=M // code line 104
M=D // code line 105
@SP // code line 106
M=M+1 // code line 107
// if-goto LOOP_START
@SP // code line 108
M=M-1 // code line 109
A=M // code line 110
D=M // code line 111
@BasicLoop$LOOP_START // code line 112
D;JNE // code line 113
// push local 0
@LCL // code line 114
D=M // code line 115
@0 // code line 116
A=D+A // code line 117
D=M // code line 118
@SP // code line 119
A=M // code line 120
M=D // code line 121
@SP // code line 122
M=M+1 // code line 123
