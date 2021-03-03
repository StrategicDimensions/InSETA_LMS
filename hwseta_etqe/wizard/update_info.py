from openerp import fields, models, api, _
from openerp.osv import osv
from datetime import date
from datetime import datetime as dt

DEBUG = True

if DEBUG:
	import logging

	logger = logging.getLogger(__name__)


	def dbg(msg):
		logger.info(msg)
else:
	def dbg(msg):
		pass


# todo:remove this record rule from live when using 	base.res_partner_portal_public_rule

class update_info(models.TransientModel):
	_name = 'update.info'

	partner_type = fields.Selection([('provider', 'Provider'), ('moderator', 'Moderator'), ('assessor', 'Assessor')])

	def _default_provider(self):
		dbg('_default_provider')
		user = self.env.user
		partner = user.partner_id
		if partner.provider:
			# self.provider_id = partner
			return partner

	@api.one
	def select_partner(self):
		user = self.env.user
		partner = user.partner_id
		if self.partner_type == 'provider':
			li_provider = user.partner_id
			# dummy, update_provider_info_form_view_id = self.pool.get('ir.model.data').get_object_reference('hwseta_etqe','update_provider_info_form')
			# dummy, update_provider_info_form_view_id = self.env.ref('hwseta_etqe.update_provider_info_form')
			update_provider_info_form_view_id = self.env.ref('hwseta_etqe.update_provider_info_form')
			view_ref = self.pool.get('ir.model.data').get_object_reference(self._cr, self._uid, 'hwseta_etqe','update_provider_info_form')
			view_id = view_ref and view_ref[1] or False,
			dbg(view_id)
			return {
				'type': 'ir.actions.act_window',
				'name': _('Sales Order'),
				'res_model': 'update.provider',
				# 'res_id': ids[0],  # If you want to go on perticuler record then you can use res_id

				'view_type': 'form',
				'view_mode': 'form',
				'view_id': view_id,
				'target': 'current',
				'nodestroy': True,
			}


class updated_providers_reject_wiz(models.TransientModel):
	_name = 'updated.providers.reject.wiz'

	comment = fields.Text()
	update_id = fields.Many2one('updated.providers')

	@api.one
	def reject_update(self):
		if self.update_id and self.comment:
			self.update_id.reject_update(self.comment)
			# raise Warning(_('found update_id'))
			ir_model_data_obj = self.env['ir.model.data']
			mail_template_id = ir_model_data_obj.get_object_reference('hwseta_etqe','email_template_prov_update_reject_notification')
			if mail_template_id:
				self.pool['email.template'].send_mail(self.env.cr, self.env.uid, mail_template_id[1], self.id,
													  force_send=True, context=self.env.context)

	# for lrq in self.env['learner.registration.qualification'].search(domain):
	_defaults = {'update_id': lambda self, cr, uid, context: context.get('update_id', False), }

