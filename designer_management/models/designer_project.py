# -*- coding: utf-8 -*-

import json
import base64
import logging

from odoo import models, fields, api, _
from odoo.exceptions import AccessError
#from jsonschema import validate, ValidationError

_logger = logging.getLogger(__name__)


class designer_project(models.Model):
    _name = 'designer.project'
    _description = 'designer project'

    # _inherit = ['mail.thread', 'mail.activity.mixin']

    designer_uuid = fields.Char()
    project_name = fields.Char(required=True, string='project_name')
    position_name = fields.Char(required=True, string='title')
    start_time = fields.Datetime(required=True, string='started at')
    end_time = fields.Datetime(required=True, string='ended at')
    is_current_job = fields.Boolean(default=False, string='is my current job')
    product = fields.Char(string='product')
    client_brand = fields.Char(required=True, string='client')
    description = fields.Text(required=True, string='description')
    active = fields.Boolean(default=True)
    photoes = fields.Many2many('ir.attachment')
    designer_info_id = fields.Many2one('designer.info',string='designer info', ondelete='cascade')
    domain_ids = fields.Many2many('designer.domain', 'designer_project_domain_rel',
            'project_id','domain_id', string='domain')
