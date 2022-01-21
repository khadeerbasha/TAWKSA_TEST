# See LICENSE file for full copyright and licensing details

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning
from datetime import date, datetime


	

class StockProductionLot(models.Model):
	_inherit = "stock.production.lot"

	production_date = fields.Datetime(string='Production Date')

class StockMove(models.Model):
	_inherit = "stock.move"
	
	production_date = fields.Datetime(string='Production Date')
	
	'''def _update_reserved_quantity(
		self,
		need,
		available_quantity,
		location_id,
		lot_id=None,
		package_id=None,
		owner_id=None,
		strict=True,
	):
		if self._context.get("sol_lot_id"):
			lot_id = self.sale_line_id.lot_id
		return super()._update_reserved_quantity(
			need,
			available_quantity,
			location_id,
			lot_id=lot_id,
			package_id=package_id,
			owner_id=owner_id,
			strict=strict,
		)'''
        
        
	#def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
		#vals = super()._prepare_move_line_vals(
			#quantity=quantity, reserved_quant=reserved_quant
		#)
		#if reserved_quant and self.sale_line_id.lot_id:
			#vals["lot_id"] = self.sale_line_id.lot_id.id
			#vals["production_date"] = self.sale_line_id.production_date
		#return vals


	#def _prepare_procurement_values(self):
		#res = super(stock_move, self)._prepare_procurement_values()
		#self.ensure_one()
		#if self.sale_line_id and self.sale_line_id.lot_id:
			#res['lot_id'] = self.sale_line_id.lot_id
		#return res

class stock_picking(models.Model):
	_inherit = 'stock.picking'

	def action_lot_number_Set(self):
		for tab in self.move_line_ids_without_package:
			tab.action_lot_set()
	
	
stock_picking()
 

class StockMoveLine(models.Model):
	_inherit = "stock.move.line"

	production_date = fields.Datetime(string='Production Date')
	
	def action_lot_set(self):
		if self.lot_id:
			self.move_id.sale_line_id.lot_id = self.lot_id.id
			self.move_id.sale_line_id.production_date = self.lot_id.production_date
			self.move_id.sale_line_id.expiration_date = self.lot_id.expiration_date
			self.production_date = self.lot_id.production_date
	
	def _assign_production_lot(self, lot):
		super()._assign_production_lot(lot)
		self.lot_id.production_date = self.production_date

    
class AccountMoveLine(models.Model):
	_inherit = "account.move.line"

	lot_id = fields.Many2one('stock.production.lot', string="Lot Number")
	production_date = fields.Datetime(related="lot_id.production_date", string='Production Date')
	expiration_date = fields.Datetime(related="lot_id.expiration_date", string='Expiration Date')

    
	@api.onchange('lot_id')
	def onchange_lot_id(self):
		if self.lot_id:
			self.expiration_date = self.lot_id.expiration_date
			self.production_date = self.lot_id.production_date
			
class SaleOrderLine(models.Model):
	_inherit = "sale.order.line"

	expiration_date = fields.Datetime(string='Expiration Date')
	lot_id = fields.Many2one('stock.production.lot', string="Lot Number", domain="[('product_id', '=', product_id)]")
	production_date = fields.Datetime(string='Production Date')
	
	'''def _prepare_procurement_values(self, group_id=False):
		vals = super()._prepare_procurement_values(group_id=group_id)
		if self.lot_id:
			vals["restrict_lot_id"] = self.lot_id.id
		return vals

	@api.onchange("product_id")
	def product_id_change(self):
		res = super().product_id_change()
		self.lot_id = False
		return res'''

	#@api.onchange("product_id")
	#def _onchange_product_id_set_lot_domain(self):
	#	return {"domain": {"lot_id": [("product_id", "=", self.product_id.id)]}}

		
	def _prepare_invoice_line(self, **optional_values):
		invoice_line = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
		invoice_line['lot_id'] = self.lot_id.id
		return invoice_line
	
	'''@api.onchange("product_id")
	def _onchange_product_id_set_lot_domain(self):
		available_lot_ids = []
		if self.order_id.warehouse_id and self.product_id:
			location = self.order_id.warehouse_id.lot_stock_id
			quants = self.env["stock.quant"].read_group(
				[
					("product_id", "=", self.product_id.id),
					("location_id", "child_of", location.id),
					("quantity", ">", 0),
					("lot_id", "!=", False),
				],
				["lot_id"],
				"lot_id",
			)
			available_lot_ids = [quant["lot_id"][0] for quant in quants]
		self.lot_id = False
		return {"domain": {"lot_id": [("id", "in", available_lot_ids)]}}

	@api.onchange('lot_id')
	def onchange_lot_id(self):
		if self.lot_id:
			self.expiration_date = self.lot_id.expiration_date
			self.production_date = self.lot_id.production_date'''
			

	
