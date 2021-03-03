# coding=utf-8
import re
import os
from datetime import datetime
import datetime as dt
import random
from dateutil.relativedelta import relativedelta

DEBUG = False

if DEBUG:
	import logging

	logger = logging.getLogger(__name__)


	def dbg(msg):
		logger.info(msg)
else:
	def dbg(msg):
		pass


### DICTS


def replace_unicode_ng(text):
	"""
	Find any unicodes and replace them with random characters
	"""
	unimap = {
		"ß": "b", "à": "a", "á": "a", "â": "a", "ã": "a", "ä": "a", "å": "a", "æ": "ae", "ç": "c",
		"è": "e", "é": "e", "ê": "e", "ë": "e", "ì": "i", "í": "i", "î": "i", "ï": "i", "ð": "o",
		"ñ": "n", "ò": "o", "ó": "o", "ô": "o", "õ": "o", "ö": "o", "ø": "o", "ù": "u", "ú": "u",
		"û": "u", "ü": "u", "ý": "y", "þ": "b", "ÿ": "y", }
	rx = random.randint(0, 4)
	rxd = {0: "a", 1: "e", 2: "i", 3: "o", 4: "u"}
	rx = rxd[rx]

	for u in unimap:
		if u in text:
			text = re.sub(u, rx, text)
	return text


def normalize_alt_id(alt_id):
	# print 'normalizing alt id'
	# print alt_id
	# if not alt_id:
	# 	return 'zzzzzzzzzzzzzzzzzzzzzzz'
	# elif '/' in alt_id:
	# 	alt_id = re.sub('/', '-', alt_id)
	alt_id = re.sub('/', '-', alt_id)
	return alt_id


def ach_status_to_code(ach_stat):
	ach_dict = {'Achieved': '15',
				'Re-Enrolled': '5',
				'Enrolled': '3'}
	return ach_dict[ach_stat]


def replace_unicode_with_normal(text):
	unimap = {
		"ß": "b", "à": "a", "á": "a", "â": "a", "ã": "a", "ä": "a", "å": "a", "æ": "ae", "ç": "c",
		"è": "e", "é": "e", "ê": "e", "ë": "e", "ì": "i", "í": "i", "î": "i", "ï": "i", "ð": "o",
		"ñ": "n", "ò": "o", "ó": "o", "ô": "o", "õ": "o", "ö": "o", "ø": "o", "ù": "u", "ú": "u",
		"û": "u", "ü": "u", "ý": "y", "þ": "b", "ÿ": "y", }
	# if lambda a, d: any(k in a for k in d):
	for x in unimap.keys():
		dbg(x)
		dbg(text)
		if x in str(text):
			re.sub(x, unimap[x], text)
	return text


def make_up_date(date, provider):
	if not date and not provider.provider_end_date:
		return '20200331'
	else:
		return date


# def yearsago(years, from_date=None):
# 	if from_date is None:
# 		from_date = datetime.now()
# 	return from_date - relativedelta(years=years)
#
#
# def year_gap_5(start, end):
# 	start = dt.datetime.strptime(start, '%Y-%m-%d')
# 	end = dt.datetime.strptime(end, '%Y-%m-%d')
# 	diff = start - end
# 	if diff > relativedelta(years=5):
# 		new_date = end - relativedelta(years=5)
# 		dbg('-----------------------------year is gapped!!!!!!!!!!!!!!!!!!!')
# 	else:
# 		new_date = start
# 	new_date = fix_dates(new_date)
# 	return new_date

from datetime import date


def fix_dates(date):
	dt_return = ''
	dbg(date)
	if not date:
		dt_return = '19890413'
	elif len(date) > 10 and type(date) == str:
		dt_return = str(datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date())
		dt_return = re.sub('-', '', dt_return)

	elif len(date) <= 10 and type(date) == str:
		dt_return = re.sub('-', '', date)
	elif type(date) == datetime:
		dt_return = str(datetime(date).date())
		dt_return = re.sub('-', '', dt_return)
	else:
		raise Warning('date fix not applied:' + str(type(date)))
	return dt_return


def to_relativedelta(tdelta):
	return relativedelta(seconds=int(tdelta.total_seconds()),
						 microseconds=tdelta.microseconds)

def delta_15_years(d1,d2):
	d1 = dt.datetime.strptime(d1, '%Y-%m-%d')
	d2 = dt.datetime.strptime(d2, '%Y-%m-%d')
	diff = d1 - d2
	dbg(diff)
	if to_relativedelta(diff) <= relativedelta(years=15):
		return True
	else:
		return False

