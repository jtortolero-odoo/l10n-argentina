###############################################################################
#
#    Copyright (c) 2018 Eynes/E-MIPS (www.eynes.com.ar)
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
    "name": "Payment Order",
    "category": "L10N AR",
    "version": "12.0.1.0.0",
    "author": "Eynes/E-MIPS",
    "license": "AGPL-3",
    "description": "Payment Order document with argentinian payment methods.",
    "depends": [
        "base_period",
<<<<<<< HEAD
=======
#        "l10n_ar_invoice_currency",
        'account_financial_report',  # only for translation in i18n/
>>>>>>> 0a3efb23238b987f350a02bf4cba405f47bc23f4
    ],
    "data": [
        "security/payment_rule.xml",
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/account_payment_order_view.xml",
        "views/account_journal_view.xml",
    ],
    "installable": True,
    "application": True,
}
