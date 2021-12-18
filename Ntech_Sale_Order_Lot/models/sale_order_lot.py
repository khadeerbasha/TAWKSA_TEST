# See LICENSE file for full copyright and licensing details

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning
from datetime import date, datetime

class ResCompany(models.Model):
    _inherit = "res.company"

    building_no = fields.Char(string='Building No.')
    area = fields.Char(string='Area')
    postal_code = fields.Char(string='Postal Code')

class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    production_date = fields.Datetime(string='Production Date')
    
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    expiration_date = fields.Datetime(string='Expiration Date')
    lot_id = fields.Many2one('stock.production.lot', string="Lot Number")
    production_date = fields.Datetime(string='Production Date')
    
    @api.onchange('lot_id')
	def onchange_lot_id(self):
		if self.lot_id:
			self.expiration_date = self.lot_id.expiration_date
			self.production_date = self.lot_id.production_date
    
    
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    expiration_date = fields.Datetime(related="sale_line_ids.expiration_date", string='Expiration Date')
    lot_id = fields.Many2one(related="sale_line_ids.lot_id", 'stock.production.lot', string="Lot Number")
    production_date = fields.Datetime(related="sale_line_ids.production_date", string='Production Date')
    
    @api.onchange('lot_id')
	def onchange_lot_id(self):
		if self.lot_id:
			self.expiration_date = self.lot_id.expiration_date
			self.production_date = self.lot_id.production_date

    def _get_payment_count(self):
        for record in self:
            record.payment_count = self.env['account.payment'].search_count([
                                    #('property_id', '=', record.property_id.id),
                                    ('tenancy_id', '=', record.id)])

    def open_entries(self):
        self.ensure_one()
        action = self.env.ref("account.action_account_payments")
        action_dict = action.read()[0] if action else {}
        action_dict["domain"] = [
                                #('property_id', '=', self.property_id.id),
                                ('tenancy_id', '=', self.id)]
        action_dict["context"] = {}
        return action_dict

    def button_register_payment(self):
        self.ensure_one()
        payment_id = False
        acc_pay_form = self.env.ref(
            'account.view_account_payment_form')
        payment_obj = self.env['account.payment']
        payment_method_id = self.env.ref(
            'account.account_payment_method_manual_in')
        vals = {
            'partner_id': self.tenant_id.parent_id.id,
            'partner_type': 'customer',
            'journal_id': self.property_id.asset_journal_id.id,
            'payment_type': 'inbound',
            'tenancy_id': self.id,
            "amount": 0.0,
            'property_id': self.property_id.id,
            'payment_method_id': payment_method_id.id
        }
        payment_id = payment_obj.create(vals)
        return {
            'view_mode': 'form',
            'view_id': acc_pay_form.id,
            'view_type': 'form',
            'res_id': payment_id and payment_id.id,
            'res_model': 'account.payment',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'domain': '[]',
            'context': {
                    'close_after_process': True,
            }
        }

    def button_initial_receive(self):
        """
        This button method is used to open the related
        account payment form view.
        @param self: The object pointer
        @return: Dictionary of values.
        """
        if not self.property_id.asset_journal_id:
            raise UserError(_("Journal Not Defined in the Property"))
        if not self.deposit > 0:
            raise UserError(_("Deposit amount should be greater then zero."))
        inv_obj = self.env['account.move']
        for rec in self:
            move_line_1 = {
                'name': 'Customer Payment',
                'partner_id': rec.tenant_id.parent_id.id,
                'analytic_account_id': rec.id,
                'account_id': self.property_id.asset_insurance_account_id.id,
                'debit': 0,
                'credit': self.deposit
            }
            move_line_2 = {
                'name': 'Customer Payment',
                'partner_id': rec.tenant_id.parent_id.id,
                'analytic_account_id': rec.id,
                'account_id': self.tenant_id.property_account_receivable_id.id,
                'debit': self.deposit,
                'credit': 0,
            }
            move_vals = {
                'ref': self.name,
                'date': date.today(),
                'type': 'entry',
                'tenant_id': self.id,
                'journal_id': self.property_id.asset_journal_id.id,
                'line_ids': [(0, 0, move_line_1), (0, 0, move_line_2)],
            }
            invoice_id = self.env['account.move'].create(move_vals)
            invoice_id.post()
            self.is_initial_receive = True



    def button_receive(self):
        """
        This button method is used to open the related
        account payment form view.
        @param self: The object pointer
        @return: Dictionary of values.
        """
        if not self.property_id.asset_journal_id:
            raise UserError(_("Journal Not Defined in the Property"))
        if not self.property_id.asset_insurance_account_id:
            raise UserError(_("Insurance Account Not Defined in the Property"))
        payment_id = False
        acc_pay_form = self.env.ref(
            'account.view_account_payment_form')
        payment_obj = self.env['account.payment']
        payment_method_id = self.env.ref(
            'account.account_payment_method_manual_in')
        for tenancy_rec in self:
            if tenancy_rec.acc_pay_dep_rec_id and \
                    tenancy_rec.acc_pay_dep_rec_id.id:
                return {
                    'view_type': 'form',
                    'view_id': acc_pay_form.id,
                    'view_mode': 'form',
                    'res_model': 'account.payment',
                    'res_id': tenancy_rec.acc_pay_dep_rec_id.id,
                    'type': 'ir.actions.act_window',
                    'target': 'current',
                    'context': self._context,
                }
            if tenancy_rec.deposit == 0.00:
                raise Warning(_('Please Enter Deposit amount.'))
            if tenancy_rec.deposit < 0.00:
                raise Warning(
                    _('The deposit amount must be strictly positive.'))
            vals = {
                'partner_id': tenancy_rec.tenant_id.parent_id.id,
                'partner_type': 'customer',
                'journal_id': self.property_id.asset_journal_id.id,
                'payment_type': 'inbound',
                'communication': 'Deposit Received',
                'tenancy_id': tenancy_rec.id,
                'amount': tenancy_rec.deposit,
                'property_id': tenancy_rec.property_id.id,
                'payment_method_id': payment_method_id.id
            }
            payment_id = payment_obj.create(vals)
        return {
            'view_mode': 'form',
            'view_id': acc_pay_form.id,
            'view_type': 'form',
            'res_id': payment_id and payment_id.id,
            'res_model': 'account.payment',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'domain': '[]',
            'context': {
                    'close_after_process': True,
            }
        }

    def button_return(self):
        if not self.property_id.asset_journal_id:
            raise UserError(_("Journal Not Defined in the Property"))
        if not self.property_id.asset_insurance_account_id:
            raise UserError(_("Insurance Account Not Defined in the Property"))
        payment_id = False
        acc_pay_form = self.env.ref(
            'account.view_account_payment_form')
        payment_obj = self.env['account.payment']
        payment_method_id = self.env.ref(
            'account.account_payment_method_manual_in')
        for tenancy_rec in self:
            # if tenancy_rec.acc_pay_dep_ret_id and \
            #         tenancy_rec.acc_pay_dep_ret_id.id:
            #     return {
            #         'view_type': 'form',
            #         'view_id': acc_pay_form.id,
            #         'view_mode': 'form',
            #         'res_model': 'account.payment',
            #         'res_id': tenancy_rec.acc_pay_dep_ret_id.id,
            #         'type': 'ir.actions.act_window',
            #         'target': 'current',
            #         'context': self._context,
            #     }
            if tenancy_rec.deposit == 0.00:
                raise Warning(_('Please Enter Deposit amount.'))
            if tenancy_rec.deposit < 0.00:
                raise Warning(
                    _('The deposit amount must be strictly positive.'))
            vals = {
                'partner_id': tenancy_rec.tenant_id.parent_id.id,
                'partner_type': 'supplier',
                'journal_id': self.property_id.asset_journal_id.id,
                'payment_type': 'outbound',
                'communication': 'Deposit Returned',
                'tenancy_id': tenancy_rec.id,
                'amount': tenancy_rec.deposit - tenancy_rec.amount_return,
                'property_id': tenancy_rec.property_id.id,
                'payment_method_id': payment_method_id.id
            }
            payment_id = payment_obj.create(vals)
        return {
            'view_mode': 'form',
            'view_id': acc_pay_form.id,
            'view_type': 'form',
            'res_id': payment_id and payment_id.id,
            'res_model': 'account.payment',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'domain': '[]',
            'context': {
                    'close_after_process': True,
            }
        }

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def post(self):
        res = super(AccountPayment, self).post()
        if self.property_id and self.tenancy_id:
            account_move_lines = self.env['account.move.line'].search([('payment_id', '=', self.id)])
            if account_move_lines and self.partner_type == 'supplier' and \
                self.payment_type == 'outbound':
                for lines in account_move_lines:
                    if lines.debit > 0:
                        lines.account_id = lines.partner_id.property_account_receivable_id.id
                    if lines.credit > 0:
                        lines.account_id = self.journal_id.default_debit_account_id.id
                if self.tenancy_id.amount_return < self.tenancy_id.deposit:
                    self.tenancy_id.amount_return += self.amount
                    if self.tenancy_id.amount_return >= self.tenancy_id.deposit:
                        self.tenancy_id.return_deposit = True
            elif account_move_lines and self.partner_type == 'customer' and \
                self.payment_type == 'inbound':
                for lines in account_move_lines:
                    if lines.debit > 0:
                        lines.account_id = self.journal_id.default_debit_account_id.id
        return res
