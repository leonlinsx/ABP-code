// push argument 1
@ARG // code line 0
D=M // code line 1
@1 // code line 2
A=D+A // code line 3
D=M // code line 4
@SP // code line 5
A=M // code line 6
M=D // code line 7
@SP // code line 8
M=M+1 // code line 9
// pop pointer 1
@R4 // code line 10
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
// push constant 0
@0 // code line 21
D=A // code line 22
@SP // code line 23
A=M // code line 24
M=D // code line 25
@SP // code line 26
M=M+1 // code line 27
// pop that 0
@THAT // code line 28
D=M // code line 29
@0 // code line 30
A=D+A // code line 31
D=A // code line 32
@R13 // code line 33
M=D // code line 34
@SP // code line 35
M=M-1 // code line 36
A=M // code line 37
D=M // code line 38
@R13 // code line 39
A=M // code line 40
M=D // code line 41
// push constant 1
@1 // code line 42
D=A // code line 43
@SP // code line 44
A=M // code line 45
M=D // code line 46
@SP // code line 47
M=M+1 // code line 48
// pop that 1
@THAT // code line 49
D=M // code line 50
@1 // code line 51
A=D+A // code line 52
D=A // code line 53
@R13 // code line 54
M=D // code line 55
@SP // code line 56
M=M-1 // code line 57
A=M // code line 58
D=M // code line 59
@R13 // code line 60
A=M // code line 61
M=D // code line 62
// push argument 0
@ARG // code line 63
D=M // code line 64
@0 // code line 65
A=D+A // code line 66
D=M // code line 67
@SP // code line 68
A=M // code line 69
M=D // code line 70
@SP // code line 71
M=M+1 // code line 72
// push constant 2
@2 // code line 73
D=A // code line 74
@SP // code line 75
A=M // code line 76
M=D // code line 77
@SP // code line 78
M=M+1 // code line 79
// sub
@SP // code line 80
M=M-1 // code line 81
A=M // code line 82
D=M // code line 83
A=A-1 // code line 84
M=M-D // code line 85
// pop argument 0
@ARG // code line 86
D=M // code line 87
@0 // code line 88
A=D+A // code line 89
D=A // code line 90
@R13 // code line 91
M=D // code line 92
@SP // code line 93
M=M-1 // code line 94
A=M // code line 95
D=M // code line 96
@R13 // code line 97
A=M // code line 98
M=D // code line 99
// label MAIN_LOOP_START
(FibonacciSeries$MAIN_LOOP_START)
// push argument 0
@ARG // code line 100
D=M // code line 101
@0 // code line 102
A=D+A // code line 103
D=M // code line 104
@SP // code line 105
A=M // code line 106
M=D // code line 107
@SP // code line 108
M=M+1 // code line 109
// if-goto COMPUTE_ELEMENT
@SP // code line 110
M=M-1 // code line 111
A=M // code line 112
D=M // code line 113
@FibonacciSeries$COMPUTE_ELEMENT // code line 114
D;JNE // code line 115
// goto END_PROGRAM
@FibonacciSeries$END_PROGRAM // code line 116
0;JMP // code line 117
// label COMPUTE_ELEMENT
(FibonacciSeries$COMPUTE_ELEMENT)
// push that 0
@THAT // code line 118
D=M // code line 119
@0 // code line 120
A=D+A // code line 121
D=M // code line 122
@SP // code line 123
A=M // code line 124
M=D // code line 125
@SP // code line 126
M=M+1 // code line 127
// push that 1
@THAT // code line 128
D=M // code line 129
@1 // code line 130
A=D+A // code line 131
D=M // code line 132
@SP // code line 133
A=M // code line 134
M=D // code line 135
@SP // code line 136
M=M+1 // code line 137
// add
@SP // code line 138
M=M-1 // code line 139
A=M // code line 140
D=M // code line 141
A=A-1 // code line 142
M=M+D // code line 143
// pop that 2
@THAT // code line 144
D=M // code line 145
@2 // code line 146
A=D+A // code line 147
D=A // code line 148
@R13 // code line 149
M=D // code line 150
@SP // code line 151
M=M-1 // code line 152
A=M // code line 153
D=M // code line 154
@R13 // code line 155
A=M // code line 156
M=D // code line 157
// push pointer 1
@R4 // code line 158
D=M // code line 159
@SP // code line 160
A=M // code line 161
M=D // code line 162
@SP // code line 163
M=M+1 // code line 164
// push constant 1
@1 // code line 165
D=A // code line 166
@SP // code line 167
A=M // code line 168
M=D // code line 169
@SP // code line 170
M=M+1 // code line 171
// add
@SP // code line 172
M=M-1 // code line 173
A=M // code line 174
D=M // code line 175
A=A-1 // code line 176
M=M+D // code line 177
// pop pointer 1
@R4 // code line 178
D=A // code line 179
@R13 // code line 180
M=D // code line 181
@SP // code line 182
M=M-1 // code line 183
A=M // code line 184
D=M // code line 185
@R13 // code line 186
A=M // code line 187
M=D // code line 188
// push argument 0
@ARG // code line 189
D=M // code line 190
@0 // code line 191
A=D+A // code line 192
D=M // code line 193
@SP // code line 194
A=M // code line 195
M=D // code line 196
@SP // code line 197
M=M+1 // code line 198
// push constant 1
@1 // code line 199
D=A // code line 200
@SP // code line 201
A=M // code line 202
M=D // code line 203
@SP // code line 204
M=M+1 // code line 205
// sub
@SP // code line 206
M=M-1 // code line 207
A=M // code line 208
D=M // code line 209
A=A-1 // code line 210
M=M-D // code line 211
// pop argument 0
@ARG // code line 212
D=M // code line 213
@0 // code line 214
A=D+A // code line 215
D=A // code line 216
@R13 // code line 217
M=D // code line 218
@SP // code line 219
M=M-1 // code line 220
A=M // code line 221
D=M // code line 222
@R13 // code line 223
A=M // code line 224
M=D // code line 225
// goto MAIN_LOOP_START
@FibonacciSeries$MAIN_LOOP_START // code line 226
0;JMP // code line 227
// label END_PROGRAM
(FibonacciSeries$END_PROGRAM)
