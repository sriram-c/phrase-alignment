rm grouping-eng
rm err
while IFS=$'\t' read -r -a myArray
do
 	echo "############${myArray[0]}###########" 
 	echo "############${myArray[0]}###########" >> err
	echo '------------' >> grouping-eng
	python align-new1.py output-uniq-sen/${myArray[0]} sen-split-new/${myArray[1]} root  >> grouping-eng 2>>err
done < all-file-list1
