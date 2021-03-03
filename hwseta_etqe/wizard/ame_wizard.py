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




class assessor_morderator_ame_wizard(models.TransientModel):
	_name = 'assessor.moderator.ame.wizard'

	assessor_id = fields.Many2one('hr.employee')
	moderator_id = fields.Many2one('hr.employee')
	assessor_or_moderator = fields.Selection([('a','Assessor'),('m','Moderator')])
	identification = fields.Char()
	ticket_num = fields.Char()
	search_by = fields.Selection(
		[('id', 'Identification Nmber'), ('number', 'Registration Number')],string="Search by")

	def get_am(self,identification):
		dbg("oi oi guv!")
		if identification:
			if self.assessor_or_moderator == 'a':
				if self.search_by == 'id':
					ass_mod_obj = self.sudo().env['hr.employee'].search([(
						'assessor_moderator_identification_id', '=', identification)],limit=1)
				elif self.search_by == 'number':
					ass_mod_obj = self.sudo().env['hr.employee'].search(
						[('assessor_seq_no', '=', identification),('is_assessors', '=', True)],limit=1)
				else:
					raise Warning('You need to choose an option in Search by !')
				# check if there was an obj or warn
				if not ass_mod_obj:
					raise Warning("Couldn't find an assessor that way")
				else:
					return "a",ass_mod_obj
			elif self.assessor_or_moderator == 'm':
				if self.search_by == 'id':
					ass_mod_obj = self.sudo().env['hr.employee'].search([
							('assessor_moderator_identification_id', '=', identification)],limit=1)
				elif self.search_by == 'number':
					ass_mod_obj = self.sudo().env['hr.employee'].search(
						[('moderator_seq_no', '=', identification),('is_moderators', '=', True)],limit=1)
				else:
					raise Warning('You need to choose an option in Search by !')
				# check if there was an obj or warn
				if not ass_mod_obj:
					raise Warning("Couldn't find an moderator that way")
				else:
					return "m",ass_mod_obj
			else:
				raise Warning('you need to choose "a" or "m" for assessors or moderators!')

	@api.onchange('identification')
	def onchange_get_am(self):
		dbg("oi oi guv!")
		if self.identification:
			a_or_m, am_obj = self.get_am(self.identification)
			if a_or_m == "a":
				self.assessor_id = am_obj.id
			elif a_or_m == "m":
				self.moderator_id = am_obj.id
			else:
				pass #raise Warning("something went wrong")

	start_date = fields.Date()
	end_date = fields.Date()
	work_email = fields.Char()

	@api.one
	def fix_email(self):
		if self.identification:
			a_or_m, am_obj = self.get_am(self.identification)
			if a_or_m == "a" or a_or_m == "m":
				if self.work_email:
					old_email = am_obj.work_email
					am_obj.work_email = self.work_email
					user_obj = self.env['res.users'].search([('assessor_moderator_id','=',am_obj.id)])
					user_obj.login = self.work_email
					partner_id = user_obj.partner_id.id
					partner_obj = self.env['res.partner'].search([('id','=',partner_id)])
					partner_obj.email = self.work_email
					msg = "ticket#:%s-%s-assessor email changed-email:%s > %s" % (self.ticket_num,str(self.identification),str(old_email),str(self.work_email))
					template = self.env.ref('hwseta_etqe.email_template_master_data_edit_notification',
											raise_if_not_found=False)
					if template:
						if template.write({'body_html': msg,'email_from':self.env.user.partner_id.email}):
							template.send_mail(am_obj.id,force_send=True)
				else:
					raise Warning('please ensure email is filled!')
			else:
				raise Warning("something went wrong")

