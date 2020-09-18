#!/bin/sh
clear

find . -name '*.class' -delete
rm -r sandbox > /dev/null 2>&1

mkdir sandbox

echo "copying files"
cp junit-jars/*.jar sandbox/
cp -r toTest/* sandbox/
cp -r tests/project/* sandbox/ > /dev/null 2>&1 || echo "project folder is empty"
cp tests/test/* sandbox/


cd sandbox/

echo "comiling project"
javac -cp .:junit.jar *.java || exit
echo "compile complete"

java -cp .:junit.jar:j2.jar  org.junit.runner.JUnitCore MyTest || exit
echo "run complete"

cd ..

echo "deleting sandbox"
find . -name '*.class' -delete
rm -r ./sandbox

echo "updating zip file"
rm t.zip > /dev/null 2>&1

cd tests
zip -r ../t.zip *

