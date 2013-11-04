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
except IndexError:
    print "No indico un parametro"
    sys.exit()

username = settings.username
pwd = settings.pwd
dbname = settings.dbname
source_table = open("plan_cuentas.csv")

cuentas = []
codes = []
ac = 101
account_id = 0;

def connect():
    # Get the uid
    sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
    uid = sock_common.login(dbname, username, pwd)

    #replace localhost with the address of the server
    sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')

    return sock, uid

#Borra las cuentas de la base de datos
def borrar_cuentas(sock, uid):
    buscar = []
    cod = sock.execute(dbname, uid, pwd, 'account.account', 'search', buscar)
    print cod
    for i in cod:
        sock.execute(dbname, uid, pwd, 'account.account', 'unlink', cod)

#Obtiene el parent_id de una cuenta
def get_parent_id(sock, uid, code):
    match = re.match("(^.*)(\.\d*)", code)
    fields = ['id']
    buscar = [('code','=', match.group(1))]
    cod = sock.execute(dbname, uid, pwd, 'account.account', 'search', buscar)
    parent_id = sock.execute(dbname, uid, pwd, 'account.account', 'read', cod, fields)
    try:
        return parent_id[0]['id']
    except IndexError:
        return []

#Define los tipos de cuentas iniciales
def tipo_cuenta(sock, uid, cuenta):
    if re.match("^[0123456789]", cuenta['code']):
        cuenta.update({'type': 'view'})
        cuenta.update({'user_type' : 1})
        cuenta.update({'reconcile' : True})
    if re.match("(^[13].\d|[13].\d.\d)", cuenta['code']):
        parent_id = get_parent_id(sock, uid, cuenta['code'])
        cuenta.update({'type': 'view'})
        cuenta.update({'user_type' : 12})
        cuenta.update({'parent_id' : parent_id})
    if re.match("^2.\d|2.\d.\d|2.\d.\d.\d.*", cuenta['code']):
        parent_id = get_parent_id(sock, uid, cuenta['code'])
        cuenta.update({'type': "view"})
        cuenta.update({'user_type' : 13})
        cuenta.update({'parent_id' : parent_id})
    if re.match("(^4.\d|4.\d\d|4.\d.\d.\d.*)", cuenta['code']):
        parent_id = get_parent_id(sock, uid, cuenta['code'])
        cuenta.update({'type': 'view'})
        cuenta.update({'user_type' : 10})
        cuenta.update({'parent_id' : parent_id})
    if re.match("(^[56789].\d)", cuenta['code']):
        parent_id = get_parent_id(sock, uid, cuenta['code'])
        cuenta.update({'type': 'view'})
        cuenta.update({'user_type' : 11})
        cuenta.update({'parent_id' : parent_id})
    if re.match("^[569].\d.\d|[569].\d.\d.\d.*", cuenta['code']):
        parent_id = get_parent_id(sock, uid, cuenta['code'])
        cuenta.update({'type': 'view'})
        cuenta.update({'user_type' : 11})
        cuenta.update({'parent_id' : parent_id})
    if re.match("^[78].\d.\d", cuenta['code']):
        parent_id = get_parent_id(sock, uid, cuenta['code'])
        cuenta.update({'type': 'other'})
        cuenta.update({'user_type' : 9})
        cuenta.update({'parent_id' : parent_id})
    if re.match("^[13].\d.\d.\d.*", cuenta['code']):
        parent_id = get_parent_id(sock, uid, cuenta['code'])
        cuenta.update({'type': 'other'})
        cuenta.update({'user_type' : 6})
        cuenta.update({'parent_id' : parent_id})

    return cuenta

