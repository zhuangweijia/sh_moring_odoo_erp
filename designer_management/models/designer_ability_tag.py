
import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError

_logger = logging.getLogger(__name__)

class designer_ability_tag(models.Model):
    _name = 'designer.ability.tag'
    _description = 'designer ability tag'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='tag name', translate=True, required=True, tracking=True)
    tag_type = fields.Selection([('0','skill'),
                                 ('1','product'),
                                 ('2','project')], required=True, tracking=True)
    status = fields.Selection([('draft','draft'),
                               ('confirm','confirm')], default='draft', tracking=True)


    def action_confirm(self):
        self.write({'status':'confirm'})

    def action_draft(self):
        self.write({'status':'draft'})

