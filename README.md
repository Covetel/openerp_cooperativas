openerp_cooperativas
====================

Openerp para cooperativas

plan_cuentas_cooperativas
--------------------------

Módulo OpenERP que instala el Plan de cuentas para las cooperativas y sus impuesto.

* Archivos:
 + plan_cuentas.csv: Contiene la lista de las cuentas. 
 + settings.py: Modulo python que contiene las variables de configuración como: nombre de la base de datos OpenERP, host, puerto, usuario, password.
 + convertocsv.py: Módulo python que genera el archivo XML con el plan de cuentas.
 + importar.py: Inserta, Actualiza el plan de cuentas en una base de datos existente en OpenERP y Crea archivo XML con información proveniente desde el archivo plan_cuentas.csv usando el módulo convertocsv.py.
```
Banderas:

crear - Crea el plan de cuentas desde el archivo plan_cuentas.csv
listar - Lista los tipos de cuentas
cuentas [codigo de cuenta] - Lista la cuenta indicada
actualizar - Actualiza las cuentas
xml - Crea xml con las cuentas y su clasificación
```

