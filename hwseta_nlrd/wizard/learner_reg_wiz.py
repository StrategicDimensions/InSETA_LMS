# coding=utf-8
from openerp import models, fields, tools, api, _

DEBUG = True

if DEBUG:
	import logging

	logger = logging.getLogger(__name__)


	def dbg(msg):
		logger.info(msg)
else:
	def dbg(msg):
		pass

class learner_reg_qual_fix_wiz(models.TransientModel):
	_name = 'learner.reg.qual.fix.wiz'

	@api.multi
	def _get_missing_status(self):
		context = self._context
		if not self.lrq_id.learner_id:
			return True

	lrq_id = fields.Many2one('learner.registration.qualification')
	missing_learner = fields.Boolean(_default=_get_missing_status)
	learner_id = fields.Many2one('hr.employee')

	@api.one
	def fix_lrq(self):
		if self.lrq_id:
			raise Warning(_('found lrq_id'))
	# for lrq in self.env['learner.registration.qualification'].search(domain):
	_defaults = { 'lrq_id': lambda self, cr, uid, context: context.get('lrq_id', False), }

# class learner_registration_qualification(models.Model):
# 	_inherit = 'learner.registration.qualification'
#
# 	@api.one
# 	def fix_lrq_wiz(self):
