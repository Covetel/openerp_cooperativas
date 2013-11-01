# -*- encoding: utf-8 -*-

{
    'name' : "Venezuela - Cooperative Accounting",
    'version' : '1.0',
    'author' : ['Covetel R.S.'],
    'category' : 'Localization/Account Charts',
    'depends': [ 
        'account',
        'base_vat',
        'account_accountant'
    ], 
    'data' : [
        'data/data_account_type.xml',
        'data/venezuela_cooperatives_chart.xml',
    ],
    'auto_install' : False,
    'installable' : True,

}
