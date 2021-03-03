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




class assessor_morderator_wizard(models.TransientModel):
	_name = 'assessor.moderator.wizard'

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
				raise Warning("something went wrong")

	start_date = fields.Date()
	end_date = fields.Date()
	moderator_start_date = fields.Date()
	moderator_end_date = fields.Date()

	@api.one
	def fix_dates(self):
		if self.identification:
			a_or_m, am_obj = self.get_am(self.identification)
			if a_or_m == "a":
				if self.start_date and self.end_date:
					old_start = am_obj.start_date
					old_end = am_obj.end_date
					am_obj.start_date = self.start_date
					am_obj.end_date = self.end_date
					msg = "ticket#:%s-%s-assessor dates changed-start:%s > %s -end:%s > %s" % (self.ticket_num,str(self.identification),str(old_start),str(self.start_date),str(old_end),str(self.end_date))
					if datetime.datetime.strptime(self.end_date, '%Y-%m-%d').date() >= datetime.datetime.today().date():
						if not am_obj.is_active_assessor:
							msg += "-marking as active assessor"
							am_obj.is_active_assessor = True
					else:
						if am_obj.is_active_assessor:
							msg += "-marking as in-active assessor"
							am_obj.is_active_assessor = False
					# am_obj.message_post(body=_(msg), type='email',subtype='mail.mt_comment', author_id=self.env.user.partner_id.id)
					template = self.env.ref('hwseta_etqe.email_template_master_data_edit_notification',
											raise_if_not_found=False)
					if template:
						if template.write({'body_html': msg,'email_from':self.env.user.partner_id.email}):
							template.send_mail(am_obj.id,force_send=True)
				else:
					raise Warning('please ensure dates are filled!')
			elif a_or_m == "m":
				if self.moderator_start_date and self.moderator_end_date:
					old_start = am_obj.moderator_start_date
					old_end = am_obj.moderator_end_date
					am_obj.moderator_start_date = self.moderator_start_date
					am_obj.moderator_end_date = self.moderator_end_date
					msg = "ticket#:%s-moderator dates changed \n start %s > %s \n end %s > %s" % (self.ticket_num,
					str(old_start), str(self.moderator_start_date), str(old_end), str(self.moderator_end_date))
					if datetime.datetime.strptime(self.moderator_end_date, '%Y-%m-%d').date() >= datetime.datetime.today().date():
						if not am_obj.is_active_moderator:
							msg += "-marking as active moderator"
							am_obj.is_active_moderator = True
					else:
						if am_obj.is_active_moderator:
							msg += "-marking as in-active moderator"
							am_obj.is_active_moderator = False
					# am_obj.message_post(body=_(msg), type='email',subtype='mail.mt_comment', author_id=self.env.user.partner_id.id)
					template = self.env.ref('hwseta_etqe.email_template_master_data_edit_notification', raise_if_not_found=False)
					if template:
						if template.write({'body_html': msg,'email_from':self.env.user.partner_id.email}):
							template.send_mail(am_obj.id,force_send=True)
				else:
					raise Warning('please ensure dates are filled!')
			else:
				raise Warning("something went wrong")

