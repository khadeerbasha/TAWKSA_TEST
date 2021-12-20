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

class StockMove(models.Model):
    _inherit = "stock.move"

    def _prepare_procurement_values(self):
        res = super(stock_move, self)._prepare_procurement_values()
        self.ensure_one()
        if self.sale_line_id and self.sale_line_id.lot_id:
            res['lot_id'] = self.sale_line_id.lot_id
        return res
    
    

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    production_date = fields.Datetime(string='Production Date')
    
    def _assign_production_lot(self, lot):
        super()._assign_production_lot(lot)
        self.lot_id.production_date = self.production_date

    
    
class SaleOrderLine(models.Model):
	_inherit = "sale.order.line"

	expiration_date = fields.Datetime(string='Expiration Date')
	lot_id = fields.Many2one('stock.production.lot', string="Lot Number", domain="[('product_id', '=', product_id)]")
	production_date = fields.Datetime(string='Production Date')

	@api.onchange('lot_id')
	def onchange_lot_id(self):
		if self.lot_id:
			self.expiration_date = self.lot_id.expiration_date
			self.production_date = self.lot_id.production_date
    
    
class AccountMoveLine(models.Model):
	_inherit = "account.move.line"

	expiration_date = fields.Datetime(related="sale_line_ids.expiration_date", string='Expiration Date')
	lot_id = fields.Many2one(related="sale_line_ids.lot_id", string="Lot Number")
	production_date = fields.Datetime(related="sale_line_ids.production_date", string='Production Date')

	@api.onchange('lot_id')
	def onchange_lot_id(self):
		if self.lot_id:
			self.expiration_date = self.lot_id.expiration_date
			self.production_date = self.lot_id.production_date
