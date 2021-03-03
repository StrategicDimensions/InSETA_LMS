from openerp import fields, models, api, _
from openerp.osv import osv
import calendar
from .. import checkers
DEBUG = True

if DEBUG:
	import logging

	logger = logging.getLogger(__name__)


	def dbg(msg):
		logger.info(msg)
else:
	def dbg(msg):
		pass
# todo:remove this record rule from live when using 	base.res_partner_portal_public_rule

class link_stakeholder(models.TransientModel):
	_name = 'link.stakeholder'

	def _default_provider(self):
		dbg('_default_provider')
		user = self.env.user
		partner = user.partner_id
		if partner.provider and not self.provider_id:
			# self.provider_id = partner
			return partner

	def _default_assessor(self):
		dbg('_default_assessor')
		user = self.env.user
		# if self.identification_id:
		# 	dbg('if self.identification_id:')
		# 	if self.search_by == 'id':
		# 		dbg("if self.search_by == 'id':")
		# 		if self.assessor_or_moderator == 'assessor':
		# 			dbg("if self.assessor_or_moderator == 'assessor':")
		# 			ass_mod_obj = self.sudo().env['hr.employee'].search([('is_active_assessor', '=', True), (
		# 				'assessor_moderator_identification_id', '=', self.identification_id)])
		# 			return ass_mod_obj
		# todo: see if there is a fkey to hr.employee. for now we will use an inverse search (not efficient)
		ass = self.env['hr.employee'].search([('user_id','=',user.id),('is_assessors','=',True)])
		dbg(ass)
		if ass and not self.assessor_id:
			dbg("ass and not self assessor")
			return ass

	def _default_moderator(self):
		dbg('_default_moderator')
		user = self.env.user
		# if self.identification_id:
		# 	dbg('if self.identification_id:')
		# 	if self.search_by == 'id':
		# 		dbg("if self.search_by == 'id':")
		# 		if self.assessor_or_moderator == 'moderator':
		# 			dbg("elif self.assessor_or_moderator == 'moderator':")
		# 			ass_mod_obj = self.sudo().env['hr.employee'].search([('is_active_moderator', '=', True), (
		# 				'assessor_moderator_identification_id', '=', self.identification_id)])
		# 			return ass_mod_obj
		# todo: see if there is a fkey to hr.employee. for now we will use an inverse search (not efficient)
		mod = self.env['hr.employee'].search([('user_id', '=', user.id), ('is_moderators', '=', True)])
		if mod and not self.moderator_id:
			return mod

	def _default_assessor_or_moderator(self):
		user = self.env.user
		partner = user.partner_id
		if not partner.provider:
			return 'provider'

	provider_id = fields.Many2one('res.partner',default=_default_provider, ondelete='cascade')
	# provider_id = fields.Many2one('res.partner',default=lambda self:self.env.user.partner_id, ondelete='cascade')
	assessor_id = fields.Many2one('hr.employee',default=_default_assessor)
	moderator_id = fields.Many2one('hr.employee',default=_default_moderator)
	assessor_or_moderator = fields.Selection([('assessor', 'Assessor'), ('moderator', 'Moderator'), ('provider', 'Provider')],default=_default_assessor_or_moderator)

	work_phone = fields.Char('Work Phone', readonly=False, size=10)
	work_email = fields.Char('Work Email', size=240)
	sla_document = fields.Many2one('ir.attachment', string="SLA Document")
	notification_letter = fields.Many2one('ir.attachment', string="Notification Letter")

	status = fields.Selection([('draft', 'Draft'), ('waiting_approval', 'Waiting Approval'), ('approved', 'Approved'),
							   ('rejected', 'Rejected')], string="Status", default='draft')
	search_by = fields.Selection([('id', 'Identification No'), ('number', 'Assessor/Moderator Number'), ('sdl', 'Provider SDL Number'), ('prov_acc', 'Provider Accreditation Number')],
								 string="Search by")
	identification_id = fields.Char()

	@api.onchange('identification_id')
	def onchange_identification_id(self):
		dbg("onchange_identification_id")
		if self.identification_id:
			if self.search_by == 'id':
				identification_id = self.identification_id
				check = checkers.said_check(identification_id)
				year = check['year']
				month = check['month']
				day = check['day']
				dbg(check)
				dbg(checkers.old_said_check(identification_id))
				if not check['valid']:
					# raise Warning('not valid' + str(check))
					if "Invalid gender" in checkers.old_said_check(identification_id):
						return {
							# 'value': {'is_existing_learner': False, 'citizen_status': '',
							# 		  'onchange_identification_number': ''},
							'warning': {'title': 'Invalid Identification Number',
										'message': 'Invalid Gender!'}}
					if "Invalid citizenship status" in checkers.old_said_check(identification_id):
						return {
							# 'value': {'is_existing_learner': False, 'citizen_status': '',
							# 		  'onchange_identification_number': ''},
							'warning': {'title': 'Invalid Identification Number',
										'message': 'Invalid citizenship status!'}}
					# if "Invalid birth date" in checkers.old_said_check(identification_id):
					if int(day) > 31 or int(day) < 1:
						return {
							# 'value': {'identification_id': ''},
							'warning': {'title': 'Invalid Identification Number',
										'message': 'Incorrect Day In Identification Number!'}}
					if int(month) > 12 or int(month) < 1:
						return {
							# 'value': {'identification_id': ''},
							'warning': {'title': 'Invalid Identification Number',
										'message': 'Incorrect Month In Identification Number!'}}
					else:
						# # Calculating last day of month.
						x_year = int(year)
						if x_year == 00:
							x_year = 2000
						last_day = calendar.monthrange(int(x_year), int(month))[1]
						if int(day) > last_day:
							return {
								# 'value': {'identification_id': ''},
								'warning': {'title': 'Invalid Identification Number',
											'message': 'Incorrect last day of month in identification number!'}}
					# if you get here and nothin has been returned yet, it means the checksum must be the issue so raise it
					return {'value': {'identification_id': ''},
							'warning': {'title': 'Invalid Identification Number',
										'message': 'Incorrect checksum!'}}
				dbg('if self.identification_id:')
				dbg("if self.search_by == 'id':")
				if self.assessor_or_moderator == 'assessor':
					dbg("if self.assessor_or_moderator == 'assessor':")
					ass_mod_obj = self.sudo().env['hr.employee'].search([('is_active_assessor', '=', True), (
						'assessor_moderator_identification_id', '=', self.identification_id)])
					self.assessor_id = ass_mod_obj.id
					self.work_email = ass_mod_obj.work_email
					self.work_phone = ass_mod_obj.person_cell_phone_number
				elif self.assessor_or_moderator == 'moderator':
					dbg("elif self.assessor_or_moderator == 'moderator':")
					ass_mod_obj = self.sudo().env['hr.employee'].search([('is_active_moderator', '=', True), (
						'assessor_moderator_identification_id', '=', self.identification_id)])
					self.moderator_id = ass_mod_obj.id
					self.work_email = ass_mod_obj.work_email
					self.work_phone = ass_mod_obj.person_cell_phone_number
				else:
					raise Warning(_('please select which partner to search. (assessor or moderator)'))
			elif self.search_by == 'number':
				dbg("elif self.search_by == 'number':")
				if self.assessor_or_moderator == 'assessor':
					dbg("if self.assessor_or_moderator == 'assessor':")
					ass_mod_obj = self.sudo().env['hr.employee'].search(
						[('is_active_assessor', '=', True), ('assessor_seq_no', '=', self.identification_id),
						 ('is_assessors', '=', True)])
					dbg(ass_mod_obj)
					self.assessor_id = ass_mod_obj.id
					self.work_email = ass_mod_obj.work_email
					self.work_phone = ass_mod_obj.person_cell_phone_number
				elif self.assessor_or_moderator == 'moderator':
					dbg("elif self.assessor_or_moderator == 'moderator':")
					ass_mod_obj = self.sudo().env['hr.employee'].search(
						[('is_active_moderator', '=', True), ('moderator_seq_no', '=', self.identification_id),
						 ('is_moderators', '=', True)])
					self.moderator_id = ass_mod_obj.id
					self.work_email = ass_mod_obj.work_email
					self.work_phone = ass_mod_obj.person_cell_phone_number
				else:
					raise Warning(_('please select which partner to search. (assessor or moderator)'))
			elif self.search_by == 'sdl':
				dbg("elif self.search_by == 'sdl':")
				if self.assessor_or_moderator == 'provider':
					dbg("if self.assessor_or_moderator == 'provider':")
					prov_obj = self.sudo().env['res.partner'].search(
						[('provider_sars_number', '=', self.identification_id),('provider', '=', True)])
					dbg(prov_obj)
					self.provider_id = prov_obj.id
					self.work_email = prov_obj.email
					self.work_phone = prov_obj.mobile
				else:
					raise Warning(_('please select which provider to search.'))
			elif self.search_by == 'prov_acc':
				dbg("elif self.search_by == 'prov_acc':")
				if self.assessor_or_moderator == 'provider':
					dbg("if self.assessor_or_moderator == 'provider':")
					prov_obj = self.sudo().env['res.partner'].search(
						[('provider_accreditation_num', '=', self.identification_id),('provider', '=', True)])
					dbg(self)
					# self.write({'provider_id':prov_obj.id,'work_email':prov_obj.email,'work_phone':prov_obj.mobile}) dont use search
					self.provider_id = prov_obj.id
					dbg(self.provider_id)
					self.work_email = prov_obj.email
					self.work_phone = prov_obj.mobile
				else:
					raise Warning(_('please select which provider to search.'))
			else:
				raise Warning(_('Assessor/Moderator not found using this number'))

	@api.one
	def link_assessor_moderator(self):
		dbg("link_assessor_moderator")
		user = self.env.user
		# partner = user.partner_id
		# partner = self.provider_id
		partner = self.env['res.partner'].browse(self.provider_id.id)
		if self.assessor_or_moderator == 'assessor':
			if self.search_by == 'id':
				ass_obj = self.sudo().env['hr.employee'].search([('is_active_assessor', '=', True), (
					'assessor_moderator_identification_id', '=', self.identification_id)])
			elif self.search_by == 'number':
				ass_obj = self.sudo().env['hr.employee'].search(
					[('is_active_assessor', '=', True), ('assessor_seq_no', '=', self.identification_id),
						('is_assessors', '=', True)])
			elif self.assessor_id:
				ass_obj = self.assessor_id
			else:
				raise Warning(_("cant find an assessor under this context, contact admin"))
			if ass_obj:
				dbg(partner)
				new_ass_dict = {'assessors_id': ass_obj.id,
								'search_by': self.search_by,
								'identification_id': self.identification_id,
								'awork_email': self.work_email,
								'awork_phone': self.work_phone,
								'assessor_sla_document': self.sla_document.id,
								'assessor_notification_letter': self.notification_letter.id,
								'creator': user.id,
								'status': 'requested',
								}
				ass_list = [(0, 0, new_ass_dict)]
				# dbg()
				partner.write({'assessors_ids': ass_list})
				new_prov_dict = {'provider_id': partner.id,
								 'provider_accreditation_num': partner.provider_accreditation_num,
								 'employer_sdl_no': partner.provider_sars_number,
								 }
				prov_list = [(0, 0, new_prov_dict)]
				ass_obj.write({'as_provider_rel_id': prov_list})
				dbg(ass_list)
				dbg(prov_list)
		elif self.assessor_or_moderator == 'moderator':
			if self.search_by == 'id':
				mod_obj = self.sudo().env['hr.employee'].search([('is_active_moderator', '=', True), (
					'assessor_moderator_identification_id', '=', self.identification_id)])
			elif self.search_by == 'number':
				mod_obj = self.sudo().env['hr.employee'].search(
					[('is_active_moderator', '=', True), ('moderator_seq_no', '=', self.identification_id),
						('is_moderators', '=', True)])
			elif self.moderator_id:
				mod_obj = self.moderator_id
			else:
				raise Warning(_("cant find a moderator under this context, contact admin"))
			if mod_obj:
				new_mod_dict = {'moderators_id': mod_obj.id,
								'identification_id': self.identification_id,
								'search_by': self.search_by,
								'mwork_email': self.work_email,
								'mwork_phone': self.work_phone,
								'moderator_sla_document': self.sla_document.id,
								'moderator_notification_letter': self.notification_letter.id,
								'creator': user.id,
								'status': 'requested',
								}
				mod_list = [(0, 0, new_mod_dict)]
				partner.write({'moderators_ids': mod_list})
				new_prov_dict = {'provider_id': partner.id,
								 'provider_accreditation_num': partner.provider_accreditation_num,
								 'employer_sdl_no': partner.provider_sars_number,
								 }
				prov_list = [(0, 0, new_prov_dict)]
				mod_obj.write({'mo_provider_rel_id': prov_list})
		else:
			raise Warning(_("You need to select a search by option before continuing"))

	@api.one
	def link_provider(self):
		dbg('link_provider')
		user = self.env.user
		dbg(self.provider_id)
		dbg(self.assessor_id)
		dbg(self._context)
		# dbg(self.read())
		prov_obj = ''
		if not self.provider_id:
			if self.search_by == 'sdl':
				dbg("elif self.search_by == 'sdl':")
				if self.assessor_or_moderator == 'provider':
					dbg("if self.assessor_or_moderator == 'provider':")
					prov_obj = self.sudo().env['res.partner'].search(
						[('provider_sars_number', '=', self.identification_id), ('provider', '=', True)])
			elif self.search_by == 'prov_acc':
				dbg("elif self.search_by == 'prov_acc':")
				if self.assessor_or_moderator == 'provider':
					dbg("if self.assessor_or_moderator == 'provider':")
					prov_obj = self.sudo().env['res.partner'].search(
						[('provider_accreditation_num', '=', self.identification_id), ('provider', '=', True)])
			else:
				raise Warning('cant get provider info, please contact system admin')
		else:
			prov_obj = self.provider_id
		if prov_obj:
			if self.assessor_id:
				dbg('both peeps')
				assessor_obj = self.assessor_id
				new_ass_dict = {'assessors_id': self.assessor_id.id,
								# 'search_by': self.search_by, #dont use this, you will get incorrect values
								'identification_id': self.identification_id,
								'awork_email': self.work_email,
								'awork_phone': self.work_phone,
								'assessor_sla_document': self.sla_document.id,
								'assessor_notification_letter': self.notification_letter.id,
								'creator': user.id,
								'status': 'requested',
								}
				ass_list = [(0, 0, new_ass_dict)]
				dbg(ass_list)
				prov_obj.write({'assessors_ids': ass_list})
				# dbg(prov_obj.assessors_ids.read())
				# raise Warning()
				new_prov_dict = {'provider_id': prov_obj.id,
								 'provider_accreditation_num': prov_obj.provider_accreditation_num,
								 'employer_sdl_no': prov_obj.provider_sars_number,
								 'create_uid': user.id,
								 }
				prov_list = [(0, 0, new_prov_dict)]
				assessor_obj.write({'as_provider_rel_id': prov_list})
			if self.moderator_id:
				dbg('both peeps')
				moderator_obj = self.moderator_id
				new_mod_dict = {'moderators_id': self.moderator_id.id,
								# 'search_by': self.search_by, #dont use this, you will get incorrect values
								'identification_id': self.identification_id,
								'mwork_email': self.work_email,
								'mwork_phone': self.work_phone,
								'moderator_sla_document': self.sla_document.id,
								'moderator_notification_letter': self.notification_letter.id,
								'creator': user.id,
								'status': 'requested',
								}
				ass_list = [(0, 0, new_mod_dict)]
				# dbg()
				prov_obj.write({'moderators_ids': ass_list})
				new_prov_dict = {'provider_id': prov_obj.id,
								 'provider_accreditation_num': prov_obj.provider_accreditation_num,
								 'employer_sdl_no': prov_obj.provider_sars_number,
								 'create_uid': user.id,
								 }
				prov_list = [(0, 0, new_prov_dict)]
				moderator_obj.write({'mo_provider_rel_id': prov_list})
		# raise Warning(_('bleh'))


