# Use RegEx to discern the badly formatted prerequisites 

##  Sequences: 
> CSE 103. A Practical Introduction to Probability and Statistics (4)
> Prerequisites: MATH **20A-B** and MATH 184A or CSE 21 or MATH 154;

> BIPN 106. Comparative Physiology (4)
> Prerequisites: BILD 2, CHEM **6A-B-C**.

##  Comma ',' as "and"
> MATH 111A. Mathematical Modeling I (4)
> Prerequisites: MATH 20D, MATH 18 or MATH 20F or MATH 31AH, and MATH 109 or MATH 31CH.
- 捕捉： `“, [A-Z]+ [0-9]+[A-Z]*” // 逗号后面直接跟course `

# Concurrent enrollment  (CSE重灾区)
> CSE 12 Prereq: "...**and** concurrent enrollment with CSE 15L"
- The *"and"* here may result in cycles in the graph. Must discern .
- 捕捉：被and分割出来的substring里有“concurrent”直接跳过

##  偷懒写法 Omitted subject name:
> BILD 2 or 3

## 逗号隔开的偷懒写法 Omitted subject name, separated by comma (PHYS重灾区):
> PHYS 1BL. Electricity and Magnetism Laboratory (2)
> Prerequisites: **PHYS 1A or 2A, 1AL or 2BL**, and MATH 10B or 20B.

## Outdated Courses
- courses are are outdated or renumbered 
- (eg. MATH 176 == CSE 100, but the former is no longer offered)

Tricky situations {

    One of xxxxx

    Any two of xxxxx


}

LIFE IS SHORT, I NEED PYTHON!!!!