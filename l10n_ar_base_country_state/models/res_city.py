##############################################################################
#   Copyright (c) 2018 Eynes/E-MIPS (www.eynes.com.ar)
#   License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################

from odoo import fields, models


class ResCity(models.Model):
    _inherit = 'res.city'

    afip_code = fields.Char(string='AFIP Code', size=16)
<<<<<<< HEAD
    zone_percentage = fields.Float(string = 'IVA Zone percentage', help = 'Porcentaje IVA crédito fiscal para contribuciones patronales.')
=======
>>>>>>> 0a3efb23238b987f350a02bf4cba405f47bc23f4
