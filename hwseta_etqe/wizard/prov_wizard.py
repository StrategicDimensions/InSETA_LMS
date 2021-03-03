# coding=utf-8
from openerp import models, fields, tools, api, _
import datetime
DEBUG = False

if DEBUG:
	import logging

	logger = logging.getLogger(__name__)


	def dbg(msg):
		logger.info(msg)
else:
	def dbg(msg):
		pass




class provider_wizard(models.TransientModel):
	_name = 'provider.wizard'

	provider_id = fields.Many2one('res.partner')
	identification = fields.Char()
	ticket_num = fields.Char()
	search_by = fields.Selection(
		[('sdl', 'SDL Number'), ('number', 'Accreditation Number')],string="Search by")
	# status_change = fields.Selection(
	# 	[('Accredited', 'Accredited'), ('Reaccredited', 'Re Accredited')], string="Status")
	status_change = fields.Selection(
		[
			('Reaccredited', 'Reaccredited'),
			('Accredited', 'Accredited'),
			('Active', 'Active'),
			('Expired', 'Expired'),
		], string="Status")

	def get_prov(self,identification):
		dbg("oi oi guv!")
		if identification:
			if self.search_by == 'id':
				prov_obj = self.sudo().env['res.partner'].search([(
						'provider_sars_number', '=', identification),('provider', '=', True)],limit=1)
			elif self.search_by == 'number':
				prov_obj = self.sudo().env['res.partner'].search(
					[('provider_accreditation_num', '=', identification),('provider', '=', True)],limit=1)
			else:
				raise Warning('You need to choose an option in Search by !')
			# check if there was an obj or warn
			if not prov_obj:
				raise Warning("Couldn't find a provider that way")
			else:
				return prov_obj
		else:
			raise Warning('Can\'t find identification!')

	@api.onchange('identification')
	def onchange_get_prov(self):
		dbg("oi oi guv!")
		if self.identification:
			prov_obj = self.get_prov(self.identification)
			self.provider_id = prov_obj.id

	start_date = fields.Date()
	end_date = fields.Date()

	@api.one
	def fix_dates(self):
		if self.identification:
			prov_obj = self.get_prov(self.identification)
			if self.start_date and self.end_date:
				old_start = prov_obj.provider_start_date
				old_end = prov_obj.provider_end_date
				old_status = prov_obj.provider_status_Id
				prov_obj.provider_start_date = self.start_date
				prov_obj.provider_end_date = self.end_date
				prov_obj.provider_status_Id = self.status_change
				msg = "ticket#:%s-%s-provider dates changed-start:%s > %s -end:%s > %s, status changed %s > %s" % (self.ticket_num,str(self.identification),str(old_start),str(self.start_date),str(old_end),str(self.end_date),str(old_status), str(self.status_change))
				if datetime.datetime.strptime(self.end_date, '%Y-%m-%d').date() >= datetime.datetime.today().date():
					if not prov_obj.is_active_provider:
						msg += "-marking as active provider"
						prov_obj.is_active_provider = True
				else:
					if prov_obj.is_active_provider:
						msg += "-marking as in-active provider"
						prov_obj.is_active_provider = False
				# prov_obj.message_post(body=_(msg), type='email',subtype='mail.mt_comment', author_id=self.env.user.partner_id.id)
				template = self.env.ref('hwseta_etqe.email_template_provider_master_data_edit_notification',
										raise_if_not_found=False)
				if template:
					if template.write({'body_html': msg,'email_from':self.env.user.partner_id.email}):
						template.send_mail(prov_obj.id,force_send=True)
			else:
				raise Warning('please ensure dates are filled!')
