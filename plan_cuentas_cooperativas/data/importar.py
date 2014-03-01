# *-* coding=utf-8 *-*
""" Instrucciones
Ejecutar:

python importar_cuentas.py

Banderas:

crear - Crea el plan de cuentas desde el archivo plan_cuentas.csv
listar - Lista los tipos de cuentas
cuentas [codigo de cuenta] - Lista la cuenta indicada
actualizar - Actualiza las cuentas
xml - Crea xml con las cuentas y su clasificación

"""

import xmlrpclib, sys, settings, re
import convertcsv

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
cuentas_csv = source_table.readlines()[0:]

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
    try:
        cod = sock.execute(dbname, uid, pwd, 'account.account', 'search', buscar)
        parent_id = sock.execute(dbname, uid, pwd, 'account.account', 'read', cod, fields)
        return parent_id[0]['id']
    except (IndexError, xmlrpclib.Fault):
        code_split = code.split(".")
        rigthside = code_split.pop()

        leftside = "".join(code_split)

        if leftside:
            pid = leftside
        else:
            pid = 0
        return pid


#Define los tipos de cuentas iniciales
def tipo_cuenta(sock, uid, cuenta):
    #Clasificación de Cuentas padre
    if re.match("^[0123456789]", cuenta['code']):
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'view', 'user_type' : 1, 'parent_id' : '', 'reconcile' : True})
    if re.match("(^[13].\d|[13].\d.\d)", cuenta['code']):
        parent_id = get_parent_id(sock, uid, cuenta['code'])
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'view', 'user_type' : 12, 'parent_id' : parent_id})
    if re.match("^2.\d|2.\d.\d|2.\d.\d.\d.*", cuenta['code']):
        parent_id = get_parent_id(sock, uid, cuenta['code'])
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': "view", 'user_type' : 13, 'parent_id' : parent_id})
    if re.match("(^4.\d|4.\d\d|4.\d.\d.\d.*)", cuenta['code']):
        parent_id = get_parent_id(sock, uid, cuenta['code'])
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'view', 'user_type' : 10, 'parent_id' : parent_id})
    if re.match("(^[56789].\d)", cuenta['code']):
        parent_id = get_parent_id(sock, uid, cuenta['code'])
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'view', 'user_type' : 11, 'parent_id' : parent_id})
    if re.match("^[569].\d.\d|[569].\d.\d.\d.*", cuenta['code']):
        parent_id = get_parent_id(sock, uid, cuenta['code'])
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'view', 'user_type' : 11, 'parent_id' : parent_id})
    if re.match("^[78].\d.\d", cuenta['code']):
        parent_id = get_parent_id(sock, uid, cuenta['code'])
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'other', 'user_type' : 9, 'parent_id' : parent_id})
    if re.match("^[13].\d.\d.\d.*", cuenta['code']):
        parent_id = get_parent_id(sock, uid, cuenta['code'])
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'other', 'user_type' : 6, 'parent_id' : parent_id})

    #Clasificación de Cuentas hijas
    #Activos
    if re.match("(1.1.3.\d\d\d)", cuenta['code']):
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'receivable', 'user_type' : 2})
    if re.match("(1.1.1.1\d\d)", cuenta['code']):
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'liquidity', 'user_type' : 5})
    if re.match("(1.1.1.2\d\d)", cuenta['code']):
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'liquidity', 'user_type' : 4})
    #Pasivos
    if re.match("(2.1.2.\d\d\d)", cuenta['code']):
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'payable', 'user_type' : 3})
    if re.match("(2.1.1.\d\d\d)", cuenta['code']):
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'other', 'user_type' : 7})
    if re.match("(2.[2-5].1.\d\d\d)", cuenta['code']):
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'other', 'user_type' : 7})
    #Patrimonio
    if re.match("(3.\d.\d.\d\d\d)", cuenta['code']):
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'other', 'user_type' : 15})
    #Ingresos
    if re.match("(4.\d.\d.\d\d\d)", cuenta['code']):
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'other', 'user_type' : 8})
    #Compras
    if re.match("(5.\d.\d.\d\d\d)", cuenta['code']):
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'other', 'user_type' : 9})
    #Gastos
    if re.match("(6.1.[1-3].\d\d\d)", cuenta['code']):
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'view', 'user_type' : 11})
    if re.match("(6.1.[1-3].\d\d\d.\d\d\d)", cuenta['code']):
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'other', 'user_type' : 9})
    if re.match("(6.1.4.\d\d\d)", cuenta['code']):
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'other', 'user_type' : 9})
    #Otros Egresos
    if re.match("(7.\d.\d)", cuenta['code']):
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'other', 'user_type' : 9})
    #Anticipos Societarios
    if re.match("(8.\d.\d)", cuenta['code']):
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'other', 'user_type' : 9})
    #Cuentas de Orden
    if re.match("(9.\d.\d.\d\d\d)", cuenta['code']):
        cuenta.update({'id' : cuenta['code'].replace('.', ''), 'type': 'other', 'user_type' : 9})

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
        if re.match("(7.1.2)", cuenta['code']):
            values = {'type': 'other', 'user_type' : 7}
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

