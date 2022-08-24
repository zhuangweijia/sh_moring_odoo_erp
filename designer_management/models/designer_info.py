# -*- coding: utf-8 -*-

import base64
import logging

from odoo import models, fields, api, _
from odoo.exceptions import AccessError
from odoo.modules.module import get_module_resource
import json
#from jsonschema import validate, ValidationError
from validator import validate
import logging
_logger = logging.getLogger(__name__)

schema_designer = {
    "lang":"required",
    "uuid":"required",
    "firstname": "required",
    "lastname": "required",
    "email":"required",
    "budget_unit_u":"required",
    "introduction_u":"required",
    "tel":"required",
    "portrait_u":"required",
    "have_exclusive_contract":"required",
    "experience_years":"required",
    "domain":"required",
    "educations":"required",
    "creation_pics":"required",
    "skill_tags":"required",
}

schema_designer2 = {
    "lang":"required",
    "uuid":"required",
    "firstname": "min:3|max:30",
    "lastname": "min:3|max30",
    "email":"mail",
    "budget_unit_u":"required",
    "introduction_u":"required",
    "tel":"required",
    "portrait_u":"required",
    "have_exclusive_contract":"required",
    "experience_years":"required",
    "domain":"required",
    "educations":"list|min:1",
    "creation_pics":"list|min:1",
    "skill_tags":"list|min:1",
}

'''  
    #"available_from":lambda x: x == null or x=="" or 
    #"available_until":"required",
    #"book_u":"required",
    "home_page":lambda x:  x == False or isinstance(x,str) and len(x)<= 50,
    "linkin_page":lambda x:  x == False or isinstance(x,str) and len(x)<= 50,
    "intermediate_agency":lambda x:  x == False or isinstance(x,str) and len(x)<= 50,
    "intermediate_contact":lambda x:  x == False or isinstance(x,str) and len(x)<= 50,
    "specialities":lambda x:   x == False or isinstance(x,str) and len(x)<= 2000,
    "memo":lambda x:  x == False or isinstance(x,str) and len(x)<= 2000,
    "postal_address":lambda x:  x == False or isinstance(x,str) and len(x)<= 200,
    "bank_account_info":lambda x:  x == False or isinstance(x,str) and len(x)<= 200,
    '''

schema_designer22_= {
    "uuid":"required",
    "first_name": "required",
    "last_name": "required",
    "email":"required|email",
}

def json_validate(schema):
    def wrapper(func):
        def inner(obj, *args, **kwargs):
            _logger.info(f"wrapper obj:{obj}")
            _logger.info(f"wrapper args:{args}")
            _logger.info(f"wrapper args[0]:{args[0]}")
            try:
                json_data = json.loads(args[0])
            except Exception as e:
                value = {
                    "result":-1,
                    "data":None,
                    "errors":"json is not validate",
                }
                return json.dumps(value)
            result,_,errors = validate(json_data,schema,return_info=True)
            if result== False:
                value = {
                    "result":-1,
                    "data":None,
                    "errors":errors,
                }
                return json.dumps(value)
            _logger.info(f"参数校验OK")
            return func(obj ,*args, **kwargs)
        return inner
    return wrapper

schema_uuid1 = {
    "uuid":"required",
}

