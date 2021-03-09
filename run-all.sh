rm output1
rm err
while IFS=$'\t' read -r -a myArray
do
 	echo "############${myArray[0]}###########" 
 	echo "############${myArray[0]}###########" >> output1
 	echo "############${myArray[0]}###########" >> err
	python align-new1.py output-uniq-sen/${myArray[0]}-wx sen-split-new/${myArray[1]} root  1> tmp 2>>err
	head -n 1 tmp > eng_sen
	tail -n -3 tmp | head -n 1 | wx_utf8 > hnd_sen
	tail -n -2 tmp | head -n 1  > eng_ch
	tail -n 1 tmp | wx_utf8 > hnd_ch

	cat eng_sen hnd_sen eng_ch hnd_ch >> output1
	echo 'done'

	#python align-new1.py output-uniq-sen/${myArray[0]} sen-split/${myArray[1]} root 1>> output1 2>> err

done < jnk1
python convert_csv_to_html.py output1 > output1.html
