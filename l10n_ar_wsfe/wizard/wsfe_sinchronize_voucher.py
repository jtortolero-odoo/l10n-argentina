##############################################################################
#   Copyright (c) 2018 Eynes/E-MIPS (www.eynes.com.ar)
#   License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
##############################################################################

import time

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT


class wsfe_sinchronize_voucher(models.TransientModel):
    """
    This wizard is used to get information about a voucher
    informed to AFIP through WSFE
    """
    _name = "wsfe.sinchronize.voucher"
    _description = "WSFE Sinchroniza Voucher"

    def _get_def_config(self):
        wsfe_conf_model = self.env['wsfe.config'].with_context(company_id=self.env.user.company_id.id)
        return wsfe_conf_model.get_config()

    def _get_def_config_wsfex(self):
        wsfe_conf_model = self.env['wsfex.config'].with_context(company_id=self.env.user.company_id.id)
        return wsfe_conf_model.get_config()

    voucher_type = fields.Many2one(
        'wsfe.voucher_type', 'Voucher Type', required=False)
    pos_id = fields.Many2one('pos.ar', 'POS', required=False)
    manual_pos_id = fields.Many2one('pos.ar', 'POS', required=False, domain=[('allow_manual_sync', '=', True)])
    config_id = fields.Many2one(
        'wsfe.config', 'Config', default=_get_def_config)
    config_wsfex_id = fields.Many2one(
        'wsfex.config', 'Config WSFEX', default=_get_def_config_wsfex)
    voucher_number = fields.Integer('Number', required=False)
    manual_voucher_number = fields.Integer('Number', required=False)
    document_type = fields.Many2one(
        'res.document.type', 'Document Type', readonly=True)
    document_number = fields.Char('Document Number', readonly=True)
    date_invoice = fields.Date('Date Invoice', readonly=False)
    manual_date_invoice = fields.Date('Date Invoice', required=False)
    amount_total = fields.Float(
        digits=dp.get_precision('Account'), string="Total", readonly=True)
    amount_no_taxed = fields.Float(
        digits=dp.get_precision('Account'), string="No Taxed", readonly=True)
    amount_taxed = fields.Float(
        digits=dp.get_precision('Account'), string="Taxed", readonly=True)
    amount_tax = fields.Float(
        digits=dp.get_precision('Account'), string="Tax", readonly=True)
    amount_exempt = fields.Float(
        digits=dp.get_precision('Account'), string="Amount Exempt",
        readonly=True)
    cae = fields.Char('CAE', size=32, required=False, readonly=False)
    manual_cae = fields.Char('CAE', size=32, required=False)
    cae_due_date = fields.Date('CAE Due Date', readonly=False)
    manual_cae_due_date = fields.Date('CAE Due Date', required=False)
    date_process = fields.Datetime('Date Processed', readonly=True)
    infook = fields.Boolean('Info OK', default=False)
    use_wsfex = fields.Boolean('Use WSFEX?', default=False)
    invoice_id = fields.Many2one('account.invoice', 'Invoice')

    @api.onchange('config_id', 'voucher_type')
    def change_pos(self):
        pos_model = self.env['pos.ar']
        wsfe_conf = self.config_id
        wsfex_conf = self.config_wsfex_id
        ids = [p.id for p in wsfe_conf.point_of_sale_ids]
        if wsfex_conf:
            ids.extend([p.id for p in wsfex_conf.point_of_sale_ids])
        denomination_id = self.voucher_type.denomination_id.id or False
        operator = 'in'
        if not denomination_id:
            operator = '='
        domain = [('id', 'in', ids),
                  ('denomination_ids', operator, denomination_id)]
        pos_ids = pos_model.search(domain)
        if len(pos_ids) == 1:
            self.pos_id = pos_ids[0]
        return {
            'domain': {
                'pos_id': domain,
            }
        }

    @api.onchange('voucher_number')
    def change_voucher_number(self):

        invoice_model = self.env['account.invoice']

        voucher_type = self.voucher_type.code
        pos = int(self.pos_id.name)
        number = self.voucher_number

        if not voucher_type or not pos or not number:
            return

        if not self.use_wsfex:
            res = self.config_id.get_voucher_info(pos, voucher_type, number)
        else:
            res = self.config_wsfex_id.get_voucher_info(pos, voucher_type, number)
            if not res['Id']:
                raise ValidationError(_('Voucher Not Found'))
        try:
            # WSFEX Does not return DocTipo
            doc_ids = self.env['res.document.type'].search(
                [('afip_code', '=', res['DocTipo'])])
        except Exception:
            document_type = False
        else:
            document_type = doc_ids and doc_ids[0] or False

        if not self.use_wsfex:
            di = time.strftime(DEFAULT_SERVER_DATE_FORMAT,
                            time.strptime(str(res['CbteFch']), '%Y%m%d'))
            dd = time.strftime(DEFAULT_SERVER_DATE_FORMAT,
                            time.strptime(str(res['FchVto']), '%Y%m%d'))
            dpr = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT,
                                time.strptime(str(res['FchProceso']),
                                            '%Y%m%d%H%M%S'))
        else:
            di = time.strftime(DEFAULT_SERVER_DATE_FORMAT,
                            time.strptime(str(res['Fecha_cbte']), '%Y%m%d'))
            dd = time.strftime(DEFAULT_SERVER_DATE_FORMAT,
                            time.strptime(str(res['Fch_venc_Cae']), '%Y%m%d'))
            dpr = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT,
                                time.strptime(str(res['Id']),
                                            '%Y%m%d%H%M%S'))

        # TODO: Tandriamos que filtrar las invoices por
        # Tipo de Comprobante tambien para ello podemos agregar
        # un par de campos mas para usarlos como filtros,
        # por ejemplo, is_debit_note y type
        self.document_type = document_type
        dres = dict(res)
        self.document_number = str(dict(res).get('DocNro') or dict(res).get('Id_impositivo'))
        self.date_invoice = di  # str(res['CbteFch']),
        self.amount_total = dres.get('ImpTotal') or dres.get('Imp_total')
        self.amount_no_taxed = dres.get('ImpTotConc', 0)
        self.amount_taxed = dres.get('ImpNeto', 0)
        self.amount_tax = dres.get('ImpIVA', 0) + dres.get('ImpTrib', 0)
        self.amount_exempt = dres.get('ImpOpEx', 0)
        self.cae = str(dres.get('CodAutorizacion') or dres.get('Cae'))
        self.cae_due_date = dd
        self.date_process = dpr
        self.infook = True

        if self.document_number == '0':
            doc_number = [False, '0', '']
        else:
            doc_number = [self.document_number]

        if not self.use_wsfex:
            domain = [
                ('amount_total', '=', self.amount_total),
                ('amount_exempt', '=', self.amount_exempt),
                ('amount_taxed', '=', self.amount_taxed),
                ('amount_no_taxed', '=', self.amount_no_taxed),
                ('state', 'in', ('draft', 'proforma2', 'proforma'))]
            if document_type and document_type.afip_code != '99':
                domain.append(('partner_id.vat', 'in', doc_number))
        else:
            domain = [
                ('partner_id.vat', '=like', str(dres['Id_impositivo'])),
                ('amount_total', '=', self.amount_total),
                ('state', 'in', ('draft', 'proforma2', 'proforma')),
                ('local', '=', False)
            ]


        invoice_ids = invoice_model.search(domain)
        if len(invoice_ids) == 1:
            self.invoice_id = invoice_ids and invoice_ids[0]

        return {
            'domain': {
                'invoice_id': domain
            }
        }

    @api.one
    def relate_invoice(self):

        # Obtenemos los datos puestos por el usuario
        invoice = self.invoice_id

        if not self.infook:
            raise UserError(
                _("WSFE Error!\n") +
                _("Sinchronize process is not correct!"))

        pos = int(self.pos_id.name)
        number = self.voucher_number
        date_invoice = self.date_invoice

        invoice.wsfe_relate_invoice(pos, number, date_invoice,
                                    self.cae, self.cae_due_date)

        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def relate_invoice_manual(self):

        # Obtenemos los datos puestos por el usuario
        invoice = self.env['account.invoice'].browse(self.env.context['active_id'])

        pos = int(self.manual_pos_id.name)
        number = self.manual_voucher_number
        date_invoice = self.manual_date_invoice

        invoice.wsfe_relate_invoice(pos, number, date_invoice,
                                    self.manual_cae, self.manual_cae_due_date)

        return {'type': 'ir.actions.act_window_close'}
