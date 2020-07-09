clear
./compile.sh

fileA="out_good.txt"

fileB="out_test.txt"

t=0
f=0
tedad=0
for i in {1..20}
do

	./good.sh
	./test.sh
     #   echo -e "\ngood : "
     #   cat out_good.txt
     #   echo -e "\ntest : "
      #  cat out_test.txt
        tedad=$(($tedad+1))
        cmp --silent $fileA $fileB &&  t=$(($t+1))
done

f=$(($tedad-$t))
echo -e "\nfalse = $f"
echo "true = $t"

rm out_good.txt
rm out_test.txt
rm rad_inp.txt
rm good.exe
rm test.exe