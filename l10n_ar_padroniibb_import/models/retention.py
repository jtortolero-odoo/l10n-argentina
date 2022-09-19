##############################################################################
#   Copyright (c) 2018 Eynes/E-MIPS (www.eynes.com.ar)
#   License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RetentionRetention(models.Model):
    _name = "retention.retention"
    _inherit = "retention.retention"

    from_register_ARBA = fields.Boolean('From ARBA Register')
    from_register_AGIP = fields.Boolean('From AGIP Register')

    @api.model
    def _get_retention_from_arba(self):
<<<<<<< HEAD
        ret = self.search([('from_register_ARBA', '=', True)])
=======
        ret = self.search([('from_register_ARBA', '=', True), ('company_id', '=', self.env.user.company_id.id)])
>>>>>>> 0a3efb23238b987f350a02bf4cba405f47bc23f4
        if len(ret) > 1:
            raise ValidationError(
                _('Retentions Improperly Configured\n') +
                _('You can not have more than one retention to update ' +
                  'from ARBA. Please review configuration'))
        elif len(ret) == 0:
            return False
        else:
            return ret

    @api.model
    def _get_retention_from_agip(self):
<<<<<<< HEAD
        ret = self.search([('from_register_AGIP', '=', True)])
=======
        ret = self.search([('from_register_AGIP', '=', True), ('company_id', '=', self.env.user.company_id.id)])
>>>>>>> 0a3efb23238b987f350a02bf4cba405f47bc23f4
        if len(ret) > 1:
            raise ValidationError(
                _('Retentions Improperly Configured\n') +
                _('You can not have more than one retention to update ' +
                  'from AGIP. Please review configuration'))
        elif len(ret) == 0:
            return False
        else:
            return ret
