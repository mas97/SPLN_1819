# Tabela Periódica:
https://data.opendatasoft.com/explore/dataset/periodic-table%40datastro/information/

# Symbols extraction:
cat periodic-table.csv | tail +2 | cut --delimiter ';' -f 2 | sort > symbols.txt
