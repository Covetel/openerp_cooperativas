# *-* coding=utf-8 *-* 
""" Instrucciones
Ejecutar:

python importar_cuentas.py

Banderas:

crear - Crea el plan de cuentas desde el archivo plan_cuentas.csv
listar - Lista los tipos de cuentas
cuentas [codigo de cuenta] - Lista la cuenta indicada

"""

import xmlrpclib, sys, settings, re

c = "";
cc = "";

try:
    c = sys.argv[1]
    cc = sys.argv[2]
except IndexError:
    print "Corriendo sin parametro"

username = settings.username
pwd = settings.pwd
dbname = settings.dbname
source_table = open("plan_cuentas.csv")

def connect():
    # Get the uid
    sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
    uid = sock_common.login(dbname, username, pwd)

    #replace localhost with the address of the server
    sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

    return sock, uid

def borrar_cuentas(sock, uid):
    buscar = []
    cod = sock.execute(dbname, uid, pwd, 'account.account', 'search', buscar)
    print cod
    for i in cod:
        sock.execute(dbname, uid, pwd, 'account.account', 'unlink', cod)


def get_parent_id(code):
    fields = ['id']
    buscar = [('code','=', code )]
    cod = sock.execute(dbname, uid, pwd, 'account.account', 'search', buscar)
    parent_id = sock.execute(dbname, uid, pwd, 'account.account', 'read', cod, fields)
    try:
        return parent_id[0]['id']
    except IndexError:
        return []

def tipo_cuenta(cuenta):
    if re.match("^\d$", cuenta['code']):
        cuenta.update({'type': 'view'})
        cuenta.update({'user_type' : 19})
        cuenta.update({'reconcile' : True})
    if re.match("(^[13456789].\d)", cuenta['code']):
        m = re.match("(^[13456789])", cuenta['code'])
        parent_id = get_parent_id(m.group(1))
        cuenta.update({'type': 'view'})
        cuenta.update({'user_type' : 12})
        cuenta.update({'parent_id' : parent_id})
    if re.match("^[123456789].\d.\d", cuenta['code']):
        m = re.match("(^[123456789].\d)", cuenta['code'])
        parent_id = get_parent_id(m.group(1))
        cuenta.update({'type': 'view'})
        cuenta.update({'user_type' : 12})
        cuenta.update({'parent_id' : parent_id})
    if re.match("^[123456789].\d.\d.\d.*", cuenta['code']):
        m = re.match("(^[123456789].\d.\d)", cuenta['code'])
        parent_id = get_parent_id(m.group(1))
        cuenta.update({'type': 'other'})
        cuenta.update({'user_type' : 6})
        cuenta.update({'parent_id' : parent_id})
    if re.match("^2.\d", cuenta['code']):
        m = re.match("(^2)", cuenta['code'])
        parent_id = get_parent_id(m.group(1))
        cuenta.update({'type': "other"})
        cuenta.update({'user_type' : 9})
        cuenta.update({'parent_id' : parent_id})

    return cuenta

def crear_cuenta(c, sock, uid, cuenta):
    if c == "crear":
        print cuenta
        account_id = sock.execute(dbname, uid, pwd, 'account.account', 'create', cuenta)
        print account_id

cuentas = []
codes = []

ac = 101

(sock, uid) = connect()

account_id = 0;

for line in source_table.readlines()[0:]:
        if True:
            
            l = line.split(",")

            code = re.sub("[\n\.]$", "", l[1])
            name = l[0].replace('"', '')

            cuenta = {
               'code': code,
               'name': name,
            }

            tipo_cuenta(cuenta)

            match = cuenta in cuentas

            if not match:
                match_code = code in codes
                
                if not match_code:
                    crear_cuenta(c, sock, uid, cuenta)

                    cuentas.append(cuenta)
                    codes.append(code)
                    ac = 101
                else:
                    code = code+"."+str(ac)
                    cuenta.update({'code':code})
                    
                    if not code in codes:
                        crear_cuenta(c, sock, uid, cuenta)

                        cuentas.append(cuenta)
                        codes.append(code)
                        ac = ac + 1

if c == "listar":
    fields = ['name', 'code']
    buscar = [('name','=', '')]
    cod = sock.execute(dbname, uid, pwd, 'account.account.type', 'search', buscar)
    for i in cod:
        types = sock.execute(dbname, uid, pwd, 'account.account.type', 'read', i, fields)
        print types

if c == "cuentas":
    fields = ['name', 'code', 'type', 'user_type']
    buscar = [('code','=', cc)]
    cod = sock.execute(dbname, uid, pwd, 'account.account.template', 'search', buscar)
    for i in cod:
        account = sock.execute(dbname, uid, pwd, 'account.account.template', 'read', i)
        print account

if c == "borrar":
    borrar_cuentas(sock, uid)
