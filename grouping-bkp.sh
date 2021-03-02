rm grouping-out
rm err
while IFS=$'\t' read -r -a myArray
do
 	echo "############${myArray[0]}###########" 
 	echo "############${myArray[0]}###########" >> err
	python align-new1.py output-uniq-sen/${myArray[0]} sen-split/${myArray[1]} root  1>> grouping-out 2>>err
	echo '----------------' >>  grouping-out 

done < jnk1
#list-all-files