def listar_tipo_cuentas(sock, uid, code):
    fields = ['name', 'code']
    if code == "":
        buscar = []
    else:
        buscar = [('id','=', code)]
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

def impuestos(sock, uid):

    #Creo la cuenta para el IVA en el plan de cuentas
    cuentas_csv.append("IVA,7.1.2")

    iva_account = {
            'code': "7.1.2",
            'name': "IVA",
    }

    tipo_cuenta(sock, uid, iva_account)

    code_find = buscar_cuentas(sock, uid, iva_account['code'])

    if not(code_find):
        iva_account_id = crear_cuenta(c, sock, uid, iva_account)

    iva_account_id = 470

    #Creo los codigos de impuesto
    imp_coop = {"name" : "Impuestos Cooperativas"}
    cod_imp_id = sock.execute(dbname, uid, pwd, 'account.tax.code', 'create', imp_coop)

    balance_imp = {"name" : "Balance de Impuestos", "parent_id" : cod_imp_id}
    bal_imp_id = sock.execute(dbname, uid, pwd, 'account.tax.code', 'create', balance_imp)

    base_imp = {"name" : "Base de Impuestos", "parent_id" : cod_imp_id}
    bas_imp_id = sock.execute(dbname, uid, pwd, 'account.tax.code', 'create', base_imp)

    rec_imp = {"name" : "Impuesto Recibido", "parent_id" : bal_imp_id, "sign" : "-1"}
    rec_imp_cod = sock.execute(dbname, uid, pwd, 'account.tax.code', 'create', rec_imp)

    rec_sale_imp =  {"name" : "Impuesto Recibido por Ventas", "parent_id": rec_imp_cod }
    r_imp_s_cod = sock.execute(dbname, uid, pwd, 'account.tax.code', 'create', rec_sale_imp)

    paid_imp = {"name" : "Impuesto Pagado", "parent_id" : bal_imp_id}
    paid_imp_cod = sock.execute(dbname, uid, pwd, 'account.tax.code', 'create', paid_imp)

    paid_purchase_imp = {"name" : "Impuesto Pagado por Compras",  "parent_id" : paid_imp_cod}
    paid_purchase_imp_cod = sock.execute(dbname, uid, pwd, 'account.tax.code', 'create', paid_purchase_imp)

    purchase_imp = {"name" : "Impuesto por Compras", "parent_id" : bas_imp_id}
    purchase_imp_cod = sock.execute(dbname, uid, pwd, 'account.tax.code', 'create', purchase_imp)

    purchase_tw_imp = {"name" : "Impuesto 12%", "parent_id" : purchase_imp_cod}
    purchase_tw_imp_cod = sock.execute(dbname, uid, pwd, 'account.tax.code', 'create', purchase_tw_imp)

    sale_imp = {"name" : "Impuesto por Ventas", "parent_id" : bas_imp_id}
    sale_imp_cod = sock.execute(dbname, uid, pwd, 'account.tax.code', 'create', sale_imp)

    sale_cero_imp = {"name" : "Impuesto 0%", "parent_id" : sale_imp_cod}
    sale_cero_imp_cod = sock.execute(dbname, uid, pwd, 'account.tax.code', 'create', sale_cero_imp)

    imp_tw = {'name' : 'Impuesto para compras 12%', 'amount' : '0.12', 'type' : 'percent', 'account_collected_id' : iva_account_id, 'account_paid_id' : iva_account_id, 'base_code_id' : purchase_tw_imp_cod, 'tax_code_id' : paid_purchase_imp_cod, 'ref_base_code_id' : purchase_tw_imp_cod, 'ref_tax_code_id' : paid_purchase_imp_cod, 'type_tax_use' : 'purchase', 'company_id': 1, 'active': True}
    imp_tw_id = sock.execute(dbname, uid, pwd, 'account.tax', 'create', imp_tw)

    imp_cero = {'name' : 'Impuesto para ventas 0%', 'amount' : '0', 'type' : 'percent', 'account_collected_id' : iva_account_id, 'account_paid_id' : iva_account_id, 'base_code_id' : sale_cero_imp_cod, 'tax_code_id' : r_imp_s_cod, 'ref_base_code_id' : sale_cero_imp_cod, 'ref_tax_code_id' : r_imp_s_cod, 'type_tax_use' : 'sale', 'company_id': 1, 'active': True}
    imp_cero_id = sock.execute(dbname, uid, pwd, 'account.tax', 'create', imp_cero)

    #Fiscal Position
    fiscal_position = {'id' : 'imp_fiscal_coop', 'name' : 'Impuesto Normal Cooperativas', 'company_id' : 1, 'active': True }
    fiscal_pos_id = sock.execute(dbname, uid, pwd, 'account.fiscal.position', 'create', fiscal_position)

    #Fiscal Taxes
    imp_fiscal = {'position_id' : fiscal_pos_id, 'tax_src_id' : imp_tw_id, 'tax_dest_id' : imp_cero_id }
    imp_f_id = sock.execute(dbname, uid, pwd, 'account.fiscal.position.tax', 'create', imp_fiscal)