class update_provider(models.TransientModel):
	_name = 'update.provider'

	def generate_msg(self, partner):
		msg = ''
		msg += '<p>Phone: ' + str(partner.phone) + '</p>'
		msg += '<p>Mobile: ' + str(partner.mobile) + '</p>'
		msg += '<p>Fax: ' + str(partner.fax) + '</p>'
		msg += '<p>Website: ' + str(partner.website) + '</p>'
		msg += '<p>---Work Address---</p>'
		msg += '<p>Street: ' + str(partner.street) + '</p>'
		msg += '<p>Street2: ' + str(partner.street2) + '</p>'
		msg += '<p>Street3: ' + str(partner.street3) + '</p>'
		msg += '<p>Suburb: ' + str(partner.suburb.name) + '</p>'
		msg += '<p>Province: ' + str(partner.state_id.name) + '</p>'
		msg += '<p>Zip: ' + str(partner.zip) + '</p>'
		msg += '<p>Country: ' + str(partner.country_id.name) + '</p>'
		msg += '<p>---Physical Address---</p>'
		msg += '<p>physical_address_1: ' + str(partner.physical_address_1) + '</p>'
		msg += '<p>physical_address_2: ' + str(partner.physical_address_2) + '</p>'
		msg += '<p>physical_address_3: ' + str(partner.physical_address_3) + '</p>'
		msg += '<p>provider_physical_suburb: ' + str(partner.provider_physical_suburb.name) + '</p>'
		msg += '<p>city_physical: ' + str(partner.city_physical.name) + '</p>'
		msg += '<p>province_code_physical: ' + str(partner.province_code_physical.name) + '</p>'
		msg += '<p>zip_physical: ' + str(partner.zip_physical) + '</p>'
		msg += '<p>country_code_physical: ' + str(partner.country_code_physical.name) + '</p>'
		msg += '<p>---Postal Address---</p>'
		msg += '<p>postal_address_1: ' + str(partner.postal_address_1) + '</p>'
		msg += '<p>postal_address_2: ' + str(partner.postal_address_2) + '</p>'
		msg += '<p>postal_address_3: ' + str(partner.postal_address_3) + '</p>'
		msg += '<p>provider_postal_suburb: ' + str(partner.provider_postal_suburb.name) + '</p>'
		msg += '<p>city_postal: ' + str(partner.city_postal.name) + '</p>'
		msg += '<p>province_code_postal: ' + str(partner.province_code_postal.name) + '</p>'
		msg += '<p>zip_postal: ' + str(partner.zip_postal) + '</p>'
		msg += '<p>country_code_postal: ' + str(partner.country_code_postal.name) + '</p>'
		msg += '<p>---Physical Address---</p>'
		msg += '<p>txtCompanyRegNo: ' + str(partner.txtCompanyRegNo) + '</p>'
		msg += '<p>txtVATRegNo: ' + str(partner.txtVATRegNo) + '</p>'
		msg += '<p>cboProviderFocus: ' + str(partner.cboProviderFocus.name) + '</p>'
		msg += '<p>txtNumStaffMembers: ' + str(partner.txtNumStaffMembers) + '</p>'
		return msg

	def _default_provider(self):
		dbg('_default_provider')
		user = self.env.user
		partner = user.partner_id
		if partner.provider:
			# self.provider_id = partner
			return partner
		context = self._context
		provider_id = context.get('provider_id', False)
		return provider_id

	page = fields.Selection([
		('terms', 'Terms & Conditions'),
		('contact', 'Contact'),
		# ('provider', 'Provider'),
		('address', 'General Address'),
		('personal_addr', 'Personal Address'),
		('postal_addr', 'Postal Address'),
		('business_info', 'Business Info'),
		('business_docs', 'Business Documents'),
		('admin', 'Internal Administration'),
		('disclaimer', 'Disclaimer'),
	], default='terms')
	provider_id = fields.Many2one('res.partner', default=_default_provider)
	disclaimer = fields.Boolean()
	reference = fields.Char()
	phone = fields.Char()  # todo: test validated
	mobile = fields.Char()  # todo: test validated
	fax = fields.Char()  # todo: test validated
	website = fields.Char()  # no validations found
	# provider section
	# provider_sic_code = fields.Char(string='SIC Code', help="SIC Code", size=50)  # no validations found
	# provider_sars_number = fields.Char(string='SDL No.', help="Provider_Sars_Number", size=50)  # no validations found
	# provider_status_Id = fields.Char(string='Provider Status', help="Provider_Status_Id", size=50)  # this shouldnt be editable,its marked Expired in py based on dates(supposed to in send_re_registration_alert_email
	# work addr section
	street = fields.Char()  # no validations found
	street2 = fields.Char()  # no validations found
	street3 = fields.Char()  # no validations found
	suburb = fields.Many2one('res.suburb')  # todo: test validated
	city = fields.Many2one('res.city')  # todo: test validated
	state_id = fields.Many2one('res.country.state')  # todo: test validated
	zip = fields.Char()  # todo: test validated
	country_id = fields.Many2one('res.country')  # todo: test validated
	# physical addr section
	physical_address_1 = fields.Char(size=50)  # no validations found
	physical_address_2 = fields.Char(size=50)  # no validations found
	physical_address_3 = fields.Char(size=50)  # no validations found
	provider_physical_suburb = fields.Many2one('res.suburb')  # todo: test validated
	city_physical = fields.Many2one('res.city')  # todo: test validated
	province_code_physical = fields.Many2one('res.country.state')  # todo: test validated
	zip_physical = fields.Char()  # todo: test validated
	country_code_physical = fields.Many2one('res.country')  # todo: test validated
	# postal addr section
	postal_address_1 = fields.Char(size=50)  # no validations found
	postal_address_2 = fields.Char(size=50)  # no validations found
	postal_address_3 = fields.Char(size=50)  # no validations found
	provider_postal_suburb = fields.Many2one('res.suburb')  # todo: test validated
	city_postal = fields.Many2one('res.city')  # todo: test validated
	province_code_postal = fields.Many2one('res.country.state')  # todo: test validated
	zip_postal = fields.Char()  # todo: test validated
	country_code_postal = fields.Many2one('res.country')  # todo: test validated
	# business info section
	txtCompanyRegNo = fields.Char(string='Company Registration Number', size=240)  # no validations found
	txtVATRegNo = fields.Char(string='VAT Number', size=240)  # no validations found
	cboProviderFocus = fields.Many2one('hwseta.provider.focus.master', string='Provider Focus')  # no validations found
	txtNumYearsCurrentBusiness = fields.Selection([
		('0', '0'),
		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),
		('6', '6'),
		('7', '7'),
		('8', '8'),
		('9', '9'),
		('10', '10'),
		('10+', '10+'),
	], string='Years in Business', size=240)  # no validations found
	txtNumStaffMembers = fields.Char(string='Number of full time staff members', size=240)  # no validations found
	# attachments in the business info section
	cipro_documents = fields.Many2one('ir.attachment', string='Cipro Documents')
	tax_clearance = fields.Many2one('ir.attachment', string='Tax Clearance')
	director_cv = fields.Many2one('ir.attachment', string='Director C.V')
	certified_copies_of_qualifications = fields.Many2one('ir.attachment', string='Certified copies of Qualifications')
	professional_body_registration = fields.Many2one('ir.attachment', string='Professional Body Registration')
	workplace_agreement = fields.Many2one('ir.attachment', string='Workplace Agreement')
	business_residence_proof = fields.Many2one('ir.attachment', string='Business Visa/Passport/Permanent residence')
	provider_learning_material = fields.Many2one('ir.attachment', string='Learning Programme Approval Report')
	skills_programme_registration_letter = fields.Many2one('ir.attachment',
														   string='Skills Programme Registration Letter')
	company_profile_and_organogram = fields.Many2one('ir.attachment', string='Company Profile  and organogram')
	quality_management_system = fields.Many2one('ir.attachment', string='Quality Management System (QMS)')
	# do something here?provider_master_contact_ids = fields.One2many('provider.master.contact', 'provider_master_contact_id',
	# 											  string='Provider Contact', track_visibility='onchange')
	# do something here?acc_multi_doc_upload_master_ids = fields.One2many('acc.multi.doc.upload', 'acc_id', string='Other Documents',
	# 												  help='Upload Document')
	# do something here?site_visit_image_master_ids = fields.One2many('site.visit.upload', 'acc_id', string='Site Visit Image Upload',
	# 											  help='Image Upload Document')
	lease_agreement_document = fields.Many2one('ir.attachment', string='Lease Document')
	# admin section for nlrd fixes
	type_id_help = 'this field is used in NLRD to classify the type of provider. options are: \n2: Development Enterprise \nNGO"3: Education \n 4: Employer \n 5: Training \n 500: Education and Training'
	provider_type_id = fields.Char(string='Provider Type', help=type_id_help,
								   size=50)  # no validations found, nlrd required
	class_id_help = 'this field is used in NLRD to classify the class of provider. options are: \n1: '
	provider_class_Id = fields.Char(string='Provider Class', help="Provider_Class_Id",
									size=50)  # no vals found, nlrd was blanket to Unknown
	provider_start_date = fields.Date(string='Start Date', track_visibility='onchange',
									  help="Provider_Start_Date")
	provider_end_date = fields.Date(string='End Date', track_visibility='onchange', help="Provider_End_Date")

	@api.multi
	@api.onchange('provider_physical_suburb','suburb','provider_postal_suburb')
	def onchange_suburb(self):
		dbg("onchange_provider_physical_suburb")
		if self.provider_physical_suburb:
			self.zip_physical = self.provider_physical_suburb.postal_code
			self.city_physical = self.provider_physical_suburb.city_id.id
			self.province_code_physical = self.provider_physical_suburb.province_id.id
			self.country_id = self.provider_physical_suburb.country_id.id
		if self.suburb:
			self.zip = self.suburb.postal_code
			self.city = self.suburb.city_id.id
			self.state_id = self.suburb.province_id.id
			self.country_id = self.suburb.country_id.id
		if self.provider_postal_suburb:
			self.zip_postal = self.provider_postal_suburb.postal_code
			self.city_postal = self.provider_postal_suburb.city_id.id
			self.state_id = self.provider_postal_suburb.province_id.id
			self.country_code_postal = self.provider_postal_suburb.country_id.id

	# this was fetched form provider accred but should be applicable here too
	@api.multi
	@api.onchange('phone', 'mobile', 'fax', 'email')
	def onchange_validate_number(self):
		dbg("onchange_validate_number")
		if self.phone:
			if not self.phone.isdigit() or len(self.phone) != 10:
				self.phone = ''
				return {'warning': {'title': 'Invalid input', 'message': 'Please enter 10 digits Phone number'}}
		if self.mobile:
			if not self.mobile.isdigit() or len(self.mobile) != 10:
				self.mobile = ''
				return {'warning': {'title': 'Invalid input', 'message': 'Please enter 10 digits Mobile number'}}
		if self.fax:
			if not self.fax.isdigit() or len(self.fax) != 10:
				self.fax = ''
				return {'warning': {'title': 'Invalid input', 'message': 'Please enter 10 digits Fax number'}}
		# if self.email:
		# 	if '@' not in self.email:
		# 		self.email = ''
		# 		return {'warning': {'email': 'Invalid input', 'message': 'Please enter valid email address'}}
		# 	unicode_email = self.email
		# 	email = unicode_email.encode("utf-8")
		# 	duplicate_match_user = self.env['res.users'].search(
		# 		['|', ('login', '=', email.strip()), ('login', '=', self.email)])
		# 	# todo:test above if/when email is added. the below is too specific but above is fine for checking if we try changing to an existing email
		# 	# duplicate_provider = self.env['provider.accreditation'].search(
		# 	# 	[('final_state', '!=', 'Rejected'), ('email', '=', email.strip())])
		# 	if duplicate_match_user:
		# 		self.email = ''
		# 		return {'warning': {'title': 'Invalid input',
		# 							'message': 'Sorry!! Provider is already registered with this email Id !'}}

	@api.onchange('disclaimer')
	def populate_fields(self):
		if self.provider_id and self.disclaimer:
			prov = self.provider_id
			self.phone = prov.phone
			self.mobile = prov.mobile
			self.fax = prov.fax
			self.website = prov.website
			self.street = prov.street
			self.street2 = prov.street2
			self.street3 = prov.street3
			self.suburb = prov.suburb.id
			self.city = prov.city.id
			self.state_id = prov.state_id.id
			self.zip = prov.zip
			self.country_id = prov.country_id
			self.physical_address_1 = prov.physical_address_1
			self.physical_address_2 = prov.physical_address_2
			self.physical_address_3 = prov.physical_address_3
			self.provider_physical_suburb = prov.provider_physical_suburb.id
			self.city_physical = prov.city_physical.id
			self.province_code_physical = prov.province_code_physical.id
			self.zip_physical = prov.zip_physical
			self.country_code_physical = prov.country_code_physical.id
			self.postal_address_1 = prov.postal_address_1
			self.postal_address_2 = prov.postal_address_2
			self.postal_address_3 = prov.postal_address_3
			self.provider_postal_suburb = prov.provider_postal_suburb.id
			self.city_postal = prov.city_postal.id
			self.province_code_postal = prov.province_code_postal.id
			self.zip_postal = prov.zip_postal
			self.country_code_postal = prov.country_code_postal.id
			self.txtCompanyRegNo = prov.txtCompanyRegNo
			self.txtVATRegNo = prov.txtVATRegNo
			self.cboProviderFocus = prov.cboProviderFocus.id
			self.txtNumYearsCurrentBusiness = prov.txtNumYearsCurrentBusiness
			self.txtNumStaffMembers = prov.txtNumStaffMembers
			self.provider_type_id = prov.provider_type_id
			self.provider_class_Id = prov.provider_class_Id
			self.provider_start_date = prov.provider_start_date
			self.provider_end_date = prov.provider_end_date
			# self.cipro_documents = prov.cipro_documents.id
			# self.tax_clearance = prov.tax_clearance.id
			# self.director_cv = prov.director_cv.id
			# self.certified_copies_of_qualifications = prov.certified_copies_of_qualifications.id
			# self.professional_body_registration = prov.professional_body_registration.id
			# self.workplace_agreement = prov.workplace_agreement.id
			# self.business_residence_proof = prov.business_residence_proof.id
			# self.provider_learning_material = prov.provider_learning_material.id
			# self.skills_programme_registration_letter = prov.skills_programme_registration_letter.id
			# self.company_profile_and_organogram = prov.company_profile_and_organogram.id
			# self.quality_management_system = prov.quality_management_system.id
			# self.lease_agreement_document = prov.lease_agreement_document.id

	@api.one
	def update(self):
		prov = self.provider_id
		vals = {
			# 'msg': msg + '</p>>--changed to--></p>' + msg2,
			'status': 'submitted',
			'provider_id': prov.id,
			'disclaimer': self.disclaimer,
			'reference': self.env['ir.sequence'].get('provider.update.reference'),
			'phone': self.phone,
			'mobile': self.mobile,
			'fax': self.fax,
			'website': self.website,
			'street': self.street,
			'street2': self.street2,
			'street3': self.street3,
			'suburb': self.suburb.id,
			'city': self.city.id,
			'state_id': self.state_id.id,
			'zip': self.zip,
			'country_id': self.country_id.id,
			'physical_address_1': self.physical_address_1,
			'physical_address_2': self.physical_address_2,
			'physical_address_3': self.physical_address_3,
			'provider_physical_suburb': self.provider_physical_suburb.id,
			'city_physical': self.city_physical.id,
			'province_code_physical': self.province_code_physical.id,
			'zip_physical': self.zip_physical,
			'country_code_physical': self.country_code_physical.id,
			'postal_address_1': self.postal_address_1,
			'postal_address_2': self.postal_address_2,
			'postal_address_3': self.postal_address_3,
			'provider_postal_suburb': self.provider_postal_suburb.id,
			'city_postal': self.city_postal.id,
			'province_code_postal': self.province_code_postal.id,
			'zip_postal': self.zip_postal,
			'country_code_postal': self.country_code_postal.id,
			'txtCompanyRegNo': self.txtCompanyRegNo,
			'txtVATRegNo': self.txtVATRegNo,
			'cboProviderFocus': self.cboProviderFocus.id,
			'txtNumYearsCurrentBusiness': self.txtNumYearsCurrentBusiness,
			'txtNumStaffMembers': self.txtNumStaffMembers,
			'provider_type_id': self.provider_type_id,
			'provider_class_Id': self.provider_class_Id,
			'provider_start_date': self.provider_start_date,
			'provider_end_date': self.provider_end_date,

			'related_phone': prov.phone,
			'related_mobile': prov.mobile,
			'related_fax': prov.fax,
			'related_website': prov.website,
			'related_street': prov.street,
			'related_street2': prov.street2,
			'related_street3': prov.street3,
			'related_suburb': prov.suburb.id,
			'related_city': prov.city.id,
			'related_state_id': prov.state_id.id,
			'related_zip': prov.zip,
			'related_country_id': prov.country_id.id,
			'related_physical_address_1': prov.physical_address_1,
			'related_physical_address_2': prov.physical_address_2,
			'related_physical_address_3': prov.physical_address_3,
			'related_provider_physical_suburb': prov.provider_physical_suburb.id,
			'related_city_physical': prov.city_physical.id,
			'related_province_code_physical': prov.province_code_physical.id,
			'related_zip_physical': prov.zip_physical,
			'related_country_code_physical': prov.country_code_physical.id,
			'related_postal_address_1': prov.postal_address_1,
			'related_postal_address_2': prov.postal_address_2,
			'related_postal_address_3': prov.postal_address_3,
			'related_provider_postal_suburb': prov.provider_postal_suburb.id,
			'related_city_postal': prov.city_postal.id,
			'related_province_code_postal': prov.province_code_postal.id,
			'related_zip_postal': prov.zip_postal,
			'related_country_code_postal': prov.country_code_postal.id,
			'related_txtCompanyRegNo': prov.txtCompanyRegNo,
			'related_txtVATRegNo': prov.txtVATRegNo,
			'related_cboProviderFocus': prov.cboProviderFocus.id,
			'related_txtNumYearsCurrentBusiness': prov.txtNumYearsCurrentBusiness,
			'related_txtNumStaffMembers': prov.txtNumStaffMembers,
			'related_provider_type_id': prov.provider_type_id,
			'related_provider_class_Id': prov.provider_class_Id,
			'related_provider_start_date': prov.provider_start_date,
			'related_provider_end_date': prov.provider_end_date,
		}
		# handle the diff if there are document updates and write partner to old doc
		nw = dt.now()
		dbg(nw)
		nw_str = nw.strftime("%d/%m/%Y, %H:%M:%S")
		if self.cipro_documents:
			vals.update({'cipro_documents': self.cipro_documents.id,'related_cipro_documents':prov.cipro_documents.id})
			# check if old doc exists to do work on it
			if prov.cipro_documents:
				prov.cipro_documents.name = 'replaced-' + nw_str + '-' + prov.cipro_documents.name
				prov.cipro_documents.res_id = prov.id
				prov.cipro_documents.res_model = 'res.partner'
		if self.tax_clearance:
			vals.update({'tax_clearance': self.tax_clearance.id,'related_tax_clearance':prov.tax_clearance.id})
			if prov.tax_clearance:
				prov.tax_clearance.name = 'replaced-' + nw_str + '-' + prov.tax_clearance.name
				prov.tax_clearance.res_id = prov.id
				prov.tax_clearance.res_model = 'res.partner'
		if self.director_cv:
			vals.update({'director_cv': self.director_cv.id,'related_director_cv':prov.director_cv.id})
			if prov.director_cv:
				prov.director_cv.name = 'replaced-' + nw_str + '-' + prov.director_cv.name
				prov.director_cv.res_id = prov.id
				prov.director_cv.res_model = 'res.partner'
		if self.certified_copies_of_qualifications:
			vals.update({'certified_copies_of_qualifications': self.certified_copies_of_qualifications.id,'related_certified_copies_of_qualifications':prov.certified_copies_of_qualifications.id})
			if prov.certified_copies_of_qualifications:
				prov.certified_copies_of_qualifications.name = 'replaced-' + nw_str + '-' + prov.certified_copies_of_qualifications.name
				prov.certified_copies_of_qualifications.res_id = prov.id
				prov.certified_copies_of_qualifications.res_model = 'res.partner'
		if self.professional_body_registration:
			vals.update({'professional_body_registration': self.professional_body_registration.id,'related_professional_body_registration':prov.professional_body_registration.id})
			if prov.professional_body_registration:
				prov.professional_body_registration.name = 'replaced-' + nw_str + '-' + prov.professional_body_registration.name
				prov.professional_body_registration.res_id = prov.id
				prov.professional_body_registration.res_model = 'res.partner'
		if self.workplace_agreement:
			vals.update({'workplace_agreement': self.workplace_agreement.id,'related_workplace_agreement':prov.workplace_agreement.id})
			if prov.workplace_agreement:
				prov.workplace_agreement.name = 'replaced-' + nw_str + '-' + prov.workplace_agreement.name
				prov.workplace_agreement.res_id = prov.id
				prov.workplace_agreement.res_model = 'res.partner'
		if self.business_residence_proof:
			vals.update({'business_residence_proof': self.business_residence_proof.id,'related_business_residence_proof':prov.business_residence_proof.id})
			if prov.business_residence_proof:
				prov.business_residence_proof.name = 'replaced-' + nw_str + '-' + prov.business_residence_proof.name
				prov.business_residence_proof.res_id = prov.id
				prov.business_residence_proof.res_model = 'res.partner'
		if self.provider_learning_material:
			vals.update({'provider_learning_material': self.provider_learning_material.id,'related_provider_learning_material':prov.provider_learning_material.id})
			if prov.provider_learning_material:
				prov.provider_learning_material.name = 'replaced-' + nw_str + '-' + prov.provider_learning_material.name
				prov.provider_learning_material.res_id = prov.id
				prov.provider_learning_material.res_model = 'res.partner'
		if self.skills_programme_registration_letter:
			vals.update({'skills_programme_registration_letter': self.skills_programme_registration_letter.id,'related_skills_programme_registration_letter':prov.skills_programme_registration_letter.id})
			if prov.skills_programme_registration_letter:
				prov.skills_programme_registration_letter.name = 'replaced-' + nw_str + '-' + prov.skills_programme_registration_letter.name
				prov.skills_programme_registration_letter.res_id = prov.id
				prov.skills_programme_registration_letter.res_model = 'res.partner'
		if self.company_profile_and_organogram:
			vals.update({'company_profile_and_organogram': self.company_profile_and_organogram.id,'related_company_profile_and_organogram':prov.company_profile_and_organogram.id})
			if prov.company_profile_and_organogram:
				prov.company_profile_and_organogram.name = 'replaced-' + nw_str + '-' + prov.company_profile_and_organogram.name
				prov.company_profile_and_organogram.res_id = prov.id
				prov.company_profile_and_organogram.res_model = 'res.partner'
		if self.quality_management_system:
			vals.update({'quality_management_system': self.quality_management_system.id,'related_quality_management_system':prov.quality_management_system.id})
			if prov.quality_management_system:
				prov.quality_management_system.name = 'replaced-' + nw_str + '-' + prov.quality_management_system.name
				prov.quality_management_system.res_id = prov.id
				prov.quality_management_system.res_model = 'res.partner'
		if self.lease_agreement_document:
			vals.update({'lease_agreement_document': self.lease_agreement_document.id,'related_lease_agreement_document':prov.lease_agreement_document.id})
			if prov.lease_agreement_document:
				prov.lease_agreement_document.name = 'replaced-' + nw_str + '-' + prov.lease_agreement_document.name
				prov.lease_agreement_document.res_id = prov.id
				prov.lease_agreement_document.res_model = 'res.partner'
		if self.disclaimer:
			ud = self.env['updated.providers'].create(vals)
		self.provider_id.chatter(self.env.user, "Information update request has been submitted")
		ir_model_data_obj = self.env['ir.model.data']
		mail_template_id = ir_model_data_obj.get_object_reference('hwseta_etqe',
																  'email_template_prov_update_submit_notification')
		if mail_template_id:
			self.pool['email.template'].send_mail(self.env.cr, self.env.uid, mail_template_id[1], ud.id,
												  force_send=True, context=self.env.context)


