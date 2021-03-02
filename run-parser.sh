stanford_parser_four_path=`echo $HOME_anu_test/Parsers/stanford-parser/stanford-parser-4.0.0`
java -mx1000m -cp $stanford_parser_four_path/*:  edu.stanford.nlp.parser.lexparser.LexicalizedParser -retainTMPSubcategories -outputFormat "xmlTree"  $stanford_parser_four_path/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz $* 1> $1-parsed.xml 2>$1-parse.log