#Actualiza los tipos de Cuentas
def actualizar_cuenta(sock, uid):
    cod = buscar_cuentas(sock, uid, "all")
    fields = ['name', 'code', 'type', 'user_type']
    for i in cod:
        cuenta = sock.execute(dbname, uid, pwd, 'account.account', 'read', i, fields)
        values = {}

        #Clasificación de Cuentas
        #Activos
        if re.match("(1.1.3.\d\d\d)", cuenta['code']):
            values = {'type': 'receivable', 'user_type' : 2}
        if re.match("(1.1.1.1\d\d)", cuenta['code']):
            values = {'type': 'liquidity', 'user_type' : 5}
        if re.match("(1.1.1.2\d\d)", cuenta['code']):
            values = {'type': 'liquidity', 'user_type' : 4}
        #Pasivos
        if re.match("(2.1.2.\d\d\d)", cuenta['code']):
            values = {'type': 'payable', 'user_type' : 3}
        if re.match("(2.1.1.\d\d\d)", cuenta['code']):
            values = {'type': 'other', 'user_type' : 7}
        if re.match("(2.[2-5].1.\d\d\d)", cuenta['code']):
            values = {'type': 'other', 'user_type' : 7}
        #Patrimonio
        if re.match("(3.\d.\d.\d\d\d)", cuenta['code']):
            values = {'type': 'other', 'user_type' : 15}
        #Ingresos
        if re.match("(4.\d.\d.\d\d\d)", cuenta['code']):
            values = {'type': 'other', 'user_type' : 8}
        #Compras
        if re.match("(5.\d.\d.\d\d\d)", cuenta['code']):
            values = {'type': 'other', 'user_type' : 9}
        #Gastos
        if re.match("(6.1.[1-3].\d\d\d)", cuenta['code']):
            values = {'type': 'view', 'user_type' : 11}
        if re.match("(6.1.[1-3].\d\d\d.\d\d\d)", cuenta['code']):
            values = {'type': 'other', 'user_type' : 9}
        if re.match("(6.1.4.\d\d\d)", cuenta['code']):
            values = {'type': 'other', 'user_type' : 9}
        #Otros Egresos
        if re.match("(7.\d.\d)", cuenta['code']):
            values = {'type': 'other', 'user_type' : 9}
        #Anticipos Societarios
        if re.match("(8.\d.\d)", cuenta['code']):
            values = {'type': 'other', 'user_type' : 9}
        #Cuentas de Orden
        if re.match("(9.\d.\d.\d\d\d)", cuenta['code']):
            values = {'type': 'other', 'user_type' : 9}

        modificar_cuenta(sock, uid, i, values)

def crear_cuenta(c, sock, uid, cuenta):
    if c == "crear":
        print cuenta
        account_id = sock.execute(dbname, uid, pwd, 'account.account', 'create', cuenta)
        print account_id

def buscar_cuentas(sock, uid, code):
    if code == "all":
        buscar = []
    else:
        buscar = [('code','=', code)]

    cod = sock.execute(dbname, uid, pwd, 'account.account', 'search', buscar)

    return cod

def modificar_cuenta(sock, uid, ids, values):
    account_id = sock.execute(dbname, uid, pwd, 'account.account', 'write', ids, values)

def listar_tipo_cuentas(sock, uid):
    fields = ['name', 'code']
    buscar = [('name','=', '')]
    cod = sock.execute(dbname, uid, pwd, 'account.account.type', 'search', buscar)
    for i in cod:
        types = sock.execute(dbname, uid, pwd, 'account.account.type', 'read', i, fields)
        print types

def detalle_cuenta(sock, uid, code):
    cod = buscar_cuentas(sock, uid, code)
    fields = []
    for i in cod:
        account = sock.execute(dbname, uid, pwd, 'account.account', 'read', i, fields)
        print account

    return cod

def insertar_plan_cuentas(source_table, sock, uid):
    global ac

    for line in source_table.readlines()[0:]:
            if True:

                l = line.split(",")

                code = re.sub("[\n\.]$", "", l[1])
                #name = l[0].replace('"', '')
                name = l[0].replace('"', '')

                cuenta = {
                   'code': code,
                   'name': name,
                }

                tipo_cuenta(sock, uid, cuenta)

                match = cuenta in cuentas

                #Valido que la cuenta no exista
                code_find = buscar_cuentas(sock, uid, code)

                #Valido que el codigo no pertenesca al plan de cuentas de cooperativa para que no sea modificado
                coop_code = re.match("^.*\..*", code)

                if code_find and not(coop_code):
                    #Modifico el campo valor de la cuenta por el nombre que tiene en el csv, si esta ya esta creada
                    values = {'name': name}
                    modificar_cuenta(sock, uid, code_find, values)
                else:
                    #Inserta las cuentas desde el csv
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
    actualizar_cuenta(sock, uid)


def main():
    (sock, uid) = connect()

    #Inserta el plan de cuentas en OpenERP
    if c == "crear":
        insertar_plan_cuentas(source_table, sock, uid)

    #Lista los tipos de cuenta
    if c == "listar":
        listar_tipo_cuentas(sock, uid)

    #Lista la cuenta pasada como parametro
    if c == "cuentas":
        try:
            cc = sys.argv[2]
        except IndexError:
            print "Indique el codigo de la cuenta"
            sys.exit()
        detalle_cuenta(sock, uid, cc)

    #Borra todas las cuentas posibles de la BD del OpenERP
    if c == "borrar":
        borrar_cuentas(sock, uid)

    #Actualiza las cuentas si estan creadas en el sistema
    if c == "actualizar":
        actualizar_cuenta(sock, uid)

main()
