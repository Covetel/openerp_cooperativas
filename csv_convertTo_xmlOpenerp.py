 # -*- coding: utf-8 -*-
import re
from lxml import etree
from xml.sax.saxutils import escape
import pprint

csv_data = open("plan_cuentas.csv", "r")
xml_export = open("venezuela_cooperativas_chart.xml", "w")

def _record_xml(code, name, parent_id, data):
    record = etree.SubElement(data, "record")
    record.set("model", "account.account.template")
    record.set("id", "account_cooperativa_" + _code_without_dots(code))

    field = etree.SubElement(record, "field")
    field.set("name", "code")
    field.text = str(code)

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
    field.set("ref", "account_type_view")
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
            
def _write_xml(cuentas, label_data):
    for i in cuentas:
        _record_xml(i['code'], i['name'], i['parent_id'], label_data)


def main():
    openerp = etree.Element("openerp")
    data = etree.SubElement(openerp, "data")
    data.set("noupdate", "1")

    pp = pprint.PrettyPrinter(indent=4)

    cuentas_without_parents = _read_file()
    cuentas_with_parents = _calculate_parent_id(cuentas_without_parents)
    _write_xml(cuentas_with_parents, data)

    etree.dump(openerp)
    xml_export.write(etree.tostring(openerp, pretty_print=True))
    xml_export.close()

main()
