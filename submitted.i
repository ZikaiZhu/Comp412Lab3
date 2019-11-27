//NAME: Zikai Zhu
//NETID: zz51
//SIM INPUT:
//OUTPUT: 1 1 2 3 5 8 13 21 34

// Comp412, Lab 2, block "test.i"

// This report block is a Lab2 test block that calculates the first nine Fibonacci numbers

//Initialize the first two elements
loadI 1 => r0
loadI 1 => r1

//Initialize some registers for storing the nine output 
loadI 1024 => r11
loadI 1028 => r21
loadI 1032 => r31
loadI 1036 => r41
loadI 1040 => r51
loadI 1044 => r61
loadI 1048 => r71
loadI 1052 => r81
loadI 1056 => r91

// calculate the Fibonacci numbers
add r0, r1 => r2
add r1, r2 => r3
add r2, r3 => r4
add r3, r4 => r5
add r4, r5 => r6
add r5, r6 => r7
add r6, r7 => r8

//Store the numbers to memory
store r0 => r11
store r1 => r21
store r2 => r31
store r3 => r41
store r4 => r51
store r5 => r61
store r6 => r71
store r7 => r81
store r8 => r91

//output the nine values
output 1024
output 1028
output 1032
output 1036
output 1040
output 1044
output 1048
output 1052
output 1056



