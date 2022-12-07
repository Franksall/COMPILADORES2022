.data
var_x:    .word      0:1
.text

main:
.data
var_x:    .word      0:1
.text

main:

sw  $fp  0($sp)
addiu  $sp  $sp-4

li  $a0,  5

sw  $a0  0($sp)
addiu  $sp  $sp-4

jal  suma

la  $t0,  var_x
sw  $a0,  0($t0)

li $v0, 1
syscall

li $v0, 10
syscall

sw  $a0,  0($sp)
addiu  $sp,  $sp,  -4


sw  $a0,  0($sp)
addiu  $sp,  $sp,  -4


move  $fp  $sp  

suma:
lw  $a0,  8($sp)

addiu  $sp,  $sp,  4

lw  $ra  4($sp)
addiu  $sp  $sp  12
lw  $fp  0($sp)
jr  $ra