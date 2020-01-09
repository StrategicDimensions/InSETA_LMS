from openerp import models, fields, api, _

DEBUG = True
if DEBUG:
	import logging

	logger = logging.getLogger(__name__)


	def dbg(msg):
		logger.info(msg)
else:
	def dbg(msg):
		pass

class res_users(models.Model):
	_inherit = 'res.users'

	@api.multi
	def copy_users_crypt(self):
		for user_copy in self.env['res.users.copy'].search([]):
			user_copy.unlink()
		for user in self.env['res.users'].search([('id','!=',1)]):
			self.env['res.users.copy'].create({'password_crypt': user.password_crypt,'password': user.password,'login': user.login,'id_copy': user.id})
			dbg(user.id)
			user.password_crypt = ''
			user.password = ''

	@api.multi
	def restore_users_crypt(self):
		for user_copy in self.env['res.users.copy'].search([]):
			real_user = self.env['res.users'].search([('id','=',user_copy.id_copy)])
			real_user.password_crypt = user_copy.password_crypt

res_users()

class ResUsersCopy(models.Model):
	_name = 'res.users.copy'

	password_crypt = fields.Char()
	password = fields.Char()
	login = fields.Char()
	id_copy = fields.Char()

ResUsersCopy()