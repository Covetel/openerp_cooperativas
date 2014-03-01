 # -*- coding: utf-8 -*-
import re
from lxml import etree
from xml.sax.saxutils import escape
import pprint

xml_export = open("venezuela_cooperatives_chart.xml", "w")

pp = pprint.PrettyPrinter(indent=4)

def _xml_record_chart(info, data):
    record = etree.SubElement(data, "record")
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

def _get_user_type_code(code):
    user_type_names = { 12 : 'asset', 6 : 'asset', 4 : 'bank', 5 : 'cash', 16 : 'check', 15 : 'equity', 9 : 'expense', 11 : 'expense', 8 : 'income', 13 : 'liability', 7 : 'liability', 3 : 'payable', 2 : 'receivable', 14 : 'tax', 10 : 'view', 1 : 'view'}
    return user_type_names[code]

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
    field.set("ref", "account_type_" + _get_user_type_code(cuenta["user_type"]))

def _write_parents_xml(cuentas, label_data):
    for i in cuentas:
        _xml_record_template(i, label_data)

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

def _tax_template(tax, data):
    record = etree.SubElement(data, "record")
    record.set("model", "account.tax.template")
    record.set("id", "tax_cooperativa_" + tax['id'])

    field = etree.SubElement(record, "field")
    field.set("name", "chart_template_id")
    field.set("ref", tax['ref'])

    field = etree.SubElement(record, "field")
    field.set("name", "name")
    field.text = str(tax['name']).decode('utf8')

    field = etree.SubElement(record, "field")
    field.set("name", "amount")
    field.set("eval", tax["eval"])
    
    field = etree.SubElement(record, "field")
    field.set("name", "type")
    field.text = tax['type']

    field = etree.SubElement(record, "field")
    field.set("name", "account_collected_id")
    field.set("ref", tax['account_collected_id'])

    field = etree.SubElement(record, "field")
    field.set("name", "account_paid_id")
    field.set("ref", tax['account_paid_id'])

    field = etree.SubElement(record, "field")
    field.set("name", "base_code_id")
    field.set("ref", tax['base_code_id'])

    field = etree.SubElement(record, "field")
    field.set("name", "tax_code_id")
    field.set("ref", tax['tax_code_id'])

    field = etree.SubElement(record, "field")
    field.set("name", "ref_base_code_id")
    field.set("ref", tax['ref_base_code_id'])

    field = etree.SubElement(record, "field")
    field.set("name", "ref_tax_code_id")
    field.set("ref", tax['ref_tax_code_id'])

    field = etree.SubElement(record, "field")
    field.set("name", "type_tax_use")
    field.text = tax['type_tax_use']

def _tax_code_template(codigos_de_impuestos, data):
    record = etree.SubElement(data, "record")
    record.set("model", "account.tax.code.template")
    record.set("id", codigos_de_impuestos['id'])

    field = etree.SubElement(record, "field")
    field.set("name", "name")
    field.text = codigos_de_impuestos['name']

    try:
        if codigos_de_impuestos['parent_id']:
            field = etree.SubElement(record, "field")
            field.set("name", "parent_id")
            field.set("ref", codigos_de_impuestos['parent_id'])
    except KeyError:
        pass

    try:
        if codigos_de_impuestos['sign']:
            field = etree.SubElement(record, "field")
            field.set("name", "sign")
            field.set("eval", codigos_de_impuestos['sign'])
    except KeyError:
        pass

def _imp_fiscal_template(imp_fiscal, data):
    record = etree.SubElement(data, "record")
    record.set("model", "account.fiscal.position.tax.template")
    record.set("id", imp_fiscal['id'])

    field = etree.SubElement(record, "field")
    field.set("name", "position_id")
    field.set("ref", imp_fiscal['position_id'])

    field = etree.SubElement(record, "field")
    field.set("name", "tax_src_id")
    field.set("ref", imp_fiscal['tax_src_id'])

    field = etree.SubElement(record, "field")
    field.set("name", "tax_dest_id")
    field.set("ref", imp_fiscal['tax_dest_id'])