def insertar_plan_cuentas(cuentas_csv, sock, uid):
    global ac

    for line in cuentas_csv:
            if True:

                l = line.split(",")

                code = re.sub("[\n\.]$", "", l[1])
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

                            tipo_cuenta(sock, uid, cuenta)

                            if not code in codes:
                                cuenta.update({'id' : cuenta['code'].replace('.', '')})
                                crear_cuenta(c, sock, uid, cuenta)

                                cuentas.append(cuenta)
                                codes.append(code)
                                ac = ac + 1

    impuestos(sock, uid)

def hacer_xml(sock, uid):
    global ac, cuentas

    for line in cuentas_csv:
            if True:

                l = line.split(",")

                code = re.sub("[\n\.]$", "", l[1])
                name = l[0].replace('"', '')
                row = ""

                cuenta = {
                   'code': code,
                   'name': name,
                }
                tipo_cuenta(sock, uid, cuenta)

                match = cuenta in cuentas

                #Inserta las cuentas desde el csv
                if not match:
                    match_code = code in codes

                    if not match_code:
                        if cuenta['parent_id'] == '':
                            cuenta.update({'parent_id' : 0})

                        cuentas.append(cuenta)

                        codes.append(code)
                        ac = 101
                    else:
                        code = code+"."+str(ac)
                        cuenta.update({'code':code})

                        tipo_cuenta(sock, uid, cuenta)

                        if not code in codes:
                            if cuenta['parent_id'] == '':
                                cuenta.update({'parent_id' : 0})
                            cuenta.update({'id' : cuenta['code'].replace('.', '')})

                            cuentas.append(cuenta)
                            codes.append(code)
                            ac = ac + 1

    convertcsv.main(cuentas)


def main():
    (sock, uid) = connect()

    #Inserta el plan de cuentas en OpenERP
    if c == "crear":
        insertar_plan_cuentas(cuentas_csv, sock, uid)

    #Lista los tipos de cuenta
    if c == "listar":
        listar_tipo_cuentas(sock, uid, '')

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

    #Hacer csv
    if c == "xml":
        hacer_xml(sock, uid)

main()
