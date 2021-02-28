#!/bin/sh

set -e

start_point="$(pwd)"


try_delete(){
    rm -r "$1" > /dev/null 2>&1 || true
}


clean() {
    cd "$start_point"
    try_delete "sandbox"
    exit
}

clear

find . -name '*.class' -delete
try_delete "sandbox"

mkdir sandbox

echo "copying files to sandbox"
cp junit-jars/*.jar sandbox/
cp -r tests/project/* sandbox/ > /dev/null 2>&1 || echo "project folder is empty"
cp -r toTest/* sandbox/
cp -r tests/test/* sandbox/

cd sandbox/

echo "comiling project"
find . -name "*.java" > sources.txt
javac -cp .:junit.jar @sources.txt || clean


echo "running MyTest"
for testFile in ./*Test.java; do
    className="$(basename "$testFile" .java)"
    echo "class name : \"$className\""
    java -cp .:junit.jar:j2.jar org.junit.runner.JUnitCore \
        "$className"  \
        || clean
done
echo "run complete"

cd ..

echo "deleting sandbox"
find . -name '*.class' -delete
rm -r ./sandbox





echo "updating solution file"
try_delete "sol.zip"
cd toTest || clean
zip -r ../sol.zip ./
cd ..


echo "updating tests zip file"
try_delete "tests.zip"
cd tests || clean
zip -r ../tests.zip ./
cd ..


clean
