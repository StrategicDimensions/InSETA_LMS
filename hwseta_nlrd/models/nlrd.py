# coding=utf-8
from openerp import models, fields, tools, api, _
from datetime import datetime
import re
from collections import OrderedDict as OD
from nlrd_dat import gendat, dat21, dat24, dat25, dat26, dat27, dat29
from nlrd_fixes import *

DEBUG = True

if DEBUG:
	import logging

	logger = logging.getLogger(__name__)


	def dbg(msg):
		logger.info(msg)
else:
	def dbg(msg):
		pass

# global_write = False
global_write = True


class nlrd_exporter(models.TransientModel):
	_name = 'nlrd.exporter'

	def check_lrq(self, lrq):
		broken = False
		msg = str(lrq.id) + '\n'
		if not lrq.learner_id.learner_identification_id and not lrq.learner_id.national_id:
			broken = True
			msg += 'no id or alt id \n'
		if not lrq.learner_qualification_parent_id.saqa_qual_id:
			broken = True
			msg += 'no qualification code \n'
		if not lrq.certificate_date:
			broken = True
			msg += 'no certificate date \n'
		if not lrq.qual_status:
			broken = True
			msg += 'no qual_status \n'
		if not lrq.assessors_id.assessor_seq_no:
			broken = True
			msg += 'no assessor number \n'
		if not lrq.provider_id:
			broken = True
			msg += 'no provider on lrq \n'
		if not lrq.start_date:
			broken = True
			msg += 'not start date \n'
		return broken, msg

	@api.multi
	def fetch_nlrd_29(self):
		domain = [('certificate_date', '>', '2019-08-01')]
		brk_count = 0
		right_count = 0
		big_daddy = ''
		for lrq in self.env['learner.registration.qualification'].search(domain):
			checked_lrq = self.check_lrq(lrq)
			broken = checked_lrq[0]
			msg = checked_lrq[1]
			if not broken:  # this is where we check if the rec is broken
				right_count += 1
				if not lrq.learner_id.alternate_id_type:
					tp = 'none'
				else:
					tp = lrq.learner_id.alternate_id_type
				val = {'national_id': lrq.learner_id.learner_identification_id,
					   'person_alternate_id': lrq.learner_id.national_id,
					   'alternate_id_type': id_type_to_code(tp),
					   'qualification_id': lrq.learner_qualification_parent_id.saqa_qual_id,
					   'learner_achievement_status_id': lrq.qual_status,
					   'assessor_registration_number': lrq.assessors_id.assessor_seq_no,
					   'learner_achievement_type_id': '6',  # todo: find or pass flat value 6 is  other
					   'learner_achievement_date': '1900-01-01',  # todo:needs eval based on learner_achievement_type_id
					   'learner_enrolled_date': fix_dates(lrq.start_date),
					   'honours_classification': '',  # not req
					   'part_of': '1',  # only allows 1 or 3/should only be 1 , blanket
					   'learnership_id': '',  # not req
					   'provider_code': lrq.provider_id.id,
					   'provider_etqa_id': '591',  # blanket
					   'assessor_etqa_id': '591',  # blanket
					   'certification_date': fix_dates(lrq.certificate_date),
					   'date_stamp': fix_dates(lrq.certificate_date),
					   'lrq_id': lrq.id,
					   'learner_id': lrq.learner_id.id,
					   }
				dbg(val)
				if global_write:
					self.env['nlrd.29'].create(val)
			else:
				brk_count += 1
				big_daddy += '\n\n' + msg
				dbg(str(lrq.id) + msg)
		dbg(big_daddy)
		dbg('broken:' + str(brk_count))
		dbg('right_count:' + str(right_count))



	def check_person(self, person):
		# checks hr.employee
		broken = False
		msg = str(person.id) + '\n'
		if person.is_learner:
			global_id = person.learner_identification_id
		elif person.is_assessors:
			global_id = person.assessor_moderator_identification_id
		else:
			global_id = person.id
			broken = True
			msg += "person is not an assessor/moderator or learner"
		if not global_id and not person.passport_id and not person.national_id:
			broken = True
			msg += 'no person learner_identification_id or passport_id or national_id \n'
		if not person.alternate_id_type and (person.national_id or person.passport_id):
			broken = True
			msg += 'no person type id but has alt type\n'
		if not person.equity and not person.is_assessors:
			broken = True
			msg += 'no person equity \n'
		if not person.is_assessors and not person.country_id:
			broken = True
			msg += 'no person country id \n'
		if not person.gender_saqa_code:
			broken = True
			msg += 'no person gender saqa code \n'
		if not person.is_assessors and not person.home_language_code:
			broken = True
			msg += 'no person home_language_code \n'
		if not person.citizen_resident_status_code:
			broken = True
			msg += 'no person citizen_resident_status_code \n'
		if not person.socio_economic_status and not person.is_assessors:
			broken = True
			msg += 'no person socio_economic_status \n'
		if not person.is_assessors and not person.dissability:
			broken = True
			msg += 'no person dissability \n'
		if not person.name:
			broken = True
			msg += "no person name \n"
		if not person.person_last_name:
			broken = True
			msg += "no person person_last_name \n"
		if not person.is_assessors and not person.person_birth_date:
			broken = True
			msg += "no person person_birth_date \n"
		if not person.is_assessors and not person.person_home_address_1:
			broken = True
			msg += "no person person_home_address_1 \n"
		if not person.is_assessors and not person.person_home_address_2:
			broken = True
			msg += "no person person_home_address_2 \n"
		if not person.is_assessors and not person.person_home_province_code:
			broken = True
			msg += "no person province \n"
		# if not person.work_province and person.is_assessors: #too strict, not req
		# 	broken = True
		# 	msg += "no assessor work province \n"
		return broken, msg

	def check_provider(self, partner):
		# checks res.partner
		broken = False
		msg = str(partner.id) + '\n'
		if not partner.provider_accreditation_num or partner.provider_accreditation_num == '0':
			broken = True
			msg += 'no provider code \n'
		# always fails???resorting to blanket
		# if not partner.provider_type_id:
		# 	broken = True
		# 	msg += 'no provider type id \n'
		if not partner.name:
			broken = True
			msg += 'no provider name \n'
		# if not partner.province_code_physical.id:#used better handling in prov to code
		# 	broken = True
		# 	msg += 'no provider province \n'
		if not partner.zip_postal:
			broken = True
			msg += 'no provider zip_postal \n'
		# always fails???resorting to blanket
		# if not partner.provider_class_Id:
		# 	broken = True
		# 	msg += 'no provider provider_class_id \n'

		return broken, msg

	@api.multi
	def fetch_nlrd_21(self):
		# domain = [('provider', '=', True), ('provider_status_Id', '!=', 'Expired')]
		domain = [('provider', '=', True)]
		brk_count = 0
		right_count = 0
		big_daddy = ''
		for provider in self.env['res.partner'].search(domain):
			if not provider.postal_address_1:
				post_addy1 = '123 Blom street'
			else:
				post_addy1 = provider.postal_address_1
			if not provider.postal_address_2:
				post_addy2 = 'Pretoria'
			else:
				post_addy2 = provider.postal_address_1
			checked_provider = self.check_provider(provider)
			broken = checked_provider[0]
			msg = checked_provider[1]
			if not broken:  # this is where we check if the rec is broken
				right_count += 1
				eddy = fix_dates(make_up_date(provider.provider_end_date, provider))
				# todo: need to check if the fields im blanking here are not required. probably better to use an int and False handler in the datgen
				val = {'Provider_Code': provider.id,
					   # 'Etqa_Id': provider.provider_etqe_id,  # ensure about blank being allowed
					   'Etqa_Id': '591',  # zz blanket
					   'Std_Industry_Class_Code': provider.provider_sic_code,
					   'Provider_Name': remove_school(strip_string(provider.name)),
					   'Provider_Type_Id': '500',
					   'Provider_Address_1': sanitize_addrs(post_addy1) + ' a',  # zz
					   'Provider_Address_2': sanitize_addrs(post_addy2) + ' a',  # zz
					   'Provider_Address_3': '',
					   'Provider_Postal_Code': cleanse_postcode(provider.zip_postal),
					   'Provider_Phone_Number': provider.phone,
					   'Provider_Fax_Number': provider.fax,
					   'Provider_Sars_Number': '',
					   'Provider_Contact_Name': '',
					   'Provider_Contact_Email_Address': sanitize_email(provider.email),
					   'Provider_Contact_Phone_Number': '',
					   'Provider_Contact_Cell_Number': provider.mobile,
					   'Provider_Accreditation_Num': provider.provider_accreditation_num,
					   'Provider_Accredit_Start_Date': fix_dates(filth_date_gap(provider.provider_start_date,eddy)),
					   'Provider_Accredit_End_Date': eddy,
					   # untested make sure
					   'Etqa_Decision_Number': '',  # blank
					   'Provider_Class_Id': '1',  # blanket
					   'Structure_Status_Id': '510',  # blanket
					   'Province_Code': province_to_code(provider.province_code_physical.id),
					   # maybe change from db id to name or something better
					   'Country_Code': 'ZA',  # blanket ZZ
					   'Latitude_Degree': '',  # blank
					   'Latitude_Minutes': '',  # blank
					   'Latitude_Seconds': '',  # blank
					   'Longitude_Degree': '',  # blank
					   'Longitude_Minutes': '',  # blank
					   'Longitude_Seconds': '',  # blank
					   'Provider_Physical_Address_1': sanitize_addrs(provider.physical_address_1) + ' a',  # zz
					   'Provider_Physical_Address_2': sanitize_addrs(provider.physical_address_2) + ' a',  # zz
					   'Provider_Physical_Address_Town': '',  # blank
					   'Provider_Phys_Address_Postcode': '',  # blank
					   'Provider_Web_Address': '',  # blank
					   'Date_Stamp': fix_dates(provider.write_date),
					   'provider_id': provider.id,
					   }
				# dbg(val)
				if global_write:
					self.env['nlrd.21'].create(val)
			else:
				brk_count += 1
				big_daddy += '\n\n' + msg
				# dbg(str(provider.id) + msg)
		dbg(big_daddy)
		dbg('broken:' + str(brk_count))
		dbg('right_count:' + str(right_count))

	@api.multi
	def fetch_nlrd_26(self):
		domain = [('is_assessors', '=', True)]
		brk_count = 0
		right_count = 0
		big_daddy = ''
		for assessor in self.env['hr.employee'].search(domain):
			checked_assessor = self.check_person(assessor)
			broken = checked_assessor[0]
			msg = checked_assessor[1]
			msg += str(assessor.is_assessors) + ' = is_assessors\n'
			if not broken:  # this is where we check if the rec is broken
				right_count += 1
				if not assessor.alternate_id_type:
					tp = 'none'
				else:
					tp = assessor.alternate_id_type
				val = {'National_Id': assessor.assessor_moderator_identification_id,
					   'Person_Alternate_Id': assessor.national_id,
					   'Alternate_Type_Id': id_type_to_code(tp),
					   'Designation_Id': '1',  # blanket
					   'Designation_Registration_Number': assessor.assessor_seq_no,
					   'Designation_Etqa_Id': '591',  # blanket
					   'Designation_Start_Date': fix_dates(assessor.start_date),
					   'Designation_End_Date': fix_dates(assessor.end_date),
					   'Structure_Status_Id': '501',  # blanket
					   'Etqa_Decision_Number': '',  # blank
					   'Provider_Code': '',
					   'Provider_Etqa_Id': '591',
					   'Date_Stamp': fix_dates(assessor.write_date),
					   'assessor_id': assessor.id,
					   }
				dbg(val)
				if global_write:
					self.env['nlrd.26'].create(val)

			else:
				brk_count += 1
				big_daddy += '\n\n' + msg
				dbg(assessor.id)
				# dbg(str(assessor.is_assessors) + str(assessor.id) + '-' + str(replace_unicode_with_normal(assessor.name)) + msg)
				dbg(str(assessor.is_assessors) + str(assessor.id) + '-' + msg)
		dbg(big_daddy)
		dbg('broken:' + str(brk_count))
		dbg('right_count:' + str(right_count))

	def check_accreditation(self, accreditation):
		broken = False
		msg = str(accreditation.id) + '\n'
		if not accreditation.qualification_id.saqa_qual_id:  # and not accreditation.learnership_id??? and not accreditation.unit standard id???????????
			broken = True
			msg += 'no qual or learnership or units \n'
		if not accreditation.accreditation_qualification_id.accreditation_number:
			broken = True
			msg += 'no accreditation number on accred %s\n' % accreditation.accreditation_qualification_id.id
		if not accreditation.accreditation_qualification_id.related_provider.id:
			broken = True
			msg += 'no accreditation provider on accred %s\n' % accreditation.accreditation_qualification_id.id
		if not accreditation.accreditation_qualification_id.related_provider.provider_start_date:
			broken = True
			msg += 'no start date %s \n' % accreditation.accreditation_qualification_id.related_provider.id
		if not accreditation.accreditation_qualification_id.related_provider.provider_end_date:
			broken = True
			msg += 'no end date %s \n' % accreditation.accreditation_qualification_id.related_provider.id
		return broken, msg

	@api.multi
	def fetch_nlrd_24(self):
		domain = [('accreditation_qualification_id.final_state', '=', 'Approved')]
		brk_count = 0
		right_count = 0
		big_daddy = ''
		for accreditation in self.env['accreditation.qualification'].search(domain):
			checked_accreditation = self.check_accreditation(accreditation)
			broken = checked_accreditation[0]
			msg = checked_accreditation[1]
			stat_code = ''
			if accreditation.accreditation_qualification_id.related_provider.active:
				stat_code = provider_accredit_status_to_code('Active')
			elif not accreditation.accreditation_qualification_id.related_provider.active:
				stat_code = provider_accredit_status_to_code('Inactive')
			if not broken:  # this is where we check if the rec is broken
				right_count += 1
				val = {'Learnership_Id': '',
					   'Qualification_Id': accreditation.qualification_id.saqa_qual_id,
					   'Unit_Standard_Id': '',  # maybe later
					   'Provider_Code': accreditation.accreditation_qualification_id.related_provider.id,
					   'Provider_Etqa_Id': '591',  # blanket
					   'Provider_Accreditation_Num': accreditation.accreditation_qualification_id.accreditation_number,
					   'Provider_Accredit_Assessor_Ind': '',  # blank
					   'Provider_Accred_Start_Date': fix_dates(
						   accreditation.accreditation_qualification_id.related_provider.provider_start_date),
					   'Provider_Accred_End_Date': fix_dates(
						   accreditation.accreditation_qualification_id.related_provider.provider_end_date),
					   'Etqa_Decision_Number': '',  # blank
					   'Provider_Accred_Status_Code': stat_code,
					   'Date_Stamp': fix_dates(accreditation.accreditation_qualification_id.write_date),
					   'accreditation_id': accreditation.id,
					   }
				dbg(val)
				if global_write:
					self.env['nlrd.24'].create(val)
			else:
				brk_count += 1
				big_daddy += '\n\n' + msg
				dbg(accreditation.id)
		dbg(big_daddy)
		dbg('accred  broken:' + str(brk_count))
		dbg('accred right_count:' + str(right_count))

	def check_register(self, register):
		broken = False
		msg = str(register.assessors_moderators_qualification_id.id) + '\n'
		if not register.qualification_id.saqa_qual_id:  # and not accreditation.learnership_id??? and not accreditation.unit standard id???????????
			broken = True
			msg += 'no qual or learnership or units \n'
		if not register.assessors_moderators_qualification_id.existing_assessor_number and not register.assessors_moderators_qualification_id.temp_assessor_seq_no and not register.assessors_moderators_qualification_id.existing_assessor_id:
			broken = True
			msg += 'no assessor number'
		if not register.assessors_moderators_qualification_id.assessor_moderator_register_date:
			broken = True
			msg += 'no register start/registration date \n'
		if not register.assessors_moderators_qualification_id.assessor_moderator_approval_date:
			broken = True
			msg += 'no register end/approval date \n'
		return broken, msg

	@api.multi
	def attach_assessor(self, register):
		msg = ''
		dbg(register.temp_assessor_seq_no)
		dbg(register.existing_assessor_id)
		assessor_object = self.env['hr.employee'].search(
			['|', ('assessor_moderator_identification_id', '=', register.temp_assessor_seq_no),
			 ('assessor_moderator_identification_id', '=', register.existing_assessor_id),
			 ('assessor_moderator_identification_id', '!=', False)])
		if len(assessor_object) > 1:
			msg += 'too many assessors found '
			return False, True, msg
		elif len(assessor_object) == 1:
			if assessor_object.is_active_assessor:
				msg += 'assessor successfully linked but assessor not active'
				return assessor_object, False, msg
			else:
				msg += 'assessor successfully linked'
				return assessor_object, False, msg
		else:
			msg += 'assessor not found'
			return False, True, msg

	@api.multi
	def fetch_nlrd_27(self):
		domain = [('assessors_moderators_qualification_id.final_state', '=', 'Approved'),
				  ('assessors_moderators_qualification_id.assessor_moderator', '=', 'assessor')]
		brk_count = 0
		right_count = 0
		big_daddy = ''
		for register in self.env['assessors.moderators.qualification'].search(domain):
			# this is way too hungry, never use, keeping for the note
			# assessor_object = self.env['hr.employee'].search(['|',('assessor_moderator_identification_id', '=', register.temp_assessor_seq_no),('assessor_moderator_identification_id', '=', register.existing_assessor_id),('is_active_assessor','=',True)])
			# if not assessor_object:
			# 	dbg('problem' + str(register.id))
			# else:
			# 	dbg('lakka')
			checked_register = self.check_register(register)
			broken = checked_register[0]
			msg = checked_register[1]
			reg_num = ''
			if register.assessors_moderators_qualification_id.temp_assessor_seq_no:
				reg_num = register.assessors_moderators_qualification_id.temp_assessor_seq_no
			elif register.assessors_moderators_qualification_id.existing_assessor_number:
				reg_num = register.assessors_moderators_qualification_id.existing_assessor_number
			elif register.assessors_moderators_qualification_id.existing_assessor_id:
				reg_num = register.assessors_moderators_qualification_id.existing_assessor_id
			registration = register.assessors_moderators_qualification_id
			attached_assessor = self.attach_assessor(registration)
			assessor_obj = attached_assessor[0]
			if assessor_obj:
				assessor_id = assessor_obj.id
			else:
				assessor_id = False
			link_broken = attached_assessor[1]
			assessor_msg = attached_assessor[2]
			if not broken:  # this is where we check if the rec is broken
				right_count += 1
				val = {'Learnership_Id': '',
					   'Qualification_Id': register.qualification_id.saqa_qual_id,
					   'Unit_Standard_Id': '',
					   'Designation_Id': '501',  # blanket req
					   'Designation_Registration_Number': reg_num,  # req
					   'Designation_Etqa_Id': '591',  # req blanket
					   'Nqf_Designation_Start_Date': fix_dates(
						   register.assessors_moderators_qualification_id.assessor_moderator_register_date),  # req
					   'Nqf_Designation_End_Date': fix_dates(
						   register.assessors_moderators_qualification_id.assessor_moderator_approval_date),  # req
					   'Etqa_Decision_Number': '',
					   'Nqf_Desig_Status_Code': 'A',  # req
					   'Date_Stamp': fix_dates(register.write_date),  # req
					   'register_id': register.id,
					   'person_id': assessor_id,
					   'stat_msg': assessor_msg,
					   'link_broken': link_broken
					   }  # req
				# dbg(val)
				dbg(assessor_msg)
				if global_write:
					self.env['nlrd.27'].create(val)
			else:
				brk_count += 1
				big_daddy += '\n\n' + msg
				dbg(register.id)
		dbg(big_daddy)
		dbg('accred  broken:' + str(brk_count))
		dbg('accred right_count:' + str(right_count))

	def check_25(self, person, l_or_a, stat_dict):
		broken = False
		msg = ''
		if l_or_a == 'a':
			msg = str(person.id) + '\n'
			if not person.assessor_id.assessor_moderator_identification_id and not person.National_Id:
				broken = True
				msg += 'assessor has no national id \n'
				stat_dict['assessor_moderator_identification_id'] += 1
			if not person.assessor_id.equity:
				broken = True
				msg += 'assessor has no equity \n'
				stat_dict['equity'] += 1
			# if not person.assessor_id.alternate_id_type:
			# 	broken = True
			# 	msg += 'assessor has no alternate_id_type \n'
			# 	stat_dict['alternate_id_type'] += 1
			if not person.assessor_id.country_id:
				broken = True
				msg += 'assessor has no country \n'
				stat_dict['country_id'] += 1
			if not person.assessor_id.home_language_code:
				broken = True
				msg += 'assessor has no home_language_code \n'
				stat_dict['home_language_code'] += 1
			if not person.assessor_id.gender:
				broken = True
				msg += 'assessor has no gender \n'
				stat_dict['gender'] += 1
			if not person.assessor_id.citizen_resident_status_code:
				broken = True
				msg += 'assessor has no citizen_resident_status_code \n'
				stat_dict['citizen_resident_status_code'] += 1
			if not person.assessor_id.socio_economic_status:
				broken = True
				msg += 'assessor has no socio_economic_status \n'
				stat_dict['socio_economic_status'] += 1
			if not person.assessor_id.disability_status:
				broken = True
				msg += 'assessor has no disability_status \n'
				stat_dict['disability_status'] += 1
			if not person.assessor_id.name:
				broken = True
				msg += 'assessor has no name \n'
				stat_dict['name'] += 1
			if not person.assessor_id.person_last_name:
				broken = True
				msg += 'assessor has no person_last_name \n'
				stat_dict['person_last_name'] += 1
			if not person.assessor_id.person_birth_date:
				broken = True
				msg += 'assessor has no person_birth_date \n'
				stat_dict['person_birth_date'] += 1
			if not person.assessor_id.person_home_province_code:
				broken = True
				msg += 'assessor has no person_home_province_code \n'
				stat_dict['person_home_province_code'] += 1
			dbg(msg)
		if l_or_a == 'l':
			person = person.lrq_id.learner_id
			msg = str(person.id) + '\n'
			if not person.learner_identification_id and not person.national_id:
				broken = True
				msg += 'learner has no national id \n'
				stat_dict['identification_id'] += 1
			if not person.equity:
				broken = True
				msg += 'learner has no equity \n'
				stat_dict['equity'] += 1
			# if not person.alternate_id_type:
			# 	broken = True
			# 	msg += 'learner has no alternate_id_type \n'
			# 	stat_dict['alternate_id_type'] += 1
			if not person.country_id:
				broken = True
				msg += 'learner has no country \n'
				stat_dict['country_id'] += 1
			if not person.home_language_code:
				broken = True
				msg += 'learner has no home_language_code \n'
				stat_dict['home_language_code'] += 1
			if not person.gender:
				broken = True
				msg += 'learner has no gender \n'
				stat_dict['gender'] += 1
			if not person.citizen_resident_status_code:
				broken = True
				msg += 'learner has no citizen_resident_status_code \n'
				stat_dict['citizen_resident_status_code'] += 1
			if not person.socio_economic_status:
				broken = True
				msg += 'learner has no socio_economic_status \n'
				stat_dict['socio_economic_status'] += 1
			if not person.disability_status:
				broken = True
				msg += 'learner has no disability_status \n'
				stat_dict['disability_status'] += 1
			if not person.name:
				broken = True
				msg += 'learner has no name \n'
				stat_dict['name'] += 1
			if not person.person_last_name:
				broken = True
				msg += 'learner has no person_last_name \n'
				stat_dict['person_last_name'] += 1
			if not person.person_birth_date:
				broken = True
				msg += 'learner has no person_birth_date \n'
				stat_dict['person_birth_date'] += 1
			if not person.person_home_province_code:
				broken = True
				msg += 'learner has no person_home_province_code \n'
				stat_dict['person_home_province_code'] += 1
			dbg(msg)
		return broken, msg, stat_dict

	@api.multi
	def fetch_nlrd_25(self):
		domain = []
		brk_count = 0
		right_count = 0
		big_daddy = ''
		unq_learner_ids = []
		unq_lrq_ids = []
		assessor_stat_dict = {
			'assessor_moderator_identification_id': 0,
			'alternate_id_type': 0,
			'equity': 0,
			'country_id': 0,
			'home_language_code': 0,
			'gender': 0,
			'citizen_resident_status_code': 0,
			'socio_economic_status': 0,
			'disability_status': 0,
			'name': 0,
			'person_last_name': 0,
			'person_birth_date': 0,
			'person_home_province_code': 0,
		}

		for assessor in self.env['nlrd.26'].search(domain):
			# dbg(assessor.read())
			checked_assessor = self.check_25(assessor, 'a', assessor_stat_dict)
			broken = checked_assessor[0]
			msg = checked_assessor[1]
			if not broken:  # this is where we check if the rec is broken
				right_count += 1
				dbg(assessor.assessor_id.country_id.name)
				if not assessor.assessor_id.alternate_id_type:
					tp = 'none'
				else:
					tp = assessor.assessor_id.alternate_id_type
				val = {'National_Id': assessor.assessor_id.assessor_moderator_identification_id or assessor.National_Id,
					   # c
					   'Person_Alternate_Id': assessor.Person_Alternate_Id,  # c
					   'Alternate_Id_Type': id_type_to_code(tp),  # req
					   'Equity_Code': equity_to_code(assessor.assessor_id.equity),  # y
					   'Nationality_Code': nationality_to_code(assessor.assessor_id.country_id.name),  # y
					   'Home_Language_Code': lang_to_code(assessor.assessor_id.home_language_code.name),  # y
					   'Gender_Code': gender_to_code(assessor.assessor_id.gender),  # y
					   'Citizen_Resident_Status_Code': assessor.assessor_id.citizen_resident_status_code,
					   # y probably needs dict def
					   'Socioeconomic_Status_Code': socio_to_code(assessor.assessor_id.socio_economic_status),  # y
					   'Disability_Status_Code': disability_status_code(assessor.assessor_id.disability_status),  # y probably needs dict def
					   # 'Person_First_Name': replace_unicode_with_normal(assessor.assessor_id.name),  # y the unicode dict is killing me
					   'Person_First_Name': assessor.assessor_id.name,  # y
					   # 'Person_Last_Name': replace_unicode_with_normal(assessor.assessor_id.person_last_name),  # y
					   'Person_Last_Name': assessor.assessor_id.person_last_name,  # y
					   'Person_Middle_Name': '',
					   'Person_Title': '',
					   'Person_Birth_Date': fix_dates(assessor.assessor_id.person_birth_date),
					   'Person_Home_Address_1': '',
					   'Person_Home_Address_2': '',
					   'Person_Home_Address_3': '',
					   'Person_Postal_Address_1': '',
					   'Person_Postal_Address_2': '',
					   'Person_Postal_Address_3': '',
					   'Person_Home_Addr_Postal_Code': '',
					   'Person_Postal_Addr_Post_Code': '',
					   'Person_Phone_Number': '',
					   'Person_Cell_Phone_Number': '',
					   'Person_Fax_Number': '',
					   'Person_Email_Address': '',
					   'Province_Code': province_to_code(assessor.assessor_id.person_home_province_code.id),  # y
					   'Provider_Code': '',  # c
					   'Provider_Etqa_Id': '591',  # c blanket
					   'Person_Previous_Alternate_Id': '',
					   'Person_Previous_Provider_Code': '',
					   'Person_Previous_Alternate_Id_Type': '',  # c
					   'Person_Previous_Provider_Lastname': '',  # c
					   'Person_Previous_Provider_Etqe_Id': '',  # c
					   'Seeing_Rating_Id': '',
					   'Hearing_Rating_Id': '',
					   'Communicating_Rating_Id': '',
					   'Remembering_Rating_Id': '',
					   'Self_Care_Rating_Id': '',
					   'Date_Stamp': fix_dates(assessor.assessor_id.write_date),  # y
					   'person_id': assessor.assessor_id.id,  # y
					   }
				# dbg(val)
				if global_write:
					dbg(assessor)
					person = self.env['nlrd.25'].create(val)
					assessor.write({'person_id': person.id})
			else:
				brk_count += 1
				big_daddy += '\n\n' + msg
				dbg(assessor.id)
		learner_stat_dict = {
			'identification_id': 0,
			'alternate_id_type': 0,
			'equity': 0,
			'country_id': 0,
			'home_language_code': 0,
			'gender': 0,
			'citizen_resident_status_code': 0,
			'socio_economic_status': 0,
			'disability_status': 0,
			'name': 0,
			'person_last_name': 0,
			'person_birth_date': 0,
			'person_home_province_code': 0,
		}
		# deduplicates lrq by unique learner
		for learner in self.env['nlrd.29'].search(domain):
			if learner.lrq_id.learner_id.id not in unq_learner_ids:
				unq_learner_ids.append(learner.lrq_id.learner_id.id)
				unq_lrq_ids.append(learner.lrq_id.id)
		dbg(unq_lrq_ids)
		dbg(unq_learner_ids)
		for lrq in self.env['nlrd.29'].search([('id', 'in', unq_lrq_ids)]):
			checked_lrq = self.check_25(lrq, 'l', learner_stat_dict)
			learner = lrq.lrq_id.learner_id
			broken = checked_lrq[0]
			msg = checked_lrq[1]
			if not broken:  # this is where we check if the rec is broken
				right_count += 1
				if not learner.alternate_id_type:
					tp = 'none'
				else:
					tp = learner.alternate_id_type
				val = {'National_Id': learner.identification_id or lrq.national_id,  # c
					   'Person_Alternate_Id': learner.national_id,  # c
					   'Alternate_Id_Type': id_type_to_code(tp),  # req
					   'Equity_Code': equity_to_code(learner.equity),  # y
					   'Nationality_Code': nationality_to_code(learner.country_id.name),  # y
					   'Home_Language_Code': lang_to_code(learner.home_language_code.name),  # y
					   'Gender_Code': gender_to_code(learner.gender),  # y
					   'Citizen_Resident_Status_Code': learner.citizen_resident_status_code,
					   # y probably needs dict def
					   'Socioeconomic_Status_Code': socio_to_code(learner.socio_economic_status),  # y
					   'Disability_Status_Code': disability_status_code(learner.disability_status),  # y probably needs dict def
					   # 'Person_First_Name': replace_unicode_with_normal(learner.name),  # y
					   'Person_First_Name': learner.name,  # y
					   # 'Person_Last_Name': replace_unicode_with_normal(learner.person_last_name),  # y
					   'Person_Last_Name': learner.person_last_name,  # y
					   'Person_Middle_Name': '',
					   'Person_Title': '',
					   'Person_Birth_Date': fix_dates(learner.person_birth_date),
					   'Person_Home_Address_1': '',
					   'Person_Home_Address_2': '',
					   'Person_Home_Address_3': '',
					   'Person_Postal_Address_1': '',
					   'Person_Postal_Address_2': '',
					   'Person_Postal_Address_3': '',
					   'Person_Home_Addr_Postal_Code': '',
					   'Person_Postal_Addr_Post_Code': '',
					   'Person_Phone_Number': '',
					   'Person_Cell_Phone_Number': '',
					   'Person_Fax_Number': '',
					   'Person_Email_Address': '',
					   'Province_Code': province_to_code(learner.person_home_province_code.id),  # y
					   'Provider_Code': '',  # c
					   'Provider_Etqa_Id': '591',  # c blanket
					   'Person_Previous_Alternate_Id': '',
					   'Person_Previous_Provider_Code': '',
					   'Person_Previous_Alternate_Id_Type': '',  # c
					   'Person_Previous_Provider_Lastname': '',  # c
					   'Person_Previous_Provider_Etqe_Id': '',  # c
					   'Seeing_Rating_Id': '',
					   'Hearing_Rating_Id': '',
					   'Communicating_Rating_Id': '',
					   'Walking_Rating_Id': '',
					   'Remembering_Rating_Id': '',
					   'Self_Care_Rating_Id': '',
					   'Date_Stamp': fix_dates(learner.write_date),  # y
					   'person_id': learner.id,
					   }
				# dbg(val)
				if global_write:
					dbg(learner)
					person = self.env['nlrd.25'].create(val)
					lrq.write({'person_id': person.id})
			else:
				brk_count += 1
				big_daddy += '\n\n' + msg
				dbg(learner.id)
		# dbg(big_daddy)
		dbg('person  broken:' + str(brk_count))
		dbg('person right_count:' + str(right_count))
		dbg(assessor_stat_dict)
		dbg(learner_stat_dict)

	# @api.multi
	# def link_lnr_from_25_to_lrq(self):

	@api.multi
	def inverse_check(self):
		lrqs_removed = 0
		assessors_removed = 0
		for lrq in self.env['nlrd.29'].search([('person_id', '!=', False)]):
			lrq.unlink()
			lrqs_removed += 1
		for assessor in self.env['nlrd.26'].search([('person_id', '!=', False)]):
			assessor.unlink()
			assessors_removed += 1
		dbg('lrq removed' + str(lrqs_removed))
		dbg('assessor removed' + str(assessors_removed))

	# @api.multi
	# def inverse_check(self):
	# 	lrqs_removed = 0
	# 	assessors_removed = 0
	# 	for lnr in self.env['nlrd.25'].search([]):  # links the file 25
	# 		lrq_rec = self.env['nlrd.29'].search([('learner_id', '=', lnr.person_id.id)])
	# 		lrq_rec.write({'person_id': lnr.id, 'stat_msg': 'successfully linked to 25'})
	# 	for lrq in self.env['nlrd.29'].search([('person_id', '=', False)]):  # marks as broken on non linked
	# 		msg = 'lrq has no linkable learner'
	# 		lrq.write({'stat_msg': msg, 'link_broken': True})
	# 		lrqs_removed += 1
	# 	for assessor in self.env['nlrd.26'].search([('person_id', '=', False)]):
	# 		# assessor.unlink()
	# 		msg = 'lrq has no linkable assessor'
	# 		assessor.write({'stat_msg': msg, 'link_broken': True})
	# 		assessors_removed += 1
	# 	dbg('lrq removed' + str(lrqs_removed))
	# 	dbg('assessor removed' + str(assessors_removed))

	@api.multi
	def unlink_all(self):
		for x in self.env['nlrd.21'].search([]):
			x.unlink()
		for x in self.env['nlrd.24'].search([]):
			x.unlink()
		for x in self.env['nlrd.25'].search([]):
			x.unlink()
		for x in self.env['nlrd.26'].search([]):
			x.unlink()
		for x in self.env['nlrd.27'].search([]):
			x.unlink()
		for x in self.env['nlrd.29'].search([]):
			x.unlink()

	@api.multi
	def gen_dats(self, num, map):
		model_name = 'nlrd.' + num
		# for x in self.env[model_name].search([('link_broken','=',False)]):
		for x in self.env[model_name].search([]):
			p_dict = x.read()[0]
			if num == '25':  # removes odoo m2o for person in file 25
				del p_dict['person_id']
			if num == '21':  # removes odoo m2o for provider in file 21
				del p_dict['provider_id']
			del p_dict['display_name']
			del p_dict['id']
			del p_dict['create_date']
			del p_dict['create_uid']
			del p_dict['write_uid']
			del p_dict['write_date']
			del p_dict['__last_update']
			dbg(p_dict)
			# gendat(OD(p_dict),map ,re.sub('.','_',model_name) + "_nlrd.dat")
			gendat(OD(p_dict), map[0], map[1], dat_names[num])

	@api.multi
	def gen_21(self):
		for x in self.env['nlrd.21'].search([]):
			p_dict = x.read()[0]
			del p_dict['provider_id']
			del p_dict['display_name']
			del p_dict['id']
			del p_dict['create_date']
			del p_dict['create_uid']
			del p_dict['write_uid']
			del p_dict['write_date']
			del p_dict['__last_update']
			# gendat(p_dict, [7, 5, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40], "_nlrd.dat")
			gendat(OD(p_dict), dat21[0], dat21[1], "21_nlrd.dat")

	@api.multi
	def gen_25(self):
		for x in self.env['nlrd.25'].search([]):
			p_dict = x.read()[0]
			del p_dict['person_id']
			del p_dict['display_name']
			del p_dict['id']
			del p_dict['create_date']
			del p_dict['create_uid']
			del p_dict['write_uid']
			del p_dict['write_date']
			del p_dict['__last_update']
			# gendat(p_dict, [7, 5, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40], "_nlrd.dat")
			dbg(p_dict)
			gendat(OD(p_dict), dat25[0], dat25[1], "25_nlrd.dat")

	@api.multi
	def gen_all_dats(self):
		num_dict = {'21': dat21,
					'24': dat24,
					'26': dat26,
					'27': dat27,
					'29': dat29,
					'25': dat25}
		for x, y in num_dict.items():
			dbg(x)
			self.gen_dats(x, y)

	@api.multi
	def do_all(self):
		self.fetch_nlrd_21()
		self.fetch_nlrd_24()
		self.fetch_nlrd_26()
		self.fetch_nlrd_27()
		self.fetch_nlrd_29()
		self.fetch_nlrd_25()
		self.inverse_check()
		self.gen_all_dats()


	@api.multi
	def diff_29_pid(self):
		# msg = ''
		# prov_nums = []
		# add_nums = []
		# diff = []
		# for prov in self.env['nlrd.21'].search([]):
		# 	if prov.Provider_Code not in prov_nums:
		# 		add_nums.append(prov.Provider_Code)
		# for lrq in self.env['nlrd.29'].search([]):
		# 	if lrq.provider_code not in prov_nums:
		# 		prov_nums.append(lrq.provider_code)
		# for x in prov_nums:
		# 	if x not in add_nums:
		# 		diff.append(x)
		# msg += str(add_nums) + '\n'
		# msg += str(prov_nums) + '\n'
		# msg += str(diff) + '\n'
		# -------------------------------------------------------
		prov_nums = []
		del_nums = []
		diff = []
		msg = ''
		for lrq in self.env['nlrd.29'].search([]):
			if lrq.provider_code not in prov_nums:
				prov_nums.append(lrq.provider_code)
		prov_del_count = 0
		prov_keep = 0
		orgininal_prov_count = len(self.env['nlrd.21'].search([]))
		for prov in self.env['nlrd.21'].search([]):
			if prov.Provider_Code not in prov_nums:
				del_nums.append(prov.Provider_Code)
				# prov.unlink()
				prov_del_count += 1
			else:
				diff.append(prov.Provider_Code)
				prov_keep += 1
		msg += 'keep providers count: ' + str(prov_keep) + '\n'
		msg += 'original providers count: ' + str(orgininal_prov_count) + '\n'
		msg += 'unq providers: ' + str(len(prov_nums)) + '\n'
		msg += 'deleted provs :' + str(prov_del_count) + '\n'
		msg += 'del providers: ' + str(del_nums) + '\n'
		msg += 'diff providers: ' + str(len(del_nums)) + '\n'
		msg += 'diff providers: ' + str(del_nums)+ '\n'
		# -----------------------------------------------------------------------
		# prov_nums = []
		# add_nums = []
		# diff = []
		# for prov in self.env['nlrd.21'].search([]):
		# 	if prov.Provider_Code not in prov_nums:
		# 		add_nums.append(prov.Provider_Code)
		# for lrq in self.env['nlrd.29'].search([]):
		# 	if lrq.provider_code not in prov_nums:
		# 		prov_nums.append(lrq.provider_code)
		# for x in prov_nums:
		# 	if x not in add_nums:
		# 		diff.append(x)
		# raise Warning(len(diff))
		raise Warning(msg)

	@api.multi
	def del_extra_provs(self):
		prov_nums = []
		del_nums = []
		diff = []
		msg = ''
		for lrq in self.env['nlrd.29'].search([]):
			if lrq.provider_code not in prov_nums:
				prov_nums.append(lrq.provider_code)
		prov_del_count = 0
		prov_keep = 0
		for prov in self.env['nlrd.21'].search([]):
			if prov.Provider_Code not in prov_nums:
				del_nums.append(prov.Provider_Code)
				# prov.unlink()
				prov_del_count += 1
			else:
				diff.append(prov.Provider_Code)
				prov_keep += 1
		for prov in del_nums:
			del_guy = self.env['nlrd.21'].search([('Provider_Code','=',prov)])
			dbg(prov)
			del_guy.unlink()

