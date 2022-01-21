# -*- coding: utf-8 -*-
from odoo import api, fields, models
import base64
from random import choice
from string import digits
import itertools
from werkzeug import url_encode
import pytz
from collections import defaultdict

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource
from odoo.addons.resource.models.resource_mixin import timezone_datetime

import json
import time
from ast import literal_eval
from collections import defaultdict
from datetime import date
from itertools import groupby
from operator import itemgetter

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, format_datetime
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.tools.misc import format_date

class sale_order(models.Model):
	_inherit = 'sale.order'

	employee_id = fields.Many2one('hr.employee',  string="Employee")

	def _prepare_invoice(self):
		invoice_vals = super(sale_order, self)._prepare_invoice()
		invoice_vals['employee_id'] = self.employee_id.id
		return invoice_vals
	
	
sale_order()

class AccountMove(models.Model):
	_inherit = "account.move"
	
	employee_id = fields.Many2one('hr.employee',  string="Employee")