class etqe_assessors_provider_rel(models.Model):
	_inherit = 'etqe.assessors.provider.rel'

	creator = fields.Many2one('res.users')

	@api.multi
	def assessor_approved_request(self):
		user = self.env.user
		if self.creator == user:
			raise osv.except_osv(_('Permission Error'), _(
				"you cant approve a request created by yourself, please ask the provider to approve."))
		else:
			self.write({'status':'waiting_approval', 'request_send':True})

	@api.multi
	def provider_approved_request(self):
		user = self.env.user
		if self.creator == user:
			raise osv.except_osv(_('Permission Error'), _(
				"you cant approve a request created by yourself, please ask the assessor to approve."))
		else:
			self.write({'status': 'waiting_approval', 'request_send': True})

	@api.multi
	def assessor_rejected_request(self):
		self.write({'status':'rejected', 'reject_request':True})


class etqe_moderators_provider_rel(models.Model):
	_inherit = 'etqe.moderators.provider.rel'

	creator = fields.Many2one('res.users')

	@api.multi
	def moderator_approved_request(self):
		user = self.env.user
		if self.creator == user:
			raise osv.except_osv(_('Permission Error'), _(
				"you cant approve a request created by yourself, please ask the provider to approve."))
		else:
			self.write({'status':'waiting_approval', 'request_send':True})

	@api.multi
	def provider_approved_request(self):
		user = self.env.user
		if self.creator == user:
			raise osv.except_osv(_('Permission Error'), _(
				"you cant approve a request created by yourself, please ask the moderator to approve."))
		else:
			self.write({'status': 'waiting_approval', 'request_send': True})

	@api.multi
	def moderator_rejected_request(self):
		self.write({'status':'rejected', 'reject_request':True})