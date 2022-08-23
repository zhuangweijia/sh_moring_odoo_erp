# -*- coding: utf-8 -*-

import base64
import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource
import json
import logging
_logger = logging.getLogger(__name__)


class designer_info(models.Model):
    _name = 'designer.info'
    _description = 'designer infomation'
    # _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin', 'image.mixin']
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']

    """
    @api.model
    def _default_image(self):
        image_path = get_module_resource('designer_management', 'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())
    """

    # base
    uuid = fields.Char(string='uuid')
    name = fields.Char(string='name', required=True)
    phone = fields.Char(string='tel', required=True)
    postal_address = fields.Char(translate=True)
    email = fields.Char(string='email', required=True)
    source = fields.Char(string='source', translate=True, default='bonjourid.com')
    image_1920 = fields.Image('portrait')
    # image_1920 = fields.Image('portrait', default=_default_image)
    intermediate_contact = fields.Char()
    intermediate_agency = fields.Char()
    is_trained = fields.Boolean(default=False)
    lastest_trained_date = fields.Date()
    e_signature_pic = fields.Many2many('ir.attachment')
    # files = fields.Many2many('ir.attachment')
    recommendation_level = fields.Selection([('1','1'), ('2','2'),
                                             ('3','3'), ('4','4'), ('5','5')],
                                             default='1', required=True)
    # project
    current_project = fields.Char(translate=True)
    book = fields.Char(translate=True)
    book_status = fields.Char(translate=True)
    project_name_list = fields.Char(translate=True)

    # money
    budget_unit = fields.Integer()
    budget_refer = fields.Char(translate=True)
    bank_account_info = fields.Char(help=_('Please enter bank account information...'), translate=True)
    # description
    specialities = fields.Char(translate=True)
    specialities_brief = fields.Char(translate=True)
    style = fields.Char(translate=True)
    brief_intro = fields.Text(string='introduction', help=_('Please enter a bio for this designer...'), translate=True)
    memo = fields.Text(string='memo', help=_('Please enter other remarks...'), translate=True)
    endorsement = fields.Text(string='endorsement', required=True, translate=True,
                              help=_("Please enter this designer's endorsement..."))
    # Cooperation
    collaboration_status = fields.Boolean(default=False)
    # tags
    skill_tag_ids = fields.Many2many('designer.skill.tag','designer_skill_tag_rel',
                                    'info_id', 'skill_id', string='Designer Skill Tag')
    project_tag_ids = fields.Many2many('designer.project.tag','designer_project_tag_rel',
                                    'info_id', 'project_id', string='Designer Project Tag')
    product_tag_ids = fields.Many2many('designer.product.tag','designer_product_tag_rel',
                                    'info_id', 'product_id', string='Designer Product Tag')
    type_id = fields.Many2one('designer.type', string='talent type')
    field_ids = fields.Many2many('designer.field', 'designer_info_field_rel',
                                 'info_id','field_id',
                                 string='domain') 
    # other
    is_exclusive_signed = fields.Boolean(default=True)
    # schedule = fields.Boolean('schedule', default=True)
    project = fields.Html('project')
    # feature = fields.Text(string='feature', help=_('Please enter the characteristics of this designer...'))
    confirmed_date = fields.Datetime()
    status = fields.Selection([('draft','draft'),
                               ('confirm', 'confirm'),
                               ('cancel', 'cancel')], default='draft')

    def action_confirm(self):
        self.write({'status': 'confirm'})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title':'确认结果',
                'message':"此设计师已入库",
                'type': 'success',
                'next': {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }
            }
        }

    def action_draft(self):
        self.write({'status': 'draft'})
        return

    def action_cancel(self):
        self.write({'status': 'cancel'})
        return

    @api.model
    def create_designer_info(self,data):
        value = {"result":True,
                 "msg":"hello,少年",
                 "data":None}
        _logger.info(f"data:{data}")
        data = json.loads(data)
        val = {
            "uuid":data.get("uuid",""),
            "name":data.get("name",""),
            "phone":data.get("phone",""),
            "email":data.get("email",""),
        }
        designer = self.env['designer.info'].create(val)
        return json.dumps(value)

    @api.model
    def get_designer_info(self,data):
        _logger.info('-- in get_designer_info: {data}')
        _logger.info('-- type of data: {type(data)}')
        value = {"result":False,
                 "msg":"hello,designer!",
                 "data":None}
        uuid =json.load(data).get("uuid")
        if uuid == None or uuid == "":
            return json.dumps(value)
        designer = self.env['designer.info'].search([['uuid',"=",uuid]])
        if len(designer) == 0:
            return json.dumps(value)
        else:
            value['result'] = True
            value['data'] = designer[0]
            return json.dumps(value)

    @api.model
    def update_designer_info(self,data):
        value = {"result":False,
                 "msg":"hello,old friend!",
                 "data":None}
        designer = self.env['designer.info'].search(['uuid',"=",uuid])
        return json.dumps()
    
class designer_type(models.Model):
    _name = 'designer.type'
    _description = 'designer type'

    name = fields.Char('desiger type', translate=True)


class designer_field(models.Model):
    _name = 'designer.field'
    _description = 'designer field'
    
    name = fields.Char('designer domain', translate=True)

