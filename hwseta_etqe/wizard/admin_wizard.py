# coding=utf-8
from openerp import models, fields, tools, api, _
import datetime
DEBUG = True

if DEBUG:
	import logging

	logger = logging.getLogger(__name__)


	def dbg(msg):
		logger.info(msg)
else:
	def dbg(msg):
		pass


class seta_admin_wizard(models.TransientModel):
	_name = 'seta.admin.wizard'

	@api.one
	def create_historical_wsp_status(self):
		msg = ''
		status_env = self.env['wsp.submission.track']
		parents = [rec.id for rec in self.env['res.partner'].search([('child_employer_ids','!=',False)])]
		wsp_submission_data = status_env.search(
			[('employer_id', 'in', parents)])
		# dbg(wsp_submission_data)
		for wsp_sub in wsp_submission_data:
			# dbg(wsp_sub)
			wsp_sub_dat = wsp_sub.read()
			if wsp_sub_dat:
				parent = self.env['res.partner'].browse(wsp_sub.employer_id.id)
				# raise Warning(wsp_sub_dat)
				for field in wsp_sub_dat[0].keys():
					if type(wsp_sub_dat[0].get(field)) == tuple:
						wsp_sub_dat[0].update({field: wsp_sub_dat[0].get(field)[0]})
				for child in parent.child_employer_ids:
					ok = False
					child_partner = child.employer_id
					if child_partner.id != parent.id:

						for child_stat in child_partner.wsp_submission_ids:
							if child_stat.name == wsp_sub_dat[0].get('name'):
								msg += wsp_sub_dat[0].get('name') + str(child_partner) + str(child_stat.id) + str(wsp_sub) + '\n'
							else:
								ok = True
					if ok:
						# dbg(child_partner)
						wsp_sub_dat[0].update({'employer_id': child_partner.id})
						wsp_submission_data = status_env.create(wsp_sub_dat[0])
						# dbg(wsp_submission_data)
		dbg(msg)

