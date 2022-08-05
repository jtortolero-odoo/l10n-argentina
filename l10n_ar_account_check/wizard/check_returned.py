
import json
from datetime import date
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ReturnedCheck(models.Model):
    _name = 'account.returned.check'
    _description = 'Returned Check'

    return_date = fields.Date(string='Return Date', required=True)
    reason = fields.Many2one(comodel_name='reason.rejected.check', string='Reason',
                             domain="[('type', '=', 'returned')]", required=True)
    generate_journal_entry = fields.Boolean(string='Generate Return Journal Entry', default=True)
    note = fields.Text(string='Observations')

    def action_return(self):
        record_id = self.env.context.get('active_ids', [])
        check_obj = self.env['account.issued.check'].browse(record_id)

        check_obj.write(
            {'reject_date': self.return_date,
             'note': self.note})

        if self.generate_journal_entry:
            self.create_returned_journal_entry(check_obj)

        # update invoice amounts
        self.update_invoice(check_obj)

        check_obj.return_check()
        return {'type': 'ir.actions.act_window_close'}

    def create_returned_journal_entry(self, check):
        move_obj = self.env['account.move']
        move_line_obj = self.env['account.move.line']
        payment_order = check.payment_order_id
        payment_check_line = payment_order.move_line_ids.filtered(lambda x:
                                                                  x.debit == 0 and x.credit != 0 and
                                                                  x.name == 'Cheque Propio ' + check.number
                                                                  )

        ctx = {
            'date': self.return_date,
            'check_move_validity': False,
        }

        # Create the account move record.
        original_move_data = payment_order.account_move_get()
        original_move_data['state'] = 'posted'
        move_recordset = move_obj.with_context(ctx).create(original_move_data)

        # Get the name of the account_move just created
        move_id = move_recordset.id
        partner_id = payment_check_line.partner_id

        # haber: cuenta a pagar establecida en la ficha del proveedor
        inverse_supplier_line = {
            'name': '/',
            'account_id': partner_id.property_account_payable_id.id,
            'move_id': move_id,
            'partner_id': partner_id.id,
            'period_id': payment_check_line.period_id.id,
            'date': self.return_date,
            'credit': payment_check_line.credit,
            'debit': 0,
            'amount_currency': payment_check_line.amount_currency,
            'journal_id': original_move_data['journal_id'],
            'currency_id': payment_check_line.currency_id.id,
            'analytic_account_id': payment_check_line.analytic_account_id.id,
            'ref': _('Cheque devuelto') + ': Cheque Propio ' + (check.number or '/'),
        }
        move_line_obj.with_context(ctx).create(inverse_supplier_line)

        # debe: cuenta del banco donde se emitió el cheque
        inverse_check_line = {
            'name': _('Cheque devuelto') + ': Cheque Propio ' + (check.number or '/'),
            'account_id': payment_check_line.account_id.id,
            'move_id': move_id,
            'partner_id': payment_check_line.partner_id.id,
            'period_id': payment_check_line.period_id.id,
            'date': self.return_date,
            'credit': 0,
            'debit': payment_check_line.credit,
            'amount_currency': payment_check_line.amount_currency,
            'journal_id': original_move_data['journal_id'],
            'currency_id': payment_check_line.currency_id.id,
            'analytic_account_id': payment_check_line.analytic_account_id.id,
            'ref': _('Cheque devuelto') + ': Cheque Propio ' + (check.number or '/'),
        }
        move_line_obj.with_context(ctx).create(inverse_check_line)

    def get_invoice_by_check(self, check):
        # hardcode invoice from check
        original_entry = check.payment_move_id
        ch_line = original_entry.line_ids.filtered(lambda x:
                                                   x.name == 'Cheque Propio ' + check.number and
                                                   x.debit == 0 and x.credit != 0)
        rev_line = original_entry.line_ids.filtered(lambda x:
                                                    x.debit != 0 and x.credit == 0 and
                                                    x.date_maturity == ch_line.date_maturity and
                                                    x.partner_id == ch_line.partner_id)
        return self.env['account.invoice'].search([('internal_number', '=', rev_line.name)])

    def update_invoice(self, check):
        ch_invoice = self.get_invoice_by_check(check)
        if not ch_invoice:
            raise UserError('No se econtró una factura asociada.')

        # outstanding payment
        payment_dict = json.loads(ch_invoice.payments_widget)
        reverse_dict = {'content': []}
        for cont in payment_dict['content']:
            if cont['amount'] == check.amount and cont['move_id'] == check.payment_move_id.id:
                cont['rev_date'] = date.today()
                reverse_dict['content'].append(cont)
        if reverse_dict:
            ch_invoice.compute_reverse_widget(reverse_dict)

        if ch_invoice.state == 'paid' and check.payment_order_id:
            check.payment_order_id.cancel_voucher()
