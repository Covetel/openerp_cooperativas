# -*- encoding: utf-8 -*-

{
    'name' : "Venezuela - Cooperative Accounting",
    'version' : '1.2',
    'author' : 'Covetel R.S.',
    'website': 'http://www.covetel.com.ve',
    'description': 'Chart Account for Cooperatives in Venezuela',
    'category' : 'Localization/Account Charts',
    'depends': [ 
        'account',
        'base_vat',
        'account_accountant'
    ], 
    'data' : [
        'data/data_account_type.xml',
        'data/venezuela_cooperatives_chart.xml',
        'data/cooperatives_chart_wizard.xml',
    ],
    'auto_install' : False,
    'installable' : True,
}
