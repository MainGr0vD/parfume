import re
str = "12 parfumeurs FRANCAIS AMBOISE parfume (m) 101ml"
str = re.sub('[0-9]{0,4}ml','',str)
str = re.sub(' parfume ',' ',str)
print(str)