
echo "############1###########" >> output
#python $HOME_phrase_alignment/align-new1.py $HOME_phrase_alignment/uniq-hnd-translation/0001-wx $HOME_phrase_alignment/eng-hnd-grp-translation/0001 11    hnd_root_list  1> tmp 2>>err
python $HOME_phrase_alignment/align-new1.py $1 $2 11    hnd_root_list  1> tmp 2>>err
head -n 1 tmp > eng_sen
tail -n -4 tmp | head -n 1 | wx_utf8 > hnd_sen
tail -n -3 tmp | head -n 1  > eng_ch
tail -n -2 tmp | wx_utf8 > hnd_ch

cat eng_sen hnd_sen eng_ch hnd_ch >> output

python convert_csv_to_html.py output > output.html
