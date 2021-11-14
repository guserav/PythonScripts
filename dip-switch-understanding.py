# Verifying the values of http://www.avr-asm-tutorial.net/avr_de/apps/tasten_schalter_adc/tasten_schalter.pdf
r0 = 4.7
rn = [68., 27., 10., 2.4]

V_max = 1024

for i in range(2 ** len(rn)):
    l_ = 0
    for j in range(len(rn)):
        if (1 << j) & i:
            l_ += 1/rn[j]
    v_out = V_max
    if l_ != 0:
        v_out = V_max * r0 / (r0 + 1 / l_)
    print("{}: {}".format(i, v_out))