class nlrd_report(models.Model):
	_name = 'nlrd.report'

	name = fields.Char()
	nlrd_21_id = fields.Many2one('nlrd.21')
	nlrd_24_id = fields.Many2one('nlrd.24')
	nlrd_25_id = fields.Many2one('nlrd.25')
	nlrd_26_id = fields.Many2one('nlrd.26')
	nlrd_27_id = fields.Many2one('nlrd.27')
	nlrd_29_id = fields.Many2one('nlrd.29')
	doc_model = fields.Char()
	doc_id = fields.Char()
	message = fields.Text()

class nlrd_29(models.Model):
	_name = 'nlrd.29'

	"""

	1. The unique identifier used here must be the same as that used for the person information record to ensure that the two structures can be properly linked together when the data is loaded.  In other words, the combination National_ID, Person_Alternate_Id and Alternative_Id_Type (Provider_Code and Provider_ETQA_ID if a student number) must exist in the person information file.
	See the notes about these identifiers for Person Information.

	2. The combination National_Id, Person_Alternate_Id, Alternative_Id_Type and Qualification_Id must be unique.

	3. If an Assessor_Registration_Number is provided and the Assessor_ETQA_ID is the same as the submitting ETQA’s ID then the Assessor_Registration_Number must exist in the Person Designation file with a Designation_Id that represents Designation = Assessor.
	4. Part_of may only have a value of 1 or 3 where:
	1 = Miscellanous stand-alone
	3 = (Part of a) Learnership

	5. If Part_of has a value of 3 then a valid Learnership_Id must be supplied.

	6.     6. Learner_Achievement_Date is only required if Learner_Achievement_Status_Id =2 or 29 (i.e. Achieved or Achieved and Not Entitled to Practise).  It is not allowed if Learner_Achievement_Status_Id=3 (i.e. Enrolled).  For all other statuses, it is optional.  If the exact achievement date is not known, 1 December of the particular year is acceptable.  Minimum: 19000101.  Maximum: Now.

	7. The Date Stamp should be the date on which the record was last updated, not the date on which it was extracted.  If, however, this date is not recorded in the source data, please make the Date Stamp equal to the Learner Achievement Date.  (This will assist in not overwriting more recent biographical learner data if the legacy achievements are received in non-chronological order).

	8. Minimum: 19000101.  Maximum: Now. Must not be greater than Learner_Achievement_Date.

	9. The Qualification ID must be one for which the ETQA is itself accredited.  Thus, it cannot be the ID of a generic qualification, as ETQAs are not accredited for generic qualifications but rather for the learning programmes recorded against them.  .  (Alternatively, it must be a Qualification ID obtained via the submission of File 22.)

	10. The certification date is the date on which the qualification was certificated.
	"""

	national_id = fields.Char()
	person_alternate_id = fields.Char()
	alternate_id_type = fields.Char()
	qualification_id = fields.Char()
	learner_achievement_status_id = fields.Char()
	assessor_registration_number = fields.Char()
	learner_achievement_type_id = fields.Char()
	learner_achievement_date = fields.Char()
	learner_enrolled_date = fields.Char()
	honours_classification = fields.Char()
	part_of = fields.Char()
	learnership_id = fields.Char()
	provider_code = fields.Char()
	provider_etqa_id = fields.Char()
	assessor_etqa_id = fields.Char()
	certification_date = fields.Char()
	date_stamp = fields.Char()
	learner_id = fields.Many2one('hr.employee')
	assessors_id = fields.Many2one('hr.employee')
	lrq_id = fields.Many2one('learner.registration.qualification')
	person_id = fields.Many2one('nlrd.25')
	link_broken = fields.Boolean()
	broken = fields.Boolean()
	stat_msg = fields.Text()


