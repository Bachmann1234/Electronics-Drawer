EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L sitstandtimercircuit-rescue:.56-7segment-backpack-sitstandlib U4
U 1 1 603AC37D
P 7700 5400
F 0 "U4" H 8228 5492 50  0000 L CNN
F 1 ".56-7segment-backpack" H 8228 5401 50  0000 L CNN
F 2 "sitstandtimercircuit:7segmentbackpack" H 7700 5400 50  0001 C CNN
F 3 "" H 7700 5400 50  0001 C CNN
	1    7700 5400
	1    0    0    -1  
$EndComp
$Comp
L sitstandlib:DS3231 U3
U 1 1 603ACDFB
P 9900 5450
F 0 "U3" H 10328 5351 50  0000 L CNN
F 1 "DS3231" H 10328 5260 50  0000 L CNN
F 2 "sitstandtimercircuit:RTC" H 9700 5450 50  0001 C CNN
F 3 "" H 9700 5450 50  0001 C CNN
	1    9900 5450
	-1   0    0    1   
$EndComp
$Comp
L sitstandlib:Feather32u4 U1
U 1 1 603ADD31
P 4550 3250
F 0 "U1" H 4550 3465 50  0000 C CNN
F 1 "Feather32u4" H 4550 3374 50  0000 C CNN
F 2 "sitstandtimercircuit:Feather" H 4550 3300 50  0001 C CNN
F 3 "" H 4550 3300 50  0001 C CNN
	1    4550 3250
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D2
U 1 1 603AF248
P 2450 3350
F 0 "D2" H 2443 3567 50  0000 C CNN
F 1 "LED" H 2443 3476 50  0000 C CNN
F 2 "LED_THT:LED_D5.0mm" H 2450 3350 50  0001 C CNN
F 3 "~" H 2450 3350 50  0001 C CNN
	1    2450 3350
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D1
U 1 1 603AFEC7
P 2450 2750
F 0 "D1" H 2443 2967 50  0000 C CNN
F 1 "LED" H 2443 2876 50  0000 C CNN
F 2 "LED_THT:LED_D5.0mm" H 2450 2750 50  0001 C CNN
F 3 "~" H 2450 2750 50  0001 C CNN
	1    2450 2750
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_Push_SPDT SW1
U 1 1 603B4C8C
P 6950 4300
F 0 "SW1" H 6950 4585 50  0000 C CNN
F 1 "SW_Push_SPDT" H 6950 4494 50  0000 C CNN
F 2 "sitstandtimercircuit:button" H 6950 4300 50  0001 C CNN
F 3 "~" H 6950 4300 50  0001 C CNN
	1    6950 4300
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 603B5CCD
P 2800 3500
F 0 "R2" H 2870 3546 50  0000 L CNN
F 1 "470" H 2870 3455 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 2730 3500 50  0001 C CNN
F 3 "~" H 2800 3500 50  0001 C CNN
	1    2800 3500
	1    0    0    -1  
$EndComp
$Comp
L Device:R R3
U 1 1 603B680A
P 6450 4150
F 0 "R3" H 6520 4196 50  0000 L CNN
F 1 "10k" H 6520 4105 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 6380 4150 50  0001 C CNN
F 3 "~" H 6450 4150 50  0001 C CNN
	1    6450 4150
	1    0    0    -1  
$EndComp
$Comp
L Device:R R1
U 1 1 603B6F10
P 3300 2900
F 0 "R1" H 3370 2946 50  0000 L CNN
F 1 "20" H 3370 2855 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 3230 2900 50  0001 C CNN
F 3 "~" H 3300 2900 50  0001 C CNN
	1    3300 2900
	1    0    0    -1  
$EndComp
$Comp
L sitstandlib:Sonar-rcwl-1601 U5
U 1 1 603B8F94
P 5800 2800
F 0 "U5" V 5285 2554 50  0000 C CNN
F 1 "Sonar-rcwl-1601" V 5376 2554 50  0000 C CNN
F 2 "sitstandtimercircuit:sonar" H 5800 2800 50  0001 C CNN
F 3 "" H 5800 2800 50  0001 C CNN
	1    5800 2800
	1    0    0    -1  
$EndComp
Wire Wire Line
	2800 3350 2600 3350
