# -*- coding: utf-8 -*-

import base64

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource


class designer_project_tag(models.Model):
    _name = 'designer.project.tag'
    _description = 'designer project tag'

    name = fields.Char('project tag', translate=True)
