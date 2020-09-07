# test case generator 
 this script can generate random test cases,
 this test cases can be used for [quera](https://quera.ir/dashboard/) judge

## how does it work?
+ it not works on windows (need bash pipe)
+ install python 3 (version >= 3.6)
+ open `gen.py` and re-write `input_rand` function 
+  run `./gen.py --help` and read help



## example

```bash
./gen.py delete
./gen.py create --sol "python -c 'print(1)'" --sol "echo 1" -n 10
./gen.py validate --sol "python -c 'print(1)'"
```

