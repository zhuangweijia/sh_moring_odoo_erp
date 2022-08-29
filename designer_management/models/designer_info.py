# -*- coding: utf-8 -*-

import json
import base64
import logging
from validator import validate
from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import AccessError
from odoo.modules.module import get_module_resource
#from jsonschema import validate, ValidationError

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
    _description = 'designer info'
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
    intermediate_contact = fields.Char(string='intermediate_contact')
    intermediate_agency = fields.Char(string='intermediate_agency')
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
    endorsement = fields.Char(string='endorsement')
    budget_unit_u = fields.Integer(string='budget_unit_u')
    specialities_u = fields.Char(string='specialities_u')
    memo_u = fields.Char(string='memo_u')
    introduction_u = fields.Char(string='introduction_u')
    tel = fields.Char(string='tel')
    portrait_u = fields.Char(string='portrait_u')
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
    type_id = fields.Many2one('designer.type', string='talent type', required=True)
    domain_ids = fields.Many2many('designer.domain', 'designer_info_domain_rel',
                                 'info_id','domain_id',
                                 string='domain') 
    book_ids = fields.One2many('designer.material.item','designer_id',string='book list')
    creation_pics_ids = fields.One2many('designer.material.item','designer_id',string='book list')
    educations_ids = fields.One2many('designer.material.item','designer_id',string='book list')
    
    # other
    is_exclusive_signed = fields.Boolean(default=True)
    project = fields.Html('project')
    confirmed_date = fields.Datetime()
    status = fields.Selection([('draft','draft'),
                               ('confirm', 'confirm'),
                               ('cancel', 'cancel')], default='draft')
    project_line = fields.One2many('designer.project', 'designer_info_id', string='Projects')
    intro_video = fields.Char(string='intro video')
    last_update_by_u = fields.Datetime(required=True)
    instagram_page = fields.Char()
    linkedin_page = fields.Char()
    behance_page = fields.Char()
    other_page = fields.Char()
    intermediate_contact_tel = fields.Char()
    intermediate_contact_email = fields.Char()


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
    def get_configuration_options(self):
        value = {"result":1,
                 "errors":"",
                 "data":None}
        val = {}
        '''  
        doms = self.env['designer.domain'].search([('')])
        val['domain'] = [d.name for d in doms]
        '''
        tags = self.env['designer.ability.tag'].search(['&',
                                                 ('tag_type',"=",'0'),
                                                 ('status','=','confirm')])
        val['skill_tags'] = [t.name for t in tags]
        pro = self.env['designer.ability.tag'].search(['&',
                                                 ('tag_type',"=",'1'),
                                                 ('status','=','confirm')])
        val['product_tags'] = [t.name for t in pro]
        proj = self.env['designer.ability.tag'].search(['&',
                                                 ('tag_type',"=",'2'),
                                                 ('status','=','confirm')])
        val['project_tags'] = [t.name for t in proj]
        
        value['data'] = val
        return json.dumps(value)


    @api.model
    def validate_step2(self,data):
        errors = []
        schema = {
                "firstname": 30, "lastname": 30,
                "introduction_u":2000, "tel":20, "portrait_u":50,

                  "home_page":50, "linkin_page":50, "intermediate_agency":50,
                  "intermediate_contact":50, "specialities":2000, "memo_u":2000,
                  "postal_address":200, "bank_account_info":200,

                  "intro_video":50, "instagram_page":50, "linkedin_page":50,
                  "behance_page":50, "other_page":50,
                  "intermediate_contact_tel":50,"intermediate_contact_email":50,}
        for k,v in schema.items():
            val = data.get(k,None)
            if val != None and val != "":
                if not isinstance(val,str):
                    errors.append(f'[{k}]: "must be str" ')
                elif len(val)>v:
                    errors.append(f'[{k}]: "max length is {v}" ')
        available_from = data.get("available_from",None)
        try:
            if available_from != None:
                t = datetime.strptime(available_from,"%Y-%m-%d")
        except Exception as e:
            errors.append(f'[{available_from}]: shoud be format of "%Y-%m-%d"')

        available_until = data.get("available_until",None)
        try:
            if available_until != None:
                t = datetime.strptime(available_until,"%Y-%m-%d")
                if datetime.strptime() < datetime.now():
                    errors.append(f'[{available_until}]: shoud be a date in the future')
        except Exception as e:
            errors.append(f'[{available_until}]: shoud be format of "%Y-%m-%d"')

        return errors
        

    @api.model
    def handle_input_list(self,designer,origin_data,input_data):
        all_skill_tag_id = []
        new_tag = list( set(input_data.get('skill_tags',[])).difference(set(origin_data.get('skill_tags',[])))  )
        for l in new_tag:
            ski = self.env['designer.ability.tag'].search([('tag_type','=','0'), ("name",'=',l),])
            if len(ski) <= 0:
                k = self.env['designer.ability.tag'].create({'name':l,'tag_type':'0','status':"draft"})
                all_skill_tag_id.append(k.id)
            else:
                project_tag_id_list.append(ski[0].id)
        exist_tag = list( set(input_data.get('skill_tags',[])).intersection(set(origin_data.get('skill_tags',[])))  )
        ski = self.env['designer.ability.tag'].search([('tag_type','=','0'), ("name",'in',exist_tag),])
        if len(ski) > 0:
            all_skill_tag_id.extend([i.id for i in ski])
        if len(all_skill_tag_id) > 0:
            designer.skill_tag_ids = [6,0,all_skill_tag_id]


        product_tag_id_list = []
        new_pro_tag = list( set(input_data.get('product_tags',[])).difference(set(origin_data.get('product_tag_ids',[])))  )
        for l in new_pro_tag:
            ski = self.env['designer.ability.tag'].search([('tag_type','=','1'), ("name",'=',l),])
            if len(ski) <= 0:
                k = self.env['designer.ability.tag'].create({'name':l,'tag_type':'1','status':"draft"})
                product_tag_id_list.append(k.id)
            else:
                product_tag_id_list.append(ski[0].id)
        exist_tag = list( set(input_data.get('product_tags',[])).intersection(set(origin_data.get('product_tag_ids',[])))  )
        ski = self.env['designer.ability.tag'].search([('tag_type','=','1'), ("name",'in',exist_tag),])
        if len(ski) > 0:
            product_tag_id_list.extend([i.id for i in ski])
        if len(product_tag_id_list) > 0:
            designer.product_tag_ids = [6,0,product_tag_id_list]


        project_tag_id = []
        new_project_tag = list( set(input_data.get('project_tags',[])).difference(set(origin_data.get('project_tag_ids',[])))  )
        for l in new_project_tag:
            ski = self.env['designer.ability.tag'].search([('tag_type','=','2'), ("name",'=',l),])
            if len(ski) <= 0:
                k = self.env['designer.ability.tag'].create({'name':l,'tag_type':'2','status':"draft"})
                project_tag_id.append(k.id)
            else:
                project_tag_id_list.append(ski[0].id)
        exist_tag = list( set(input_data.get('project_tags',[])).intersection(set(origin_data.get('project_tag_ids',[])))  )
        ski = self.env['designer.ability.tag'].search([('tag_type','=','1'), ("name",'in',exist_tag),])
        if len(ski) > 0:
            project_tag_id.extend([i.id for i in ski])
        if len(project_tag_id) > 0:
            designer.project_tag_ids = [6,0,project_tag_id]


        domain_id = []
        new_domain = list( set(input_data.get('domain',[])).difference(set(origin_data.get('domain',[])))  )
        for l in new_domain:
            ski = self.env['designer.domain'].search([("name",'=',l),])
            if len(ski) <= 0:
                k = self.env['designer.domain'].create({'name':l})
                domain_id.append(k.id)
            else:
                domain_id.append(ski[0].id)
        exist_dom = list( set(input_data.get('domain',[])).intersection(set(origin_data.get('domain',[])))  )
        ski = self.env['designer.domain'].search([('tag_type','=','1'), ("name",'in',exist_dom),])
        if len(ski) > 0:
            domain_id.extend([i.id for i in ski])
        if len(domain_id) > 0:
            designer.project_tag_ids = [6,0,domain_id]
        


        new_book = list( set(input_data.get('book_u',[])).difference(set(origin_data.get('book_u',[])))  )
        for b in new_book:
            designer_id.book_ids = [(0,0,{'url':b,'material_type':'0'})]
        book_to_del = list( set(origin_data.get('book_u',[])).difference(set(input_data.get('book_u',[]))  ))
        if len(book_to_del) > 0:
            mlist = self.env['designer.material.item'].search(['&', 
                                                              ("url",'in',book_to_del),
                                                              ("designer_id",'=',designer_id.id),
                                                             ])
            for m in mlist:
                desiger_id.book_ids = [2,m.id]


        pics = list( set(input_data.get('creation_pics',[])).difference(set(origin_data.get('creation_pics',[])))  )
        for b in pics:
            designer_id.book_ids = [(0,0,{'url':b,'material_type':'1'})]
        pics_to_del = list( set(origin_data.get('creation_pics',[])).difference(set(input_data.get('creation_pics',[]))))
        if len(pics_to_del) > 0:
            mlist = self.env['designer.material.item'].search(['&', 
                                                              ("url",'in',pics_to_del),
                                                              ("designer_id",'=',designer_id.id),
                                                             ])
            for m in mlist:
                desiger_id.creation_pics_ids = [2,m.id]


        edus = list( set(input_data.get('educations',[])).difference(set(origin_data.get('educations',[])))  )
        for b in edus:
            designer_id.book_ids = [(0,0,{'name':b,'material_type':'2'})]
        edus_to_del = list( set(origin_data.get('educations',[])).difference(set(input_data.get('educations',[]))  ))
        if len(edus_to_del ) > 0:
            mlist = self.env['designer.material.item'].search(['&', 
                                                              ("name",'in',edus_to_del),
                                                              ("designer_id",'=',designer_id.id),
                                                             ])
            for m in mlist:
                desiger_id.educations_ids = [2,m.id]
        return []


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

        errors = self.validate_step2(json_data)
        if len(errors) > 0:
            value["errors"] = errors
            return json.dumps(value)

        uuid = json_data['uuid']
        designer_id = self.env['designer.info'].search([['uuid',"=",uuid]])
        if len(designer_id ) > 0:
            value['errors'] = "uuid is exist"
            return json.dumps(value)
        val = self.get_designer_value_from_json(json_data)
        self.env['designer.info'].create(val)

        input_list_data = self.get_designer_list_from_json(json_data)
        self.handle_input_list(designer_id,{},input_list_data)

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

            "intro_video":data.get("linkin_page",""),
            "instagram_page":data.get('instagram_page',''),
            "linkedin_page":data.get('linkedin_page',''),
            "behance_page":data.get('behance_page',''),
            "other_page":data.get('other_page',''),
            "intermediate_contact_tel":data.get('intermediate_contact_tel',''),
            "intermediate_contact_email":data.get('intermediate_contact_email',''),
        }
        return val

    @api.model
    def get_designer_list_from_json(self,data):
        val = {}
        val['book_u'] = data.get("book_u",[])
        val['educations'] = data.get("educations",[])
        val['creation_pics'] = data.get("creation_pics",[])
        val['domain'] = data.get("domain",[])
        val['skill_tags'] = data.get("skill_tags",[])
        val['product_tags'] = data.get("product_tags",[])
        val['project_tags'] = data.get("project_tags",[])
        return val

    @api.model
    def get_desiger_info_from_db(self,designer):
        #designer = self.env['designer.info'].browse(designer_id)
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
            
            "intermediate_agenc":designer.intermediate_agenc,
            "other_page":designer.other_page,
            "intermediate_contact_tel":designer.intermediate_contact_tel,
            "intermediate_contact_email":designer.intermediate_contact_email,
        }
        val['book_u'] = [b.url for b in designer.book_ids]
        val['educations'] = [b.name for b in designer.educations_ids]
        val['creation_pics'] = [b.url for b in designer.creation_pics_ids]
        val['domain'] = [b.name for b in designer.domain_ids]
        val['skill_tags'] = [b.name for b in designer.skill_tags]
        val['product_tags'] = [b.name for b in designer.product_tags]
        val['project_tags'] = [b.name for b in designer.project_tags]
        return val

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
        val = self.get_desiger_info_from_db(designer_id[0])
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

        errors = self.validate_step2(json_data)
        if len(errors) > 0:
            value["errors"] = errors
            return json.dumps(value)

        uuid = json_data['uuid']
        designer_id = self.env['designer.info'].search([['uuid',"=",uuid]])
        if len(designer) == 0:
            value['errors'] = "can't find designer_info by uuid"
            return json.dumps(value)

        val = self.get_designer_value_from_json(json_data)
        try:
            designer.write(val)
        except Exception as e:
            value['errors'] = str(e) 
            return json.dumps(value)

        origin_data = self.get_desiger_info_from_db(designer_id)
        input_list_val = self.get_designer_list_from_json(json_data)
        self.handle_input_list(designer_id,origin_data,input_list_val)

        value['result'] = 1
        return json.dumps(value)
    

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