def check_delta(start, end):
	start = dt.datetime.strptime(start, '%Y-%m-%d')
	end = dt.datetime.strptime(end, '%Y-%m-%d')
	diff = start - end
	if to_relativedelta(diff) >= relativedelta(years=5):
		return 5
	elif to_relativedelta(diff) >= relativedelta(years=3):
		return 3


def subtract_years(start, end, years):
	start = dt.datetime.strptime(start, '%Y-%m-%d')
	end = dt.datetime.strptime(end, '%Y-%m-%d')
	diff = start - end
	if to_relativedelta(diff) > relativedelta(years=years):
		try:
			return end.replace(year=end.year - years)
		except ValueError:
			return end + (date(end.year - years, 1, 1) - date(end.year, 1, 1))


def year_gap(start, end, years):
	# print 'doing year gap' + str(start) + str(end)
	start = dt.datetime.strptime(start, '%Y-%m-%d')
	end = dt.datetime.strptime(end, '%Y-%m-%d')
	diff = end - start
	if to_relativedelta(diff) >= relativedelta(years=years):
		# raise Warning('change dt ' + str(diff))
		# print 'banging a change --------------------------------------'
		new_date = end - relativedelta(years=years)
	else:
		new_date = start
	# new_date = fix_dates(new_date)
	# print type(new_date)
	new_date = datetime.strftime(new_date, '%Y-%m-%d')
	# new_date = str(datetime(new_date).date())
	new_date = re.sub('-', '', new_date)
	# print new_date
	return new_date


def sanitize_email(email):
	email = re.sub(' ', '', email)
	return email


def sanitize_addrs(addr):
	addr = re.sub(";", " ", str(addr))
	addr = re.sub('"', '', str(addr))
	addr = str.strip(str(addr))
	return addr


def remove_zeros_from_string(text):
	"""
	Some people have 0s in their names. This isn't allowed, so just sub them with blanks
	"""
	return re.sub("0", "", text)


def dual_name_removal(text):
	if not text:
		raise Warning('no name brand')
	# print text
	"""
	Some people have two names in the first name field. This isn't allowed, so split it and only return the first part
	"""
	text_split = text.split(" ")
	return text_split[0]


def gender_to_code(gen):
	gender_map = {
		False: "F",
		"female": "F",
		"male": "M",
	}
	return gender_map[gen]


def citizen_map(cit):
	cit_map = {
		False: "U",
		"dual": "D",
		"PR": "PR",
		"unknown": "U",
		"other": "O",
		"sa": "SA",

	}
	try:
		return cit_map[cit]
	except:
		return "U"


def nationality_to_code(nat):
	nat_map = {
		"COLOMBIA": "U",
		"MOZAMBIQUE":"MOZ",
		"South Africa": "SA",
		"sa (DO NOT USE!)": "SA",
		"SA (DO NOT USE!)": "SA",
		"S A (DO NOT USE!)": "SA",
		"SADC except SA": "SDC",
		"Angola": "ANG",
		"Botswana": "BOT",
		"LESOTHO": "LES",
		"MALAWI": "MAL",
		"Malawi": "MAL",
		"Mauritius": "MAU",
		"Mozambique": "MOZ",
		"NAMIBIA": "NAM",
		"Namibia": "NAM",
		"Seychelles": "SEY",
		"SWAZILAND": "SWA",
		"Swaziland": "SWA",
		"Tanzania": "TAN",
		"Zaire": "ZAI",
		"Zambia": "ZAM",
		"ZAMBIA": "ZAM",
		"ZIMBABWE": "ZIM",
		"Asian countries": "AIS",
		"Australia	Oceania	countries": "AUS",
		"European	countries": "EUR",
		"North	American	countries": "NOR",
		"South / Central American": "SOU",
		"Rest	of	Africa": "ROA",
		"NIGERIA": "ROA",
		"CONGO": "ROA",
		"UGANDA": "ROA",
		"Other & rest of Oceania": "OOC",
		'ANGOLA': "U",
		'GHANA': "U",
		'CAMEROON': "U",
		"LAO PEOPLE'S DEMOCRATIC REPUBLIC": "U",
		"COTE D'IVOIRE": "U",
		'AFGHANISTAN': "U",
		False: "U",
		"Unspecified": "U",
		"N / A: Institution": "NOT",
	}
	return nat_map[nat]


