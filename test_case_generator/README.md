# test case generator 
 this script can generate random test cases,
 this test cases can be used for [quera](https://quera.ir/dashboard/) judge

## how does it work?
+ unfortunately (or fortunately) it not works on windows 
+ you need to have python3 installed (version >= 3.6)
+ you have to manually open `gen.py` and config it 
+ then you should just run 	`python3 gen.py` and wait (or maybe enter inputs, base on your config)

## what should i config?
 in `gen.py` there are 3 things to config:

### (**essential**) `solution1` and `solution2`: how to run two solutions of your program 
 + first you should copy solution(s) near gen.py
 + if you have only one solution *(not recommended)* you can set solution2 same as solution1 
 + how to set? 
  	1. for example solution1 is a python file named `sol1.py`, we write: `solution1 = "python3 sol1.py"`
	2. and solution2 is a compiled binary named `a.out`: we write `solution2 = "./a.out"`
	3. for java files (assume `A.java`), you sould compile it and write: `solution1 = "java A"`

### (*optional*)  number of test cases
 + you should set the `END` variable to number of test cases you want

### (**essential**) algorithm of create random 	
 + the program need to know, how to generate random input 
 + you should **rewrite** `input_rand()` depends on question structore in every question
 + you can also replace `input_rand()` with `input()` to handle manual input (call `input()` instead of `input_rand()`)

### (*optional*) path of output 
 + you can also change input folder and output folder to save test cases 
 + but its not recommended to split them, in and out folder should be near


  