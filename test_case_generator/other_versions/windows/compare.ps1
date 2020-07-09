./compile.ps1

$fileA = "out_good.txt"

$fileB = "out_test.txt"

$t = 0
$f = 0
$tedad = 20
For ($i=1; $i -le $tedad; $i++) 
{
	./good.ps1
	./test.ps1

	if ( (Get-FileHash $fileA).hash  -eq (Get-FileHash $fileB).hash)
	    {$t = $t+1}
}

$f = $tedad - $t
"false = $f"
"true = $t"
pause

rm out_good.txt
rm out_test.txt
rm rad_inp.txt
rm good.exe
rm test.exe


