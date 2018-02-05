#!/usr/bin/python
# coding:UTF-8

import re

if __name__ == '__main__':


    line = "Cats 12 are smarter than dogs"

    # searchObj = re.search(r'(.*) are (.*?) .*', line)
    # searchObj = re.search(r'(.*) are (.*)', line)
    searchObj = re.search(r'(.*)1(2 a.*?)(a|g|s)$', line)

    if searchObj:
        print "searchObj.group()  : |%s|" % searchObj.group()
        print "searchObj.group(1) : |%s|" % searchObj.group(1)
        print "searchObj.group(2) : |%s|" % searchObj.group(2)
        print "searchObj.group(2) : |%s|" % searchObj.group(3)
    else:
        print "Nothing found!!"


    find_res = re.findall(r'(.*)1(2 a.*?)',line)
    print find_res
    print find_res[0][0]
    print find_res[0][1]