class nlrd_21(models.Model):
	_name = 'nlrd.21'

	Provider_Code = fields.Char()
	Etqa_Id = fields.Char()
	Std_Industry_Class_Code = fields.Char()
	Provider_Name = fields.Char()
	Provider_Type_Id = fields.Char()
	Provider_Address_1 = fields.Char()
	Provider_Address_2 = fields.Char()
	Provider_Address_3 = fields.Char()
	Provider_Postal_Code = fields.Char()
	Provider_Phone_Number = fields.Char()
	Provider_Fax_Number = fields.Char()
	Provider_Sars_Number = fields.Char()
	Provider_Contact_Name = fields.Char()
	Provider_Contact_Email_Address = fields.Char()
	Provider_Contact_Phone_Number = fields.Char()
	Provider_Contact_Cell_Number = fields.Char()
	Provider_Accreditation_Num = fields.Char()
	Provider_Accredit_Start_Date = fields.Char()
	Provider_Accredit_End_Date = fields.Char()
	Etqa_Decision_Number = fields.Char()
	Provider_Class_Id = fields.Char()
	Structure_Status_Id = fields.Char()
	Province_Code = fields.Char()
	Country_Code = fields.Char()
	Latitude_Degree = fields.Char()
	Latitude_Minutes = fields.Char()
	Latitude_Seconds = fields.Char()
	Longitude_Degree = fields.Char()
	Longitude_Minutes = fields.Char()
	Longitude_Seconds = fields.Char()
	Provider_Physical_Address_1 = fields.Char()
	Provider_Physical_Address_2 = fields.Char()
	Provider_Physical_Address_Town = fields.Char()
	Provider_Phys_Address_Postcode = fields.Char()
	Provider_Web_Address = fields.Char()
	Date_Stamp = fields.Char()
	provider_id = fields.Many2one('res.partner')
	link_broken = fields.Boolean()
	broken = fields.Boolean()
	stat_msg = fields.Text()


