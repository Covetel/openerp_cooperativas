 # -*- coding: utf-8 -*-
import re
from lxml import etree
from xml.sax.saxutils import escape
import pprint

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

def _xml_record_template(cuenta, data):
    record = etree.SubElement(data, "record")
    record.set("model", "account.account.template")
    record.set("id", "account_cooperativa_" + cuenta['id'])

    field = etree.SubElement(record, "field")
    field.set("name", "code")
    field.text = cuenta['code']

    field = etree.SubElement(record, "field")
    field.set("name", "name")
    field.text = str(cuenta['name']).decode('utf8')

    if str(cuenta['code']) != "0":
        field = etree.SubElement(record, "field")
        field.set("name", "parent_id")
        field.set("ref", "account_cooperativa_" + str(cuenta['parent_id']))
    
    field = etree.SubElement(record, "field")
    field.set("name", "reconcile")
    field.set("eval", str(cuenta['reconcile']))

    field = etree.SubElement(record, "field")
    field.set("name", "type")
    field.text = str(cuenta['type'])

    field = etree.SubElement(record, "field")
    field.set("name", "user_type")
    field.set("ref", "account_type_" + cuenta["type"])

def _write_parents_xml(cuentas, label_data):
    for i in cuentas:
        _xml_record_template(i, label_data)

def main(cuentas):
    openerp = etree.Element("openerp")
    data = etree.SubElement(openerp, "data")
    data.set("noupdate", "1")

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

    _write_parents_xml(cuentas, data)

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
