for f in sen-split/*
do
	utf8_wx $f | perl -i.bak -pe 's/[^[:ascii:]]//g' > $f-wx
	
done
