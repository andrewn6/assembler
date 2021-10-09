lw r4, 176(r0)
lw r3, 177(r0)
sub r2, r4, r1
bez r2, 8
sw r1, 252(r0)
bez r0, -8
add r1, r1, r3
sll r0, r0, r0
bez r0, -2