def _fiscal_mapping_template(fiscal_mapping, data):
    record = etree.SubElement(data, "record")
    record.set("model", "account.fiscal.position.template")
    record.set("id", fiscal_mapping['id'])

    field = etree.SubElement(record, "field")
    field.set("name", "name")
    field.text = fiscal_mapping['name']

    field = etree.SubElement(record, "field")
    field.set("name", "chart_template_id")
    field.set("ref", fiscal_mapping['chart_template_id'])

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

    cuentas_de_impuesto = [
            {'id' : 'iva', 'code' : '7.1.2', 'parent_id' : '71', 'name' : 'IVA', 'type' : 'other', 'user_type' : 7, 'reconcile' : 'True'},
    ]

    _write_parents_xml(cuentas_de_impuesto, data)

    codigos_de_impuestos =[
        #Impuesto de Facturas
            {"id" : "tax_code_coop", "name" : "Impuestos Cooperativas"},
            {"id" : "tax_code_balance_coop", "name" : "Balance de Impuestos", "parent_id" : "tax_code_coop"},
            #Impuesto Recibido
            {"id" : "tax_code_input" ,  "name" : "Impuesto Recibido", "parent_id" : "tax_code_balance_coop", "sign" : "-1"},
            {"id" : "tax_code_input_v", "name" : "Impuesto Recibido por Ventas",  "parent_id" : "tax_code_input"},
            #Impuesto Pagado
            {"id" : "tax_code_output" ,  "name" : "Impuesto Pagado", "parent_id" : "tax_code_balance_coop"},
            {"id" : "tax_code_output_c", "name" : "Impuesto Pagado por Compras",  "parent_id" : "tax_code_output"},
        #Base de Impuestos
            {"id" : "tax_code_base_coop", "name" : "Base de Impuestos", "parent_id" : "tax_code_coop"},
            #Base impuesto por compras
            {"id" : "tax_code_compras", "name" : "Impuesto por Compras", "parent_id" : "tax_code_base_coop"},
            {"id" : "tax_code_compras_12", "name" : "Impuesto 12%", "parent_id" : "tax_code_compras"},
            #Base de impuesto por ventas
            {"id" : "tax_code_ventas", "name" : "Impuesto por Ventas", "parent_id" : "tax_code_base_coop"},
            {"id" : "tax_code_ventas_0", "name" : "Impuesto 0%", "parent_id" : "tax_code_ventas"},
    ]

    for cdi in codigos_de_impuestos:
        _tax_code_template(cdi, data)

    info = {
        "id" : "ve_chart_coop",
        "name" : "Venezuela Cooperative - Account",
        "account_root_id" : "account_cooperativa_0",
        "tax_code_root_id" : "tax_code_coop",
        "bank_account_view_id" : "account_cooperativa_111201",
        "property_account_receivable" : "account_cooperativa_113101",
        "property_account_payable" : "account_cooperativa_212106",
        "property_account_expense_categ" : "account_cooperativa_511101",
        "property_account_income_categ" : "account_cooperativa_412101",
        "property_account_income_opening" : "",
        "property_account_expense_opening" : "",
        "complete_tax_set" : "True"
    }
    _xml_record_chart(info, data)

    impuestos = [
            #Impuesto 12%
            {'id' : "imp_compras_12", 'ref' : "ve_chart_coop", 'code' : 'impuesto_compras_12', 'name' : 'Impuesto para compras 12%', "eval" : "0.12", "type" : "percent", "account_collected_id" : "account_cooperativa_iva", "account_paid_id" : "account_cooperativa_iva", "base_code_id" : "tax_code_compras_12", "tax_code_id" : "tax_code_output_c", "ref_base_code_id" : "tax_code_compras_12", "ref_tax_code_id" : "tax_code_output_c", "type_tax_use" : "purchase"},
            #Impuesto 0%
            {'id' : "imp_ventas_0", 'ref' : "ve_chart_coop", 'code' : 'impuesto_ventas_0', 'name' : 'Impuesto para ventas 0%', "eval" : "0", "type" : "percent", "account_collected_id" : "account_cooperativa_iva", "account_paid_id" : "account_cooperativa_iva", "base_code_id" : "tax_code_ventas_0", "tax_code_id" : "tax_code_input_v", "ref_base_code_id" : "tax_code_ventas_0", "ref_tax_code_id" : "tax_code_input_v", "type_tax_use" : "sale"},
    ]

    for imp in impuestos:
        _tax_template(imp, data)

    #Fiscal Mapping
    fiscal_mapping = {"id" : "imp_fiscal_coop", "name" : "Impuesto Normal Cooperativas", "chart_template_id" : "ve_chart_coop"}

    _fiscal_mapping_template(fiscal_mapping, data)

    #Fiscal Taxes
    imp_fiscal = [
            {"id" : "imp_normal_coop", "position_id" : "imp_fiscal_coop", "tax_src_id" : "tax_cooperativa_imp_compras_12", "tax_dest_id" : "tax_cooperativa_imp_ventas_0" },
    ]

    for imf in imp_fiscal:
        _imp_fiscal_template(imf, data)

    etree.dump(openerp)
    xml_export.write(etree.tostring(openerp, pretty_print=True))
    xml_export.close()
