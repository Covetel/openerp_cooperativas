from osv import osv, fields
import time
import logging

_logger = logging.getLogger(__name__)

class sunacoop_cooperativas(osv.osv): 
    _name = "sunacoop.cooperativas"

    def _get_cantidad_socios(self,cr,uid,ids,field,arg,context=None):
        res = {}
        for record in self.browse(cr,uid,ids,context=context):
            cant = len(record.asociados)
            res[record.id] = cant
        return res
        
    def name_get(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        res = []
        for record in self.browse(cr,uid,ids,context=context):
            res.append((record.id, record.razon_social))
        return res

    def _check_rif(self,cr,uid,ids,context=None):
        record = self.browse(cr,uid,ids,context=context)
        for data in record:
            if data.rif.find("J-") != 0:
                return False
        return True

    def _check_rif_numeros(self,cr,uid,ids,context=None):
        record = self.browse(cr,uid,ids,context=context)
        for data in record:
            if any(c.isalpha() for c in data.rif[2:]):
                return False
        return True

    def _check_cant_socios(self,cr,uid,ids,context=None):
        for record in self.browse(cr,uid,ids,context):
            if record.cantidad_socios >= 5:
                return True
        return False

    _constraints = [
        (_check_rif, "El rif es invalido debe contener J- al principio", ['rif']),
        (_check_rif_numeros, "El rif no puede contener otras letras", ['rif']),
        (_check_cant_socios, "La cantidad de asociados debe ser mayor o igual a 5", ['asociados']),
        
        ]

    _columns = { 
        'rif' : fields.char("Rif",size=12,required=True),
        'numero_expediente' : fields.integer("Numero de Expediente",required=True),
        'fecha_registro' : fields.date('Fecha de Registro',required=True),
        'razon_social' : fields.char("Razon Social",size=128,required=True),
        'numero_folio' : fields.integer("Numero de Folio",required=True),
        'numero_tomo' : fields.integer("Numero de Tomo",required=True),
        'registro_inscrito' : fields.char("Registro Inscrito",size=128,
                                          required=True),
        'direccion' : fields.char("Direccion",size=256,required=True),
        'direccion2' : fields.char("Direccion2",size=256),
        'estado' : fields.many2one("sunacoop.estados","Estado",required=True),
        'municipio' : fields.many2one("sunacoop.municipios","Municipio",
                                      required=True),
        'parroquia' : fields.many2one("sunacoop.parroquias","Parroquia",
                                      required=True),
        'asociados' : fields.one2many("sunacoop.asociados","cooperativa_id", 
                                     "Asociados", required=True),
        'cantidad_socios' : fields.function(_get_cantidad_socios,type='integer',
                                            string="Cantidad de Asociados",
                                            required=True),
        }

    _defaults = {
        'fecha_registro' : lambda *a: time.strftime('%Y-%m-%d'),
        }
sunacoop_cooperativas()    

class sunacoop_estados(osv.osv):
    _name = 'sunacoop.estados'
    _columns = {
        'name' : fields.char("Nombre", size=128),
        }
sunacoop_estados()

class sunacoop_municipios(osv.osv):
    _name = 'sunacoop.municipios'
    _columns = {
        'name' : fields.char("Nombre", size=128),
        'padre' : fields.many2one("sunacoop.estados", "Estado")
        }
sunacoop_municipios()

class sunacoop_parroquias(osv.osv):
    _name = 'sunacoop.parroquias'
    _columns = { 
        'name' : fields.char("Nombre", size=128),
        'padre' : fields.many2one("sunacoop.municipios", "Municipio")
        }
sunacoop_parroquias()

class sunacoop_asociados(osv.osv) :
    _name = "sunacoop.asociados"
    _columns = { 
        'nombres' : fields.char("Nombres", size=128),
        'apellidos' : fields.char("Apellidos", size=128),
        'cedula' : fields.char("Documento de Identidad", size=12),
        'direccion' : fields.char("Direccion", size=256),
        'estado' : fields.many2one("sunacoop.estados", "Estado"),
        'municipio' : fields.many2one("sunacoop.municipios", "Municipio"),
        'parroquia' : fields.many2one("sunacoop.parroquias", "Parroquia"),
        'cooperativa_id' : fields.many2one('sunacoop.cooperativas', "Cooperativa"),
        }
    _default = {

        }
sunacoop_asociados()
