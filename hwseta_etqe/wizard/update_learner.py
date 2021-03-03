from openerp import fields, models, api, _
from openerp.osv import osv
import datetime
from datetime import date
from datetime import datetime as dt
import calendar
from .. import checkers

DEBUG = True

if DEBUG:
	import logging

	logger = logging.getLogger(__name__)


	def dbg(msg):
		logger.info(msg)
else:
	def dbg(msg):
		pass

class updated_learner_reject_wiz(models.TransientModel):
	_name = 'updated.learner.reject.wiz'

	comment = fields.Text()
	update_id = fields.Many2one('updated.learner')

	@api.one
	def reject_update(self):
		if self.update_id and self.comment:
			self.update_id.reject_update(self.comment)
			# raise Warning(_('found update_id'))
			ir_model_data_obj = self.env['ir.model.data']
			mail_template_id = ir_model_data_obj.get_object_reference('hwseta_etqe',
																	  'email_template_learner_update_reject_notification')
			if mail_template_id:
				self.pool['email.template'].send_mail(self.env.cr, self.env.uid, mail_template_id[1], self.id,
													  force_send=True, context=self.env.context)

	# for lrq in self.env['learner.registration.qualification'].search(domain):
	_defaults = {'update_id': lambda self, cr, uid, context: context.get('update_id', False), }

