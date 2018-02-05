#!/usr/bin/env python
# coding=utf-8
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


# 如果直接安装 python-ladp 出现错误，就需要 sudo apt-get install python-dev libldap2-dev libsasl2-dev libssl-dev
# to be able to import ldap run pip install python-ldap

import ldap

LDAP_SERVER="ldap://192.168.1.11:389"


def get_ldap_connect(ldap_server):
    # connect = ldap.open(ldap_server)
    connect = ldap.initialize(ldap_server)

    return connect


def ldap_search_by_username(connect,username):
    '''
    根据 ladp 的配置不同选取，不同筛选条件
    :param connect: 
    :param username: 
    :return: 
    '''
    searchFilter = "uid=" + username
    searchFilter = "cn=" + username
    base_dn = "dc=triangle,dc=com"
    res = connect.search_s(base_dn, ldap.SCOPE_SUBTREE, searchFilter)
    dn_list = []
    for dn, entry in res:
        dn_list.append(dn)

    return dn_list


def ldap_authentication(username, password):

    connect = get_ldap_connect(LDAP_SERVER)
    dn_list = ldap_search_by_username(connect, username)
    # print dn_list
    for user_dn in dn_list:
        try:
            connect.bind_s(user_dn, password)
            connect.unbind_s()
            return True
        except ldap.LDAPError:
            continue
    connect.unbind_s()
    return False


def ldap_authentication_direct(username,password):
    ldap_server = LDAP_SERVER

    # the following is the user_dn format provided by the ldap server
    user_dn = "uid=" + username + ",ou=hadoop,dc=triangle,dc=com"
    # adjust this to your base dn for searching
    base_dn = "dc=triangle,dc=com"
    # connect = ldap.open(ldap_server)
    connect = ldap.initialize(ldap_server)
    search_filter = "uid=" + username
    try:
        # if authentication successful, get the full user data
        connect.bind_s(user_dn, password)
        result = connect.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
        # return all user data results
        connect.unbind_s()
        # print result
        return True

    except ldap.LDAPError:
        connect.unbind_s()
        # print "authentication error"
        return False



if __name__ == "__main__":

    username = "sdfasdfasdf"

    password = "fasdfasdfas"


    print ldap_authentication(username, password)

    connect = get_ldap_connect(LDAP_SERVER)
    dn_list = ldap_search_by_username(connect, username)
    print dn_list

    pass
