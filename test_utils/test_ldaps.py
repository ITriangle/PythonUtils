import ldap3
from ldap3 import Server, Connection, ALL


def ldap_authentication(username,password,host,port):
    # the following is the user_dn format provided by the ldap server
    user_dn = "uid=" + username + ",ou=hadoop,dc=ipin,dc=com"
    # adjust this to your base dn for searching
    base_dn = "dc=ipin,dc=com"
    search_filter = "(uid={})".format(username)
    conn = None

    try:

        server = Server(host=host, port=port, get_info=ALL)
        # server = Server(host='192.168.1.11',port=389)
        conn = Connection(server, user=user_dn, password=password)
        conn.open()
        conn.bind()
        # conn.search(base_dn, '('+ search_filter + ')')
        conn.search(base_dn, search_filter)
        print(conn.entries)
        conn.unbind()

        return True

    except:
        if conn is not None:
            conn.unbind()

        return False

if __name__ == '__main__':

    ldap_authentication(host='192.168.1.11', port=389,username='username',password='password')
