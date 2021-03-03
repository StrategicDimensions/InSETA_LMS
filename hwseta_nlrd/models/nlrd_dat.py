# coding=utf-8
from collections import OrderedDict as OD
import re
import os

DEBUG = True
# DEBUG = False

if DEBUG:
	import logging

	logger = logging.getLogger(__name__)


	def dbg(msg):
		logger.info(msg)
else:
	def dbg(msg):
		pass
"""
load specifications (DAT)
"""
unimap = {
		"ß": "b", "à": "a", "á": "a", "â": "a", "ã": "a", "ä": "a", "å": "a", "æ": "ae", "ç": "c",
		"è": "e", "é": "e", "ê": "e", "ë": "e", "ì": "i", "í": "i", "î": "i", "ï": "i", "ð": "o",
		"ñ": "n", "ò": "o", "ó": "o", "ô": "o", "õ": "o", "ö": "o", "ø": "o", "ù": "u", "ú": "u",
		"û": "u", "ü": "u", "ý": "y", "þ": "b", "ÿ": "y", }
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
# file widths
dat21 = [[20, 10, 10, 128, 10, 50, 50, 50, 4, 20, 20, 20, 50, 50, 20, 20, 20,
		  8, 8, 20, 10, 10, 2, 4, 3, 2, 6, 2, 2, 6, 50, 50, 50, 4, 50, 8, ],
		 ['Provider_Code',
		  'Etqa_Id',
		  # ensure about blank being allowed
		  'Std_Industry_Class_Code',
		  'Provider_Name',
		  'Provider_Type_Id',
		  'Provider_Address_1',
		  'Provider_Address_2',
		  'Provider_Address_3',
		  'Provider_Postal_Code',
		  'Provider_Phone_Number',
		  'Provider_Fax_Number',
		  'Provider_Sars_Number',
		  'Provider_Contact_Name',
		  'Provider_Contact_Email_Address',
		  'Provider_Contact_Phone_Number',
		  'Provider_Contact_Cell_Number',
		  'Provider_Accreditation_Num',
		  'Provider_Accredit_Start_Date',
		  'Provider_Accredit_End_Date',
		  'Etqa_Decision_Number',  # blank
		  'Provider_Class_Id',  # blanket
		  'Structure_Status_Id',  # blanket
		  'Province_Code',
		  'Country_Code',
		  'Latitude_Degree',  # blank
		  'Latitude_Minutes',  # blank
		  'Latitude_Seconds',  # blank
		  'Longitude_Degree',  # blank
		  'Longitude_Minutes',  # blank
		  'Longitude_Seconds',  # blank
		  'Provider_Physical_Address_1',  # blank
		  'Provider_Physical_Address_2',  # blank
		  'Provider_Physical_Address_Town',  # blank
		  'Provider_Phys_Address_Postcode',  # blank
		  'Provider_Web_Address',  # blank
		  'Date_Stamp', ]]

# dat24 = [10, 10, 10, 20, 10, 20, 1, 8, 8, 20, 10, 8, ]
dat24 = [[10, 10, 10, 20, 10, 20, 1, 8, 8, 20, 10, 8, ], ['Learnership_Id',
														  'Qualification_Id',
														  'Unit_Standard_Id',  # maybe later
														  'Provider_Code',
														  'Provider_Etqa_Id',  # blanket
														  'Provider_Accreditation_Num',
														  'Provider_Accredit_Assessor_Ind',  # blank
														  'Provider_Accred_Start_Date',
														  'Provider_Accred_End_Date',
														  'Etqa_Decision_Number',  # blank
														  'Provider_Accred_Status_Code',
														  'Date_Stamp', ]]

dat25 = [[15, 20, 3, 10, 3, 10, 1, 10, 2, 10, 45, 26, 50, 10, 8, 50, 50, 50, 50, 50,
		  50, 4, 4, 20, 20, 20, 50, 2, 20, 10, 45, 20, 3, 20, 10, 2, 2, 2, 2, 2, 2, 8, ], ['National_Id',  # c
																							   'Person_Alternate_Id',
																							   'Alternate_Id_Type',
																							   'Equity_Code',  # y
																							   'Nationality_Code',  # y
																							   'Home_Language_Code',
																							   'Gender_Code',  # y
																							   'Citizen_Resident_Status_Code',
																							   'Socioeconomic_Status_Code',
																							   'Disability_Status_Code',
																							   'Person_Last_Name',  # y
																							   'Person_First_Name',  # y
																							   'Person_Middle_Name',
																							   'Person_Title',
																							   'Person_Birth_Date',
																							   'Person_Home_Address_1',
																							   'Person_Home_Address_2',
																							   'Person_Home_Address_3',
																							   'Person_Postal_Address_1',
																							   'Person_Postal_Address_2',
																							   'Person_Postal_Address_3',
																							   'Person_Home_Addr_Postal_Code',
																							   'Person_Postal_Addr_Post_Code',
																							   'Person_Phone_Number',
																							   'Person_Cell_Phone_Number',
																							   'Person_Fax_Number',
																							   'Person_Email_Address',
																							   'Province_Code',  # y
																							   'Provider_Code',  # c
																							   'Provider_Etqa_Id',
																							   'Person_Previous_Provider_Lastname',
																							   'Person_Previous_Alternate_Id',
																							   'Person_Previous_Alternate_Id_Type',
																							   'Person_Previous_Provider_Code',
																							   'Person_Previous_Provider_Etqe_Id',
																							   'Seeing_Rating_Id',
																							   'Hearing_Rating_Id',
																							   'Communicating_Rating_Id',
																							   'Walking_Rating_Id',
																							   'Remembering_Rating_Id',
																							   'Self_Care_Rating_Id',
																							   'Date_Stamp',  # y
																							   ]]

