import itertools
from lxml import etree

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp.tools import float_compare
import openerp.addons.decimal_precision as dp

class account_move_line(models.Model):
    _inherit = "account.move.line"

    '''@api.onchange('discount', 'discount_price')
    def onchange_discount(self):
        if self.discount > 0.00:
            disc_price = self.price_unit * self.quantity
            tab = (disc_price*(self.discount/100))
            self.discount_price = tab'''


    discount_price = fields.Monetary(string='Discount Amount',compute='_compute_total_discount')

    def _compute_total_discount(self):
       for record in self:
           record.discount_price = ((record.price_unit * record.quantity)*(record.discount/100))
    
    
class ResPartner(models.Model):
	_inherit = "res.partner"

	building_no = fields.Char(string='Building No.')
	area = fields.Char(string='Area')
	postal_code = fields.Char(string='Postal Code')
	branch_name = fields.Char(string='Branch Name')
	

	
class ResCompany(models.Model):
	_inherit = "res.company"

	building_no = fields.Char(string='Building No.')
	area = fields.Char(string='Area')
	postal_code = fields.Char(string='Postal Code')
	branch_name = fields.Char(string='Branch Name')