class update_learner(models.TransientModel):
	_name = 'update.learner'


	def _default_assessor(self):
		dbg('_default_assessor')
		user = self.env.user
		assessor = user.assessor_moderator_id
		if assessor.is_assessors:
			# self.provider_id = partner
			return assessor

	page = fields.Selection([
		('terms', 'Terms & Conditions'),
		('contact', 'Contact'),
		('status', 'Status'),
		('citizenship', 'Citizenship'),
		('address', 'General Address'),
		('personal_addr', 'Personal Address'),
		('postal_addr', 'Postal Address'),
		# ('business_info', 'Business Info'),
		('business_docs', 'Business Documents'),
		('disclaimer', 'Disclaimer'),
	], default='terms')
	learner_id = fields.Many2one('hr.employee', default=_default_assessor)
	disclaimer = fields.Boolean()
	reference = fields.Char()
	# uncomment below when we have function to update the user as well
	# work_email = fields.Char()
	# cit section
	citizen_resident_status_code = fields.Selection(
		[('sa', 'SA - South Africa'), ('dual', 'D - Dual (SA plus other)'), ('other', 'O - Other'),
		 ('PR', 'PR - Permanent Resident'), ('unknown', 'U - Unknown')], string='Citizen Status')
	citizen_status_saqa_code = fields.Selection([('sa', 'SA'), ('d', 'D'), ('o', 'O'), ('pr', 'PR'), ('u', 'U')],
												string='Citizen Status SAQA Code')
	country_id = fields.Many2one('res.country', string='Country of Nationality')
	unknown_type = fields.Selection([
		('political_asylum', 'Political Asylum'),
		('refugee', 'Refugee'),], string='Type')
	unknown_type_document = fields.Many2one('ir.attachment', string="Type Document")
	nationality_saqa_code = fields.Selection([('sa', 'SA')], string='Nationality SAQA Code')
	learner_identification_id = fields.Char("R.S.A.Identification No.", size=13)
	alternate_id_type = fields.Selection(
		[('saqa_member', '521 - SAQA Member ID'), ('passport_number', '527 - Passport Number'),
		 ('drivers_license', '529 - Drivers License'), ('temporary_id_number', '531 - Temporary ID number'),
		 ('none', '533 - None'), ('unknown', '535 - Unknown'), ('student_number', '537 - Student number'),
		 ('work_permit_number', '538 - Work Permit Number'), ('employee_number', '539 - Employee Number'),
		 ('birth_certificate_number', '540 - Birth Certificate Number'),
		 ('hsrc_register_number', ' 541 - HSRC Register Number'), ('etqe_record_number', '561 - ETQA Record Number'),
		 ('refugee_number', '565 - Refugee Number')], string='Alternate ID Type')
	person_birth_date = fields.Date(string='Birth Date')
	gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')
	passport_id = fields.Char('Passport No')
	national_id = fields.Char(string='National Id', size=20)
	home_language_code = fields.Many2one('res.lang', string='Home Language Code', size=6)
	home_lang_saqa_code = fields.Selection(
		[('eng', 'Eng'), ('afr', 'Afr'), ('xho', 'Xho'), ('set', 'Set'), ('zul', 'Zul'), ('sep', 'Sep'), ('tsh', 'Tsh'),
		 ('ses', 'Ses'), ('xit', 'Xit'), ('swa', 'Swa'), ('nde', 'Nde'), ('u', 'U'), ('oth', 'Oth')],
		string='Home Lanaguage SAQA Code')
	disability_status_saqa = fields.Selection(
		[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('9', '9'), ('n', 'N')],
		string='Disability SAQA Code')
	# rating section
	seeing_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Seeing Rating Id',
		track_visibility='onchange')
	hearing_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Hearing Rating Id',
		track_visibility='onchange')
	walking_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Walking Rating Id',
		track_visibility='onchange')
	remembering_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Remembering Rating Id',
		track_visibility='onchange')
	communicating_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Communicating Rating Id',
		track_visibility='onchange')
	self_care_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Self Care Rating Id',
		track_visibility='onchange')
	# contact info section
	person_title = fields.Selection(
		[('adv', 'Adv.'), ('dr', 'Dr'), ('mr', 'Mr'), ('mrs', 'Mrs'), ('ms', 'Ms'), ('prof', 'Prof')], string='Title',
		track_visibility='onchange')
	person_last_name = fields.Char(string='Last Name', size=45)
	person_name = fields.Char(string='First Name', size=50)
	initials = fields.Char(string='Initials')
	cont_number_home = fields.Char(string='Home Number', size=10)
	cont_number_office = fields.Char(string='Office Number', size=10)
	work_phone = fields.Char()
	person_fax_number = fields.Char(string='Tele Fax Number ', size=10)

	current_occupation = fields.Char(string='Current Occupation')
	years_in_occupation = fields.Char(string='Years in Occupation')
	person_cell_phone_number = fields.Char()
	department = fields.Char()
	manager = fields.Char()
	job_title = fields.Char()
	# status section
	marital = fields.Selection(
		[('single', 'Single'), ('married', 'Married'), ('widower', 'Widower'),('widow', 'Widow'), ('divorced', 'Divorced')],
		'Marital Status')
	dissability = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Dissability")
	disability_status = fields.Selection([
		('sight', 'Sight ( even with glasses )'),
		('hearing', 'Hearing ( even with h.aid )'),
		('communication', 'Communication ( talk/listen)'),
		('physical', 'Physical ( move/stand, etc)'),
		('intellectual', 'Intellectual ( learn,etc)'),
		('emotional', 'Emotional ( behav/psych)'),
		('multiple', 'Multiple'),
		('disabled', 'Disabled but unspecified'),
		('none', 'None')], string='Disability Status')
	socio_economic_status = fields.Selection([('employed', 'Employed'), ('unemployed', 'Unemployed, seeking work'),
											  ('Not working, not looking', 'Not working, not looking'),
											  ('Home-maker (not working)', 'Home-maker (not working)'),
											  ('Scholar/student (not w.)', 'Scholar/student (not w.)'),
											  ('Pensioner/retired (not w.)', 'Pensioner/retired (not w.)'),
											  ('Not working - disabled', 'Not working - disabled'),
											  ('Not working - no wish to w', 'Not working - no wish to w'),
											  ('Not working - N.E.C.', 'Not working - N.E.C.'),
											  ('N/A: aged <15', 'N/A: aged <15'),
											  ('N/A: Institution', 'N/A: Institution'),
											  ('Unspecified', 'Unspecified'), ], string='Socio Economic Status')
	equity = fields.Selection([('black_african', 'Black: African'), ('black_indian', 'Black: Indian / Asian'),
							   ('black_coloured', 'Black: Coloured'), ('other', 'Other'), ('unknown', 'Unknown'),
							   ('white', 'White')], string='Equity')
	# learner data section
	highest_education = fields.Char(string='Highest Education')
	# address section
	work_address = fields.Char()
	work_address2 = fields.Char()
	work_address3 = fields.Char()
	person_suburb = fields.Many2one('res.suburb')
	work_city = fields.Many2one('res.city')
	work_province = fields.Many2one('res.country.state')
	work_zip = fields.Char()
	work_country = fields.Many2one('res.country')
	work_municipality = fields.Many2one('res.municipality')
	# home addr
	person_home_address_1 = fields.Char(string='Home Address 1', size=50)
	person_home_address_2 = fields.Char(string='Home Address 2', size=50)
	person_home_address_3 = fields.Char(string='Home Address 3', size=50)
	person_home_suburb = fields.Many2one('res.suburb', string='Home Suburb')
	person_home_city = fields.Many2one('res.city', string='Home City')
	physical_municipality = fields.Many2one('res.municipality', string='Physical Municipality')
	person_home_province_code = fields.Many2one('res.country.state', string='Home Province Code')
	country_home = fields.Many2one('res.country', string='Home Country')
	person_home_zip = fields.Char(string='Home Zip')
	# person_home_addr_post_code = fields.Char(string='Home Addr Post Code', size=4)
	same_as_home = fields.Boolean(string='Same As Home Address')
	person_postal_address_1 = fields.Char(string='Postal Address 1', size=50)
	person_postal_address_2 = fields.Char(string='Postal Address 2', size=50)
	person_postal_address_3 = fields.Char(string='Postal Address 3', size=50)
	person_postal_suburb = fields.Many2one('res.suburb', string='Postal Suburb')
	person_postal_city = fields.Many2one('res.city', string='Postal City')
	postal_municipality = fields.Many2one('res.municipality', string='Postal Municipality')
	person_postal_province_code = fields.Many2one('res.country.state', string='Postal Province Code')
	person_postal_zip = fields.Char(string='Postal Zip')
	country_postal = fields.Many2one('res.country', string='Postal Country')
	# documents section
	id_document = fields.Many2one('ir.attachment', string='ID Document', help='Upload Document')
	learner_master_other_docs_ids = fields.Many2many('acc.multi.doc.upload', string='Document', help='Upload Document')

	@api.multi
	@api.onchange('same_as_home')
	def onchange_sameas_home(self):
		if self.same_as_home:
			self.person_postal_address_1 = self.person_home_address_1
			self.person_postal_address_2 = self.person_home_address_2
			self.person_postal_address_3 = self.person_home_address_3
			self.person_postal_suburb =  self.person_home_suburb
			self.person_postal_city =  self.person_home_city
			self.person_postal_province_code =  self.person_home_province_code.id
			self.person_postal_zip = self.person_home_zip
			self.country_postal =  self.country_home.id

	@api.multi
	@api.onchange('learner_identification_id')
	def onchange_id_number(self):
		if self.learner_identification_id:
			identification_id = self.learner_identification_id
			check = checkers.said_check(identification_id)
			year = check['year']
			month = check['month']
			day = check['day']
			if not check['valid']:
				# raise Warning('not valid' + str(check))
				if "Invalid gender" in checkers.old_said_check(identification_id):
					self.learner_identification_id = ''
					return {
						'value': {'learner_identification_id': ''},
						'warning': {'title': 'Invalid Identification Number',
									'message': 'Invalid Gender!'}}
				if "Invalid citizenship status" in checkers.old_said_check(identification_id):
					self.learner_identification_id = ''
					return {
						'value': {'learner_identification_id': ''},
						'warning': {'title': 'Invalid Identification Number',
									'message': 'Invalid citizenship status!'}}
				# if "Invalid birth date" in checkers.old_said_check(identification_id):
				if int(day) > 31 or int(day) < 1:
					self.learner_identification_id = ''
					return {
						'value': {'learner_identification_id': ''},
						'warning': {'title': 'Invalid Identification Number',
									'message': 'Incorrect Day In Identification Number!'}}
				if int(month) > 12 or int(month) < 1:
					self.learner_identification_id = ''
					return {
						'value': {'learner_identification_id': ''},
						'warning': {'title': 'Invalid Identification Number',
									'message': 'Incorrect Month In Identification Number!'}}
				else:
					# # Calculating last day of month.
					x_year = int(year)
					if x_year == 00:
						x_year = 2000
					last_day = calendar.monthrange(int(x_year), int(month))[1]
					if int(day) > last_day:
						self.learner_identification_id = ''
						return {
							'value': {'learner_identification_id': ''},
							'warning': {'title': 'Invalid Identification Number',
										'message': 'Incorrect last day of month in identification number!'}}
				# if you get here and nothin has been returned yet, it means the checksum must be the issue so raise it
				self.learner_identification_id = ''
				return {'value': {'learner_identification_id': ''},
						'warning': {'title': 'Invalid Identification Number',
									'message': 'Incorrect checksum!'}}
			gender_digit = str(identification_id)[6:10]
			citizenship = str(identification_id)[10:11]

			if gender_digit:
				if int(gender_digit) <= 4999:
					# val.update({'gender': 'female'})
					self.gender = 'female'
				elif int(gender_digit) >= 5000:
					# val.update({'gender': 'male'})
					self.gender = 'male'
			if citizenship:
				if int(citizenship) == 0:
					# val.update({'citizen_resident_status_code': 'sa'})
					self.citizen_resident_status_code = 'sa'
				elif int(citizenship) == 1:
					# val.update({'citizen_resident_status_code': 'PR'})
					self.citizen_resident_status_code = 'PR'

			if int(year) == 00 or int(year) >= 01 and int(year) <= 20:
				birth_date = dt.strptime('20' + year + '-' + month + '-' + day, '%Y-%m-%d').date()
			else:
				birth_date = dt.strptime('19' + year + '-' + month + '-' + day, '%Y-%m-%d').date()
			self.person_birth_date = birth_date


	# this was fetched form provider accred but should be applicable here too
	# @api.multi
	# @api.onchange('cont_number_home', 'cont_number_office', 'person_fax_number', 'work_phone')
	# def onchange_validate_number(self):
	# 	dbg("onchange_validate_number")
	# 	if self.cont_number_home:
	# 		if not self.cont_number_home.isdigit() or len(self.cont_number_home) != 10:
	# 			self.cont_number_home = ''
	# 			return {'warning': {'title': 'Invalid input', 'message': 'Please enter 10 digits number'}}
	# 	if self.cont_number_office:
	# 		if not self.cont_number_office.isdigit() or len(self.cont_number_office) != 10:
	# 			self.cont_number_office = ''
	# 			return {'warning': {'title': 'Invalid input', 'message': 'Please enter 10 digits number'}}
	# 	if self.work_phone:
	# 		if not self.work_phone.isdigit() or len(self.work_phone) != 10:
	# 			self.work_phone = ''
	# 			return {'warning': {'title': 'Invalid input', 'message': 'Please enter 10 digits number'}}
	# 	if self.person_fax_number:
	# 		if not self.person_fax_number.isdigit() or len(self.person_fax_number) != 10:
	# 			self.person_fax_number = ''
	# 			return {'warning': {'title': 'Invalid input', 'message': 'Please enter 10 digits number'}}

	@api.multi
	@api.onchange('person_suburb', 'person_home_suburb', 'person_postal_suburb')
	def onchange_suburb(self):
		dbg("onchange_suburb")
		if self.person_suburb:
			self.work_zip = self.person_suburb.postal_code
			self.work_city = self.person_suburb.city_id.id
			self.work_municipality = self.person_suburb.municipality_id.id
			self.work_province = self.person_suburb.province_id.id
			self.work_country = self.person_suburb.country_id.id
		if self.person_home_suburb:
			self.person_home_zip = self.person_home_suburb.postal_code
			self.person_home_city = self.person_home_suburb.city_id.id
			self.physical_municipality = self.person_home_suburb.municipality_id.id
			self.person_home_province_code = self.person_home_suburb.province_id.id
			self.country_home = self.person_home_suburb.country_id.id
		if self.person_postal_suburb:
			self.person_postal_zip = self.person_postal_suburb.postal_code
			self.person_postal_city = self.person_postal_suburb.city_id.id
			self.postal_municipality = self.person_postal_suburb.municipality_id.id
			self.person_postal_province_code = self.person_postal_suburb.province_id.id
			self.country_postal = self.person_postal_suburb.country_id.id

	@api.multi
	@api.onchange('cont_number_home', 'cont_number_office', 'person_fax_number', 'work_phone')
	def onchange_validate_number(self):
		dbg("onchange_validate_number")
		if self.cont_number_home:
			if not self.cont_number_home.isdigit() or len(self.cont_number_home) != 10:
				self.cont_number_home = ''
				return {'warning': {'title': 'Invalid input', 'message': 'Please enter 10 digits number'}}
		if self.cont_number_office:
			if not self.cont_number_office.isdigit() or len(self.cont_number_office) != 10:
				self.cont_number_office = ''
				return {'warning': {'title': 'Invalid input', 'message': 'Please enter 10 digits number'}}
		if self.work_phone:
			if not self.work_phone.isdigit() or len(self.work_phone) != 10:
				self.work_phone = ''
				return {'warning': {'title': 'Invalid input', 'message': 'Please enter 10 digits number'}}
		if self.person_fax_number:
			if not self.person_fax_number.isdigit() or len(self.person_fax_number) != 10:
				self.person_fax_number = ''
				return {'warning': {'title': 'Invalid input', 'message': 'Please enter 10 digits number'}}

	@api.onchange('disclaimer')
	def populate_fields(self):
		if self.learner_id and self.disclaimer:
			lnr = self.learner_id
			dbg(lnr.citizen_resident_status_code)
			self.citizen_resident_status_code = lnr.citizen_resident_status_code
			self.citizen_status_saqa_code = lnr.citizen_status_saqa_code
			self.country_id = lnr.country_id
			self.unknown_type = lnr.unknown_type
			self.unknown_type_document = lnr.unknown_type_document
			self.nationality_saqa_code = lnr.nationality_saqa_code
			self.learner_identification_id = lnr.learner_identification_id
			self.alternate_id_type = lnr.alternate_id_type
			self.person_birth_date = lnr.person_birth_date
			self.gender = lnr.gender
			self.passport_id = lnr.passport_id
			self.national_id = lnr.national_id
			self.home_language_code = lnr.home_language_code
			self.home_lang_saqa_code = lnr.home_lang_saqa_code
			self.disability_status_saqa = lnr.disability_status_saqa
			self.seeing_rating_id = lnr.seeing_rating_id
			self.hearing_rating_id = lnr.hearing_rating_id
			self.walking_rating_id = lnr.walking_rating_id
			self.remembering_rating_id = lnr.remembering_rating_id
			self.communicating_rating_id = lnr.communicating_rating_id
			self.self_care_rating_id = lnr.self_care_rating_id
			self.person_title = lnr.person_title
			self.person_last_name = lnr.person_last_name
			self.person_name = lnr.person_name
			self.initials = lnr.initials
			self.cont_number_home = lnr.cont_number_home
			self.cont_number_office = lnr.cont_number_office
			self.work_phone = lnr.work_phone
			self.person_fax_number = lnr.person_fax_number
			self.current_occupation = lnr.current_occupation
			self.years_in_occupation = lnr.years_in_occupation
			self.person_cell_phone_number = lnr.person_cell_phone_number
			self.department = lnr.department
			self.manager = lnr.manager
			self.job_title = lnr.job_title
			self.marital = lnr.marital
			self.dissability = lnr.dissability
			self.disability_status = lnr.disability_status
			self.socio_economic_status = lnr.socio_economic_status
			self.equity = lnr.equity
			self.highest_education = lnr.highest_education
			self.work_address = lnr.work_address
			self.work_address2 = lnr.work_address2
			self.work_address3 = lnr.work_address3
			self.person_suburb = lnr.person_suburb
			self.work_city = lnr.work_city
			self.work_province = lnr.work_province
			self.work_zip = lnr.work_zip
			self.work_country = lnr.work_country
			self.work_municipality = lnr.work_municipality
			self.person_home_address_1 = lnr.person_home_address_1
			self.person_home_address_2 = lnr.person_home_address_2
			self.person_home_address_3 = lnr.person_home_address_3
			self.person_home_suburb = lnr.person_home_suburb
			self.person_home_city = lnr.person_home_city
			self.physical_municipality = lnr.physical_municipality
			self.person_home_province_code = lnr.person_home_province_code
			self.country_home = lnr.country_home
			self.person_home_zip = lnr.person_home_zip
			self.same_as_home = lnr.same_as_home
			self.person_postal_address_1 = lnr.person_postal_address_1
			self.person_postal_address_2 = lnr.person_postal_address_2
			self.person_postal_address_3 = lnr.person_postal_address_3
			self.person_postal_suburb = lnr.person_postal_suburb
			self.person_postal_city = lnr.person_postal_city
			self.postal_municipality = lnr.postal_municipality
			self.person_postal_province_code = lnr.person_postal_province_code
			self.person_postal_zip = lnr.person_postal_zip
			self.country_postal = lnr.country_postal


	@api.one
	def update(self):
		lnr = self.learner_id
		lang_dict = {
			'English':'eng',
			'isiZulu':'zul',
			'sePedi':'sep',
			'tshivenda':'tsh',
			'seSotho':'ses',
			'xiTsonga':'xit',
			'siSwati':'swa',
			'Ndebele':'nde',
			'seTswana':'set',
			'Afrikaans':'afr',
			'isiXhosa':'xho',
					 }
		disability_dict = {
			'sight':'1',
			'hearing':'2',
			'communication':'3',
			'physical':'4',
			'intellectual':'5',
			'emotional':'6',
			'multiple':'7',
			'disabled':'9',
			'none':'n'
						}
		socio_dict = {
			'employed': '1',
			'unemployed': '2',
			'Not working, not looking': '3',
			'Home-maker (not working)': '4',
			'Scholar/student (not w.)': '6',
			'Pensioner/retired (not w.)': '7',
			'Not working - disabled': '8',
			'Not working - no wish to w': '9',
			'Not working - N.E.C.': '10',
			'N/A: aged <15': '97',
			'N/A: Institution': '98',
			'Unspecified': 'U',
		}
		equity_dict = {
			'black_african':'ba',
			'black_indian':'bi',
			'black_coloured':'bc',
			'other':'oth',
			'unknown':'u',
			'white':'wh',
		}
		if lnr:
			vals = {
				# 'msg': msg + '</p>>--changed to--></p>' + msg2,
				'status': 'submitted',
				'learner_id': lnr.id,
				'disclaimer': self.disclaimer,
				'reference': self.env['ir.sequence'].get('learner.update.reference'),
				'citizen_resident_status_code':self.citizen_resident_status_code,
				'citizen_status_saqa_code':self.citizen_status_saqa_code,
				'country_id':self.country_id.id,
				'unknown_type':self.unknown_type,
				'unknown_type_document':self.unknown_type_document,
				'nationality_saqa_code':self.nationality_saqa_code,
				'learner_identification_id':self.learner_identification_id,
				'alternate_id_type':self.alternate_id_type,
				'person_birth_date':self.person_birth_date,
				'gender':self.gender,
				'passport_id':self.passport_id,
				'national_id':self.national_id,
				'home_language_code':self.home_language_code.id,
				'home_lang_saqa_code':self.home_lang_saqa_code,
				'disability_status_saqa':self.disability_status_saqa,
				'seeing_rating_id':self.seeing_rating_id,
				'hearing_rating_id':self.hearing_rating_id,
				'walking_rating_id':self.walking_rating_id,
				'remembering_rating_id':self.remembering_rating_id,
				'communicating_rating_id':self.communicating_rating_id,
				'self_care_rating_id':self.self_care_rating_id,
				'person_title':self.person_title,
				'person_last_name':self.person_last_name,
				'person_name':self.person_name,
				'name': self.person_name + ' ' + self.person_last_name,
				'initials':self.initials,
				'cont_number_home':self.cont_number_home,
				'cont_number_office':self.cont_number_office,
				'work_phone':self.work_phone,
				'person_fax_number':self.person_fax_number,
				'current_occupation':self.current_occupation,
				'years_in_occupation':self.years_in_occupation,
				'person_cell_phone_number':self.person_cell_phone_number,
				'department':self.department,
				'manager':self.manager,
				'job_title':self.job_title,
				'marital':self.marital,
				'dissability':self.dissability,
				'disability_status':self.disability_status,
				'socio_economic_status':self.socio_economic_status,
				'equity':self.equity,
				'highest_education':self.highest_education,
				'work_address':self.work_address,
				'work_address2':self.work_address2,
				'work_address3':self.work_address3,
				'person_suburb':self.person_suburb.id,
				'work_city':self.work_city.id,
				'work_province':self.work_province.id,
				'work_zip':self.work_zip,
				'work_country':self.work_country.id,
				'work_municipality':self.work_municipality.id,
				'person_home_address_1':self.person_home_address_1,
				'person_home_address_2':self.person_home_address_2,
				'person_home_address_3':self.person_home_address_3,
				'person_home_suburb':self.person_home_suburb.id,
				'person_home_city':self.person_home_city.id,
				'physical_municipality':self.physical_municipality.id,
				'person_home_province_code':self.person_home_province_code.id,
				'country_home':self.country_home.id,
				'person_home_zip':self.person_home_zip,
				'same_as_home':self.same_as_home,
				'person_postal_address_1':self.person_postal_address_1,
				'person_postal_address_2':self.person_postal_address_2,
				'person_postal_address_3':self.person_postal_address_3,
				'person_postal_suburb':self.person_postal_suburb.id,
				'person_postal_city':self.person_postal_city.id,
				'postal_municipality':self.postal_municipality.id,
				'person_postal_province_code':self.person_postal_province_code.id,
				'person_postal_zip':self.person_postal_zip,
				'country_postal':self.country_postal.id,



				'related_citizen_resident_status_code':lnr.citizen_resident_status_code,
				'related_citizen_status_saqa_code':lnr.citizen_status_saqa_code,
				'related_country_id':lnr.country_id.id,
				'related_unknown_type':lnr.unknown_type,
				'related_unknown_type_document':lnr.unknown_type_document,
				'related_nationality_saqa_code':lnr.nationality_saqa_code,
				'related_learner_identification_id':lnr.learner_identification_id,
				'related_alternate_id_type':lnr.alternate_id_type,
				'related_person_birth_date':lnr.person_birth_date,
				'related_gender':lnr.gender,
				'related_passport_id':lnr.passport_id,
				'related_national_id':lnr.national_id,
				'related_home_language_code':lnr.home_language_code.id,
				'related_home_lang_saqa_code':lnr.home_lang_saqa_code,
				'related_disability_status_saqa':lnr.disability_status_saqa,
				'related_seeing_rating_id':lnr.seeing_rating_id,
				'related_hearing_rating_id':lnr.hearing_rating_id,
				'related_walking_rating_id':lnr.walking_rating_id,
				'related_remembering_rating_id':lnr.remembering_rating_id,
				'related_communicating_rating_id':lnr.communicating_rating_id,
				'related_self_care_rating_id':lnr.self_care_rating_id,
				'related_person_title':lnr.person_title,
				'related_person_last_name':lnr.person_last_name,
				'related_person_name':lnr.person_name,
				'related_name':lnr.name,
				'related_initials':lnr.initials,
				'related_cont_number_home':lnr.cont_number_home,
				'related_cont_number_office':lnr.cont_number_office,
				'related_work_phone':lnr.work_phone,
				'related_person_fax_number':lnr.person_fax_number,
				'related_current_occupation':lnr.current_occupation,
				'related_years_in_occupation':lnr.years_in_occupation,
				'related_person_cell_phone_number':lnr.person_cell_phone_number,
				'related_department':lnr.department,
				'related_manager':lnr.manager,
				'related_job_title':lnr.job_title,
				'related_marital':lnr.marital,
				'related_dissability':lnr.dissability,
				'related_disability_status':lnr.disability_status,
				'related_socio_economic_status':lnr.socio_economic_status,
				'related_equity':lnr.equity,
				'related_highest_education':lnr.highest_education,
				'related_work_address':lnr.work_address,
				'related_work_address2':lnr.work_address2,
				'related_work_address3':lnr.work_address3,
				'related_person_suburb':lnr.person_suburb.id,
				'related_work_city':lnr.work_city.id,
				'related_work_province':lnr.work_province.id,
				'related_work_zip':lnr.work_zip,
				'related_work_country':lnr.work_country.id,
				'related_work_municipality':lnr.work_municipality.id,
				'related_person_home_address_1':lnr.person_home_address_1,
				'related_person_home_address_2':lnr.person_home_address_2,
				'related_person_home_address_3':lnr.person_home_address_3,
				'related_person_home_suburb':lnr.person_home_suburb.id,
				'related_person_home_city':lnr.person_home_city.id,
				'related_physical_municipality':lnr.physical_municipality.id,
				'related_person_home_province_code':lnr.person_home_province_code.id,
				'related_country_home':lnr.country_home.id,
				'related_person_home_zip':lnr.person_home_zip,
				'related_same_as_home':lnr.same_as_home,
				'related_person_postal_address_1':lnr.person_postal_address_1,
				'related_person_postal_address_2':lnr.person_postal_address_2,
				'related_person_postal_address_3':lnr.person_postal_address_3,
				'related_person_postal_suburb':lnr.person_postal_suburb.id,
				'related_person_postal_city':lnr.person_postal_city.id,
				'related_postal_municipality':lnr.postal_municipality.id,
				'related_person_postal_province_code':lnr.person_postal_province_code.id,
				'related_person_postal_zip':lnr.person_postal_zip,
				'related_country_postal':lnr.country_postal.id,

			}
			if self.home_language_code:
				vals.update({'home_lang_saqa_code':lang_dict[self.home_language_code.name]})

			# handle the diff if there are document updates and write partner to old doc
			nw = dt.now()
			dbg(nw)
			nw_str = nw.strftime("%d/%m/%Y, %H:%M:%S")

			if self.id_document:
				vals.update({'id_document': self.id_document.id, 'related_id_document': lnr.id_document.id})
				# check if old doc exists to do work on it
				if lnr.id_document:
					lnr.id_document.name = 'replaced-' + nw_str + '-' + lnr.id_document.name
					lnr.id_document.res_id = lnr.id
					lnr.id_document.res_model = 'hr.employee'
			if self.unknown_type_document:
				vals.update({'unknown_type_document': self.unknown_type_document.id, 'related_unknown_type_document': lnr.unknown_type_document.id})
				# check if old doc exists to do work on it
				if lnr.unknown_type_document:
					lnr.unknown_type_document.name = 'replaced-' + nw_str + '-' + lnr.unknown_type_document.name
					lnr.unknown_type_document.res_id = lnr.id
					lnr.unknown_type_document.res_model = 'hr.employee'
			if self.learner_master_other_docs_ids:
				vals.update({'learner_master_other_docs_ids': [(6,0,[doc.id for doc in self.learner_master_other_docs_ids])],
							 'related_learner_master_other_docs_ids': [doc.id for doc in
																	   lnr.learner_master_other_docs_ids]})
				# doc_list = []
				# for doc in self.learner_master_other_docs_ids:
				# 	dbg(doc)
				# 	doc_list.append(doc.id)
				# vals.update({'learner_master_other_docs_ids':[(6, 0, doc_list)]})
				# vals.update({'learner_master_other_docs_ids':doc_list,'related_learner_master_other_docs_ids':[doc.id for doc in lnr.learner_master_other_docs_ids]})
				# for doc in self.learner_master_other_docs_ids:

			if self.disclaimer:
				dbg('valzzzzzzzzzzzzzz' + str(vals))
				ud = self.env['updated.learner'].create(vals)
			self.learner_id.chatter(self.env.user, "Information update request has been submitted")
			ir_model_data_obj = self.env['ir.model.data']
			mail_template_id = ir_model_data_obj.get_object_reference('hwseta_etqe',
																	  'email_template_learner_update_submit_notification')
			if mail_template_id:
				self.pool['email.template'].send_mail(self.env.cr, self.env.uid, mail_template_id[1], ud.id,
													  force_send=True, context=self.env.context)
		else:
			raise Warning('no assessor found')


