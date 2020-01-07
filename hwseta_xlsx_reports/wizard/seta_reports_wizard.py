from openerp import models, fields, api, _
from datetime import datetime, timedelta
import time
import pprint

DEBUG = True

if DEBUG:
    import logging

    logger = logging.getLogger(__name__)


    def dbg(msg):
        logger.info(msg)
else:
    def dbg(msg):
        pass


class SETAReport(models.TransientModel):
    _name = 'seta.reports'

    # def last_day_of_month(self, date):
    #     dbg('last_day_of_month')
    #     if date.month == 12:
    #         return date.replace(day=31)
    #     return date.replace(month=date.month + 1, day=1) - timedelta(days=1)
    #
    # @api.onchange('report_type')
    # def _get_default_date_range(self):
    #     dbg('get_default_date_start')
    #     for report in self:
    #         today_date = datetime.today()
    #         if report.report_type == '_cml_report' or report.report_type == '_sale_report':
    #             dbg('cml or sale')
    #             report.from_date = today_date.replace(day=1)
    #             report.to_date = self.last_day_of_month(today_date.date())
    #         else:
    #             dbg('pipeline')
    #             report.from_date = time.strftime('%Y-01-01')
    #             report.to_date = time.strftime('%Y-12-31')

    name = fields.Char("Report Title", required=True)
    from_date = fields.Date("From", required=True)
    to_date = fields.Date("To", required=True)
    report_type = fields.Selection([('_accreditation_analysis', 'Accreditation Analysis'),
                                    ('_sale_report', 'Sale Report')], string="Report Type", required=True)

    headers = fields.Char("Headers")
    state = fields.Selection([('active', 'Active'),
                              ('cancel', 'Cancelled'),
                              ('all', 'All')], string="State", default='active')

    @api.multi
    def extract(self):
        report_method = getattr(self, self.report_type)
        result_url = report_method()
        dbg(self.id)
        return {
            'type': 'ir.actions.act_url',
            'url': result_url % self.id,
            'target': 'new',
            'res_id': self.id,
        }

    def _accreditation_analysis(self):
        accreds = self.env['provider.accreditation'].search(
            [('create_date', '>=', self.from_date), ('create_date', '<=', self.to_date)])
        # vals = []
        headers = [_('REF'), _('NAME'), _('phone'), _('email'), _('reg dt'), _('approve dt'), _('extension'), _('exist'), _('final state')]

        for accred in accreds:
            val = {
                'provider_accreditation_ref': accred.provider_accreditation_ref,
                'name':accred.name,
                'phone':accred.phone,
                'email':accred.email,
                'provider_register_date':accred.provider_register_date,
                'provider_approval_date':accred.provider_approval_date,
                'is_extension_of_scope':accred.is_extension_of_scope,
                'is_existing_provider':accred.is_existing_provider,
                'final_state':accred.final_state,
                'report_id':self.id
            }

            self.env['seta.reports.accreditations'].create(val)
        self.headers = pprint.saferepr(headers)

        return "/report_export/accreditation_analysis/%s"


class SETAReportAccreditations(models.TransientModel):
    _name = 'seta.reports.accreditations'

    provider_accreditation_ref = fields.Char("REF")
    name = fields.Char("Name")
    final_state = fields.Char()
    phone = fields.Char()
    email = fields.Char()
    provider_register_date = fields.Date(string='Provider Accreditation Date')
    provider_approval_date = fields.Date(string='Provider Accreditation Date')
    is_extension_of_scope = fields.Boolean()
    is_existing_provider = fields.Boolean()

    report_id = fields.Many2one("seta.reports", "Report Id")
