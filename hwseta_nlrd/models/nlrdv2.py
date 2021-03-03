# coding=utf-8
from openerp import models, fields, tools, api, _
from datetime import datetime
import re
from collections import OrderedDict as OD
from nlrd_dat import gendat, dat21, dat24, dat25, dat26, dat27, dat29
from nlrd_fixes import *

BEBUG = True

if BEBUG:
	import logging

	logger = logging.getLogger(__name__)


	def bbg(msg):
		logger.info(msg)
else:
	def bbg(msg):
		pass

DEBUG = False

if DEBUG:
	import logging

	logger = logging.getLogger(__name__)


	def dbg(msg):
		logger.info(msg)
else:
	def dbg(msg):
		pass

LOGIT = True

# global_write = False
global_write = True



class nlrd_exporter(models.TransientModel):
	_name = 'nlrd.exporter2'


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
		# os.chdir("/var/log/odoo")
		# os.remove("dats.tar")
		# os.system("tar cvf dats.tar *.dat")
		# dbg("DILLMAN:"+str(os.getcwd()))
		# os.remove("*.dat")

	def logit(self, doc_id, doc_model, msg):
		if LOGIT:
			name = str(doc_model) + ',' + str(doc_id) + ',' + str(msg)
			values = {'name': name,'doc_id': doc_id, 'doc_model': doc_model, 'message': msg}
			self.env['nlrd.report'].create(values)

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
	def purge_dupe_lrq(self):
		unq_lnrs = []
		# build unq learners
		for x in self.env['nlrd.29'].search([('national_id','!=','')]):
			if x.national_id not in unq_lnrs:
				unq_lnrs.append(x.national_id)
		# find all duplicated learners by unq learner nat id
		for unq_lnr in unq_lnrs:
			bbg(unq_lnr)
			bunch_29 = self.env['nlrd.29'].search([('national_id','=',unq_lnr)])
			qual_dict = {}
			lnr_qual_list = []
			# find all bunches of odoo lrqs with a matching learner and qual id
			for lrq in bunch_29:
				bbg(lrq)
				# build up a list of lrqs per bunch of matches
				if lrq.qualification_id not in lnr_qual_list:
					lnr_qual_list.append(lrq.qualification_id)
				match = self.env['nlrd.29'].search([('national_id','=',unq_lnr),('qualification_id','in',lnr_qual_list)])
				# check if we have more than one match of learner and qual
				# also check if we have a cert num and is ach and is competent
				if len(match) > 1:
					full_competent = True
					full_ach = True
					full_cert = True
					lrq_match_list = []
					# set a match flag if all ticks are right
					for matcher in match:
						if not matcher.lrq_id.is_learner_achieved:
							full_competent = False
						if not matcher.lrq_id.is_complete:
							full_ach = False
						if not matcher.lrq_id.certificate_no:
							full_cert = False
						# append all matches that are ticked
						lrq_match_list.append(matcher.lrq_id.id)
					# check if all flags are ticked
					if full_cert and full_competent and full_ach:
						bbg(lrq_match_list)
						# get the latest
						mx_guy = max(lrq_match_list)
						# remove the lates so we dont delete it
						lrq_match_list.remove(mx_guy)
						# loop through the ones we want to unlink
						for remover in lrq_match_list:
							# set an odoo obj
							remover_obj = self.env['learner.registration.qualification'].search([('id','=',remover)])
							# you know what this is
							# todo: uncomment for live run
							remover_obj.unlink()
							bbg('dropping true duplicates:' + str(remover_obj))
						# raise Warning('full true issue' + str(mx_guy))

	@api.multi
	def purge_dupe_lrq_foreign(self):
		unq_lnrs = []
		# build unq learners
		for x in self.env['nlrd.29'].search([('person_alternate_id', '!=', '')]):
			if x.person_alternate_id not in unq_lnrs:
				unq_lnrs.append(x.person_alternate_id)
		# find all duplicated learners by unq learner nat id
		for unq_lnr in unq_lnrs:
			bbg(unq_lnr)
			bunch_29 = self.env['nlrd.29'].search([('person_alternate_id', '=', unq_lnr)])
			qual_dict = {}
			lnr_qual_list = []
			# find all bunches of odoo lrqs with a matching learner and qual id
			for lrq in bunch_29:
				bbg(lrq)
				# build up a list of lrqs per bunch of matches
				if lrq.qualification_id not in lnr_qual_list:
					lnr_qual_list.append(lrq.qualification_id)
				match = self.env['nlrd.29'].search(
					[('person_alternate_id', '=', unq_lnr), ('qualification_id', 'in', lnr_qual_list)])
				# check if we have more than one match of learner and qual
				# also check if we have a cert num and is ach and is competent
				if len(match) > 1:
					full_competent = True
					full_ach = True
					full_cert = True
					lrq_match_list = []
					# set a match flag if all ticks are right
					for matcher in match:
						if not matcher.lrq_id.is_learner_achieved:
							full_competent = False
						if not matcher.lrq_id.is_complete:
							full_ach = False
						if not matcher.lrq_id.certificate_no:
							full_cert = False
						# append all matches that are ticked
						lrq_match_list.append(matcher.lrq_id.id)
					# check if all flags are ticked
					if full_cert and full_competent and full_ach:
						bbg(lrq_match_list)
						# get the latest
						mx_guy = max(lrq_match_list)
						# remove the lates so we dont delete it
						lrq_match_list.remove(mx_guy)
						# loop through the ones we want to unlink
						for remover in lrq_match_list:
							# set an odoo obj
							remover_obj = self.env['learner.registration.qualification'].search([('id', '=', remover)])
							# you know what this is
							# todo: uncomment for live run
							remover_obj.unlink()
							bbg('dropping true duplicates:' + str(remover_obj))
				# raise Warning('full true issue' + str(mx_guy))

	@api.multi
	def purge_dupe_lrq_no_cert(self):
		unq_lnrs = []
		# build unq learners
		for x in self.env['nlrd.29'].search([('national_id', '!=', '')]):
			if x.national_id not in unq_lnrs:
				unq_lnrs.append(x.national_id)
		# find all duplicated learners by unq learner nat id
		for unq_lnr in unq_lnrs:
			bbg(unq_lnr)
			bunch_29 = self.env['nlrd.29'].search([('national_id', '=', unq_lnr)])
			lnr_qual_list = []
			# find all bunches of odoo lrqs with a matching learner and qual id
			for lrq in bunch_29:
				bbg(lrq)
				# build up a list of lrqs per bunch of matches
				if lrq.qualification_id not in lnr_qual_list:
					lnr_qual_list.append(lrq.qualification_id)
				match = self.env['nlrd.29'].search(
					[('national_id', '=', unq_lnr), ('qualification_id', 'in', lnr_qual_list)])
				# check if we have more than one match of learner and qual
				# also check if we have a cert num and is ach and is competent
				if len(match) > 1:
					fully_cert = True
					for matcher in match:
						if not matcher.lrq_id.certificate_no:
							fully_cert = False
					if fully_cert:
						raise Warning(
							'cant drop, all have certs but not all are achieved and competent' + str(match))
					else:
						bbg('can drop')
						for matcher in match:
							if not matcher.lrq_id.certificate_no:
								remover_obj = self.env['learner.registration.qualification'].search(
									[('id', '=', matcher.lrq_id.id)])
								# todo: uncomment for live run
								remover_obj.unlink()
								bbg('dropping with no cert:' + str(remover_obj))



	def check_lrq(self, lrq):
		broken = False
		msg = str(lrq.id) + '\n'
		if not lrq.learner_id.learner_identification_id and not lrq.learner_id.national_id:
			broken = True
			msg += 'no id or alt id \n'
		if not lrq.learner_qualification_id and not lrq.learner_id:
			broken = True
			msg += 'no learner regsitration attached \n'
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
		dbg(msg)
		return broken, msg

	@api.multi
	def build_lrq_29(self):
		domain = [('certificate_date', '>', '2020-04-01')]
		brk_count = 0
		right_count = 0
		big_daddy = ''
		alt_ident = 7
		for lrq in self.env['learner.registration.qualification'].search(domain):
			checked_lrq = self.check_lrq(lrq)
			broken = checked_lrq[0]
			msg = checked_lrq[1]
			if not broken:  # this is where we check if the rec is broken
				alt_ident += 1
				right_count += 1
				alt_id = ''
				if lrq.learner_id.learner_identification_id:
					nat = lrq.learner_id.learner_identification_id
					tp = 'none'
					alt_id = ''
				elif lrq.learner_id.national_id:
					alt_id = lrq.learner_id.national_id
					tp = 'passport_number'
					nat = ''
				elif lrq.learner_id.passport_id:
					alt_id = lrq.learner_id.passport_id
					tp = 'passport_number'
					nat = ''
				else:
					alt_id = 'tmp' + str(alt_ident)
					tp = 'passport_number'
					nat = ''
				alt_id = normalize_alt_id(alt_id)
				ach_status_to_code(lrq.qual_status)
				if lrq.qual_status == 'Achieved':
					ach_date = fix_dates(lrq.certificate_date)
				elif ach_status_to_code(lrq.qual_status)=='3' and lrq.certificate_date:
					ach_date = ''
				else:
					ach_date = ''
				#if 'z' in alt_id:
				#	raise Warning('manzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
				val = {'national_id': nat,
					   'person_alternate_id': alt_id,
					   'alternate_id_type': id_type_to_code(tp),
					   'qualification_id': lrq.learner_qualification_parent_id.saqa_qual_id,
					   'learner_achievement_status_id': ach_status_to_code(lrq.qual_status),
					   'assessor_registration_number': lrq.assessors_id.assessor_seq_no,
					   'learner_achievement_type_id': '6',  # todo: find or pass flat value 6 is  other
					   'learner_achievement_date': ach_date,  # todo:needs eval based on learner_achievement_type_id
					   'learner_enrolled_date': fix_dates(lrq.start_date),
					   'honours_classification': '',  # not req
					   'part_of': '1',  # only allows 1 or 3/should only be 1 , blanket
					   'learnership_id': '',  # not req
					   'provider_code': lrq.provider_id.id,
					   'provider_etqa_id': '591',  # blanket
					   'assessor_etqa_id': '591',  # blanket
					   'certification_date': ach_date,
					   'date_stamp': fix_dates(lrq.write_date),
					   'lrq_id': lrq.id,
					   'learner_id': lrq.learner_id.id,
					   'assessors_id': lrq.assessors_id.id,
					   }
				# dbg(val)
				if global_write:
					self.env['nlrd.29'].create(val)
			else:
				brk_count += 1
				big_daddy += '\n\n' + msg
				dbg(str(lrq.id) + msg)
				alt_ident += 1
				right_count += 1
				alt_id = ''
				if lrq.learner_id.learner_identification_id:
					nat = lrq.learner_id.learner_identification_id
					tp = 'none'
					alt_id = ''
				elif lrq.learner_id.national_id:
					alt_id = lrq.learner_id.national_id
					tp = 'passport_number'
					nat = ''
				elif lrq.learner_id.passport_id:
					alt_id = lrq.learner_id.passport_id
					tp = 'passport_number'
					nat = ''
				else:
					alt_id = 'tmp' + str(alt_ident)
					tp = 'passport_number'
					nat = ''
				alt_id = normalize_alt_id(alt_id)
				ach_status_to_code(lrq.qual_status)
				if lrq.qual_status == 'Achieved':
					ach_date = fix_dates(lrq.certificate_date)
				else:
					ach_date = ''
				#if 'z' in alt_id:
				#	raise Warning('fuck manzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
				val = {'national_id': nat,
					   'person_alternate_id': alt_id,
					   'alternate_id_type': id_type_to_code(tp),
					   'qualification_id': lrq.learner_qualification_parent_id.saqa_qual_id,
					   'learner_achievement_status_id': ach_status_to_code(lrq.qual_status),
					   'assessor_registration_number': lrq.assessors_id.assessor_seq_no,
					   'learner_achievement_type_id': '6',  # todo: find or pass flat value 6 is  other
					   'learner_achievement_date': ach_date,  # todo:needs eval based on learner_achievement_type_id
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
					   'assessors_id': lrq.assessors_id.id,
					   'link_broken': True,
					   'broken': True,
					   'stat_msg': msg,
					   }
				# dbg(val)
				if global_write:
					self.env['nlrd.29'].create(val)
		dbg(big_daddy)
		dbg('broken:' + str(brk_count))
		dbg('right_count:' + str(right_count))

	def check_postal_word_count(self, postal):
		if len(postal.split()) > 2:
			return True
		else:
			return False

	def do_postal_word_split(self, postal):
		return postal.split()

	def check_provider(self, partner):
		# checks res.partner
		broken = False
		msg = str(partner.id) + '\n'
		if not partner.provider_accreditation_num or partner.provider_accreditation_num == '0':
			broken = True
			msg += 'no provider code \n'
		# todo: allow fixing as this is never filled
		if not partner.provider_type_id:
			broken = True
			msg += 'no provider type id \n'
		if not partner.name:
			broken = True
			msg += 'no provider name \n'
		if partner.provider_start_date and partner.provider_end_date:
			start = dt.datetime.strptime(partner.provider_start_date, '%Y-%m-%d')
			end = dt.datetime.strptime(partner.provider_end_date, '%Y-%m-%d')
			if start + relativedelta(years=5) <= end:
				broken = True
				msg += 'provider date gap bigger than 5 years \n'
		if not partner.province_code_physical.id:#used better handling in prov to code
			broken = True
			msg += 'no provider province \n'
		if not partner.zip_postal:
			broken = True
			msg += 'no provider zip_postal \n'
		# todo: allow fixing as this is never filled
		if not partner.provider_class_Id:
			broken = True
			msg += 'no provider provider_class_id \n'
		if not partner.provider_type_id:
			broken = True
			msg += 'no provider provider_type_id \n'

		return broken, msg

	@api.multi
	def build_providers_21(self):
		prov_nums = []
		for lrq in self.env['nlrd.29'].search([]):
			if lrq.provider_code not in prov_nums:
				prov_nums.append(lrq.provider_code)
		domain = [('id', 'in', prov_nums)]
		brk_count = 0
		right_count = 0
		big_daddy = ''
		for provider in self.env['res.partner'].search(domain):

			checked_provider = self.check_provider(provider)
			broken = checked_provider[0]
			msg = checked_provider[1]
			if not provider.postal_address_1:
			# 	for postal in [provider.postal_address_3, provider.postal_address_2]:
			# 		if check_postal_word_count(postal) > 2:
			# 			post_addy1=do_postal_word_split(postal)[0]
			# 			post_addy2=do_postal_word_split(postal)[1]
			# 			post_addy3=do_postal_word_split(postal)[2:]
			# if not provider.postal_address_2:
			# 	for postal in [provider.postal_address_1, provider.postal_address_3]:
			# 		if check_postal_word_count(postal) > 2:
			# 			post_addy1=do_postal_word_split(postal)[0]
			# 			post_addy2=do_postal_word_split(postal)[1]
			# 			post_addy3=do_postal_word_split(postal)[2:]
			# if not provider.postal_address_3:
			# 	for postal in [provider.postal_address_1, provider.postal_address_2]:
			# 		if check_postal_word_count(postal) > 2:
			# 			post_addy1=do_postal_word_split(postal)[0]
			# 			post_addy2=do_postal_word_split(postal)[1]
			# 			post_addy3=do_postal_word_split(postal)[2:]

				post_addy1 = '123 Blom street'
				broken = True
				msg += '\n missing postal addr 1'
			else:
				post_addy1 = provider.postal_address_1
			if not provider.postal_address_2:
				post_addy2 = 'Pretoria'
				broken = True
				msg += '\n missing postal addr 2'
			else:
				post_addy2 = provider.postal_address_1
			if not broken:  # this is where we check if the rec is broken
				right_count += 1
				start_dt = provider.provider_start_date
				end_dt = provider.provider_end_date
				# todo: need to check if the fields im blanking here are not required. probably better to use an int and False handler in the datgen
				val = {'Provider_Code': provider.id,
					   # 'Etqa_Id': provider.provider_etqe_id,  # ensure about blank being allowed
					   'Etqa_Id': '591',  # zz blanket
					   'Std_Industry_Class_Code': provider.provider_sic_code,
					   'Provider_Name': remove_school(strip_string(provider.name)),
					   'Provider_Type_Id': provider_type_id_to_code(provider.provider_type_id),
					   'Provider_Address_1': sanitize_addrs(post_addy1) + ' a',  # zz
					   'Provider_Address_2': sanitize_addrs(post_addy2) + ' a',  # zz
					   'Provider_Address_3': '',
					   'Provider_Postal_Code': cleanse_postcode(provider.zip_postal),
					   'Provider_Phone_Number': strip_string(provider.phone),
					   'Provider_Fax_Number': strip_string(provider.fax),
					   'Provider_Sars_Number': '',
					   'Provider_Contact_Name': '',
					   'Provider_Contact_Email_Address': sanitize_email(provider.email),
					   'Provider_Contact_Phone_Number': '',
					   'Provider_Contact_Cell_Number': strip_string(provider.mobile),
					   'Provider_Accreditation_Num': provider.provider_accreditation_num,
					   'Provider_Accredit_Start_Date': year_gap(start_dt,end_dt,5),
					   'Provider_Accredit_End_Date': fix_dates(end_dt),
					   # untested make sure
					   'Etqa_Decision_Number': '',  # blank
					   'Provider_Class_Id': provider_class_to_code(provider.provider_class_Id),  # blanket
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
				right_count += 1
				start_dt = provider.provider_start_date
				end_dt = provider.provider_end_date
				# todo: need to check if the fields im blanking here are not required. probably better to use an int and False handler in the datgen
				val = {'Provider_Code': provider.id,
					   # 'Etqa_Id': provider.provider_etqe_id,  # ensure about blank being allowed
					   'Etqa_Id': '591',  # zz blanket
					   'Std_Industry_Class_Code': provider.provider_sic_code,
					   'Provider_Name': remove_school(strip_string(provider.name)),
					   'Provider_Type_Id': provider_type_id_to_code(provider.provider_type_id),
					   'Provider_Address_1': sanitize_addrs(post_addy1) + ' a',  # zz
					   'Provider_Address_2': sanitize_addrs(post_addy2) + ' a',  # zz
					   'Provider_Address_3': '',
					   'Provider_Postal_Code': cleanse_postcode(provider.zip_postal),
					   'Provider_Phone_Number': strip_string(provider.phone),
					   'Provider_Fax_Number': strip_string(provider.fax),
					   'Provider_Sars_Number': '',
					   'Provider_Contact_Name': '',
					   'Provider_Contact_Email_Address': sanitize_email(provider.email),
					   'Provider_Contact_Phone_Number': '',
					   'Provider_Contact_Cell_Number': strip_string(provider.mobile),
					   'Provider_Accreditation_Num': provider.provider_accreditation_num,
					   'Provider_Accredit_Start_Date': year_gap(start_dt,end_dt,5),
					   'Provider_Accredit_End_Date': fix_dates(end_dt),
					   # untested make sure
					   'Etqa_Decision_Number': '',  # blank
					   'Provider_Class_Id': provider_class_to_code(provider.provider_class_Id),  # blanket
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
					   'broken': True,
					   'stat_msg': msg,
					   }
				# dbg(val)
				if global_write:
					self.env['nlrd.21'].create(val)
		# dbg(str(provider.id) + msg)
		dbg(big_daddy)
		dbg('broken:' + str(brk_count))
		dbg('right_count:' + str(right_count))

	def check_accreditation(self, accreditation):
		broken = False
		msg = str(accreditation.id) + '\n'
		if not accreditation.qualification_id.saqa_qual_id:  # and not accreditation.learnership_id??? and not accreditation.unit standard id???????????
			broken = True
			msg += 'no qual or learnership or units \n'
		if not accreditation.accreditation_qualification_id.provider_accreditation_num:
			broken = True
			msg += 'no accreditation number on accred %s\n' % accreditation.accreditation_qualification_id.id
		if not accreditation.accreditation_qualification_id.id:
			broken = True
			msg += 'no accreditation provider on accred %s\n' % accreditation.accreditation_qualification_id.id
		if not accreditation.accreditation_qualification_id.provider_start_date:
			broken = True
			msg += 'no start date %s \n' % accreditation.accreditation_qualification_id.id
		if not accreditation.accreditation_qualification_id.provider_end_date:
			broken = True
			msg += 'no end date %s \n' % accreditation.accreditation_qualification_id.id
		return broken, msg


	@api.multi
	def check_prov_acc(self):
		acc_ids = []
		for prov in self.env['nlrd.21'].search([]):
			for acc in prov.provider_id.qualification_ids:
				if acc.id not in acc_ids:
					acc_ids.append(acc.id)
		dbg(acc_ids)
		accs = self.env['provider.master.qualification'].search([('id','=',acc_ids)])
		dbg(accs)

	@api.multi
	def build_prov_acc_24(self):
		acc_ids = []
		for prov in self.env['nlrd.21'].search([]):
			for acc in prov.provider_id.qualification_ids:
				if acc.id not in acc_ids:
					acc_ids.append(acc.id)
		domain = [('id', 'in', acc_ids)]
		# domain = [('accreditation_qualification_id.final_state', '=', 'Approved')]
		brk_count = 0
		right_count = 0
		big_daddy = ''
		for accreditation in self.env['provider.master.qualification'].search(domain):
			checked_accreditation = self.check_accreditation(accreditation)
			broken = checked_accreditation[0]
			msg = checked_accreditation[1]
			stat_code = ''
			accred_code = ''
			if accreditation.accreditation_qualification_id.active:
				stat_code = provider_accredit_status_to_code('Active')
				accred_code = accreditation.qualification_id.saqa_qual_id
			elif not accreditation.accreditation_qualification_id.active:
				stat_code = provider_accredit_status_to_code('Inactive')
				accred_code = accreditation.qualification_id.saqa_qual_id
			if accreditation.qualification_id.is_archive:
				stat_code = provider_accredit_status_to_code('Inactive')
				#if accreditation.qualification_id.name == 'NC: Occupational Hygiene and Safety':
				if 'NC: Occupational Hygiene and Safety' in accreditation.qualification_id.name:
					accred_code = '79806'
			if not broken:  # this is where we check if the rec is broken
				right_count += 1
				start_dt = accreditation.accreditation_qualification_id.provider_start_date
				end_dt = accreditation.accreditation_qualification_id.provider_end_date
				val = {'Learnership_Id': '',
					   'Qualification_Id': accred_code,
					   'Unit_Standard_Id': '',  # maybe later
					   'Provider_Code': accreditation.accreditation_qualification_id.id,
					   'Provider_Etqa_Id': '591',  # blanket
					   'Provider_Accreditation_Num': accreditation.accreditation_qualification_id.provider_accreditation_num,
					   'Provider_Accredit_Assessor_Ind': '',  # blank
					   'Provider_Accred_Start_Date': year_gap(start_dt,end_dt,5),
					   'Provider_Accred_End_Date': fix_dates(end_dt),
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
				start_dt = accreditation.accreditation_qualification_id.provider_start_date
				end_dt = accreditation.accreditation_qualification_id.provider_end_date
				val = {'Learnership_Id': '',
					   'Qualification_Id': accreditation.qualification_id.saqa_qual_id,
					   'Unit_Standard_Id': '',  # maybe later
					   'Provider_Code': accreditation.accreditation_qualification_id.id,
					   'Provider_Etqa_Id': '591',  # blanket
					   'Provider_Accreditation_Num': accreditation.accreditation_qualification_id.provider_accreditation_num,
					   'Provider_Accredit_Assessor_Ind': '',  # blank
					   'Provider_Accred_Start_Date': year_gap(start_dt,end_dt,5),
					   'Provider_Accred_End_Date': fix_dates(end_dt),
					   'Etqa_Decision_Number': '',  # blank
					   'Provider_Accred_Status_Code': stat_code,
					   'Date_Stamp': fix_dates(accreditation.accreditation_qualification_id.write_date),
					   'accreditation_id': accreditation.id,
					   'broken': True,
					   'stat_msg': msg,
					   }
				dbg(val)
				if global_write:
					self.env['nlrd.24'].create(val)
				big_daddy += '\n\n' + msg
				dbg(accreditation.id)
		dbg(big_daddy)
		dbg('accred  broken:' + str(brk_count))
		dbg('accred right_count:' + str(right_count))

	# old def used wrong base model to fetch data
	# @api.multi
	# def build_prov_acc_24(self):
	# 	prov_nums = []
	# 	for prov in self.env['nlrd.21'].search([]):
	# 		if prov.Provider_Code not in prov_nums:
	# 			prov_nums.append(prov.Provider_Code)
	# 	domain = [('id', 'in', prov_nums)]
	# 	# domain = [('accreditation_qualification_id.final_state', '=', 'Approved')]
	# 	brk_count = 0
	# 	right_count = 0
	# 	big_daddy = ''
	# 	for accreditation in self.env['accreditation.qualification'].search(domain):
	# 		checked_accreditation = self.check_accreditation(accreditation)
	# 		broken = checked_accreditation[0]
	# 		msg = checked_accreditation[1]
	# 		stat_code = ''
	# 		if accreditation.accreditation_qualification_id.related_provider.active:
	# 			stat_code = provider_accredit_status_to_code('Active')
	# 		elif not accreditation.accreditation_qualification_id.related_provider.active:
	# 			stat_code = provider_accredit_status_to_code('Inactive')
	# 		if not broken:  # this is where we check if the rec is broken
	# 			right_count += 1
	# 			val = {'Learnership_Id': '',
	# 				   'Qualification_Id': accreditation.qualification_id.saqa_qual_id,
	# 				   'Unit_Standard_Id': '',  # maybe later
	# 				   'Provider_Code': accreditation.accreditation_qualification_id.related_provider.id,
	# 				   'Provider_Etqa_Id': '591',  # blanket
	# 				   'Provider_Accreditation_Num': accreditation.accreditation_qualification_id.accreditation_number,
	# 				   'Provider_Accredit_Assessor_Ind': '',  # blank
	# 				   'Provider_Accred_Start_Date': fix_dates(
	# 					   accreditation.accreditation_qualification_id.related_provider.provider_start_date),
	# 				   'Provider_Accred_End_Date': fix_dates(
	# 					   accreditation.accreditation_qualification_id.related_provider.provider_end_date),
	# 				   'Etqa_Decision_Number': '',  # blank
	# 				   'Provider_Accred_Status_Code': stat_code,
	# 				   'Date_Stamp': fix_dates(accreditation.accreditation_qualification_id.write_date),
	# 				   'accreditation_id': accreditation.id,
	# 				   }
	# 			dbg(val)
	# 			if global_write:
	# 				self.env['nlrd.24'].create(val)
	# 		else:
	# 			brk_count += 1
	# 			val = {'Learnership_Id': '',
	# 				   'Qualification_Id': accreditation.qualification_id.saqa_qual_id,
	# 				   'Unit_Standard_Id': '',  # maybe later
	# 				   'Provider_Code': accreditation.accreditation_qualification_id.related_provider.id,
	# 				   'Provider_Etqa_Id': '591',  # blanket
	# 				   'Provider_Accreditation_Num': accreditation.accreditation_qualification_id.accreditation_number,
	# 				   'Provider_Accredit_Assessor_Ind': '',  # blank
	# 				   'Provider_Accred_Start_Date': fix_dates(
	# 					   accreditation.accreditation_qualification_id.related_provider.provider_start_date),
	# 				   'Provider_Accred_End_Date': fix_dates(
	# 					   accreditation.accreditation_qualification_id.related_provider.provider_end_date),
	# 				   'Etqa_Decision_Number': '',  # blank
	# 				   'Provider_Accred_Status_Code': stat_code,
	# 				   'Date_Stamp': fix_dates(accreditation.accreditation_qualification_id.write_date),
	# 				   'accreditation_id': accreditation.id,
	# 				   'broken': True,
	# 				   }
	# 			dbg(val)
	# 			if global_write:
	# 				self.env['nlrd.24'].create(val)
	# 			big_daddy += '\n\n' + msg
	# 			dbg(accreditation.id)
	# 	dbg(big_daddy)
	# 	dbg('accred  broken:' + str(brk_count))
	# 	dbg('accred right_count:' + str(right_count))

	def check_person(self, person):
		# checks hr.employee
		broken = False
		msg = str(person.id) + '\n'
		global_id = False
		if person.is_learner:
			global_id = person.learner_identification_id
		elif person.is_assessors:
			if person.assessor_moderator_identification_id:
				if len(person.assessor_moderator_identification_id) != 13:
					broken = True
					msg += 'person len(id number) is not SA'
				else:
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
		if not person.equity and not person.is_assessors:
			broken = True
			msg += 'no person equity \n'
		if person.person_birth_date:
			dob = dt.datetime.strptime(person.person_birth_date, '%Y-%m-%d').date()
			now = datetime.today().date()
			if dob + relativedelta(years=15) > now:
			# 	raise Warning(str(person) + str(now) + ">" + person.person_birth_date)
			# diff = now - dob
			# dbg(diff)
			# if to_relativedelta(diff) >= relativedelta(years=15):
				broken = True
				msg += 'Person age is less than 15 years \n dob:' + person.person_birth_date + '\n'
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


	@api.multi
	def build_ass_26(self):
		mix_assr_dict = {}
		unq_ass_qual_ids = []
		for assr in self.env['nlrd.29'].search([]):
			if assr.assessor_registration_number and assr.assessor_registration_number not in unq_ass_qual_ids:
				mix_assr_dict.update({assr.assessor_registration_number: assr.assessors_id.id})
			else:
				dbg("ommit????")
		unq_ass_qual_ids = [x for x in mix_assr_dict.values()]
		domain = [('id', 'in', unq_ass_qual_ids)]
		# domain = [('is_assessors', '=', True)]
		brk_count = 0
		right_count = 0
		big_daddy = ''
		alt_ident = 0
		for assessor in self.env['hr.employee'].search(domain):
			checked_assessor = self.check_person(assessor)
			broken = checked_assessor[0]
			msg = checked_assessor[1]
			msg += str(assessor.is_assessors) + ' = is_assessors\n'
			alt_ident += 1
			alt_id = False
			nat = ''
			tp = ''
			if assessor.assessor_moderator_identification_id  and len(assessor.assessor_moderator_identification_id) == 13:
				try:
					int(str(assessor.assessor_moderator_identification_id))
					nat = assessor.assessor_moderator_identification_id
					tp = 'none'
					alt_id = ''
				except:
					alt_id = 'tmp'+str(alt_ident)
					tp = 'passport_number'

			elif assessor.national_id:
				alt_id = assessor.national_id
				tp = 'passport_number'
				nat = ''
			elif assessor.passport_id:
				alt_id = assessor.passport_id
				tp = 'passport_number'
				nat = ''
			else:
				alt_id = 'tmp' + str(alt_ident)
				tp = 'passport_number'
				nat = ''
				broken = True
				msg += '\n no id/nat/passport found'
			# if assessor.id == 81408:
			# 	print alt_id
			alt_id = normalize_alt_id(alt_id)
			# if assessor.id == 81408:
			# 	print alt_id
			if not broken:  # this is where we check if the rec is broken
				right_count += 1

				val = {'National_Id': nat,
					   'Person_Alternate_Id': alt_id,
					   'Alternate_Type_Id': id_type_to_code(tp),
					   'Designation_Id': '1',  # blanket
					   'Designation_Registration_Number': assessor.assessor_seq_no,
					   'Designation_Etqa_Id': '591',  # blanket
					   # 'Designation_Start_Date': year_gap(assessor.start_date,assessor.end_date,3),
					   # 'Designation_End_Date': fix_dates(assessor.end_date),
					   # todo: is this ok as a blanket? dont remember writing it and feels gross(occurs in multiple places)
					   'Designation_Start_Date': '20180401',  # req
					   'Designation_End_Date': '20200331',  # req
					   'Structure_Status_Id': '501',  # blanket
					   'Etqa_Decision_Number': '',  # blank
					   'Provider_Code': '',
					   'Provider_Etqa_Id': '591',
					   'Date_Stamp': fix_dates(assessor.write_date),
					   'assessor_id': assessor.id,
					   }
				dbg(val)
				# if assessor.id == 81408:
				# 	print alt_id
				# 	raise Warning(assessor.passport_id)
				if global_write:
					self.env['nlrd.26'].create(val)

			else:
				brk_count += 1
				val = {'National_Id': nat,
					   'Person_Alternate_Id': alt_id,
					   'Alternate_Type_Id': id_type_to_code(tp),
					   'Designation_Id': '1',  # blanket
					   'Designation_Registration_Number': assessor.assessor_seq_no,
					   'Designation_Etqa_Id': '591',  # blanket
					   # 'Designation_Start_Date': year_gap(assessor.start_date,assessor.end_date,3),
					   # 'Designation_End_Date': fix_dates(assessor.end_date),
					   'Designation_Start_Date': '20180401',  # req
					   'Designation_End_Date': '20200331',  # req
					   'Structure_Status_Id': '501',  # blanket
					   'Etqa_Decision_Number': '',  # blank
					   'Provider_Code': '',
					   'Provider_Etqa_Id': '591',
					   'Date_Stamp': fix_dates(assessor.write_date),
					   'assessor_id': assessor.id,
					   'broken': True,
					   'stat_msg': msg,
					   }
				dbg(val)
				# if assessor.id == 81408:
				# 	raise Warning(assessor.passport_id)
				if global_write:
					self.env['nlrd.26'].create(val)
				big_daddy += '\n\n' + msg
				dbg(assessor.id)
				# dbg(str(assessor.is_assessors) + str(assessor.id) + '-' + str(replace_unicode_with_normal(assessor.name)) + msg)
				dbg(str(assessor.is_assessors) + str(assessor.id) + '-' + msg)
		dbg(big_daddy)
		dbg('broken:' + str(brk_count))
		dbg('right_count:' + str(right_count))

	def check_register(self, register):
		broken = False
		msg = str(register.assessors_moderators_qualification_hr_id.id) + '\n'
		if not register.qualification_hr_id.saqa_qual_id:  # and not accreditation.learnership_id??? and not accreditation.unit standard id???????????
			broken = True
			msg += 'no qual or learnership or units \n'
		if not register.assessors_moderators_qualification_hr_id.assessor_seq_no:
			broken = True
			msg += 'no assessor number'
		if not register.assessors_moderators_qualification_hr_id.start_date:
			broken = True
			msg += 'no register start/registration date \n'
		if not register.assessors_moderators_qualification_hr_id.end_date:
			broken = True
			msg += 'no register end/approval date \n'
		return broken, msg

	@api.multi
	def build_ass_reg_27(self):
		assessor_nums = []
		for ass in self.env['nlrd.26'].search([]):
			if ass.assessor_id.id not in assessor_nums:
				assessor_nums.append(ass.assessor_id.id)
		domain = [('assessors_moderators_qualification_hr_id', 'in', assessor_nums)]

		# domain = [('assessors_moderators_qualification_id.final_state', '=', 'Approved'),
		# 		  ('assessors_moderators_qualification_id.assessor_moderator', '=', 'assessor')]
		brk_count = 0
		right_count = 0
		big_daddy = ''
		for register in self.env['assessors.moderators.qualification.hr'].search(domain):
			checked_register = self.check_register(register)
			broken = checked_register[0]
			msg = checked_register[1]
			if not broken:  # this is where we check if the rec is broken
				right_count += 1
				val = {'Learnership_Id': '',
					   'Qualification_Id': register.qualification_hr_id.saqa_qual_id,
					   'Unit_Standard_Id': '',
					   'Designation_Id': '1',  # blanket req
					   'Designation_Registration_Number': register.assessors_moderators_qualification_hr_id.assessor_seq_no,  # req
					   'Designation_Etqa_Id': '591',  # req blanket
					   # 'Nqf_Designation_Start_Date': year_gap(
						#    register.assessors_moderators_qualification_hr_id.start_date,register.assessors_moderators_qualification_hr_id.end_date,3),  # req
					   # 'Nqf_Designation_End_Date': fix_dates(
						#    register.assessors_moderators_qualification_hr_id.end_date),  # req
					   'Nqf_Designation_Start_Date': '20180401',  # req
					   'Nqf_Designation_End_Date': '20200331',  # req
					   'Etqa_Decision_Number': '',
					   'Nqf_Desig_Status_Code': 'A',  # req
					   'Date_Stamp': fix_dates(register.assessors_moderators_qualification_hr_id.write_date),  # req
					   'register_id': register.id,
					   'person_id': register.assessors_moderators_qualification_hr_id.id,
					   }  # req
				# dbg(val)
				if global_write:
					self.env['nlrd.27'].create(val)
			else:
				brk_count += 1
				val = {'Learnership_Id': '',
					   'Qualification_Id': register.qualification_hr_id.saqa_qual_id,
					   'Unit_Standard_Id': '',
					   'Designation_Id': '1',  # blanket req
					   'Designation_Registration_Number': register.assessors_moderators_qualification_hr_id.assessor_seq_no,
					   # req
					   'Designation_Etqa_Id': '591',  # req blanket
					   # 'Nqf_Designation_Start_Date': year_gap(
						#    register.assessors_moderators_qualification_hr_id.start_date,register.assessors_moderators_qualification_hr_id.end_date,3),  # req
					   # 'Nqf_Designation_End_Date': fix_dates(
						#    register.assessors_moderators_qualification_hr_id.end_date),  # req
					   'Nqf_Designation_Start_Date': '20180401',  # req
					   'Nqf_Designation_End_Date': '20200331',  # req
					   'Etqa_Decision_Number': '',
					   'Nqf_Desig_Status_Code': 'A',  # req
					   'Date_Stamp': fix_dates(register.assessors_moderators_qualification_hr_id.write_date),  # req
					   'register_id': register.id,
					   'person_id': register.assessors_moderators_qualification_hr_id.id,
					   'broken': True,
					   'stat_msg': msg,
					   }  # req
				# dbg(val)
				if global_write:
					self.env['nlrd.27'].create(val)
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
			if not person.assessor_id.assessor_moderator_identification_id and not\
					person.National_Id and not person.assessor_id.national_id and not\
					person.assessor_id.passport_id:
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
			if not person.assessor_id.country_id and not person.assessor_id.country_home:
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
			if not person.learner_identification_id and not person.national_id and not person.passport_id:
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
			if not person.country_id and not person.country_home:
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
	def build_person_25(self):
		domain = []
		brk_count = 0
		right_count = 0
		big_daddy = ''
		unq_learner_ids = []
		unq_ass_qual_ids = []
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
		alt_ident = 0
		mix_assr_dict = {}
		for assr in self.env['nlrd.26'].search(domain):
			if assr.National_Id and assr.National_Id not in unq_ass_qual_ids:
				mix_assr_dict.update({assr.National_Id:assr.id})
			elif assr.Person_Alternate_Id and assr.Person_Alternate_Id not in unq_ass_qual_ids:
				mix_assr_dict.update({assr.Person_Alternate_Id:assr.id})
			else:
				dbg("ommit????")
		unq_ass_qual_ids = [x for x in mix_assr_dict.values()]
		for assessor in self.env['nlrd.26'].search([('id', 'in', unq_ass_qual_ids)]):
			# dbg(assessor.read())
			checked_assessor = self.check_25(assessor, 'a', assessor_stat_dict)
			broken = checked_assessor[0]
			msg = checked_assessor[1]
			alt_ident += 1
			if assessor.assessor_id.assessor_moderator_identification_id and len(assessor.assessor_id.assessor_moderator_identification_id) == 13:
				try:
					int(str(assessor.assessor_id.assessor_moderator_identification_id))
					nat = assessor.assessor_id.assessor_moderator_identification_id
					tp = 'none'
					alt_id = ''
				except:
					alt_id = 'tmp'+str(alt_ident)
					tp = 'passport_number'
			elif assessor.assessor_id.national_id:
				alt_id = assessor.assessor_id.national_id
				tp = 'passport_number'
				nat = ''
			elif assessor.assessor_id.passport_id:
				alt_id = assessor.assessor_id.passport_id
				tp = 'passport_number'
				nat = ''
			else:
				alt_id = 'tmp' + str(alt_ident)
				tp = 'passport_number'
				nat = ''
			alt_id = normalize_alt_id(alt_id)
			country = assessor.assessor_id.country_id
			if not country:
				country = assessor.assessor_id.country_home
			if not broken:  # this is where we check if the rec is broken
				right_count += 1

				val = {'National_Id': nat,
					   # c
					   'Person_Alternate_Id': alt_id,  # c
					   'Alternate_Id_Type': id_type_to_code(tp),  # req
					   'Equity_Code': equity_to_code(assessor.assessor_id.equity),  # y
					   'Nationality_Code': nationality_to_code(country.name),  # y
					   'Home_Language_Code': lang_to_code(assessor.assessor_id.home_language_code.name),  # y
					   'Gender_Code': gender_to_code(assessor.assessor_id.gender),  # y
					   'Citizen_Resident_Status_Code': citizen_map(assessor.assessor_id.citizen_resident_status_code),
					   # y probably needs dict def
					   'Socioeconomic_Status_Code': socio_to_code(assessor.assessor_id.socio_economic_status),  # y
					   'Disability_Status_Code': disability_status_code(assessor.assessor_id.disability_status),  # y probably needs dict def
					   # 'Person_First_Name': replace_unicode_with_normal(assessor.assessor_id.name),  # y the unicode dict is killing me
					   'Person_First_Name': dual_name_removal(assessor.assessor_id.name),  # y
					   # 'Person_Last_Name': replace_unicode_with_normal(assessor.assessor_id.person_last_name),  # y
					   'Person_Last_Name': dual_name_removal(assessor.assessor_id.person_last_name),  # y
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
				val = {'National_Id': nat,
					   # c
					   'Person_Alternate_Id': alt_id,  # c
					   'Alternate_Id_Type': id_type_to_code(tp),  # req
					   'Equity_Code': equity_to_code(assessor.assessor_id.equity),  # y
					   'Nationality_Code': nationality_to_code(assessor.assessor_id.country_id.name),  # y
					   'Home_Language_Code': lang_to_code(assessor.assessor_id.home_language_code.name),  # y
					   'Gender_Code': gender_to_code(assessor.assessor_id.gender),  # y
					   'Citizen_Resident_Status_Code': citizen_map(assessor.assessor_id.citizen_resident_status_code),
					   # y probably needs dict def
					   'Socioeconomic_Status_Code': socio_to_code(assessor.assessor_id.socio_economic_status),  # y
					   'Disability_Status_Code': disability_status_code(assessor.assessor_id.disability_status),  # y probably needs dict def
					   # 'Person_First_Name': replace_unicode_with_normal(assessor.assessor_id.name),  # y the unicode dict is killing me
					   'Person_First_Name': dual_name_removal(assessor.assessor_id.name),  # y
					   # 'Person_Last_Name': replace_unicode_with_normal(assessor.assessor_id.person_last_name),  # y
					   'Person_Last_Name': dual_name_removal(assessor.assessor_id.person_last_name),  # y
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
					   'broken': True,  # y
					   'stat_msg': msg,  # y
					   }
				# dbg(val)
				if global_write:
					dbg(assessor)
					person = self.env['nlrd.25'].create(val)
					assessor.write({'person_id': person.id})
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
		mix_dict = {}
		# for learner in self.env['nlrd.29'].search(domain):
		# 	if learner.lrq_id.learner_id.id not in unq_learner_ids:
		# 		mix_dict.update({learner.learner_id.id:learner.id})
		# unq_lrq_ids = [x for x in mix_dict.values()]
		for learner in self.env['nlrd.29'].search(domain):
			if learner.national_id and learner.national_id not in unq_learner_ids:
				mix_dict.update({learner.national_id:learner.id})
			elif learner.person_alternate_id and learner.person_alternate_id not in unq_learner_ids:
				mix_dict.update({learner.person_alternate_id:learner.id})
			else:
				dbg("ommit????")
		unq_lrq_ids = [x for x in mix_dict.values()]
		for lrq in self.env['nlrd.29'].search([('id', 'in', unq_lrq_ids)]):
			checked_lrq = self.check_25(lrq, 'l', learner_stat_dict)
			learner = lrq.lrq_id.learner_id
			broken = checked_lrq[0]
			msg = checked_lrq[1]
			name = ''
			if not learner:
				msg += '\n no linked learner for:' + str(lrq)
				msg += "\n trying to see if there is a learner reg and if that learner reg has been updated to master"
				if lrq.lrq_id.learner_qualification_id:
					reg = lrq.lrq_id.learner_qualification_id
					if reg.state == "draft":
						msg += "\n found a draft reg, will try update to master"
						reg.action_submit_button()
						reg.action_approved_button()
				if not lrq.lrq_id.learner_id:
					# raise Warning("problems" + str(lrq.lrq_id))
					msg += "\n was unable to set the draft reg in order to approve to master"
					broken = True
					self.logit(lrq.lrq_id.id,'learner.regsitration.qualification',"was unable to set the draft reg in order to approve to master")
				learner = lrq.lrq_id.learner_id
			if learner:
				if learner.name:
					name = learner.name
				elif learner.name_related:
					name = learner.name_related
				else:
					broken = True
					self.logit(lrq.lrq_id.id, 'learner.regsitration.qualification',
							   "learner has no name")
					msg += '\n the learner has no name '
					name = 'placeholder....'
					# raise Warning(str(lrq) + ' no name:' + str(learner))
				name = dual_name_removal(name)
			else:
				broken = True
				msg += "\n still cant find a learner"
				self.logit(lrq.lrq_id.id, 'learner.regsitration.qualification',
						   "still cant find a learner")
			if learner.person_last_name:
				pl_name = dual_name_removal(learner.person_last_name)
			else:
				broken = True
				msg += '\n learner has no last name'
				self.logit(lrq.lrq_id.id, 'learner.regsitration.qualification',
						   "learner has no last name")
				pl_name = 'placeholder....'
			alt_ident += 1
			if learner.learner_identification_id:
				nat = learner.learner_identification_id
				tp = 'none'
				alt_id = ''
			elif learner.national_id:
				alt_id = learner.national_id
				tp = 'passport_number'
				nat = ''
			elif learner.passport_id:
				alt_id = learner.passport_id
				tp = 'passport_number'
				nat = ''
			else:
				alt_id = 'tmp' + str(alt_ident)
				tp = 'passport_number'
				nat = ''
				broken = True
				msg += '\n no id/nat/passport'
				self.logit(lrq.lrq_id.id, 'learner.regsitration.qualification',
						   "no id/nat/passport")
			alt_id = normalize_alt_id(alt_id)
			country = learner.country_id
			if not country:
				country = learner.country_home
			if not broken:  # this is where we check if the rec is broken
				right_count += 1

				val = {'National_Id': nat,  # c
					   'Person_Alternate_Id': alt_id,  # c
					   'Alternate_Id_Type': id_type_to_code(tp),  # req
					   'Equity_Code': equity_to_code(learner.equity),  # y
					   'Nationality_Code': nationality_to_code(country.name),  # y
					   'Home_Language_Code': lang_to_code(learner.home_language_code.name),  # y
					   'Gender_Code': gender_to_code(learner.gender),  # y
					   'Citizen_Resident_Status_Code': citizen_map(learner.citizen_resident_status_code),
					   # y probably needs dict def
					   'Socioeconomic_Status_Code': socio_to_code(learner.socio_economic_status),  # y
					   'Disability_Status_Code': disability_status_code(learner.disability_status),  # y probably needs dict def
					   # 'Person_First_Name': replace_unicode_with_normal(learner.name),  # y
					   'Person_First_Name': name,  # y
					   # 'Person_Last_Name': replace_unicode_with_normal(learner.person_last_name),  # y
					   'Person_Last_Name': pl_name,  # y
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
				val = {'National_Id': nat,  # c
					   'Person_Alternate_Id': alt_id,  # c
					   'Alternate_Id_Type': id_type_to_code(tp),  # req
					   'Equity_Code': equity_to_code(learner.equity),  # y
					   'Nationality_Code': nationality_to_code(learner.country_id.name),  # y
					   'Home_Language_Code': lang_to_code(learner.home_language_code.name),  # y
					   'Gender_Code': gender_to_code(learner.gender),  # y
					   'Citizen_Resident_Status_Code': citizen_map(learner.citizen_resident_status_code),
					   # y probably needs dict def
					   'Socioeconomic_Status_Code': socio_to_code(learner.socio_economic_status),  # y
					   'Disability_Status_Code': disability_status_code(learner.disability_status),  # y probably needs dict def
					   # 'Person_First_Name': replace_unicode_with_normal(learner.name),  # y
					   'Person_First_Name': name,  # y
					   # 'Person_Last_Name': replace_unicode_with_normal(learner.person_last_name),  # y
					   'Person_Last_Name': pl_name,  # y
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
					   'broken': True,
					   'stat_msg': msg,
					   }
				# dbg(val)
				if global_write:
					dbg(learner)
					person = self.env['nlrd.25'].create(val)
					lrq.write({'person_id': person.id})
				big_daddy += '\n\n' + msg
				dbg(learner.id)
		# dbg(big_daddy)
		dbg('person  broken:' + str(brk_count))
		dbg('person right_count:' + str(right_count))
		dbg(assessor_stat_dict)
		dbg(learner_stat_dict)

	@api.multi
	# def purge_dupe_lrq(self):
	# 	learners = {}
	# 	for lrq in self.env['nlrd.29'].search([]):
	# 		dbg(learners)
	# 		ident = lrq.national_id or lrq.person_alternate_id
	# 		if ident not in learners:
	# 			learners.update({ident:[lrq.qualification_id]})
	# 		else:
	# 			if lrq.qualification_id in learners.get(ident):
	# 				lrq.unlink()
	# 			else:
	# 				learners.get(ident).append(lrq.qualification_id)

	@api.multi
	def report_link_issues(self):
		lrq_list = []
		lrq_prov_list = []
		lrq_ass_list = []
		lrq_lnr_list = []
		msg = ''
		for lrq in self.env['nlrd.29'].search([]):
			dbg('lrq:' + str(lrq.id))
			lrq_list.append(lrq.id)
			if lrq.provider_code not in lrq_prov_list:
				lrq_prov_list.append(lrq.provider_code)
				# dbg('appending unq prov:' + str(lrq.provider_code))
			if lrq.assessors_id.id not in lrq_ass_list:
				lrq_ass_list.append(lrq.assessors_id.id)
				# dbg('appending unq assessor:' + str(lrq.assessors_id.id))
			if lrq.lrq_id.learner_id.id not in lrq_lnr_list:
				lrq_lnr_list.append(lrq.lrq_id.learner_id.id)
				# dbg('appending unq learner:' + str(lrq.lrq_id.learner_id.id))
		msg += 'lrq:' + str(len(lrq_list)) + '\n'
		msg += 'unq providers in lrq:' + str(len(lrq_prov_list)) + '\n'
		msg += 'unq assessors in lrq:' + str(len(lrq_ass_list)) + '\n'
		msg += 'unq learners in lrq:' + str(len(lrq_lnr_list)) + '\n'
		act_prov_list = []
		diff_prov_list = []
		for act_prov in self.env['nlrd.21'].search([]):
			if act_prov.Provider_Code not in act_prov_list:
				act_prov_list.append(act_prov.Provider_Code)
				if act_prov.Provider_Code not in lrq_prov_list:
					diff_prov_list.append(act_prov.Provider_Code)
		for x in act_prov_list:
			if x not in lrq_prov_list:
				dbg('problemsssssss!!!!!!!!!! prov in 21 but not 25')
		msg += 'provider count in 21: ' + str(len(act_prov_list)) + '\n'
		msg += 'provider diff in 21 vs 25: ' + str(diff_prov_list) + '\n'
		act_ass_list = []
		diff_ass_list = []
		for act_ass in self.env['nlrd.26'].search([]):
			if act_ass.assessor_id.id not in act_ass_list:
				act_ass_list.append(act_ass.assessor_id.id)
				if act_ass.assessor_id.id not in lrq_ass_list:
					diff_ass_list.append(act_ass.assessor_id.id)
		for x in act_ass_list:
			if x not in lrq_ass_list:
				dbg('problemsssssss!!!!!!!!!! ass in 26 but not 25')
		msg += 'ass count in 21: ' + str(len(act_ass_list)) + '\n'
		msg += 'ass diff in 21 vs 25: ' + str(diff_ass_list) + '\n'
		act_prov_acc_list = []
		for act_prov_acc in self.env['nlrd.24'].search([]):
			if act_prov_acc.Provider_Code not in act_prov_acc_list:
				act_prov_acc_list.append(act_prov_acc.Provider_Code)
		msg += 'prov acc count in 24: ' + str(len(act_prov_acc_list)) + '\n'
		act_ass_acc_list = []
		for act_ass_acc in self.env['nlrd.27'].search([]):
			if act_ass_acc.register_id.assessors_moderators_qualification_hr_id.id not in act_ass_acc_list:
				act_ass_acc_list.append(act_ass_acc.register_id.assessors_moderators_qualification_hr_id.id)
		msg += 'actual ass acc count in 27:' + str(len(act_ass_acc_list)) + '\n'
		bbg(msg)
		raise Warning(msg)

	# @api.multi
	# def find_missing_learners(self):
	# 	unq_lrq_ids = []
	# 	unq_learner_ids = []
	# 	mix_dict = {}
	# 	for learner in self.env['nlrd.29'].search([]):
	# 		if learner.learner_id.id not in unq_learner_ids:
	# 			unq_learner_ids.append(learner.learner_id.id)
	# 	dbg(len(unq_learner_ids))
	# 	dbg('--------------------------')
	# 	learner_stat_dict = {
	# 		'identification_id': 0,
	# 		'alternate_id_type': 0,
	# 		'equity': 0,
	# 		'country_id': 0,
	# 		'home_language_code': 0,
	# 		'gender': 0,
	# 		'citizen_resident_status_code': 0,
	# 		'socio_economic_status': 0,
	# 		'disability_status': 0,
	# 		'name': 0,
	# 		'person_last_name': 0,
	# 		'person_birth_date': 0,
	# 		'person_home_province_code': 0,
	# 	}
	# 	right_count = 0
	# 	broken_count = 0
	# 	for learner in self.env['nlrd.29'].search([]):
	# 		if learner.learner_id.id not in mix_dict:
	# 			mix_dict.update({learner.learner_id.id:learner.id})
	# 	dbg(len(mix_dict))
	# 	unq_lrq_ids = [x for x in mix_dict.values()]
	# 	for lrq in self.env['nlrd.29'].search([('id', 'in', unq_lrq_ids)]):
	# 		checked_lrq = self.check_25(lrq, 'l', learner_stat_dict)
	# 		learner = lrq.lrq_id.learner_id
	# 		broken = checked_lrq[0]
	# 		msg = checked_lrq[1]
	# 		if not broken:  # this is where we check if the rec is broken
	# 			right_count += 1
	# 		else:
	# 			broken_count += 1
	# 	dbg(right_count)
	# 	dbg(broken_count)
	# 	dbg(learner_stat_dict)

	@api.multi
	def do_all_v2(self):
		self.build_lrq_29()
		self.build_providers_21()
		self.build_prov_acc_24()
		self.build_ass_26()
		self.build_ass_reg_27()
		self.build_person_25()

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
