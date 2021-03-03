# coding=utf-8
from openerp import models, fields, tools, api, _
import datetime as dt
from dateutil.relativedelta import relativedelta

DEBUG = True

if DEBUG:
	import logging

	logger = logging.getLogger(__name__)


	def dbg(msg):
		logger.info(msg)
else:
	def dbg(msg):
		pass

def to_relativedelta(tdelta):
	return relativedelta(seconds=int(tdelta.total_seconds()),
						 microseconds=tdelta.microseconds)

BAD_WORDS = [
	'section',
	'ext',
	'extension',
	'str',
	'street',
	'cres',
	'crescent',
	'ave',
	'avenue',
	'blvd',
	'boulevard',
	'road',
	'rd,'
	'drive',
	'dr',
	'park',
	'north',
	'east',
	'south',
	'west',
	'block',

]


def country_check(person):
	country = False
	msg = ''
	# try set country in citizen details to same as home country in addresses
	country = person.country_home if person.country_home else False
	msg = 'set country in citizen details to same as home country in addresses'
	# try to set country based on work country
	if not country:
		country = person.work_country if person.work_country else False
		msg = 'set country based on work country'
	# try to set country based on postal country
	if not country:
		country = person.country_postal if person.country_postal else False
		msg = 'set country based on postal country'
	# try to set country based on home province
	if not country:
		country = person.person_home_province_code.country_id if person.person_home_province_code.country_id else False
		msg = 'set country based on home province'
	# try set the country based on work province
	if not country:
		country = person.work_province.country_id if person.work_province.country_id else False
		msg = 'set country based on work province'
	# try set the country based on physical_municipality
	if not country:
		country = person.physical_municipality.country_id if person.physical_municipality else False
		msg = 'set the country based on physical_municipality'
	# try set the country based on work_municipality
	if not country:
		country = person.work_municipality.country_id if person.work_municipality else False
		msg = 'set the country based on work_municipality'
	# try set the country based on postal_municipality
	if not country:
		country = person.postal_municipality.country_id if person.postal_municipality else False
		msg = 'set the country based on postal_municipality'
	# try set the country based on person_home_suburb
	if not country:
		country = person.person_home_suburb.country_id if person.person_home_suburb else False
		msg = 'set the country based on person_home_suburb'
	# try set the country based on person_suburb
	if not country:
		country = person.person_suburb.country_id if person.person_suburb else False
		msg = 'set the country based on person_suburb'

	# return a generic msg about no way to make match
	if not country:
		msg = 'found no way to match'
	return country, msg

def province_check(person):
	province = False
	msg = ''
	# try set the province based on work province
	province = person.work_province if person.work_province else False
	if province:
		msg = 'set province based on work province'
	# try set the province based on work province
	if not province:
		province = person.work_province if person.work_province else False
		msg = 'set province based on work province'
	# try set the province based on physical_municipality
	if not province:
		province = person.physical_municipality.province_id if person.physical_municipality else False
		msg = 'set the province based on physical_municipality'
	# try set the province based on work_municipality
	if not province:
		province = person.work_municipality.province_id if person.work_municipality else False
		msg = 'set the province based on work_municipality'
	# try set the province based on postal_municipality
	if not province:
		province = person.postal_municipality.province_id if person.postal_municipality else False
		msg = 'set the province based on postal_municipality'
	# try set the province based on person_home_suburb
	if not province:
		province = person.person_home_suburb.province_id if person.person_home_suburb else False
		msg = 'set the province based on person_home_suburb'
	# try set the province based on person_suburb
	if not province:
		province = person.person_suburb.province_id if person.person_suburb else False
		msg = 'set the province based on person_suburb'


	# return a generic msg about no way to make match
	if not province:
		msg = 'found no way to match'
	return province, msg

def gender_check(person):
	gender = False
	msg = ''
	# if person.person_title:
	# 	if person.person_title in ['Mr',]:

