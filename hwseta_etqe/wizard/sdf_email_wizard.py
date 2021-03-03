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




class sdf_email_wizard(models.TransientModel):
	_name = 'sdf.email.wizard'

	sdf_id = fields.Many2one('hr.employee')
	identification = fields.Char()
	ticket_num = fields.Char()
	search_by = fields.Selection(
		[('id', 'Identification Nmber')],string="Search by")

	def get_sdf(self,identification):
		dbg("oi oi guv!")
		if identification:
			sdf_obj = self.sudo().env['hr.employee'].search([('identification_id','=',self.identification)])
			return sdf_obj
		else:
			raise Warning('You need an SDF ID!')

	@api.onchange('identification')
	def onchange_get_sdf(self):
		dbg("oi oi guv!")
		if self.identification:
			self.sdf_id = self.get_sdf(self.identification)
		else:
			pass #raise Warning("something went wrong")

	start_date = fields.Date()
	end_date = fields.Date()
	work_email = fields.Char()

	@api.one
	def fix_email(self):
		if self.identification:
			sdf_obj = self.get_sdf(self.identification)
			if sdf_obj:
				if self.work_email:
					old_email = sdf_obj.work_email
					sdf_obj.work_email = self.work_email
					user_obj = self.env['res.users'].search([('sdf_id','=',sdf_obj.id)])
					user_obj.login = self.work_email
					partner_id = user_obj.partner_id.id
					partner_obj = self.env['res.partner'].search([('id','=',partner_id)])
					partner_obj.email = self.work_email
					msg = "ticket#:%s-%s-sdf email changed-email:%s > %s" % (self.ticket_num,str(self.identification),str(old_email),str(self.work_email))
					template = self.env.ref('hwseta_etqe.email_template_master_data_edit_notification',
											raise_if_not_found=False)
					if template:
						if template.write({'body_html': msg,'email_from':self.env.user.partner_id.email}):
							template.send_mail(sdf_obj.id,force_send=True)
				else:
					raise Warning('please ensure email is filled!')
			else:
				raise Warning("something went wrong")

