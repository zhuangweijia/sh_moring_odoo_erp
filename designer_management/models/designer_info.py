# -*- coding: utf-8 -*-

import base64

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource


class designer_info(models.Model):
    _name = 'designer.info'
    _description = 'designer infomation'

    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin', 'image.mixin']

    name = fields.Char('设计师/工作室名称')
    phone = fields.Char('电话')
    email = fields.Char('电子邮件')

    @api.model
    def _default_image(self):
        image_path = get_module_resource('designer_management', 'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    image_1920 = fields.Image('图像', default=_default_image)
    schedule = fields.Boolean('档期', default=True)
    address = fields.Char('邮寄地址', translate=True)
    bank_account = fields.Char('银行账户信息', help='请输入银行账户信息..')
    project = fields.Html('项目经历')
    recommend_degree = fields.Selection([('0','0'), ('1','1'), ('2','2'), ('3','3'),
                                         ('4','4'),], string="推荐度", default='0')
    is_trained = fields.Boolean(string='是否培训过', default=False)
    is_exclusive_signed = fields.Boolean(string='是否签署过唯一排他协议', default=True)
    type_id = fields.Many2one('designer.type', string='设计师类型')
    field_ids = fields.Many2many('designer.field', 'designer_info_field_rel','info_id','field_id', string='领域')

    feature = fields.Text(string='特点', help='请输入此设计师的特点...')
    endorsement = fields.Text(string='背书', help='请输入此设计师的背书...')
    note = fields.Text(string='备注', help='请输入其他备注信息...')
    brief_intro = fields.Text(string='简介', help='请输入此设计师的简介...')

    is_cooperate = fields.Boolean(string='合作状态', default=False)
    cooperate_pjt = fields.Char(string='正在合作项目') #TODO: 应该是关联关系
    cooperate_note = fields.Text(string='合作项目/来源备注')
    budget_refer = fields.Text(string='预算参考')

    files = fields.Many2many('ir.attachment', string='电子签名图片/文件')

    status = fields.Selection([('draft','草稿'),
                               ('confirm', '已入库'),
                               ('cancel', '已作废')], default='draft')

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


class designer_type(models.Model):
    _name = 'designer.type'
    _description = 'designer type'

    name = fields.Char('类型', help='设计师类型', translate=True)


class designer_field(models.Model):
    _name = 'designer.field'
    _description = 'designer field'
    
    name = fields.Char('领域', translate=True)