class nlrd_admin_wiz(models.TransientModel):
	_name = 'nlrd.admin.wiz'

	learner_id = fields.Many2one('hr.employee')

	@api.multi
	def unlink_all(self):
		for x in self.env['nlrd.report'].search([]):
			x.unlink()

	# crap and slow
	# def build_addr_dicts(self):
	# 	city_dict = {}
	# 	for city in self.env['res.city'].search([('name', '!=', False)]):
	# 		city_dict.update({city: city.name.lower()})
	# 	suburb_dict = {}
	# 	for suburb in self.env['res.suburb'].search([('name', '!=', False)]):
	# 		suburb_dict.update({suburb: suburb.name.lower()})
	# 	district_dict = {}
	# 	for district in self.env['res.district'].search([('name', '!=', False)]):
	# 		district_dict.update({district: district.name.lower()})
	# 	return {'cd':city_dict,'sd':suburb_dict,'dd':district_dict}

	def fix_addr(self,addr_string, hr):
		dbg(addr_string)
		addr_string = ''.join([i for i in addr_string if not i.isdigit()])
		dbg(addr_string)
		# city_dict = addr_dicts.get('cd')
		# suburb_dict = addr_dicts.get('sd')
		# district_dict = addr_dicts.get('dd')
		addr_list = []
		if addr_string:
			addr_list = addr_string.split()
		for word in addr_list:
			dbg('checking dd')
			if not word in BAD_WORDS:
				for cd in self.env['res.city'].search([('name','ilike',word),('province_id','!=',False)]):
					prov = cd.province_id
					return prov, "got province:%s from city:%s in the address:%s" % (prov.name, cd.name, addr_string)
				for dd in self.env['res.district'].search([('name','ilike',word),('province_id','!=',False)]):
					prov = dd.province_id
					return prov, "got province:%s from district:%s in the address:%s" % (prov.name, dd.name, addr_string)
				for sd in self.env['res.suburb'].search([('name','ilike',word),('province_id','!=',False)]):
					prov = sd.province_id
					return prov, "got province:%s from suburb:%s in the address:%s" % (prov.name, sd.name, addr_string)
			else:
				dbg('bad word found ' + str(word))
			# crap and slow
			# for city_id in city_dict.keys():
			# 	if word == city_dict.get(city_id) and city_id.province_id:
			# 		prov = city_id.province_id
			# 		return prov, "got province:%s from city:%s in the addres:%s" % (prov.name,city_id.name,addr_string)
			# dbg('checking sd')
			# for suburb_id in suburb_dict.keys():
			# 	if word == suburb_dict.get(suburb_id) and suburb_id.province_id:
			# 		prov = suburb_id.province_id
			# 		return prov, "got province:%s from suburb:%s in the addres:%s" % (prov.name,suburb_id.name,addr_string)
			# dbg('checking dd')
			# for district_id in district_dict.keys():
			# 	if word == district_dict.get(district_id) and district_id.province_id:
			# 		prov = district_id.province_id
			# 		return prov, "got province:%s from district:%s in the addres:%s" % (prov.name,district_id.name,addr_string)
		return False, 'no dice'

				# raise Warning(_(word))

	@api.one
	def fix_assessor(self):
		assessors_fixed = []
		for nlrd26_id in self.env['nlrd.26'].search([('broken', '=', True)]):
			msg = ""
			assessor_obj = nlrd26_id.assessor_id
			if "person len(id number) is not SA" in nlrd26_id.stat_msg:
				if assessor_obj.assessor_moderator_identification_id:
					replacer_num = assessor_obj.assessor_moderator_identification_id
					if not assessor_obj.passport_id:
						assessor_obj.alternate_id_type = 'passport_number'
						assessor_obj.passport_id = replacer_num
					elif not assessor_obj.national_id:
						assessor_obj.alternate_id_type = 'passport_number'
						assessor_obj.national_id = replacer_num
					msg += "-set the id type to passport_number after finding national_id or passport_id was blank but got non-sa digit count on the assessor_moderator_identification_id"
			if "no person type id but has alt type" in nlrd26_id.stat_msg:
				if not assessor_obj.alternate_id_type and (assessor_obj.national_id or assessor_obj.passport_id):
					assessor_obj.alternate_id_type = 'passport_number'
					msg += "set the id type to passport_number after finding national_id or passport_id"
			if "no id/nat/passport found" in nlrd26_id.stat_msg:
				msg += "-no id/nat/passport found-tmp generator used"
			assessors_fixed.append({nlrd26_id:msg})
		for af in assessors_fixed:
			for afd in af.keys():
				name = str(afd.id) + '-' + str(af.get(afd))
				values = {'name':name,'nlrd_26_id':afd.id,'doc_id':afd.id,'doc_model':'nlrd.26','message':af.get(afd)}
				self.env['nlrd.report'].create(values)

	@api.one
	def fix_assessor_qual(self):
		assessor_quals_fixed = []
		for nlrd27_id in self.env['nlrd.27'].search([('broken', '=', True)]):
			msg = ""
			assessor_qual_obj = nlrd27_id.register_id
			if "no qual or learnership or units" in nlrd27_id.stat_msg:
				msg += "no qual or learnership or units"
			assessor_quals_fixed.append({nlrd27_id: msg})
		for aqf in assessor_quals_fixed:
			for aqfd in aqf.keys():
				name = str(aqf.get(aqfd))
				values = {'name': name, 'nlrd_27_id': aqfd.id, 'doc_id': aqfd.id, 'doc_model': 'nlrd.27',
						  'message': aqf.get(aqfd)}
				self.env['nlrd.report'].create(values)

	@api.one
	def fix_lrq(self):
		lrqs_deleted = []
		for nlrd29_id in self.env['nlrd.29'].search([('broken', '=', True)]):
			dbg(nlrd29_id)
			lrq_object = nlrd29_id.lrq_id
			dbg(lrq_object)
			# check if the nlrd rec has the error string we want
			if "no assessor number" in nlrd29_id.stat_msg:
				"""
				found no assessor attached to this lrq, so start to find out if they have another one thats valid
				this helps us assume that the broken one is just an orphan
				"""

				if lrq_object.learner_id:
					lrq_dict = {}
					if lrq_object.learner_id.learner_qualification_ids:
						for lrq in lrq_object.learner_id.learner_qualification_ids:
							dbg(lrq.read()[0])
							# find a healthy copy
							if not lrq_object == lrq and \
								lrq_object.learner_qualification_parent_id == lrq.learner_qualification_parent_id \
								and lrq.assessors_id and lrq.moderators_id and lrq.batch_id and lrq.start_date and\
								lrq.end_date and lrq.certificate_no:
								lrq_dict.update(
										{nlrd29_id: {'status': "clean replace", 'replacer': lrq, 'record_data': lrq_object.read()[0]}})
					if lrq_dict:
						lrqs_deleted.append(lrq_dict)
				dbg("delete len after no ass:" + str(len(lrqs_deleted)))
			if "no id or alt id" in nlrd29_id.stat_msg or "no learner regsitration attached" in nlrd29_id.stat_msg:
				if lrq_object.certificate_no:
					lrq_dict = {}
					for a_lrq in self.env['learner.registration.qualification'].search([('certificate_no','=',lrq_object.certificate_no)]):
						if lrq_object.certificate_no == a_lrq.certificate_no and not lrq_object == a_lrq:
							dbg("found a matching certificate_no: " + str(lrq_object.certificate_no) + " vs " + str(a_lrq.certificate_no))
							lrq_dict.update(
								{nlrd29_id: {'status': "straight delete on matched cert num, no reg ref, draft assessment",
											 'replacer': a_lrq, 'record_data': lrq_object.read()[0]}})
					# try find a match by batch and assessments batch:
					if lrq_object.batch_id:
						matched_assessment = self.env['provider.assessment'].search([('batch_id','=',lrq_object.batch_id.id),('state','!=','draft')])
						lrq_dict.update(
								{nlrd29_id: {'status': "straight delete, no reg ref, no non-draft assessment", 'replacer': "N/A", 'record_data': lrq_object.read()[0]}})
						dbg(matched_assessment)
						draft_assessments = matched_assessment = self.env['provider.assessment'].search([('batch_id','=',lrq_object.batch_id.id)])
						dbg("drafts" + str(draft_assessments))
						lrq_dict.update(
							{nlrd29_id: {'status': "straight delete on matched batch, no reg ref, draft assessment",
										 'replacer': draft_assessments, 'record_data': lrq_object.read()[0]}})
						if lrq_dict:
							lrqs_deleted.append(lrq_dict)
		dbg("need to delete these recs!!! lrqs_deleted")
		dbg(lrqs_deleted)
		for ld in lrqs_deleted:
			for ldd in ld.keys():
				name = str(ld.get(ldd))
				values = {'name': name, 'nlrd_29_id': ldd.id, 'doc_id': ldd.id, 'doc_model': 'nlrd.29',
							  'message': ld.get(ldd)}
				self.env['nlrd.report'].create(values)
				ldd.lrq_id.unlink()


	@api.one
	def fix_person(self):
		fixed_people = []
		unknown_lang = self.env['res.lang'].search([('name','=','Unknown')],limit=1)
		for nlrd25_id in self.env['nlrd.25'].search([('broken', '=', True)]):
			dbg(nlrd25_id)
			dbg(nlrd25_id.stat_msg)
			person_object = nlrd25_id.person_id
			dbg(person_object)
			msg = ""
			# check if the nlrd rec has the error string we want
			if "Person age is less than 15 years" in nlrd25_id.stat_msg:
				dbg("Person age is less than 15 years")
				dob = dt.datetime.strptime(person_object.person_birth_date, '%Y-%m-%d')
				now = dt.datetime.today()
				diff = now - dob
				if to_relativedelta(diff) >= relativedelta(years=15):
					new_date = now - relativedelta(years=15)
				else:
					new_date = dob
				new_date = dt.datetime.strftime(new_date, '%Y-%m-%d')
				person_object.person_birth_date = new_date
				msg += "Setting dob to 15 years behind today"
			if "learner has no person_birth_date" in nlrd25_id.stat_msg:
				dbg("learner has no person_birth_date")
				msg += "learner has no person_birth_date"
			if "learner has no equity" in nlrd25_id.stat_msg:
				msg += "learner has no equity-"
				person_object.equity = "unknown"
				msg += "-blanket on equity as unknown"
			if "learner has no home_language_code" in nlrd25_id.stat_msg:
				msg += "learner has no home_language_code -"
				person_object.home_language_code = unknown_lang
				msg += "(blanket)set the home language to Unknown"
			if "learner has no person_home_province_code" in nlrd25_id.stat_msg:
				province, mesg = province_check(person_object)
				msg += "learner has no person_home_province_code-"
				# try set the province based on person_home_zip
				if not province:
					suburb = self.env['res.suburb'].search([('postal_code', '=',person_object.person_home_zip)],limit=1)
					province = suburb.province_id
					mesg = 'set the province based on person_home_zip,'
				if not province:
					suburb = self.env['res.suburb'].search([('postal_code', '=',person_object.work_zip)],limit=1)
					province = suburb.province_id
					mesg = 'set the province based on work_zip,'
				if not province:
					suburb = self.env['res.suburb'].search([('postal_code', '=',person_object.person_postal_zip)],limit=1)
					province = suburb.province_id
					mesg = 'set the province based on person_postal_zip,'
				dbg("home province is " + str(province.name))
				if not province:
					if not person_object.person_home_address_1 == '.' and not person_object.person_home_address_2 == '.':
						if person_object.person_home_address_1:
							province, mesg = self.fix_addr(person_object.person_home_address_1,person_object)
						# check if the prv has been filled above
						if person_object.person_home_address_2 and not province:
							province, mesg = self.fix_addr(person_object.person_home_address_2,person_object)
					else:
						mesg = '-just dots'
				person_object.person_home_province_code = province
				# if prov is still blank after reverse search and zip code lookup , add generic msg about the flop
				if not province:
					msg = 'found no way to match province'
				msg+= mesg

				dbg(msg)
				dbg(province)
				# fixed_people.append({nlrd25_id: "assessor has no person_home_province_code-" + msg})
			if "assessor has no person_home_province_code" in nlrd25_id.stat_msg:
				province, mesg = province_check(person_object)
				msg += "assessor has no person_home_province_code-"
				# try set the province based on person_home_zip
				if not province:
					suburb = self.env['res.suburb'].search([('postal_code', '=',person_object.person_home_zip)],limit=1)
					province = suburb.province_id
					mesg = 'set the province based on person_home_zip,'
				if not province:
					suburb = self.env['res.suburb'].search([('postal_code', '=',person_object.work_zip)],limit=1)
					province = suburb.province_id
					mesg = 'set the province based on work_zip,'
				if not province:
					suburb = self.env['res.suburb'].search([('postal_code', '=',person_object.person_postal_zip)],limit=1)
					province = suburb.province_id
					mesg = 'set the province based on person_postal_zip,'
				dbg("home province is " + str(province.name))
				if not province:
					if not person_object.person_home_address_1 == '.' and not person_object.person_home_address_2 == '.':
						if person_object.person_home_address_1:
							province, mesg = self.fix_addr(person_object.person_home_address_1,person_object)
						# check if it found a prov above
						if person_object.person_home_address_2 and not province:
							province, mesg = self.fix_addr(person_object.person_home_address_2,person_object)
					else:
						dbg('just dots')
						mesg = '-just dots'
				person_object.person_home_province_code = province
				# if prov is still blank after reverse search and zip code lookup , add generic msg about the flop
				if not province:
					msg += 'found no way to match province'
					mesg = ''
				msg+= mesg
				dbg(msg)
				dbg(province)
				# fixed_people.append({nlrd25_id: "assessor has no person_home_province_code-" + msg})
			if "assessor has no country" in nlrd25_id.stat_msg:
				country, mesg = country_check(person_object)
				msg += "-" + mesg
				person_object.country_id = country
				dbg(msg)
				dbg(country)
				fixed_people.append({nlrd25_id: "assessor has no country-" + msg})
			if "learner has no country" in nlrd25_id.stat_msg:
				country, mesg = country_check(person_object)
				msg += "-" + mesg
				person_object.country_id = country
				dbg(msg)
				dbg(country)
				fixed_people.append({nlrd25_id: "learner has no country-" + msg})
			if "assessor has no equity" in nlrd25_id.stat_msg:
				dbg("assessor has no equity")
				# blanket as unknown
				person_object.equity = "unknown"
				msg += "-blanket on equity as unknown"
			if "assessor has no gender" in nlrd25_id.stat_msg:
				dbg("assessor has no gender")
				msg += "assessor has no gender"
			if "assessor has no person_birth_date" in nlrd25_id.stat_msg:
				dbg("assessor has no person_birth_date")
				msg += "assessor has no person_birth_date"
			if "assessor has no national id" in nlrd25_id.stat_msg:
				dbg("assessor has no national id")
				msg += "assessor has no national id"
			if "assessor has no socio_economic_status" in nlrd25_id.stat_msg:
				dbg("assessor has no socio_economic_status")
				# blanket as "unspecified"
				person_object.socio_economic_status = "Unspecified"
				msg += "-blanket on socio_economic_status as Unspecified"
			if "assessor has no home_language_code " in nlrd25_id.stat_msg:
				msg += "assessor has no home_language_code -"
				person_object.home_language_code = unknown_lang
				msg += "(blanket)set the home language to Unknown"
			if "assessor has no disability_status" in nlrd25_id.stat_msg:
				dbg("assessor has no disability_status ")
				# blanket as "none"
				person_object.disability_status = "none"
				msg += "-blanket on disability_status as none"
			fixed_people.append({nlrd25_id: msg})
		dbg(fixed_people)
		for fp in fixed_people:
			for fpd in fp.keys():
				if not fp.get(fpd):
					msg = fpd.stat_msg
				else:
					msg = fp.get(fpd)
				name = str(msg)
				values = {'name':name,'nlrd_25_id':fpd.id,'doc_id':fpd.id,'doc_model':'nlrd.25','message':msg}
				self.env['nlrd.report'].create(values)
			
	@api.one
	def fix_provider(self):
		fixed_provs = []
		for nlrd21_id in self.env['nlrd.21'].search([('broken', '=', True)]):
			prov_object = nlrd21_id.provider_id
			msg = ""
			# check if the nlrd rec has the error string we want
			if "provider date gap bigger than 5 years" in nlrd21_id.stat_msg:
				start = dt.datetime.strptime(prov_object.provider_start_date, '%Y-%m-%d')
				end = dt.datetime.strptime(prov_object.provider_end_date, '%Y-%m-%d')
				diff = end - start
				if to_relativedelta(diff) >= relativedelta(years=5):
					new_date = end - relativedelta(years=5)
				else:
					new_date = start
				new_date = dt.datetime.strftime(new_date, '%Y-%m-%d')
				prov_object.provider_start_date = new_date
				msg += 'setting prov start date to ' + str(new_date)
			if "no provider provider_class_id" in nlrd21_id.stat_msg:
				if not prov_object.provider_class_Id:
					class_dict = {1: 'Unknown',
								  3: 'Foreign',
								  4: 'Public',
								  5: 'Private',
								  6: 'Interim (SAQA use only)',
								  7: 'NGO / CBO',
								  8: 'Mixed: Public and Private',
								  }
					prov_object.provider_class_Id = 'Unknown'
					msg += 'setting the class id to Unknown'
			if "no provider type id " in nlrd21_id.stat_msg:
				if not prov_object.provider_type_id:
					type_dict = {2: 'Development Enterprise NGO',
								 3: 'Education',
								 4: 'Employer',
								 5: 'Training',
								 500: 'Education and Training'
								 }
					prov_object.provider_type_id = 'Education and Training'
					msg += 'setting the type id to Education and Training'
			fixed_provs.append({nlrd21_id: msg})
		dbg(fixed_provs)
		for fp in fixed_provs:
			for fpd in fp.keys():
				name = str(fp.get(fpd))
				values = {'name':name,'nlrd_21_id':fpd.id,'doc_id':fpd.id,'doc_model':'nlrd.21','message':fp.get(fpd)}
				self.env['nlrd.report'].create(values)

	@api.one
	def purge_dupe_amr(self):
		deleted_amrs = []
		for assr in self.env['hr.employee'].search([('is_assessors','=',True)]):
			amrs = []
			dbg(assr)
			msg = ''
			for amr in assr.qualification_ids:
				if amr.saqa_qual_id in amrs:
					msg += 'deleting amr, found duplicate'
					deleted_amrs.append({assr:amr.read()})
					amr.unlink()
					dbg('deleting amr')
				else:
					dbg("unique amr")
					amrs.append(amr.saqa_qual_id)
		for da in deleted_amrs:
			for dad in da.keys():
				name = str(da.get(dad))
				values = {'name':name,'doc_id':dad.id,'doc_model':'amr','message':da.get(dad)}
				self.env['nlrd.report'].create(values)

	@api.multi
	def do_all_admin(self):
		self.purge_dupe_amr()
		self.fix_lrq()
		self.fix_assessor_qual()
		self.fix_assessor()
		self.fix_provider()
		self.fix_person()
