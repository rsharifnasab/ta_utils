#!/bin/sh
clear

find . -name '*.class' -delete
rm -r sandbox > /dev/null 2>&1

mkdir sandbox

echo "copying files to sandbox"
cp junit-jars/*.jar sandbox/
cp -r tests/project/* sandbox/ > /dev/null 2>&1 || echo "project folder is empty"
cp -r toTest/* sandbox/
cp -r tests/test/* sandbox/

cd sandbox/ || exit

echo "comiling project"
find . -name "*.java" > sources.txt
javac -cp .:junit.jar @sources.txt || exit

echo "running SampleTest"
java -cp .:junit.jar:j2.jar  org.junit.runner.JUnitCore SampleTest || exit

echo "running MyTest"
java -cp .:junit.jar:j2.jar  org.junit.runner.JUnitCore MyTest || exit
echo "run complete"

cd ..

echo "deleting sandbox"
find . -name '*.class' -delete
# rm -r ./sandbox

echo "updating zip file"
rm t.zip > /dev/null 2>&1

cd tests || exit
zip -r ../t.zip ./




