for f in output-uniq-sen/*
do
	utf8_wx $f | perl  -pe 's/[^[:ascii:]]//g' > $f-wx
done
