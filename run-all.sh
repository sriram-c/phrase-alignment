rm output
rm err
while IFS=$'\t' read -r -a myArray
do
 	echo "############${myArray[0]}###########" 
 	echo "############${myArray[0]}###########" >> output
 	echo "############${myArray[0]}###########" >> err
	python align-new1.py uniq-hnd-translation/${myArray[0]}-wx eng-hnd-grp-translation/${myArray[1]} ${myArray[2]}    root  1> tmp 2>>err
	head -n 1 tmp > eng_sen
	tail -n -4 tmp | head -n 1 | wx_utf8 > hnd_sen
	tail -n -3 tmp | head -n 1  > eng_ch
	tail -n -2 tmp | wx_utf8 > hnd_ch

	cat eng_sen hnd_sen eng_ch hnd_ch >> output
	echo 'done'


done < $1
python convert_csv_to_html.py output > output.html