dat26 = [[15, 20, 3, 5, 20, 10, 8, 8, 10, 20, 20, 10, 8, ], ['National_Id',
															 'Person_Alternate_Id',
															 'Alternate_Type_Id',
															 'Designation_Id',  # blanket
															 'Designation_Registration_Number',
															 'Designation_Etqa_Id',  # blanket
															 'Designation_Start_Date',
															 'Designation_End_Date',
															 'Structure_Status_Id',  # blanket
															 'Etqa_Decision_Number',  # blank
															 'Provider_Code',
															 'Provider_Etqa_Id',
															 'Date_Stamp', ]]

dat27 = [[10, 10, 10, 5, 20, 10, 8, 8, 20, 10, 8, ], ['Learnership_Id',
													  'Qualification_Id',
													  'Unit_Standard_Id',
													  'Designation_Id',  # blanket req
													  'Designation_Registration_Number',  # req
													  'Designation_Etqa_Id',  # req blanket
													  'Nqf_Designation_Start_Date',  # req
													  'Nqf_Designation_End_Date',  # req
													  'Etqa_Decision_Number',
													  'Nqf_Desig_Status_Code',  # req
													  'Date_Stamp',  # req
													  ]]

dat29 = [[15, 20, 3, 10, 3, 20, 3, 8, 8, 3, 2, 10, 20, 10, 10, 8, 8, ], ['national_id',
																		 'person_alternate_id',
																		 'alternate_id_type',
																		 'qualification_id',
																		 'learner_achievement_status_id',
																		 'assessor_registration_number',
																		 'learner_achievement_type_id',
																		 # todo: find or pass flat value 6 is  other
																		 'learner_achievement_date',
																		 # todo:needs eval based on learner_achievement_type_id
																		 'learner_enrolled_date',
																		 'honours_classification',  # not req
																		 'part_of',
																		 'learnership_id',  # not req
																		 'provider_code',
																		 'provider_etqa_id',  # blanket
																		 'assessor_etqa_id',  # blanket
																		 'certification_date',
																		 'date_stamp', ]]
"""
The example dictionary below contains the same structure as the actual dictionaries
Odoo passes to the create function.
"""

example_val = OD({
	"National_Id": "8510105114085",
	"Person_Alternate_Id": "",
	"Alternate_Type_Id": "533",
	"Designation_Id": "1",  # blanket
	"Designation_Registration_Number": "HW591AR1677",
	"Designation_Etqa_Id": "591",  # blanket
	"Designation_Start_Date": "20171201",
	"Designation_End_Date": "20200331",
	"Structure_Status_Id": "501",  # blanket
	"Etqa_Decision_Number": "",  # blank
	"Provider_Code": "778631",
	"Provider_Etqa_Id": "591",
	"Date_Stamp": "20180101",
	"assessor_id": "101147",
})


def gendat(vald, lens, fields_list, datfile_name):
	"""
	This will take each dictionary and create a dat file.

	Usage will be:

	from nlrd_dat import gendat

	gendat(the_dictionary_that_gets_passed_to_create, lengths_according_to_nlrd, name_of_dat_file)

	One thing to note though, the list that gets generated by the list() function below
	may end up being in the wrong order unless we use OrderedDictionaries. Luckily, these
	are in the collections module in the standard library and Odoo should not have difficulty
	handling them as if they were normal dictionaries.
	"""

	fmt = ""
	endtup = []
	vall = list(vald.values())

	for x in range(0, len(lens)):

		fmt += "%-*s"
		endtup.append(lens[x])

		# if len(lens) != len(vall):
		# 	raise AssertionError('field length and length list are not same len ' + str(len(lens)) + str(len(vall)))
		try:
			if not vald[fields_list[x]]:
				endtup.append(''[0:lens[x]])
			elif type(vald[fields_list[x]]) == int:
				valu = vald[fields_list[x]]
				valu = valu.encode("ascii")
				endtup.append(str(valu)[0:lens[x]])
			# if lambda a, d: any(k in a for k in d):
			else:
				valu = vald[fields_list[x]]
				valu = valu.encode("ascii")
				endtup.append(valu[0:lens[x]])
			dbg(len(fields_list))
			dbg(len(endtup))
		except UnicodeEncodeError:
			if not vald[fields_list[x]]:
				endtup.append(''[0:lens[x]])
			elif type(vald[fields_list[x]]) == int:
				valu = vald[fields_list[x]]
				endtup.append(str(valu)[0:lens[x]])
			# if lambda a, d: any(k in a for k in d):
			else:
				valu = "CHEESE"
				endtup.append(valu[0:lens[x]])
			dbg(len(fields_list))
			dbg(len(endtup))

	dbg(endtup)
	fmt += "\r\n"
	try:
		with open("/var/log/odoo/nlrd_dat_files/"+datfile_name, 'a') as f:
			f.write(fmt % tuple(endtup))
	except IOError:
		with open("/var/log/odoo/nlrd_dat_files/"+datfile_name, 'w') as f:
			f.write(fmt % tuple(endtup))

# test code, comment it out so the std out doesn't get dirty
# print(gendat(example_val, [20,20,20,20,30,30,30,30,20,20,20,20,40,40],"nlrd.dat"))
# print(gendat(example_val, dat26,"nlrd1.dat"))
