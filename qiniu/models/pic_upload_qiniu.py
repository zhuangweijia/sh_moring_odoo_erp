#!/usr/bin/env python
# coding=utf-8

import re
import logging
import pdfplumber
import docx
import pandas as pd

from odoo import api, fields, models, _ 
# from odoo.exceptions import UserError, AccessError, except_orm


class picUpload(models.Model):
    _name = 'pic.upload'
    _description = 'Pic Upload'
    # _inherit = ['mail.activity.mixin', 'mail.thread']

    name = fields.Char(string='姓名')
    avatar = fields.Image(string='照片')
    files = fields.Many2many('ir.attachment', string='Files')
