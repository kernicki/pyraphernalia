#!/bin/bash

test_dir="./lsequels/tests/__temp_tests/"
mkdir -p $test_dir

# with padding; dot delimiter
ext1="ext1"
filename1="file1."
for i in {-150..0100}
do
    path=$test_dir$filename1$i.$ext1
    touch $path
done

# make gaps
rm "$test_dir$filename1"{0088..0095}."$ext1"
rm "$test_dir$filename1"0050."$ext1"


# no padding; _ delimit
ext1="ext2"
filename1="file2.0005_"
for i in {9985..10000}
do
    path=$test_dir$filename1$i.$ext1
    touch $path
done
# make gaps
rm "$test_dir$filename1"9995."$ext1"


# no insane padding; - delimit
ext1="ext3"
filename1="f0005-"
for i in {00000000985..00000001000}
do
    path=$test_dir$filename1$i.$ext1
    touch $path
done
# make gaps
#rm "$filename1"{0088..0095}."$ext1"
