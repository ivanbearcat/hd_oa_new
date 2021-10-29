from ldap3 import Server, Connection, ALL, NTLM
from hd_oa.settings import LDAP_AUTH_URL, LDAP_AUTH_SEARCH_BASE, LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN
from hd_oa.settings import LDAP_AUTH_CONNECTION_USERNAME, LDAP_AUTH_CONNECTION_PASSWORD, LDAP_SERVER_IP

def search_user_info(user):
    ad = Server(LDAP_AUTH_URL, get_info=ALL, use_ssl=True)  # 要修改密码必须启用ssl
    # ldap可用字段
    # attr_list = ['distinguishedName', 'cn', 'uid', 'displayName', 'mail', 'telephoneNumber', 'userAccountControl',
    #              'sAMAccountName', 'pwdLastSet', 'department', 'employeeID']
    # 链接ldap服务器
    conn = Connection(ad, user=f'{LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN}\\{LDAP_AUTH_CONNECTION_USERNAME}',
                      password=LDAP_AUTH_CONNECTION_PASSWORD, authentication=NTLM,
                      auto_bind=True)

    # 增加账号
    # user = 'CN=hd-yanglin3,OU=Users,OU=npnets,DC=npnets,DC=cn'
    # conn.add(user, object_class='user', attributes={'displayName': 'hd-yanglin3', 'sAMAccountName': 'hd-yanglin3',
    #                                                 'userPrincipalName': 'hd-yanglin3',
    #                                                 'mail': 'hd-yanglin@npnets.com', 'description': '杨林3'})
    # 账号查询
    res = conn.search(LDAP_AUTH_SEARCH_BASE, f"(sAMAccountName={user})", attributes=['*'])
    if res:
        return {
            'name': str(conn.entries[0]['displayName']),
            'telephone': str(conn.entries[0]['telephoneNumber'])
        }

# 修改密码
def change_passwd(user, passwd):
    ad = Server(LDAP_SERVER_IP, get_info=ALL, use_ssl=True)
    conn = Connection(ad, user=f'{LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN}\\{LDAP_AUTH_CONNECTION_USERNAME}',
                      password=LDAP_AUTH_CONNECTION_PASSWORD, authentication=NTLM,
                      auto_bind=True)

    cn = f'CN={user},OU=Users,OU=npnets,DC=npnets,DC=cn'
    result = conn.extend.microsoft.modify_password(cn, passwd)
    return result

# test
# print(search_user_info('hd-xuezm'))
# print(change_passwd('hd-xuezm', 'Aa1234!@#!@#'))