class updated_providers(models.Model):
	_name = 'updated.providers'

	"""
	this keeps the memory of what the prov wanted to change, it gets a submitted state on creation by provider
	it will then show up for internal staff to click approve , which will then write the vals
	update the chatter of old and new plus submitter and approver
	"""
	status = fields.Selection([('submitted', 'Submitted'), ('approved', 'Approved'), ('rejected', 'Rejected')])
	msg = fields.Text()
	provider_id = fields.Many2one('res.partner')
	disclaimer = fields.Boolean()
	reference = fields.Char()
	action_date = fields.Date()
	action_partner = fields.Many2one('res.partner')
	# start of actual fields
	phone = fields.Char()
	mobile = fields.Char()
	fax = fields.Char()
	website = fields.Char()

	# provider_sic_code = fields.Char(string='SIC Code', help="SIC Code", size=50)  # no validations found
	# provider_sars_number = fields.Char(string='SDL No.', help="Provider_Sars_Number", size=50)  # no validations found
	# provider_type_id = fields.Char(string='Provider Type', help="Provider_Type_Id",
	# 							   size=50)  # no validations found, nlrd required
	# provider_class_Id = fields.Char(string='Provider Class', help="Provider_Class_Id",
	# 								size=50)  # no vals found, nlrd was blanket to Unknown
	# provider_status_Id = fields.Char(string='Provider Status', help="Provider_Status_Id",
	# 								 size=50)  # this shouldnt be editable,its marked Expired in py based on dates(supposed to in send_re_registration_alert_email

	street = fields.Char()
	street2 = fields.Char()
	street3 = fields.Char()
	suburb = fields.Many2one('res.suburb')
	city = fields.Many2one('res.city')
	state_id = fields.Many2one('res.country.state')
	zip = fields.Char()
	country_id = fields.Many2one('res.country')

	physical_address_1 = fields.Char()
	physical_address_2 = fields.Char()
	physical_address_3 = fields.Char()
	provider_physical_suburb = fields.Many2one('res.suburb')
	city_physical = fields.Many2one('res.city')
	province_code_physical = fields.Many2one('res.country.state')
	zip_physical = fields.Char()
	country_code_physical = fields.Many2one('res.country')

	postal_address_1 = fields.Char()
	postal_address_2 = fields.Char()
	postal_address_3 = fields.Char()
	provider_postal_suburb = fields.Many2one('res.suburb')
	city_postal = fields.Many2one('res.city')
	province_code_postal = fields.Many2one('res.country.state')
	zip_postal = fields.Char()
	country_code_postal = fields.Many2one('res.country')
	# business info section
	txtCompanyRegNo = fields.Char(string='Company Registration Number')
	txtVATRegNo = fields.Char(string='VAT Number')
	cboProviderFocus = fields.Many2one('hwseta.provider.focus.master', string='Provider Focus')
	txtNumYearsCurrentBusiness = fields.Selection([
		('0', '0'),
		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),
		('6', '6'),
		('7', '7'),
		('8', '8'),
		('9', '9'),
		('10', '10'),
		('10+', '10+'),
	], string='Years in Business', size=240)
	txtNumStaffMembers = fields.Char(string='Number of full time staff members')

	# attachments in the business info section
	cipro_documents = fields.Many2one('ir.attachment', string='Cipro Documents')
	tax_clearance = fields.Many2one('ir.attachment', string='Tax Clearance')
	director_cv = fields.Many2one('ir.attachment', string='Director C.V')
	certified_copies_of_qualifications = fields.Many2one('ir.attachment', string='Certified copies of Qualifications')
	professional_body_registration = fields.Many2one('ir.attachment', string='Professional Body Registration')
	workplace_agreement = fields.Many2one('ir.attachment', string='Workplace Agreement')
	business_residence_proof = fields.Many2one('ir.attachment', string='Business Visa/Passport/Permanent residence')
	provider_learning_material = fields.Many2one('ir.attachment', string='Learning Programme Approval Report')
	skills_programme_registration_letter = fields.Many2one('ir.attachment',
														   string='Skills Programme Registration Letter')
	company_profile_and_organogram = fields.Many2one('ir.attachment', string='Company Profile  and organogram')
	quality_management_system = fields.Many2one('ir.attachment', string='Quality Management System (QMS)')
	# do something here?provider_master_contact_ids = fields.One2many('provider.master.contact', 'provider_master_contact_id',
	# 											  string='Provider Contact', track_visibility='onchange')
	# do something here?acc_multi_doc_upload_master_ids = fields.One2many('acc.multi.doc.upload', 'acc_id', string='Other Documents',
	# 												  help='Upload Document')
	# do something here?site_visit_image_master_ids = fields.One2many('site.visit.upload', 'acc_id', string='Site Visit Image Upload',
	# 											  help='Image Upload Document')
	lease_agreement_document = fields.Many2one('ir.attachment', string='Lease Document')
	# admin section
	type_id_help = 'this field is used in NLRD to classify the type of provider. options are: \n2: Development Enterprise \nNGO"3: Education \n 4: Employer \n 5: Training \n 500: Education and Training'
	provider_type_id = fields.Char(string='Provider Type', help=type_id_help,
								   size=50)  # no validations found, nlrd required
	provider_class_Id = fields.Char(string='Provider Class', help="Provider_Class_Id",
									size=50)  # no vals found, nlrd was blanket to Unknown
	provider_start_date = fields.Date(string='Start Date', track_visibility='onchange',
									  help="Provider_Start_Date")
	provider_end_date = fields.Date(string='End Date', track_visibility='onchange', help="Provider_End_Date")
	# start of related fields for display only
	related_phone = fields.Char()
	related_mobile = fields.Char()
	related_fax = fields.Char()
	related_website = fields.Char()

	related_street = fields.Char()
	related_street2 = fields.Char()
	related_street3 = fields.Char()
	related_suburb = fields.Many2one('res.suburb')
	related_city = fields.Many2one('res.city')
	related_state_id = fields.Many2one('res.country.state')
	related_zip = fields.Char()
	related_country_id = fields.Many2one('res.country')

	related_physical_address_1 = fields.Char()
	related_physical_address_2 = fields.Char()
	related_physical_address_3 = fields.Char()
	related_provider_physical_suburb = fields.Many2one('res.suburb')
	related_city_physical = fields.Many2one('res.city')
	related_province_code_physical = fields.Many2one('res.country.state')
	related_zip_physical = fields.Char()
	related_country_code_physical = fields.Many2one('res.country')

	related_postal_address_1 = fields.Char()
	related_postal_address_2 = fields.Char()
	related_postal_address_3 = fields.Char()
	related_provider_postal_suburb = fields.Many2one('res.suburb')
	related_city_postal = fields.Many2one('res.city')
	related_province_code_postal = fields.Many2one('res.country.state')
	related_zip_postal = fields.Char()
	related_country_code_postal = fields.Many2one('res.country')

	# related_business info section
	related_txtCompanyRegNo = fields.Char(string='Company Registration Number')
	related_txtVATRegNo = fields.Char(string='VAT Number')

	related_cboProviderFocus = fields.Many2one('hwseta.provider.focus.master', string='Provider Focus')
	related_txtNumYearsCurrentBusiness = fields.Selection([
		('0', '0'),
		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),
		('6', '6'),
		('7', '7'),
		('8', '8'),
		('9', '9'),
		('10', '10'),
		('10+', '10+'),
	], string='Years in Business', size=240)
	related_txtNumStaffMembers = fields.Char(string='Number of full time staff members')

	# attachments in the business info section
	related_cipro_documents = fields.Many2one('ir.attachment', string='Cipro Documents')
	related_tax_clearance = fields.Many2one('ir.attachment', string='Tax Clearance')
	related_director_cv = fields.Many2one('ir.attachment', string='Director C.V')
	related_certified_copies_of_qualifications = fields.Many2one('ir.attachment', string='Certified copies of Qualifications')
	related_professional_body_registration = fields.Many2one('ir.attachment', string='Professional Body Registration')
	related_workplace_agreement = fields.Many2one('ir.attachment', string='Workplace Agreement')
	related_business_residence_proof = fields.Many2one('ir.attachment', string='Business Visa/Passport/Permanent residence')
	related_provider_learning_material = fields.Many2one('ir.attachment', string='Learning Programme Approval Report')
	related_skills_programme_registration_letter = fields.Many2one('ir.attachment',string='Skills Programme Registration Letter')
	related_company_profile_and_organogram = fields.Many2one('ir.attachment', string='Company Profile  and organogram')
	related_quality_management_system = fields.Many2one('ir.attachment', string='Quality Management System (QMS)')
	related_lease_agreement_document = fields.Many2one('ir.attachment', string='Lease Document')
	type_id_help = 'this field is used in NLRD to classify the type of provider. options are: \n2: Development Enterprise \nNGO"3: Education \n 4: Employer \n 5: Training \n 500: Education and Training'
	related_provider_type_id = fields.Char(string='Provider Type', help=type_id_help,
								   size=50)  # no validations found, nlrd required
	related_provider_class_Id = fields.Char(string='Provider Class', help="Provider_Class_Id",
									size=50)  # no vals found, nlrd was blanket to Unknown
	related_provider_start_date = fields.Date(string='Start Date', track_visibility='onchange',
									  help="Provider_Start_Date")
	related_provider_end_date = fields.Date(string='End Date', track_visibility='onchange', help="Provider_End_Date")

	@api.one
	def approve_update(self):
		vals = self.read()
		dbg(vals)
		doc_list = [
			'cipro_documents',
			'tax_clearance',
			'director_cv',
			'certified_copies_of_qualifications',
			'professional_body_registration',
			'workplace_agreement',
			'business_residence_proof',
			'provider_learning_material',
			'skills_programme_registration_letter',
			'company_profile_and_organogram',
			'quality_management_system',
			'lease_agreement_document',
		]
		# handle tuples, replace the tuple with its own id
		for val in vals[0].keys():
			dbg(vals[0].get(val))
			dbg(type(vals[0].get(val)))
			if type(vals[0].get(val)) == tuple:
				vals[0].update({val:vals[0].get(val)[0]})
		for doc in doc_list:
			if not vals[0].get(doc):
				del vals[0][doc]
		self.status = 'approved'
		self.action_date = date.today()
		self.action_partner = self.env.user.partner_id
		self.provider_id.write(vals)
		# self.provider_id.chatter(self.env.user, "Information update request has been approved")
		ir_model_data_obj = self.env['ir.model.data']
		mail_template_id = ir_model_data_obj.get_object_reference('hwseta_etqe',
																  'email_template_prov_update_approve_notification')
		if mail_template_id:
			self.pool['email.template'].send_mail(self.env.cr, self.env.uid, mail_template_id[1], self.id,
												  force_send=True, context=self.env.context)
		# self.provider_id.chatter(self.env.user, self.msg)

	@api.one
	def reject_update(self,msg):
		self.status = 'rejected'
		self.action_date = date.today()
		self.action_partner = self.env.user.partner_id
		self.provider_id.chatter(
			self.env.user,
			self.reference + '-Update has been rejected with the following comments: \n' + msg
								)

class res_partner(models.Model):
	_inherit = 'res.partner'

	update_ids = fields.One2many('updated.providers', 'provider_id')
