import re

file = open('listener.ora', 'r+')

listener_ora = file.read()

easy_connects = {}
# list_re = "^(\w+?)\s?=.*?SID_DESC\s?=\s?(.+?)\).*?SID_NAME\s?=\s?(\d+?)\).* ?ORACLE_HOME\s?=\s?(.+?)\)"
# list_re = "^\.*SID_DESC\s?=\s?(.+?)\).*?SID_NAME\s?=\s?(\d+?)\).* ?ORACLE_HOME\s?=\s?(.+?)\)"
# listener_ora = "   SID_DESC = (GLOBAL_DBNAME = testdb1)(SID_NAME = testdb1)(ORACLE_HOME = /u01/app/oracle/product/10.2.0/db_1)"


#list_re = "\(\s*(?:SID_NAME)\s*=\s*\w+\s*\)"
list_re = "\(\s*(?:SID_DESC)\s*=\s*\.*\s*\)"
print(re.findall(list_re, listener_ora, re.M + re.S))
#print(re.match(list_re, listener_ora, re.M + re.S))
print(re.finditer(list_re, listener_ora, re.M + re.S))

filenames = re.findall('\w+\.(?:txt|php|css)', listener_ora)
print(filenames)
for match in re.finditer(list_re, listener_ora, re.M + re.S):
     t = match.groups()
     #easy_connects[t[0]] = "%s:%s/%s" % t[1:]
     print(t)
     print(match)


print (easy_connects)