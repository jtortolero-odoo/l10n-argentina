##############################################################################
#   Copyright (c) 2018 Eynes/E-MIPS (www.eynes.com.ar)
#   License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################

from odoo import _, fields, models
from odoo.exceptions import UserError


class WizardCreateCheck(models.Model):
    _name = "wizard.create.check"
    _description = "Wizard Create Check"

    bank_account_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Bank', required=True)
    start_num = fields.Char(
        string='Start number of check',
<<<<<<< HEAD
        size=20, required=True)
    end_num = fields.Char(string='End number of check', size=20, required=True)
=======
        size=20)
    end_num = fields.Char(string='End number of check', size=20)
>>>>>>> 0a3efb23238b987f350a02bf4cba405f47bc23f4
    checkbook_num = fields.Char(
        string='Checkbook number', size=20, required=True)
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        required=True, default=lambda self: self.env.user.company_id.id)
    type = fields.Selection([
        ('common', 'Common'),
        ('postdated', 'Post-dated')],
        string='Checkbook Type',
<<<<<<< HEAD
        help="If common, checks only have issued_date. \
        If post-dated they also have payment date",
        required=True)
=======
        help="If common, checks only have issued_date. If post-dated they also have payment date")
    checkbook_type = fields.Selection([
        ('physical', 'Physical'),
        ('virtual', 'Virtual'),
        ('echeq', 'Echeq')],
        string='Checkbook Class')
>>>>>>> 0a3efb23238b987f350a02bf4cba405f47bc23f4

    def create_checkbook(self):
        checkbook_obj = self.env['account.checkbook']
        checkbook_id = False
        for form in self:
<<<<<<< HEAD
            start_num = int(form.start_num)
            end_num = int(form.end_num)
            if start_num > end_num:
                raise UserError(
                    _('Error creating Checkbook!\n' +
                      'End number cannot be lower than Start number'))

            # Creamos los cheques numerados
            checks = []
            for n in range(start_num, end_num + 1):
                check_vals = {'name': str(n), 'type': form.type}
                checks.append((0, 0, check_vals))

            # Creamos la chequera
            checkbook_vals = {
                'name': form.checkbook_num,
                'bank_id': form.bank_account_id.bank_id.id,
                'bank_account_id': form.bank_account_id.id,
                'check_ids': checks,
                'type': form.type,
            }

            checkbook_id = checkbook_obj.create(checkbook_vals)
=======
            if form.checkbook_type != "echeq":
                start_num = int(form.start_num)
                end_num = int(form.end_num)
                if start_num > end_num:
                    raise UserError(
                        _('Error creating Checkbook!\n' +
                        'End number cannot be lower than Start number'))

                # Creamos los cheques numerados
                checks = []
                for n in range(start_num, end_num + 1):
                    check_vals = {'name': str(n), 'type': form.type}
                    checks.append((0, 0, check_vals))

                # Creamos la chequera
                checkbook_vals = {
                    'name': form.checkbook_num,
                    'bank_id': form.bank_account_id.bank_id.id,
                    'bank_account_id': form.bank_account_id.id,
                    'check_ids': checks,
                    'type': form.type,
                    'checkbook_type': form.checkbook_type,
                }

                checkbook_id = checkbook_obj.create(checkbook_vals)
            else:
                checkbook_vals = {
                    'name': form.checkbook_num,
                    'bank_id': form.bank_account_id.bank_id.id,
                    'bank_account_id': form.bank_account_id.id,
                    'type': form.type,
                    'checkbook_type': form.checkbook_type,
                }

                checkbook_id = checkbook_obj.create(checkbook_vals)
>>>>>>> 0a3efb23238b987f350a02bf4cba405f47bc23f4

        if not checkbook_id:
            return {'type': 'ir.actions.act_window_close'}

        return {
            'domain': [('id', '=', str(checkbook_id.id))],
            'name': 'Checkbook',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.checkbook',
            'view_id': False,
            'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window'
        }