class updated_learner(models.Model):
	_name = 'updated.learner'

	"""
	this keeps the memory of what the prov wanted to change, it gets a submitted state on creation by provider
	it will then show up for internal staff to click approve , which will then write the vals
	update the chatter of old and new plus submitter and approver
	"""
	status = fields.Selection([('submitted', 'Submitted'), ('approved', 'Approved'), ('rejected', 'Rejected')])
	msg = fields.Text()
	learner_id = fields.Many2one('hr.employee')
	disclaimer = fields.Boolean()
	reference = fields.Char()
	action_date = fields.Date()
	action_partner = fields.Many2one('res.partner')
	# cit section
	citizen_resident_status_code = fields.Selection(
		[('sa', 'SA - South Africa'), ('dual', 'D - Dual (SA plus other)'), ('other', 'O - Other'),
		 ('PR', 'PR - Permanent Resident'), ('unknown', 'U - Unknown')], string='Citizen Status')
	citizen_status_saqa_code = fields.Selection([('sa', 'SA'), ('d', 'D'), ('o', 'O'), ('pr', 'PR'), ('u', 'U')],
												string='Citizen Status SAQA Code')
	country_id = fields.Many2one('res.country', string='Country of Nationality')
	unknown_type = fields.Selection([
		('political_asylum', 'Political Asylum'),
		('refugee', 'Refugee'), ], string='Type')
	unknown_type_document = fields.Many2one('ir.attachment', string="Type Document")
	nationality_saqa_code = fields.Selection([('sa', 'SA')], string='Nationality SAQA Code')
	learner_identification_id = fields.Char("R.S.A.Identification No.", size=13)
	alternate_id_type = fields.Selection(
		[('saqa_member', '521 - SAQA Member ID'), ('passport_number', '527 - Passport Number'),
		 ('drivers_license', '529 - Drivers License'), ('temporary_id_number', '531 - Temporary ID number'),
		 ('none', '533 - None'), ('unknown', '535 - Unknown'), ('student_number', '537 - Student number'),
		 ('work_permit_number', '538 - Work Permit Number'), ('employee_number', '539 - Employee Number'),
		 ('birth_certificate_number', '540 - Birth Certificate Number'),
		 ('hsrc_register_number', ' 541 - HSRC Register Number'), ('etqe_record_number', '561 - ETQA Record Number'),
		 ('refugee_number', '565 - Refugee Number')], string='Alternate ID Type')
	person_birth_date = fields.Date(string='Birth Date')
	gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')
	passport_id = fields.Char('Passport No')
	national_id = fields.Char(string='National Id', size=20)
	home_language_code = fields.Many2one('res.lang', string='Home Language Code', size=6)
	home_lang_saqa_code = fields.Selection(
		[('eng', 'Eng'), ('afr', 'Afr'), ('xho', 'Xho'), ('set', 'Set'), ('zul', 'Zul'), ('sep', 'Sep'), ('tsh', 'Tsh'),
		 ('ses', 'Ses'), ('xit', 'Xit'), ('swa', 'Swa'), ('nde', 'Nde'), ('u', 'U'), ('oth', 'Oth')],
		string='Home Lanaguage SAQA Code')
	disability_status_saqa = fields.Selection(
		[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('9', '9'), ('n', 'N')],
		string='Disability SAQA Code')
	# rating section
	seeing_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Seeing Rating Id',
		track_visibility='onchange')
	hearing_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Hearing Rating Id',
		track_visibility='onchange')
	walking_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Walking Rating Id',
		track_visibility='onchange')
	remembering_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Remembering Rating Id',
		track_visibility='onchange')
	communicating_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Communicating Rating Id',
		track_visibility='onchange')
	self_care_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Self Care Rating Id',
		track_visibility='onchange')
	# contact info section
	person_title = fields.Selection(
		[('adv', 'Adv.'), ('dr', 'Dr'), ('mr', 'Mr'), ('mrs', 'Mrs'), ('ms', 'Ms'), ('prof', 'Prof')], string='Title',
		track_visibility='onchange')
	person_last_name = fields.Char(string='Last Name', size=45)
	person_name = fields.Char(string='First Name', size=50)
	name = fields.Char(string='Name', size=50)
	initials = fields.Char(string='Initials')
	cont_number_home = fields.Char(string='Home Number', size=10)
	cont_number_office = fields.Char(string='Office Number', size=10)
	work_phone = fields.Char()
	person_fax_number = fields.Char(string='Tele Fax Number ', size=10)

	current_occupation = fields.Char(string='Current Occupation')
	years_in_occupation = fields.Char(string='Years in Occupation')
	person_cell_phone_number = fields.Char()
	department = fields.Char()
	manager = fields.Char()
	job_title = fields.Char()
	# status section
	marital = fields.Selection(
		[('single', 'Single'), ('married', 'Married'), ('widower', 'Widower'), ('widow', 'Widow'),
		 ('divorced', 'Divorced')],
		'Marital Status')
	dissability = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Dissability")
	disability_status = fields.Selection([
		('sight', 'Sight ( even with glasses )'),
		('hearing', 'Hearing ( even with h.aid )'),
		('communication', 'Communication ( talk/listen)'),
		('physical', 'Physical ( move/stand, etc)'),
		('intellectual', 'Intellectual ( learn,etc)'),
		('emotional', 'Emotional ( behav/psych)'),
		('multiple', 'Multiple'),
		('disabled', 'Disabled but unspecified'),
		('none', 'None')], string='Disability Status')
	socio_economic_status = fields.Selection([('employed', 'Employed'), ('unemployed', 'Unemployed, seeking work'),
											  ('Not working, not looking', 'Not working, not looking'),
											  ('Home-maker (not working)', 'Home-maker (not working)'),
											  ('Scholar/student (not w.)', 'Scholar/student (not w.)'),
											  ('Pensioner/retired (not w.)', 'Pensioner/retired (not w.)'),
											  ('Not working - disabled', 'Not working - disabled'),
											  ('Not working - no wish to w', 'Not working - no wish to w'),
											  ('Not working - N.E.C.', 'Not working - N.E.C.'),
											  ('N/A: aged <15', 'N/A: aged <15'),
											  ('N/A: Institution', 'N/A: Institution'),
											  ('Unspecified', 'Unspecified'), ], string='Socio Economic Status')
	equity = fields.Selection([('black_african', 'Black: African'), ('black_indian', 'Black: Indian / Asian'),
							   ('black_coloured', 'Black: Coloured'), ('other', 'Other'), ('unknown', 'Unknown'),
							   ('white', 'White')], string='Equity')
	# learner data section
	highest_education = fields.Char(string='Highest Education')
	# address section
	work_address = fields.Char()
	work_address2 = fields.Char()
	work_address3 = fields.Char()
	person_suburb = fields.Many2one('res.suburb')
	work_city = fields.Many2one('res.city')
	work_province = fields.Many2one('res.country.state')
	work_zip = fields.Char()
	work_country = fields.Many2one('res.country')
	work_municipality = fields.Many2one('res.municipality')
	# home addr
	person_home_address_1 = fields.Char(string='Home Address 1', size=50)
	person_home_address_2 = fields.Char(string='Home Address 2', size=50)
	person_home_address_3 = fields.Char(string='Home Address 3', size=50)
	person_home_suburb = fields.Many2one('res.suburb', string='Home Suburb')
	person_home_city = fields.Many2one('res.city', string='Home City')
	physical_municipality = fields.Many2one('res.municipality', string='Physical Municipality')
	person_home_province_code = fields.Many2one('res.country.state', string='Home Province Code')
	country_home = fields.Many2one('res.country', string='Home Country')
	person_home_zip = fields.Char(string='Home Zip')
	# person_home_addr_post_code = fields.Char(string='Home Addr Post Code', size=4)
	same_as_home = fields.Boolean(string='Same As Home Address')
	person_postal_address_1 = fields.Char(string='Postal Address 1', size=50)
	person_postal_address_2 = fields.Char(string='Postal Address 2', size=50)
	person_postal_address_3 = fields.Char(string='Postal Address 3', size=50)
	person_postal_suburb = fields.Many2one('res.suburb', string='Postal Suburb')
	person_postal_city = fields.Many2one('res.city', string='Postal City')
	postal_municipality = fields.Many2one('res.municipality', string='Postal Municipality')
	person_postal_province_code = fields.Many2one('res.country.state', string='Postal Province Code')
	person_postal_zip = fields.Char(string='Postal Zip')
	country_postal = fields.Many2one('res.country', string='Postal Country')
	# documents section
	id_document = fields.Many2one('ir.attachment', string='ID Document', help='Upload Document')
	learner_master_other_docs_ids = fields.Many2many('acc.multi.doc.upload', string='Document', help='Upload Document')

	# cit section
	related_citizen_resident_status_code = fields.Selection(
		[('sa', 'SA - South Africa'), ('dual', 'D - Dual (SA plus other)'), ('other', 'O - Other'),
		 ('PR', 'PR - Permanent Resident'), ('unknown', 'U - Unknown')], string='Citizen Status')
	related_citizen_status_saqa_code = fields.Selection([('sa', 'SA'), ('d', 'D'), ('o', 'O'), ('pr', 'PR'), ('u', 'U')],
												string='Citizen Status SAQA Code')
	related_country_id = fields.Many2one('res.country', string='Country of Nationality')
	related_unknown_type = fields.Selection([
		('political_asylum', 'Political Asylum'),
		('refugee', 'Refugee'), ], string='Type')
	related_unknown_type_document = fields.Many2one('ir.attachment', string="Type Document")
	related_nationality_saqa_code = fields.Selection([('sa', 'SA')], string='Nationality SAQA Code')
	related_learner_identification_id = fields.Char("R.S.A.Identification No.", size=13)
	related_alternate_id_type = fields.Selection(
		[('saqa_member', '521 - SAQA Member ID'), ('passport_number', '527 - Passport Number'),
		 ('drivers_license', '529 - Drivers License'), ('temporary_id_number', '531 - Temporary ID number'),
		 ('none', '533 - None'), ('unknown', '535 - Unknown'), ('student_number', '537 - Student number'),
		 ('work_permit_number', '538 - Work Permit Number'), ('employee_number', '539 - Employee Number'),
		 ('birth_certificate_number', '540 - Birth Certificate Number'),
		 ('hsrc_register_number', ' 541 - HSRC Register Number'), ('etqe_record_number', '561 - ETQA Record Number'),
		 ('refugee_number', '565 - Refugee Number')], string='Alternate ID Type')
	related_person_birth_date = fields.Date(string='Birth Date')
	related_gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')
	related_passport_id = fields.Char('Passport No')
	related_national_id = fields.Char(string='National Id', size=20)
	related_home_language_code = fields.Many2one('res.lang', string='Home Language Code', size=6)
	related_home_lang_saqa_code = fields.Selection(
		[('eng', 'Eng'), ('afr', 'Afr'), ('xho', 'Xho'), ('set', 'Set'), ('zul', 'Zul'), ('sep', 'Sep'), ('tsh', 'Tsh'),
		 ('ses', 'Ses'), ('xit', 'Xit'), ('swa', 'Swa'), ('nde', 'Nde'), ('u', 'U'), ('oth', 'Oth')],
		string='Home Lanaguage SAQA Code')
	related_disability_status_saqa = fields.Selection(
		[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('9', '9'), ('n', 'N')],
		string='Disability SAQA Code')
	# rating section
	related_seeing_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Seeing Rating Id',
		track_visibility='onchange')
	related_hearing_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Hearing Rating Id',
		track_visibility='onchange')
	related_walking_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Walking Rating Id',
		track_visibility='onchange')
	related_remembering_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Remembering Rating Id',
		track_visibility='onchange')
	related_communicating_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Communicating Rating Id',
		track_visibility='onchange')
	related_self_care_rating_id = fields.Selection(
		[('1', 'No difficulty'), ('2', 'Some difficulty'), ('3', 'A lot of difficulty'), ('4', 'Cannot do at all'),
		 ('6', 'Cannot yet be determined'), ('60', 'May be part of multiple difficulties (TBC)'),
		 ('70', 'May have difficulty (TBC)'), ('80', 'Former difficulty - none now')], string='Self Care Rating Id',
		track_visibility='onchange')
	# contact info section
	related_person_title = fields.Selection(
		[('adv', 'Adv.'), ('dr', 'Dr'), ('mr', 'Mr'), ('mrs', 'Mrs'), ('ms', 'Ms'), ('prof', 'Prof')], string='Title',
		track_visibility='onchange')
	related_person_last_name = fields.Char(string='Last Name', size=45)
	related_person_name = fields.Char(string='First Name', size=50)
	related_name = fields.Char(string='Name', size=50)
	related_initials = fields.Char(string='Initials')
	related_cont_number_home = fields.Char(string='Home Number', size=10)
	related_cont_number_office = fields.Char(string='Office Number', size=10)
	related_work_phone = fields.Char()
	related_person_fax_number = fields.Char(string='Tele Fax Number ', size=10)

	related_current_occupation = fields.Char(string='Current Occupation')
	related_years_in_occupation = fields.Char(string='Years in Occupation')
	related_person_cell_phone_number = fields.Char()
	related_department = fields.Char()
	related_manager = fields.Char()
	related_job_title = fields.Char()
	# status section
	related_marital = fields.Selection(
		[('single', 'Single'), ('married', 'Married'), ('widower', 'Widower'), ('widow', 'Widow'),
		 ('divorced', 'Divorced')],
		'Marital Status')
	related_dissability = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Dissability")
	related_disability_status = fields.Selection([
		('sight', 'Sight ( even with glasses )'),
		('hearing', 'Hearing ( even with h.aid )'),
		('communication', 'Communication ( talk/listen)'),
		('physical', 'Physical ( move/stand, etc)'),
		('intellectual', 'Intellectual ( learn,etc)'),
		('emotional', 'Emotional ( behav/psych)'),
		('multiple', 'Multiple'),
		('disabled', 'Disabled but unspecified'),
		('none', 'None')], string='Disability Status')
	related_socio_economic_status = fields.Selection([('employed', 'Employed'), ('unemployed', 'Unemployed, seeking work'),
											  ('Not working, not looking', 'Not working, not looking'),
											  ('Home-maker (not working)', 'Home-maker (not working)'),
											  ('Scholar/student (not w.)', 'Scholar/student (not w.)'),
											  ('Pensioner/retired (not w.)', 'Pensioner/retired (not w.)'),
											  ('Not working - disabled', 'Not working - disabled'),
											  ('Not working - no wish to w', 'Not working - no wish to w'),
											  ('Not working - N.E.C.', 'Not working - N.E.C.'),
											  ('N/A: aged <15', 'N/A: aged <15'),
											  ('N/A: Institution', 'N/A: Institution'),
											  ('Unspecified', 'Unspecified'), ], string='Socio Economic Status')
	related_equity = fields.Selection([('black_african', 'Black: African'), ('black_indian', 'Black: Indian / Asian'),
							   ('black_coloured', 'Black: Coloured'), ('other', 'Other'), ('unknown', 'Unknown'),
							   ('white', 'White')], string='Equity')
	# learner data section
	related_highest_education = fields.Char(string='Highest Education')
	# address section
	related_work_address = fields.Char()
	related_work_address2 = fields.Char()
	related_work_address3 = fields.Char()
	related_person_suburb = fields.Many2one('res.suburb')
	related_work_city = fields.Many2one('res.city')
	related_work_province = fields.Many2one('res.country.state')
	related_work_zip = fields.Char()
	related_work_country = fields.Many2one('res.country')
	related_work_municipality = fields.Many2one('res.municipality')
	# home addr
	related_person_home_address_1 = fields.Char(string='Home Address 1', size=50)
	related_person_home_address_2 = fields.Char(string='Home Address 2', size=50)
	related_person_home_address_3 = fields.Char(string='Home Address 3', size=50)
	related_person_home_suburb = fields.Many2one('res.suburb', string='Home Suburb')
	related_person_home_city = fields.Many2one('res.city', string='Home City')
	related_physical_municipality = fields.Many2one('res.municipality', string='Physical Municipality')
	related_person_home_province_code = fields.Many2one('res.country.state', string='Home Province Code')
	related_country_home = fields.Many2one('res.country', string='Home Country')
	related_person_home_zip = fields.Char(string='Home Zip')
	# person_home_addr_post_code = fields.Char(string='Home Addr Post Code', size=4)
	related_same_as_home = fields.Boolean(string='Same As Home Address')
	related_person_postal_address_1 = fields.Char(string='Postal Address 1', size=50)
	related_person_postal_address_2 = fields.Char(string='Postal Address 2', size=50)
	related_person_postal_address_3 = fields.Char(string='Postal Address 3', size=50)
	related_person_postal_suburb = fields.Many2one('res.suburb', string='Postal Suburb')
	related_person_postal_city = fields.Many2one('res.city', string='Postal City')
	related_postal_municipality = fields.Many2one('res.municipality', string='Postal Municipality')
	related_person_postal_province_code = fields.Many2one('res.country.state', string='Postal Province Code')
	related_person_postal_zip = fields.Char(string='Postal Zip')
	related_country_postal = fields.Many2one('res.country', string='Postal Country')
	# documents section
	related_id_document = fields.Many2one('ir.attachment', string='ID Document', help='Upload Document')
	related_learner_master_other_docs_ids = fields.Many2many('acc.multi.doc.upload', string='Document', help='Upload Document')


	@api.one
	def approve_update(self):
		vals = self.read()
		dbg(vals)
		doc_list = [
			'id_document',
			'unknown_type_document',
		]
		# handle tuples, replace the tuple with its own id
		for val in vals[0].keys():
			dbg(vals[0].get(val))
			dbg(type(vals[0].get(val)))
			if type(vals[0].get(val)) == tuple:
				vals[0].update({val: vals[0].get(val)[0]})
		for doc in doc_list:
			if not vals[0].get(doc):
				del vals[0][doc]
		self.status = 'approved'
		self.action_date = date.today()
		self.action_partner = self.env.user.partner_id
		dbg('vals after tuple augment')
		# deal with m2m writing correctly
		if vals[0].get('learner_master_other_docs_ids'):
			original_docs = [(6,0,vals[0].get('learner_master_other_docs_ids'))]
			vals[0].update({'learner_master_other_docs_ids':original_docs})
		dbg(vals)
		self.learner_id.write(vals[0])
		# self.provider_id.chatter(self.env.user, "Information update request has been approved")
		ir_model_data_obj = self.env['ir.model.data']
		mail_template_id = ir_model_data_obj.get_object_reference('hwseta_etqe',
																  'email_template_learner_update_approve_notification')
		if mail_template_id:
			self.pool['email.template'].send_mail(self.env.cr, self.env.uid, mail_template_id[1], self.id,
												  force_send=True, context=self.env.context)
		# self.provider_id.chatter(self.env.user, self.msg)

	@api.one
	def reject_update(self,msg):
		self.status = 'rejected'
		self.action_date = date.today()
		self.action_partner = self.env.user.partner_id
		self.learner_id.chatter(
			self.env.user,
			self.reference + '-Update has been rejected with the following comments: \n' + msg
								)

class hr_employee(models.Model):
	_inherit = 'hr.employee'

	update_ids = fields.One2many('updated.learner', 'learner_id')

	# def chatter(self, author, msg):
	# 	self.message_post(body=_(msg), subtype='mail.mt_comment', author_id=author.partner_id.id)