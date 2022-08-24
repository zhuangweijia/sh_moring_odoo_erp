# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError

_logger = logging.getLogger(__name__)


class designer_type(models.Model):
    _name = 'designer.type'
    _description = 'designer type'

    name = fields.Char('desiger type', translate=True)


class designer_domain(models.Model):
    _name = 'designer.domain'
    _description = 'designer domain'
    
    name = fields.Char('designer domain', translate=True)