class nlrd_24(models.Model):
	_name = 'nlrd.24'

	Learnership_Id = fields.Char()
	Qualification_Id = fields.Char()
	Unit_Standard_Id = fields.Char()
	Provider_Code = fields.Char()
	Provider_Etqa_Id = fields.Char()
	Provider_Accreditation_Num = fields.Char()
	Provider_Accredit_Assessor_Ind = fields.Char()
	Provider_Accred_Start_Date = fields.Char()
	Provider_Accred_End_Date = fields.Char()
	Etqa_Decision_Number = fields.Char()
	Provider_Accred_Status_Code = fields.Char()
	Date_Stamp = fields.Char()
	accreditation_id = fields.Many2one('provider.master.qualification')
	link_broken = fields.Boolean()
	broken = fields.Boolean()
	stat_msg = fields.Text()


class nlrd_25(models.Model):
	_name = 'nlrd.25'

	National_Id = fields.Char()
	Person_Alternate_Id = fields.Char()
	Alternate_Id_Type = fields.Char()
	Equity_Code = fields.Char()
	Nationality_Code = fields.Char()
	Home_Language_Code = fields.Char()
	Gender_Code = fields.Char()
	Citizen_Resident_Status_Code = fields.Char()
	Socioeconomic_Status_Code = fields.Char()
	Disability_Status_Code = fields.Char()
	Person_First_Name = fields.Char()
	Person_Last_Name = fields.Char()
	Person_Middle_Name = fields.Char()
	Person_Title = fields.Char()
	Person_Birth_Date = fields.Char()
	Person_Home_Address_1 = fields.Char()
	Person_Home_Address_2 = fields.Char()
	Person_Home_Address_3 = fields.Char()
	Person_Postal_Address_1 = fields.Char()
	Person_Postal_Address_2 = fields.Char()
	Person_Postal_Address_3 = fields.Char()
	Person_Home_Addr_Postal_Code = fields.Char()
	Person_Postal_Addr_Post_Code = fields.Char()
	Person_Phone_Number = fields.Char()
	Person_Cell_Phone_Number = fields.Char()
	Person_Fax_Number = fields.Char()
	Person_Email_Address = fields.Char()
	Province_Code = fields.Char()
	Provider_Code = fields.Char()
	Provider_Etqa_Id = fields.Char()
	Person_Previous_Provider_Lastname = fields.Char()
	Person_Previous_Alternate_Id = fields.Char()
	Person_Previous_Alternate_Id_Type = fields.Char()
	Person_Previous_Provider_Code = fields.Char()
	Person_Previous_Provider_Etqe_Id = fields.Char()
	Seeing_Rating_Id = fields.Char()
	Hearing_Rating_Id = fields.Char()
	Communicating_Rating_Id = fields.Char()
	Walking_Rating_Id = fields.Char()
	Remembering_Rating_Id = fields.Char()
	Self_Care_Rating_Id = fields.Char()
	Date_Stamp = fields.Char()
	person_id = fields.Many2one('hr.employee')
	broken = fields.Boolean()
	link_broken = fields.Boolean()
	stat_msg = fields.Text()