# def quaL_status_to_code(status):
# 	quals = {'Re-enrolled':'5',
# 			 ''}

def provider_accredit_status_to_code(pas):
	provider_accredit_status_code_map = {
		"Active": "A",
		"Inactive": "I",
		"Legacy": "L",
		"Provisional": "V",
	}
	return provider_accredit_status_code_map[pas]


def assessor_ind_to_code(ai):
	assessor_ind_map = {
		"Yes": "Y",
		"No": "N",
	}
	return assessor_ind_map[ai]


def part_of_id_to_code(poi):
	part_of_id_map = {
		"Miscellanous stand - alone": 1,
		"(Part of a) Qualification": 2,
		"(Part of a) Learnership": 3,
	}
	return part_of_id_map[poi]


def structure_status_to_code(ss):
	structure_status_map = {
		"Registered": "501",
		"Proposed": "506",
		"Accredited": "510",
		"Reaccredited": "511",
		"De - accredited": "512",
		"Accredited - Provisional": "513",
		"Withdrawn": "514",
		"Unsuccessful": "515",
		"Previously	used in Interim	process": "574",
		"Closed(Legacy)": "575",
	}


def provider_class_to_code(pc):
	provider_class_map = {
		"Unknown": "1",
		"Foreign": "3",
		"Public": "4",
		"Private": "5",
		"Interim(SAQA use only)": "6",
		"NGO / CBO": "7",
		"Mixed: Public and Private": "8",
	}
	return provider_class_map.get(pc, "1")


def provider_type_id_to_code(pti):
	provider_type_map = {
		"2": "Development Enterprise	NGO",
		"3": "Education",
		"4": "Employer",
		"5": "Training",
		"500": "Education and Training",
	}
	provider_type_map = {
		"2": "2",
		"3": "3",
		"4": "4",
		"5": "5",
		"500": "500",
	}
	return provider_type_map.get(pti, "500")


def equity_to_code(eq):
	equity_map = {
		"black_indian": "BI",
		"black_in": "BI",
		"white": "Wh",
		"black_coloured": "BC",
		"block_col": "BC",
		"black_af": "BA",
		"black_african": "BA",
		"black_co": "BC",
		"other": "Oth",
		False: "U",
		None: "U",
		"None": "U",
		"BA": "BA",
		"BC": "BC",
		"BI": "BI",
		"Wh": "Wh",
		"Oth": "Oth",
		"U": "U",
		"unknown": "U",
	}
	return equity_map[eq]


def socio_to_code(soc):
	socio_map = {'Unspecified': "U",
				 False: "U",
				 'unemployed': "02",
				 'Home-maker (not working)': '04',
				 'Pensioner/retired (not w.)': '07',
				 'Not working - disabled': '08',
				 'Not working - no wish to w': '09',
				 'Not working - N.E.C.': '10',
				 'N/A: Institution': '98',
				 'employed': '01',
				 'N/A: aged <15': '97',
				 'Scholar/student (not w.)': '06',
				 'Not working, not looking': '03'}
	return socio_map[soc]


def province_to_code(prov):
	prov_map = {68: "1", 60: "2", 67: "3", 61: "4", 63: "5", 116: "N",
				66: "6", 62: "7", 65: "8", 64: "9", False: "N", None: "N", "None": "N",
				"nan": "N", "na": "N", }
	return prov_map[prov]


def lang_to_code(lang):
	langs = {'English': 'Eng',
			 'isiZulu': 'Zul',
			 'Ndebele': 'Nde',
			 'Afrikaans': 'Afr',
			 'Other': 'Oth',
			 'South African Sign Language': 'SASL',
			 'sePedi': 'Sep',
			 'seSotho': 'Ses',
			 'seTswana': 'Set',
			 'siSwati': 'Swa',
			 'tshivenda': 'Tsh',
			 False: 'U',
			 'Unknown': 'U',
			 'isiXhosa': 'Xho',
			 'xiTsonga': 'Xit',
			 }
	return langs[lang]


def filth_date_gap(start, end):
	if end == '20200331':
		return '20150331'
	else:
		return start


def extract_first_name(name):
	names = name.split(' ')
	if len(names) > 1:
		return names[0]
	else:
		return name


