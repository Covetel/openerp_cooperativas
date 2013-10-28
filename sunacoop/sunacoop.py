from osv import osv, fields
import logging

_logger = logging.getLogger(__name__)

class sunacoop_cooperativas(osv.osv): 
    _name = "sunacoop.cooperativas"

    def _get_cantidad_socios(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for record in  self.browse(cr, uid, ids, context=context):
            res[record.id] = len(record.asociados)
        return res

        
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            res.append((record.id, record.razon_social))
        return res

    _columns = { 
        'numero_expediente' : fields.integer("Numero de Expediente"),
        'fecha_registro' : fields.date('Fecha de Registro'),
        'razon_social' : fields.char("Razon Social", size=128, required=True),
        'numero_folio' : fields.integer("Numero de Folio"),
        'numero_tomo' : fields.integer("Numero de Tomo"),
        'registro_inscrito' : fields.char("Registro Inscrito", size=128),
        'direccion' : fields.char("Direccion", size=256),
        'direccion2' : fields.char("Direccion2", size=256),
        'estado' : fields.many2one("sunacoop.estados", "Estado"),
        'municipio' : fields.many2one("sunacoop.municipios", "Municipio"),
        'parroquia' : fields.many2one("sunacoop.parroquias", "Parroquia"),
        'asociados' : fields.one2many("sunacoop.asociados", "cooperativa_id", 
                                     "Asociados"),
        'cantidad_socios' : fields.function(_get_cantidad_socios, type='integer', string="Cantidad de Asociados"),
        }

    _defaults = {

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
        'cedula' : fields.integer("Documento de Identidad"),
        'direccion' : fields.char("Direccion", size=256),
        'estado' : fields.many2one("sunacoop.estados", "Estado"),
        'municipio' : fields.many2one("sunacoop.municipios", "Municipio"),
        'parroquia' : fields.many2one("sunacoop.parroquias", "Parroquia"),
        'cooperativa_id' : fields.many2one('sunacoop.cooperativas', "Cooperativa"),
        }
    _default = {}
sunacoop_asociados()
