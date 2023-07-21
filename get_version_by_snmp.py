from pysnmp.hlapi import *

SNMPv3 = {
    'AGENT': '10.16.93.99',
    'PORT': 161,
    'USER': 'aztc',
    'MD5_AUTH': '@AzTcCtZa13',
    'DES_PRIV': '13AzTcCtZa@'
}

subnet_prefix = '10.16.93.'
subnet_mask = 24



def get_subnet(first_three_octets, subnet_mask=24):
    if(subnet_mask != 24):
        pass

    subnet = []
    for last_octet in range(1,255):
        subnet.append(first_three_octets + str(last_octet))
    
    return subnet
    
subnet = get_subnet(subnet_prefix)

for host in subnet:
    iterator = getCmd(
        SnmpEngine(),
        UsmUserData(SNMPv3['USER'], SNMPv3['MD5_AUTH'], SNMPv3['DES_PRIV']),
        UdpTransportTarget((host, SNMPv3['PORT'])),
        ContextData(),
        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0))
    )


    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(host, errorIndication)

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:
        for varBind in varBinds:
            print(host, ' = '.join([x.prettyPrint() for x in varBind]))