def validate_uuid(schema):
    def wrapper(func):
        def inner(obj, *args, **kwargs):
            _logger.info(f"wrapper obj:{obj}")
            _logger.info(f"wrapper args:{args}")
            _logger.info(f"wrapper args[0]:{args[0]}")
            try:
                json_data = json.loads(args[0])
            except Exception as e:
                value = {
                    "result":-1,
                    "data":None,
                    "errors":"json is not validate",
                }
                return json.dumps(value)
            result,_,errors = validate(json_data,schema,return_info=True)
            if result== False:
                value = {
                    "result":-1,
                    "data":None,
                    "errors":errors,
                }
                return json.dumps(value)
            return func(obj ,*args, **kwargs)
        return inner
    return wrapper




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

    # 用于同步的冗余字段 add by eric
    lang = fields.Char(string='lang')
    firstname = fields.Char(string='first_name')
    lastname = fields.Char(string='last_name')
    endorsement = fields.Char(string='last_name')
    budget_unit_u = fields.Integer(string='budget_unit_u')
    specialities_u = fields.Char(string='specialities_u')
    memo_u = fields.Char(string='memo_u')
    introduction_u = fields.Char(string='introduction_u')
    tel = fields.Char(string='tel')
    portrait_u = fields.Char(string='portrait_u')
    #intermediate_agency = fields.Char(string='intermediate_agency')
    #intermediate_contact = fields.Char(string='intermediate_contact')
    #email = fields.Char(string='email')
    #postal_address = fields.Char(string='postal_address')
    #bank_account_info = fields.Char(string='bank_account_info')
    have_exclusive_contract = fields.Integer(string='have_exclusive_contract')
    excluesive_contract_content_u = fields.Char(string='excluesive_contract_content_u')
    available_from = fields.Date(string='available_from')
    available_util = fields.Date(string='available_util')
    home_page = fields.Char(string='home_page')
    linkin_page = fields.Char(string='linkin_page')
    experience_years = fields.Char(string='experience_years')


    
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
    skill_tag_ids = fields.Many2many('designer.ability.tag','designer_skill_tag_rel',
                                    'info_id', 'skill_id', string='Designer Skill Tag',
                                     domain="[('tag_type','=','0')]")
    project_tag_ids = fields.Many2many('designer.ability.tag','designer_project_tag_rel',
                                    'info_id', 'project_id', string='Designer Project Tag',
                                     domain="[('tag_type','=','2')]")
    product_tag_ids = fields.Many2many('designer.ability.tag','designer_product_tag_rel',
                                    'info_id', 'product_id', string='Designer Product Tag',
                                     domain="[('tag_type','=','1')]")
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
        value = {"result":-1,
                 "errors":"",
                 "data":None}
        try:
            json_data = json.loads(data)
        except Exception as e:
            value["errors"] ="json is not validate"
            return json.dumps(value)

        result,_,errors = validate(json_data ,schema_designer ,return_info=True)
        if result== False:
            value["errors"] = errors
            return json.dumps(value)

        val = self.get_designer_value_from_json(json_data)
        self.env['designer.info'].create(val)

        value['result'] = 1
        return json.dumps(value)

    @api.model
    def get_designer_value_from_json(self,data):
        val = {
            "uuid":data["uuid"],
            "lang":data["lang"],
            "firstname":data["firstname"],
            "lastname":data["lastname"],
            "budget_unit_u":data["budget_unit_u"],
            "introduction_u":data["introduction_u"],
            "email":data["email"],
            "tel":data["tel"],
            "portrait_u":data["portrait_u"],
            "experience_years":data["experience_years"],
            "have_exclusive_contract":data["have_exclusive_contract"],
            "excluesive_contract_content_u":data.get("excluesive_contract_content_u",""),

            "endorsement":data.get("endorsement",""),
            "specialities_u":data.get("specialities_u",""),
            "memo_u":data.get("memo_u",""),
            "intermediate_agency":data.get("intermediate_agency",""),
            "intermediate_contact":data.get("intermediate_contact",""),
            "available_from":data.get("available_from",None),
            "available_util":data.get("available_util",None),
            "home_page":data.get("home_page",""),
            "linkin_page":data.get("linkin_page",""),
            "postal_address":data.get("postal_address",""),
            "bank_account_info":data.get("bank_account_info",""),
        }
        '''   
        book_u educations creation_pics
        domain skill_tags product_tags project_tags
        '''
        return val


    @api.model
    def get_desiger_info_from_db(self,designer_id):
        _logger.info(f"designer_id:{designer_id}")
        designer = self.env['designer.info'].browse([designer_id])
        _logger.info(f"designer :{designer}")
        _logger.info(f"type(designer):{type(designer)}")
        if isinstance(designer,tuple):
            designer = designer[0]
        _logger.info(f"designer :{designer}")
        val = {
            "firstname":designer.firstname,
            "lastname":designer.lastname,
            "endorsement":designer.endorsement,
            "budget_unit_u":designer.budget_unit_u,
            "specialities_u":designer.specialities_u,
            "memo_u":designer.memo_u,
            "introduction_u":designer.introduction_u,
            "intermediate_agency":designer.intermediate_agency,
            "intermediate_contact":designer.intermediate_contact,
            "email":designer.email,
            "tel":designer.tel,
            "portrait_u":designer.portrait_u,
            "postal_address":designer.postal_address,
            "bank_account_info":designer.bank_account_info,
            "have_exclusive_contract":designer.have_exclusive_contract,
            "excluesive_contract_content_u":designer.excluesive_contract_content_u,
            "available_from":designer.available_from,
            "available_util":designer.available_util,
            "home_page":designer.home_page,
            "linkin_page":designer.linkin_page,
            "experience_years":designer.experience_years,
        }
        '''   
        book_u educations creation_pics
        domain skill_tags product_tags project_tags
        '''
        return designer,val


    @api.model
    def get_designer_info(self,data):
        value = {"result":-1,
                 "errors":"",
                 "data":None}
        try:
            json_data = json.loads(data)
        except Exception as e:
            value["errors"] ="json is not validate"
            return json.dumps(value)

        result,_,errors = validate(json_data ,schema_uuid1 ,return_info=True)
        if result== False:
            value["errors"] = errors
            return json.dumps(value)
        uuid = json_data['uuid']
        designer_id = self.env['designer.info'].search([['uuid',"=",uuid]])
        if len(designer_id ) == 0:
            value['errors'] = "can't find designer_info by uuid"
            return json.dumps(value)
        '''
        try:
            designer_id = self.env['designer.info'].search([['uuid',"=",uuid]])
            if len(designer_id) == 0:
                value['errors'] = "can't find designer_info by uuid"
                return json.dumps(value)
        except Exception as e:
            value['errors'] = 'not valid uuid'
            return json.dumps(value)
            '''
        _,val = self.get_desiger_info_from_db(designer_id)
        value['result'] = 1
        value['data'] = val
        return json.dumps(value)

    @api.model
    def update_designer_info(self,data):
        value = {"result":-1,
                 "errors":"",
                 "data":None}
        try:
            json_data = json.loads(data)
        except Exception as e:
            value["errors"] ="json is not validate"
            return json.dumps(value)

        result,_,errors = validate(json_data ,schema_designer ,return_info=True)
        if result== False:
            value["errors"] = errors
            return json.dumps(value)

        uuid = json_data['uuid']
        try:
            designer_id = self.env['designer.info'].search([['uuid',"=",uuid]])
            if len(designer) == 0:
                value['errors'] = "can't find designer_info by uuid"
                return json.dumps(value)
        except Exception as e:
            value['errors'] = 'not valid uuid'
            return json.dumps(value)
            
        designer,val = self.get_desiger_info_from_db(designer_id)

        try:
            designer.write(val)
        except Exception as e:
            value['errors'] = str(e) 
            return json.dumps(value)
        value['result'] = 1
        return json.dumps(value)
    
class designer_type(models.Model):
    _name = 'designer.type'
    _description = 'designer type'

    name = fields.Char('desiger type', translate=True)


class designer_field(models.Model):
    _name = 'designer.field'
    _description = 'designer field'
    
    name = fields.Char('designer domain', translate=True)

