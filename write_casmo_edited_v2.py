#!/usr/bin/env python3

# 2/2/26 -> edited by afe to make into nuscale current design
enr =     [ 2.0, 2.65, 3.0, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0 ] #j

gdwt =    [     0,      2,      4,      6,      8] #i
density = [10.289, 10.229, 10.169, 10.109, 10.049] #i formula from pwr.equilibrium from Studsvik
rf =      [  1.00,   0.98,   0.96,   0.94,   0.92] #i reduction factor for U-235 in gad pins

gdpins = [0, 4, 8, 12, 16, 20, 24, 28] #number gd pins in a fuel assembly

gd_lfu = { #'x' = number of gd pins. LFU has octant symmetry. numbers in structure correspond
# with a pin type ID that's defined earlier in the input file (idk where?)
# usually 0 = water-filled 1 = standard fuel pin 2 = Gd pin

'28':"""LFU 
0
1 1
2 1 1
0 1 1 0
1 1 2 1 1
2 1 1 1 1 0
0 1 1 0 1 1 2
1 1 1 2 1 1 1 1
1 1 1 1 1 1 1 1 1""",

'24':"""LFU
0
1 1
1 1 2
0 1 1 0
1 1 1 1 2
1 2 1 1 1 0
0 1 1 0 1 1 1
1 1 1 1 2 1 1 1
1 1 1 1 1 1 1 1 1""",

'20':"""LFU
0
1 1
1 1 2
0 1 1 0
1 1 1 1 1
1 2 1 1 1 0
0 1 1 0 2 1 1
1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1""",

'16' :"""LFU
 0
 1 1
 1 1 2
 0 1 1 0
 1 1 1 1 1
 2 1 1 1 1 0
 0 1 1 0 2 1 1
 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1""", # I created this one

'12' :"""LFU
 0
 1 1
 1 1 1
 0 1 1 0
 2 1 1 1 1
 1 1 1 1 1 0
 0 1 1 0 2 1 1
 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1""", # I created this one

'8':"""LFU
 0
 1 1
 1 1 1
 0 1 1 0
 1 1 1 1 1
 1 1 2 1 1 0
 0 1 1 0 1 1 1
 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1""",     # cms test case

'4':"""LFU
0
1 1
1 1 1
0 1 1 0
1 1 1 1 2
1 1 1 1 1 0
0 1 1 0 1 1 1
1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1""",

'0':"""LFU
0
1 1
1 1 1
0 1 1 0
1 1 1 1 1
1 1 1 1 1 0
0 1 1 0 1 1 1
1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1"""}

shfile = 'run.sh'
for j in range(len(enr)):
    for i in range(len(gdwt)):
        for k in range(len(gdpins)):
            if gdwt[i] == 0 or gdpins[k] == 0:  #EDIT-fix this, creates a whole bunch of 0% gad cases
                continue
            name = f'{enr[j]}_{gdpins[k]}x{gdwt[i]}'
            filename = name + '.inp'
            with open(shfile, 'a') as af:
                af.write(f'/usr/local/neapps/casmo/bin/casmo4e {filename}\n')
            with open(filename, 'w') as wf:
                wf.write(f"""TTL *  17x17 PWR FA WITH GAD FOR NU-160
SIM '{name}'
TFU=1004.45 TMO=555.37 BOR=1900
PDE 80.6195 'KWL'
PRE 137.895

PWR 17 1.26 21.50
SPA 14.574,,, 8.14 / 304=100 *ZR-4

FUE 1 10.58 / {enr[j]}
FUE 2 {density[i]} / {enr[j]*rf[i]} 64016={gdwt[i]}

PIN 1 .410 .417 .475
PIN 2 .573 .613 / 'MOD' 'BOX'                         * Instrument tube
PIN 3 .573 .613 / 'MOD' 'BOX'                         * Guide tube
PIN 3 .434  .438  .485  .573  .613  /
      'AIC' 'AIR' 'CRS' 'MOD' 'BOX' // 1 'CR1' 'ROD'  * CR in guide tube

{gd_lfu[str(gdpins[k])]}

LPI
 2
 1 1
 1 1 1
 3 1 1 3
 1 1 1 1 1
 1 1 1 1 1 3
 3 1 1 3 1 1 1
 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1
DEP -75
S3C
STA
END""")