Wire Wire Line
	2600 2750 3300 2750
Wire Wire Line
	7150 4500 7150 4400
Wire Wire Line
	4850 4500 7150 4500
Wire Wire Line
	6450 4300 6750 4300
Wire Wire Line
	5750 3000 5750 4000
Wire Wire Line
	5750 4000 4850 4000
Wire Wire Line
	4850 4100 5850 4100
Wire Wire Line
	5850 4100 5850 3000
NoConn ~ 4250 3500
NoConn ~ 4250 3300
NoConn ~ 4250 3700
NoConn ~ 4250 4000
NoConn ~ 4250 4100
NoConn ~ 4250 4200
NoConn ~ 4250 4300
NoConn ~ 4250 4400
NoConn ~ 4250 4500
NoConn ~ 4250 4600
NoConn ~ 4850 3700
NoConn ~ 4850 3800
NoConn ~ 4850 3900
NoConn ~ 4850 4200
NoConn ~ 4850 4300
NoConn ~ 4850 4400
NoConn ~ 4850 4600
NoConn ~ 9550 5350
NoConn ~ 9650 5350
NoConn ~ 9750 5350
NoConn ~ 9850 5350
NoConn ~ 4250 4700
NoConn ~ 7150 4200
$Comp
L sitstandtimercircuit-rescue:.56-7segment-backpack-sitstandlib U2
U 1 1 603A9EDB
P 5600 5400
F 0 "U2" H 6128 5492 50  0000 L CNN
F 1 ".56-7segment-backpack" H 6128 5401 50  0000 L CNN
F 2 "sitstandtimercircuit:7segmentbackpack" H 5600 5400 50  0001 C CNN
F 3 "" H 5600 5400 50  0001 C CNN
	1    5600 5400
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0101
U 1 1 605830FD
P 1800 3150
F 0 "#PWR0101" H 1800 2900 50  0001 C CNN
F 1 "GND" H 1805 2977 50  0000 C CNN
F 2 "" H 1800 3150 50  0001 C CNN
F 3 "" H 1800 3150 50  0001 C CNN
	1    1800 3150
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0102
U 1 1 6058371C
P 1500 1900
F 0 "#PWR0102" H 1500 1750 50  0001 C CNN
F 1 "+3.3V" H 1515 2073 50  0000 C CNN
F 2 "" H 1500 1900 50  0001 C CNN
F 3 "" H 1500 1900 50  0001 C CNN
	1    1500 1900
	1    0    0    -1  
$EndComp
Wire Wire Line
	2800 3650 2800 3900
Wire Wire Line
	2800 3900 4250 3900
Wire Wire Line
	4250 3800 3300 3800
Wire Wire Line
	3300 3800 3300 3050
Wire Wire Line
	4250 3400 3550 3400
Wire Wire Line
	3550 3400 3550 1900
Wire Wire Line
	3550 1900 3350 1900
Wire Wire Line
	1800 3150 1900 3150
Wire Wire Line
	3100 3150 3100 3600
Wire Wire Line
	3100 3600 4250 3600
Wire Wire Line
	2300 3350 2000 3350
Wire Wire Line
	2000 3350 2000 3150
Connection ~ 2000 3150
Wire Wire Line
	2000 3150 2100 3150
Wire Wire Line
	2300 2750 2100 2750
Wire Wire Line
	2100 2750 2100 3150
Connection ~ 2100 3150
Wire Wire Line
	7650 5350 7650 5100
Wire Wire Line
	7650 5100 2250 5100
Wire Wire Line
	2250 5100 2250 3150
Connection ~ 2250 3150
Wire Wire Line
	10150 5350 10150 2450
Wire Wire Line
	10150 2450 2750 2450
Wire Wire Line
	2750 2450 2750 3150
Connection ~ 2750 3150
Wire Wire Line
	2750 3150 2850 3150
Wire Wire Line
	6450 4000 6450 2650
Wire Wire Line
	6450 2650 2850 2650
Wire Wire Line
	2850 2650 2850 3150
Connection ~ 2850 3150
Wire Wire Line
	2850 3150 3100 3150
Wire Wire Line
	2650 3150 2650 2150
