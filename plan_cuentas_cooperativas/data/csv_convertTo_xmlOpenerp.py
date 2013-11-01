 # -*- coding: utf-8 -*-
import re
from lxml import etree
from xml.sax.saxutils import escape
import pprint

csv_data = open("plan_cuentas.csv", "r")
xml_export = open("venezuela_cooperatives_chart.xml", "w")

pp = pprint.PrettyPrinter(indent=4)

def _xml_record_chart(info, data):
    record = etree.SubElement(data, "record")
#    record = etree.Element("record")
    record.set("model", "account.chart.template")
    record.set("id", info["id"])

    field = etree.SubElement(record, "field")
    field.set("name", "name")
    field.text = info["name"]

    field = etree.SubElement(record, "field")
    field.set("name", "account_root_id")
    field.set("ref", info["account_root_id"])

    field = etree.SubElement(record, "field")
    field.set("name", "tax_code_root_id")
    field.set("ref", info["tax_code_root_id"])

    field = etree.SubElement(record, "field")
    field.set("name", "bank_account_view_id")
    field.set("ref", info["bank_account_view_id"])

    field = etree.SubElement(record, "field")
    field.set("name", "property_account_receivable")
    field.set("ref", info["property_account_receivable"])

    field = etree.SubElement(record, "field")
    field.set("name", "property_account_payable")
    field.set("ref", info["property_account_payable"])

    field = etree.SubElement(record, "field")
    field.set("name", "property_account_expense_categ")
    field.set("ref", info["property_account_expense_categ"])

    field = etree.SubElement(record, "field")
    field.set("name", "property_account_income_categ")
    field.set("ref", info["property_account_income_categ"])

    field = etree.SubElement(record, "field")
    field.set("name", "property_account_income_opening")
    field.set("ref", info["property_account_income_opening"])

    field = etree.SubElement(record, "field")
    field.set("name", "property_account_expense_opening")
    field.set("ref", info["property_account_expense_opening"])
    
    field = etree.SubElement(record, "field")
    field.set("name", "complete_tax_set")
    field.set("eval", info["complete_tax_set"])

def _xml_record_type(model_type, data):
    name_fix = lambda x: x.replace(" ", "_").lower()
    record = etree.SubElement(data, "record")
    record.set("model", "account.account.type")
    if len(model_type) > 3:
        record.set("id", "account_type_" + name_fix(model_type[0]))
    else:
        record.set("id", "account_type_" + name_fix(model_type[0]) + "1")

    field = etree.SubElement(record, "field")
    field.set("name", "name")
    field.text = model_type[0]

    field = etree.SubElement(record, "field")
    field.set("name", "code")
    if len(model_type) > 3:
        field.text = model_type[0].lower()
    else:
        field.text = model_type[1]

    if len(model_type) > 3:
        field = etree.SubElement(record, "field")
        field.set("name", "close_method")
        field.text = model_type[1]

    field = etree.SubElement(record, "field")
    field.set("name", "report_type")
    field.text = model_type[2]

users_types = { 
        "view" : [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ],
        "asset_view1" : [
            "11", "11/1-6", "12", "121", "13", "13/1-2", "14" , "14/1-2", "15", 
            "151", "16", "161"
        ],
        "liability view1" : [ "x" ],
        "income_view1" : [ "x" ],
        "expense_view1" : [ "x" ],
        "asset" : [ "" ],
        "cash" : [ "111/101-102" ],
        "bank" : [ "111201" ],
        "payable" : [ "212/102-108" ],
        "receivable" : [ "113/101-107", "113199" ],
        "liability" : [ "x" ],
        "income" : [ "x" ],
        "expense" : [ "" ],
        "tax" : [ "x" ],
        "equity" : [ "x" ],
        "chk" : [ "x" ],
}

