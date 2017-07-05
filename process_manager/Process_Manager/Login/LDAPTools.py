# -*- coding: UTF-8 -*-
import sys, ldap
import ldap

SERVER_NAME = '10.0.14.2'
SERVER_PORT = 389
BASE_DN = 'ou=tech,dc=piaozhijia,dc=com'

def LDAPLogin(user,pwd):
        try:
            #验证用户
            conn = ldap.open(SERVER_NAME, SERVER_PORT)
            conn.protocol_version = ldap.VERSION3
            username = "cn=%s,ou=tech,dc=piaozhijia,dc=com" % (user)
            password = pwd
            conn.simple_bind_s(username, password)

            #获取用户信息
            searchScope = ldap.SCOPE_SUBTREE
            searchFilter = "cn=" + user
            resultID = conn.search(BASE_DN, searchScope, searchFilter, None)
            while 1:
                result_type, result_data = conn.result(resultID, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        dt={'result':True,'uid':result_data[0][1]['uid'][0],'sn':result_data[0][1]['sn'][0],'mail':result_data[0][1]['mail'][0]}
        except ldap.LDAPError:
            dt = {'result':False}
        return dt