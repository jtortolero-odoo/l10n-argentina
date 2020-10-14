###############################################################################
#
#    Copyright (c) 2019 Eynes/E-MIPS (www.eynes.com.ar)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    "name": "Retentions for ARGENTINA (Retenciones)",
    "category": "L10N AR",
    "version": "12.0.2.0.0",
    "author": "Eynes/E-MIPS",
    "license": "AGPL-3",
    "description": "Implementation of Retentions Taxes for Argentina",
    "depends": [
        "l10n_ar_retentions_perceptions_common",
        "l10n_ar_account_payment_order",
    ],
    "data": [
        "security/res_groups_data.xml",
        "security/ir.model.access.csv",
        "views/retention_view.xml",
        "views/voucher_payment_receipt_view.xml",
        "views/menuitems.xml",
    ],
    "installable": True,
    "application": True,
}
