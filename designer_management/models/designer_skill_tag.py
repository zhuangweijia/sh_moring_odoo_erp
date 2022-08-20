# -*- coding: utf-8 -*-

import base64

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource


class designer_skill(models.Model):
    _name = 'designer.skill.tag'
    _description = 'designer skill.tag'

    name = fields.Char('skill tag', translate=True)