def _users_types(code):
    for key, values in users_types.iteritems():
        for value in values:
            if "/" in value:
                padre = value.split("/")
                rango = str(padre[1]).split("-")
                desde, to = tuple(rango)
                for i in range(int(desde), int(to) + 1):
                    if code == padre[0] + str(i): 
                        return key
            else:
                if code == value:
                    return key

def _xml_record_template(code, name, parent_id, data):
    record = etree.SubElement(data, "record")
    record.set("model", "account.account.template")
    code_without_dots = _code_without_dots(code)
    record.set("id", "account_cooperativa_" + code_without_dots)

    field = etree.SubElement(record, "field")
    field.set("name", "code")
    field.text = code

    field = etree.SubElement(record, "field")
    field.set("name", "name")
    field.text = str(name).decode('utf8')

    if str(code) != "0":
        field = etree.SubElement(record, "field")
        field.set("name", "parent_id")
        field.set("ref", "account_cooperativa_" + str(parent_id))
    
    field = etree.SubElement(record, "field")
    field.set("name", "reconcile")
    if str(code) == "0":
        field.set("eval", "False")
    else:
        field.set("eval", "True")

    field = etree.SubElement(record, "field")
    field.set("name", "type")
    field.text = "view"

    field = etree.SubElement(record, "field")
    type = _users_types(code_without_dots)
    field.set("ref", "account_type_" + "view")
    #field.set("ref", "account_type_" + str(type))
    field.set("name", "user_type")

def _code_without_dots(code):
    return str(code.replace('.', ""))

def _read_file():
    cuentas = []
    for line in csv_data.readlines()[0:]:
        info = line.split(",")

        code = re.sub("[\n\.]$", "", info[1])
        name = info[0].replace('"', '')
        cuenta = {
            "code" : code,
            "name" : name
        }
        cuentas.append(cuenta)
        
    return sorted(cuentas, key = lambda cuenta: cuenta["code"])

def _calculate_parent_id(cuentas_without_parents):
    cuentas = []
    for cuenta in cuentas_without_parents:
        code_split = cuenta['code'].split(".")
        rigthside = code_split.pop()

        leftside = _code_without_dots("".join(code_split))

        if leftside:
            cuenta["parent_id"] = leftside
        else:
            cuenta["parent_id"] = 0
        cuentas.append(cuenta)
    return cuentas
            
def _write_parents_xml(cuentas, label_data):
    for i in cuentas:
        _xml_record_template(i['code'], i['name'], i['parent_id'], label_data)


def main():
    openerp = etree.Element("openerp")
    data = etree.SubElement(openerp, "data")
    data.set("noupdate", "1")

    cuentas_without_parents = _read_file()
    cuentas_with_parents = _calculate_parent_id(cuentas_without_parents)

    # len 3 = (Name, code, report_type)
    # len 4 = (Name, close_method, report_type, "")
    accounts = [
        ("Income View", "view", "income"), # A cobrar
        ("Expense View", "expense", "expense"), # A pagar
        ("Asset View", "asset", "asset"), # Banco
        ("Liability View", "liability", "liability"), # Egreso
        ("Tax", "unreconciled", "expense", ""), # Egreso
        ("Equity", "balance", "liability", ""), # Egreso
        ("Check", "balance", "asset", ""), # Egreso
    ]

    for account in accounts:
        _xml_record_type(account, data)
    _write_parents_xml(cuentas_with_parents, data)

    info = {
        "id" : "ve_chart_coop",
        "name" : "Venezuela Cooperative - Account",
        "account_root_id" : "account_cooperativa_0",
        "tax_code_root_id" : "",
        "bank_account_view_id" : "account_cooperativa_111201",
        "property_account_receivable" : "",
        "property_account_payable" : "",
        "property_account_expense_categ" : "",
        "property_account_income_categ" : "",
        "property_account_income_opening" : "",
        "property_account_expense_opening" : "",
        "complete_tax_set" : "False"
    }
    _xml_record_chart(info, data)

    etree.dump(openerp)
    xml_export.write(etree.tostring(openerp, pretty_print=True))
    xml_export.close()

main()
