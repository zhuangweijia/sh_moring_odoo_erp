# -*- coding: utf-8 -*-

import base64

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource


class designer_product_tag(models.Model):
    _name = 'designer.product.tag'
    _description = 'designer product.tag'

    name = fields.Char('product tag', translate=True)
