clear
./compile.sh

fileA="out_good.txt"

fileB="out_test.txt"

t=0
f=0
tedad=20
for i in {1..$tedad}
do
	./good.sh
	./test.sh
 #      cmp --silent $old $new || t++
done

f=$tedad-$t
echo "false = $t"
echo "true = $f"
#pause

rm out_good.txt
rm out_test.txt
rm rad_inp.txt
rm good.exe
rm test.exe;