class nlrd_26(models.Model):
	_name = 'nlrd.26'

	National_Id = fields.Char()
	Person_Alternate_Id = fields.Char()
	Alternate_Type_Id = fields.Char()
	Designation_Id = fields.Char()
	Designation_Registration_Number = fields.Char()
	Designation_Etqa_Id = fields.Char()
	Designation_Start_Date = fields.Char()
	Designation_End_Date = fields.Char()
	Structure_Status_Id = fields.Char()
	Etqa_Decision_Number = fields.Char()
	Provider_Code = fields.Char()
	Provider_Etqa_Id = fields.Char()
	Date_Stamp = fields.Char()
	assessor_id = fields.Many2one('hr.employee')
	person_id = fields.Many2one('nlrd.25')
	link_broken = fields.Boolean()
	broken = fields.Boolean()
	stat_msg = fields.Text()


class nlrd_27(models.Model):
	_name = 'nlrd.27'

	Learnership_Id = fields.Char()
	Qualification_Id = fields.Char()
	Unit_Standard_Id = fields.Char()
	Designation_Id = fields.Char()
	Designation_Registration_Number = fields.Char()
	Designation_Etqa_Id = fields.Char()
	Nqf_Designation_Start_Date = fields.Char()
	Nqf_Designation_End_Date = fields.Char()
	Etqa_Decision_Number = fields.Char()
	Nqf_Desig_Status_Code = fields.Char()
	Date_Stamp = fields.Char()
	register_id = fields.Many2one('assessors.moderators.qualification.hr')
	person_id = fields.Many2one('hr.employee')
	broken = fields.Boolean()
	link_broken = fields.Boolean()
	stat_msg = fields.Text()