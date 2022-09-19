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
    "name": "Account Check",
    "category": "L10N AR",
    "version": "12.0.1.0.0",
    "author": "Eynes/E-MIPS",
    "license": "AGPL-3",
    "description": "Allows to manage checks.",
    "depends": [
        "account",
        "l10n_ar_account_payment_order",
        "l10n_ar_point_of_sale",
<<<<<<< HEAD
=======
        'report_xlsx',
        'web_notify',
>>>>>>> 0a3efb23238b987f350a02bf4cba405f47bc23f4
    ],
    "data": [
        "security/account_check_security.xml",
        "security/ir.model.access.csv",
<<<<<<< HEAD
        "wizard/annull_checks_view.xml",
        "wizard/view_check_deposit.xml",
        "wizard/view_check_reject.xml",
=======
        "security/ir_rule.xml",
        "wizard/annull_checks_view.xml",
        "wizard/view_check_deposit.xml",
        "wizard/view_check_reject.xml",
        "wizard/check_returned_view.xml",
>>>>>>> 0a3efb23238b987f350a02bf4cba405f47bc23f4
        "wizard/add_checks_view.xml",
        "wizard/accredit_checks_view.xml",
        "views/account_check_view.xml",
        "wizard/create_checkbook_view.xml",
        "views/checkbook_view.xml",
        "views/account_payment_order_view.xml",
        "views/account_voucher_view.xml",
        "views/partner_view.xml",
<<<<<<< HEAD
=======
        'views/reason_rejected_check_view.xml',
        'views/account_invoice_view.xml',
        'wizard/report_returned_view.xml',
        'report/report_returned_check_view.xml',
    ],
    'qweb': [
        'static/src/xml/reverse_payment.xml',
>>>>>>> 0a3efb23238b987f350a02bf4cba405f47bc23f4
    ],
    "installable": True,
    "application": True,
}
