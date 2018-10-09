# Clean file with words
cat words.txt | sed 's/\t/;/g' | cut -d ';' -f 2 | iconv -f latin1 -t ascii//TRANSLIT | sed -e 'y/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz/' | sort | uniq
