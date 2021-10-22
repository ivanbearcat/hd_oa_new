from ldap3 import Server, Connection, ALL, NTLM


ad = Server('ldap://192.168.9.251:389', get_info=ALL, use_ssl=True)  # 要修改密码必须启用ssl
attr_list = ['distinguishedName', 'cn', 'uid', 'displayName', 'mail', 'telephoneNumber', 'userAccountControl',
             'sAMAccountName', 'pwdLastSet', 'department', 'employeeID']
# 链接ldap服务器
conn = Connection(ad, user='npnets\\ad-acount', password='0d^7^UPqj0', authentication=NTLM,
                  auto_bind=True)

dn = 'OU=Users,OU=npnets,DC=npnets,DC=cn'
# 增加账号
user = 'CN=hd-yanglin3,OU=Users,OU=npnets,DC=npnets,DC=cn'
conn.add(user, object_class='user', attributes={'displayName': 'hd-yanglin3', 'sAMAccountName': 'hd-yanglin3',
                                                'userPrincipalName': 'hd-yanglin3',
                                                'mail': 'hd-yanglin@npnets.com', 'description': '杨林3'})
# 账号查询
u_info = conn.search(dn, "(sAMAccountName=hd-yanglin)", attributes=['*'])

for user in conn.entries:
    print(user['displayName'])
    print(user['telephoneNumber'])