Wire Wire Line
	2650 2150 6750 2150
Wire Wire Line
	6750 2150 6750 3200
Wire Wire Line
	6750 3200 5950 3200
Wire Wire Line
	5950 3200 5950 3000
Connection ~ 2650 3150
Wire Wire Line
	2650 3150 2750 3150
Wire Wire Line
	5650 3000 5650 3650
Wire Wire Line
	5650 3650 5100 3650
Wire Wire Line
	5100 3650 5100 1700
Wire Wire Line
	5100 1700 3350 1700
Wire Wire Line
	3350 1700 3350 1900
Connection ~ 3350 1900
Wire Wire Line
	3350 1900 2100 1900
Wire Wire Line
	5450 5250 1600 5250
Wire Wire Line
	1600 5250 1600 1900
Connection ~ 1600 1900
Wire Wire Line
	1600 1900 1500 1900
Wire Wire Line
	10250 5350 10250 1600
Wire Wire Line
	10250 1600 1850 1600
Wire Wire Line
	1850 1600 1850 1900
Connection ~ 1850 1900
Wire Wire Line
	1850 1900 1700 1900
Wire Wire Line
	7550 5200 7100 5200
Wire Wire Line
	7100 5200 7100 5950
Wire Wire Line
	7100 5950 1300 5950
Wire Wire Line
	1300 5950 1300 1400
Wire Wire Line
	1300 1400 1700 1400
Wire Wire Line
	1700 1400 1700 1900
Connection ~ 1700 1900
Wire Wire Line
	1700 1900 1600 1900
Wire Wire Line
	5550 5350 5550 5000
Wire Wire Line
	5550 5000 1700 5000
Wire Wire Line
	1700 5000 1700 2800
Wire Wire Line
	1700 2800 1900 2800
Wire Wire Line
	1900 2800 1900 3150
Connection ~ 1900 3150
Wire Wire Line
	1900 3150 2000 3150
Wire Wire Line
	7550 5200 7550 5350
Wire Wire Line
	5450 5250 5450 5350
Wire Wire Line
	4850 4800 5650 4800
Wire Wire Line
	5650 4800 5650 5350
Wire Wire Line
	5650 4800 7750 4800
Wire Wire Line
	7750 4800 7750 5350
Connection ~ 5650 4800
Wire Wire Line
	7750 4800 9950 4800
Wire Wire Line
	9950 4800 9950 5350
Connection ~ 7750 4800
Wire Wire Line
	4850 4700 5750 4700
Wire Wire Line
	5750 4700 5750 5350
Wire Wire Line
	5750 4700 7850 4700
Wire Wire Line
	7850 4700 7850 5350
Connection ~ 5750 4700
Wire Wire Line
	7850 4700 10050 4700
Wire Wire Line
	10050 4700 10050 5350
Connection ~ 7850 4700
Wire Wire Line
	2100 3150 2250 3150
$Comp
L power:PWR_FLAG #FLG0101
U 1 1 60631CA4
P 2100 1850
F 0 "#FLG0101" H 2100 1925 50  0001 C CNN
F 1 "PWR_FLAG" H 2100 2023 50  0000 C CNN
F 2 "" H 2100 1850 50  0001 C CNN
F 3 "~" H 2100 1850 50  0001 C CNN
	1    2100 1850
	1    0    0    -1  
$EndComp
Wire Wire Line
	2100 1850 2100 1900
Connection ~ 2100 1900
Wire Wire Line
	2100 1900 1850 1900
Wire Wire Line
	2250 3150 2300 3150
$Comp
L power:PWR_FLAG #FLG0102
U 1 1 6063FA23
P 2300 3100
F 0 "#FLG0102" H 2300 3175 50  0001 C CNN
F 1 "PWR_FLAG" H 2300 3273 50  0000 C CNN
F 2 "" H 2300 3100 50  0001 C CNN
F 3 "~" H 2300 3100 50  0001 C CNN
	1    2300 3100
	1    0    0    -1  
$EndComp
Wire Wire Line
	2300 3150 2300 3100
Connection ~ 2300 3150
Wire Wire Line
	2300 3150 2650 3150
NoConn ~ 4250 4800
NoConn ~ -9600 -7550
$EndSCHEMATC
