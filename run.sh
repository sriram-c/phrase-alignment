rm output
counter=1
for i in jnk-uniq1/*
do
	echo $i
	echo '############'$counter'###########' >> output
	python align-new1.py $i >> output
	counter=$((counter+1))
done
