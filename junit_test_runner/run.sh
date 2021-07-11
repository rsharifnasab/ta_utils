#!/bin/sh

set -o errexit
set -o nounset

start_point="$(pwd)"

when_fail="--allow"

if [ $# -ge 1 ] && [ -n "$1" ]
then
    when_fail="$1"
fi

try_delete(){
    rm -r "$1" > /dev/null 2>&1 || true
}

clean() {
    cd "$start_point"
    find . -name '*.class' -delete
    try_delete "sandbox"
}

terminate(){
    clean
    exit
}

test_fail(){
    if [ "$when_fail" = "--fail" ] || [ "$when_fail" = "-f" ]; then
        terminate
    else [ "$when_fail" = "--allow" ] || [ "$when_fail" = "-a" ];
        true
    fi;
}


clear #screen
clean

mkdir sandbox

echo "-> copying files to sandbox"
cp junit-jars/*.jar sandbox/
cp -r tests/project/* sandbox/ > /dev/null 2>&1 \
    || echo "-> project folder is empty"
cp -r sol/* sandbox/
cp -r tests/test/* sandbox/

cd sandbox/

echo "-> comiling project"
find . -name "*.java" > sources.txt
javac --release 11 -cp .:junit-platform-console.jar:hamcrest.jar @sources.txt || terminate

echo "-> running tests"

for testFile in ./*Test.java; do
  className="$(basename "$testFile" .java)"
  echo "--> testing \"$className\""
  #  java -cp .:junit.jar:hamcrest.jar org.junit.runner.JUnitCore \
  #      "$className"  || test_fail


  #  java -cp .:junit.jar:hamcrest.jar MyRunner

  java -jar junit-platform-console.jar --class-path "." --scan-class-path

  break
done

echo "-> run complete"
cd ../


echo "-> create solution zip"
try_delete "sol.zip"
(
    cd sol || terminate
    zip -q -r ../sol.zip ./
)


echo "-> update tests zip"
try_delete "tests.zip"
(
    cd tests || terminate
    zip -q -r ../tests.zip ./
)


echo "-> cleaning up."
clean
echo "-> Done"
