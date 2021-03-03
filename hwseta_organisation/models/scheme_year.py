from openerp import models, fields, api, _

DEBUG = False

if DEBUG:
	import logging

	logger = logging.getLogger(__name__)


	def dbg(msg):
		logger.info(msg)
else:
	def dbg(msg):
		pass


class seta_branches(models.Model):
	_inherit = 'wsp.submission.track'

	org_year = fields.Many2one('scheme.year')

	@api.one
	def set_syncable_scheme_year(self):
		bad_stats = []
		year_env = self.env['scheme.year']
		stat_env = self.env['wsp.submission.track']
		for stat in stat_env.search([]):
			dbg(stat)
			if stat.fiscal_year:
				dbg('fiscal' + str(stat.fiscal_year))
				good_year = year_env.search([('code','=',stat.fiscal_year.scheme_year_id.name)])
				dbg('fiscal' + str(good_year))
				if good_year:
					stat.org_year = good_year.id
			elif stat.scheme_year_id:
				dbg('scheme' + str(stat.scheme_year_id))
				good_year = year_env.search([('code', '=', stat.scheme_year_id.name)])
				dbg('scheme' + str(good_year))
				if good_year:
					stat.org_year = good_year.id
			else:
				bad_stats.append(stat)