def disability_status_code(ds):
	dsmap = {
		'sight': "01",
		'hearing': "02",
		'communication': '03',
		'physical': '04',
		'intellectual': '05',
		'emotional': '06',
		'multiple': '07',
		'disabled': '09',
		'none': 'N',
	}
	try:
		return dsmap[ds]
	except:
		return "N"


def id_type_to_code(id_type):
	# v = [('saqa_member', '521 - SAQA Member ID'), ('passport_number', '527 - Passport Number'),
	# 	 ('drivers_license', '529 - Drivers License'), ('temporary_id_number', '531 - Temporary ID number'),
	# 	 ('none', '533 - None'), ('unknown', '535 - Unknown'), ('student_number', '537 - Student number'),
	# 	 ('work_permit_number', '538 - Work Permit Number'), ('employee_number', '539 - Employee Number'),
	# 	 ('birth_certificate_number', '540 - Birth Certificate Number'),
	# 	 ('hsrc_register_number', ' 541 - HSRC Register Number'),
	# 	 ('etqe_record_number', '561 - ETQA Record Number'), ('refugee_number', '565 - Refugee Number')]
	# todo: complete missing

	id_type_map = {
		'none': 533,
		'passport_number': 527,
		'refugee_number': 565,
		'drivers_license': 529,
		'temporary_id_number': 531,
		'unknown': 535,
		'student_number': 537,
		'work_permit_number': 538,
		'employee_number': 539,
		'birth_certificate_number': 540,
		'saqa_member': 521,
	}

	return id_type_map.get(id_type, 535)


### FIXES
today = datetime.now()
td_year = today.year
if len(str(today.month)) == 1:
	month = '0' + str(today.month)
else:
	month = str(today.month)
if len(str(today.day)) == 1:
	day = '0' + str(today.day)
else:
	day = str(today.day)
tm = str(td_year)[2:4] + str(month) + str(day)
hm = "HWSE"
dat_names = {
	'21': str(hm) + "21" + str(tm) + ".dat",
	'24': str(hm) + "24" + str(tm) + ".dat",
	'25': str(hm) + "25" + str(tm) + ".dat",
	'26': str(hm) + "26" + str(tm) + ".dat",
	'27': str(hm) + "27" + str(tm) + ".dat",
	'29': str(hm) + "29" + str(tm) + ".dat",
}


def cleanse_date(date):
	"""
	Date will be converted to a string, cut off at 10 characters,
	and any dashes removed.
	"""
	date = str(date)
	date = date[0:10]
	return re.sub("-", "", date)


def cleanse_postcode(postcode):
	"""
	Return default value if the postcode has an issue
	"""
	try:
		if len(abs(postcode)) != 4:
			return "2001"
		else:
			return postcode
	except:
		return "2001"


def strip_string(x):
	"""
	Strip string and return
	"""
	if not x:
		return ''
	return x.strip()


def remove_school(provider_name):
	"""
	Replace invalid keywords with blank and return string

	%FURTHER EDUCATION% or %FETC% or % FET% or % SCHOOL% or % SKOOL% or %TECHNICAL COLLEGE%
	or %TEGNIESE KOLLEGE% or TECHNISA'
	"""
	inv_names = ['FURTHER EDUCATION', 'FETC', 'FET', 'SCHOOL', 'SKOOL', 'TECHNICAL COLLEGE', 'COLLEGE',
				 'TEGNIESE', 'KOLLEGE', 'TECHNISA', 'UNIVERSITY', 'UNIVERSITEIT', 'TECHNIKON', 'TEGNIKON', 'UNISA']

	replacement_list = []
	for inv_name in inv_names:
		if inv_name in provider_name:
			replacement_list.append(inv_name)
		elif inv_name.title() in provider_name:
			replacement_list.append(inv_name.title())
		elif inv_name.upper() in provider_name:
			replacement_list.append(inv_name.upper())
		elif inv_name.lower() in provider_name:
			replacement_list.append(inv_name.lower())
		else:
			return provider_name
		new_name = ""
		for r in replacement_list:
			dbg('------------------------------name had school')
			new_name = re.sub(r, "", new_name)
		return new_name


def province_fix(prov):
	"""
	If there's an illegal province code or bad combination, set to
	N for South Africa National.
	"""
	return "N"


def unix2dos(filename):
	"""
	Convert DAT file to DOS format
	"""
	try:
		os.popen("unix2dos " + filename)
		return True
	except Exception as e:
		return e

# print (dat21_filename,dat24_filename,dat25_filename,dat26_filename,dat27_filename,dat29_filename)
