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
                                    ('_assessment_analysis', 'Assessment Analysis'),
                                    ('_etqa_sdps_no_learners', 'etqa_sdps_no_learners'),
                                    ('_register_approval_analysis', 'register approval analysis'),
                                    ('_late_assessment_accreditation_analysis', 'provider acrred 140 days'),
                                    ('_mod_ass_register_8week_analysis', '_mod_ass_register_8week_analysis'),
                                    ('_assessment_approval_analysis', '_assessment_approval_analysis'),
                                    ('_accreditation_etqa_approval_analysis', 'Provider Accreditation application recommendations from Provinces Approved/Declined by ETQA Head Office.'),
                                    ('_sale_report', 'Sale Report')], string="Report Type", required=True)

    headers = fields.Char("Headers")
    state = fields.Selection([('active', 'Active'),
                              ('cancel', 'Cancelled'),
                              ('all', 'All')], string="State", default='active')
    assessment_state = fields.Selection([('draft', 'Draft'),
                                        ('submitted', 'Submitted'),
                                        ('learners', 'Learners'),
                                        ('verify', 'Verify'),
                                        ('evaluate', 'Evaluate'),
                                        ('achieved', 'Achieved'),
                                        ])
    qual_skill_assessment = fields.Selection([('qual', 'qual'),
                              ('skill', 'skill'),
                              ('lp', 'lp')])
    register_assessor_or_moderator = fields.Selection([('assessor', 'Assessor'),('moderator', 'Moderator')])

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

    def _etqa_sdps_no_learners(self):
        domain = [('provider_end_date', '>=', self.from_date), ('provider_end_date', '<=', self.to_date)]
        expirings = self.env['res.partner'].search(domain)
        dbg(expirings)
        headers = [ _('NAME'),_('Provider Accreditation Number'), ('Primary Accrediting Body'),
                    ('Accreditation Start Date'), ('Accreditation Start Date'), ('Email Address'),
                    ('Physical Address'), ('Province'), ('Accredited Qualification Title'),
                    ('Qualification ID')]

        for expiring in expirings:
            has_learners = False
            for qualification in expiring.qualification_ids:
                if self.env['learner.registration'].search([('provider_id','=',expiring.id),('learner_qualification_ids,learner_qualification_parent_id','=',qualification)]):
                    has_learners = True
            if not has_learners:
                val = {
                        'provider_id': expiring.id,
                        'report_id': self.id
                }

            self.env['seta.reports.etqa.sdps.no.learners'].create(val)
        self.headers = pprint.saferepr(headers)

        return "/report_export/sdps_no_learners/%s"

    def _register_approval_analysis(self):
        undefined_prov = self.env.ref('hwseta_xlsx_reports.state_UNDEFINED').id
        domain = [('create_date', '>=', self.from_date), ('create_date', '<=', self.to_date),('final_state','!=','Draft')]
        ass_mod = ''
        if self.register_assessor_or_moderator:
            domain.append(('assessor_moderator', '=', self.register_assessor_or_moderator))
            if self.register_assessor_or_moderator == 'moderator':
                ass_mod = 'Moderator'
            elif self.register_assessor_or_moderator == 'assessor':
                ass_mod = 'Assessor'
        registrations = self.env['assessors.moderators.register'].search(domain)
        # vals = []
        headers = [_('Province'),
                   _('Number of applications submitted to Provincial Office'),
                   _('Number of %s Registration Applications Approved ' % ass_mod),
                   _('Number of %s Registration Applications Declined ' % ass_mod),
                   _('Percentage of %s Registration applications approved ' % ass_mod),
                   _('Percentage of %s Registration applications declined ' % ass_mod)]
        dbg(registrations)
        provinces = {}
        provinces[undefined_prov] = {'approved_count': 0, 'denied_count': 0, 'approved_perc': 0,
                                     'denied_perc': 0, 'total': 0}
        for reg in registrations:
            if reg.work_province.id not in provinces.keys():
                # raise Warning(_('no prvince selected in ' + str(reg)))
                provinces[reg.work_province.id] = {'approved_count':0,'denied_count':0,'approved_perc':0,'denied_perc':0,'total':0}
                if reg.final_state == 'Approved':
                    provinces[reg.work_province.id]['approved_count'] += 1
                if reg.final_state == 'Rejected':
                    provinces[reg.work_province.id]['denied_count'] += 1
                provinces[reg.work_province.id]['total'] += 1
            else:
                if not reg.work_province:
                    if reg.final_state == 'Approved':
                        provinces[undefined_prov]['approved_count'] += 1
                    if reg.final_state == 'Rejected':
                        provinces[undefined_prov]['denied_count'] += 1
                    provinces[undefined_prov]['total'] += 1
                else:
                    if reg.final_state == 'Approved':
                        provinces[reg.work_province.id]['approved_count'] += 1
                    if reg.final_state == 'Rejected':
                        provinces[reg.work_province.id]['denied_count'] += 1
                    provinces[reg.work_province.id]['total'] += 1
        dbg(provinces)
        for province in provinces.keys():
            dbg('prov' + str(province))
            dbg('total' + str(provinces[province]['total']))
            if provinces[province]['total'] != 0:
                provinces[province]['denied_perc'] = round(100 * float(provinces[province]['denied_count']) / float(provinces[province]['total']),2)
                provinces[province]['approved_perc'] = round(100 * float(provinces[province]['approved_count']) / float(provinces[province]['total']),2)
            else:
                provinces[province]['denied_perc'] = 0
                provinces[province]['approved_perc'] = 0
            # dbg('prov' + str(province))
            # dbg('denied count' + str(provinces[province]['denied_count']))
            # dbg('approved_count' + str(provinces[province]['approved_count']))
            # dbg('total' + str(provinces[province]['total']))
            # dbg('approved_perc' + str(provinces[province]['approved_perc']))
            # dbg('denied_perc' + str(provinces[province]['denied_perc']))
            # dbg('-----------------------------------')
            prov = {'province':province,
                    'total':provinces[province]['total'],
                    'denied_perc':provinces[province]['denied_perc'],
                    'denied_count':provinces[province]['denied_count'],
                    'approved_perc':provinces[province]['approved_perc'],
                    'approved_count':provinces[province]['approved_count'],
                    'report_id':self.id
                    }
            self.env['seta.reports.register'].create(prov)
        self.headers = pprint.saferepr(headers)

        return "/report_export/register_approval_analysis/%s"

    def _accreditation_etqa_approval_analysis(self):
        undefined_prov = self.env.ref('hwseta_xlsx_reports.state_UNDEFINED').id
        accreds = self.env['provider.accreditation'].search(
            [('create_date', '>=', self.from_date), ('create_date', '<=', self.to_date)])
        # vals = []
        headers = [_('Province'),
                   _('Number of Provider Accreditation applications recommended to ETQA '),
                   _('Number Approved by ETQA'),
                   _('Number Declined by ETQA'),
                   _('% approved by ETQA '),
                   _('% Declined by ETQA ')]
        provinces = {}
        provinces[undefined_prov] = {'approved_count': 0, 'denied_count': 0, 'approved_perc': 0,
                                     'denied_perc': 0, 'total': 0}
        for accred in accreds:
            dbg(accred.state)
            # if a new prov is found add a key with 0 values on ints
            if accred.state_id.id not in provinces.keys():
                # raise Warning(_('no prvince selected in ' + str(reg)))
                provinces[accred.state_id.id] = {'approved_count': 0,
                                                 'denied_count': 0,
                                                 'approved_perc': 0,
                                                 'denied_perc': 0,
                                                 'total': 0}
                if accred.final_state == 'Approved':
                    provinces[accred.state_id.id]['approved_count'] += 1
                if accred.final_state == 'Rejected':
                    provinces[accred.state_id.id]['denied_count'] += 1
                provinces[accred.state_id.id]['total'] += 1
            # else it chooses the undefined province from data xml
            else:
                if not accred.state_id:
                    if accred.final_state == 'Approved':
                        provinces[undefined_prov]['approved_count'] += 1
                    if accred.final_state == 'Rejected':
                        provinces[undefined_prov]['denied_count'] += 1
                    provinces[undefined_prov]['total'] += 1
                else:
                    if accred.final_state == 'Approved':
                        provinces[accred.state_id.id]['approved_count'] += 1
                    if accred.final_state == 'Rejected':
                        provinces[accred.state_id.id]['denied_count'] += 1
                    provinces[accred.state_id.id]['total'] += 1
        dbg(provinces)
        for province in provinces.keys():
            dbg('prov' + str(province))
            dbg('total' + str(provinces[province]['total']))
            if provinces[province]['total'] != 0:
                provinces[province]['denied_perc'] = round(
                    100 * float(provinces[province]['denied_count']) / float(provinces[province]['total']), 2)
                provinces[province]['approved_perc'] = round(
                    100 * float(provinces[province]['approved_count']) / float(provinces[province]['total']), 2)
            else:
                provinces[province]['denied_perc'] = 0
                provinces[province]['approved_perc'] = 0
            prov = {'province': province,
                    'total': provinces[province]['total'],
                    'denied_perc': provinces[province]['denied_perc'],
                    'denied_count': provinces[province]['denied_count'],
                    'approved_perc': provinces[province]['approved_perc'],
                    'approved_count': provinces[province]['approved_count'],
                    'report_id': self.id
                    }
            self.env['seta.reports.etqa.approval.accreditation.analysis'].create(prov)
        self.headers = pprint.saferepr(headers)
        return "/report_export/accreditation_etqa_approval_analysis/%s"

    def _mod_ass_register_8week_analysis(self):
        undefined_prov = self.env.ref('hwseta_xlsx_reports.state_UNDEFINED').id
        domain = [('create_date', '>=', self.from_date), ('create_date', '<=', self.to_date),('final_state','!=','Draft')]
        ass_mod = ''
        if self.register_assessor_or_moderator:
            domain.append(('assessor_moderator', '=', self.register_assessor_or_moderator))
            if self.register_assessor_or_moderator == 'moderator':
                ass_mod = 'Moderator'
            elif self.register_assessor_or_moderator == 'assessor':
                ass_mod = 'Assessor'
        registrations = self.env['assessors.moderators.register'].search(domain)
        # vals = []
        headers = [_('%s ID No' % ass_mod),
                   _('%s Name' % ass_mod),
                   _('%s Surname' %ass_mod),
                   _('Province'),
                   _('Date of %s Application Submission' % ass_mod),
                   _('Date Approved/Declined by Provincial Manager '),
                   _('Number of days it took for the Provincial Office to approve/decline(<=8 weeks/35 days) a %s Application' % ass_mod),
                   _('%s Application Status' % ass_mod)]
        broken_regs = []
        for reg in registrations:
            stat_dict = {}
            if reg.final_state in ['Recommended', 'Submitted', 'Approved', 'Evaluated', 'Recommended2', 'Validated', 'Rejected']:
                if len(reg.assessors_moderators_status_ids) > 2:
                    dbg(reg.assessors_moderators_ref)
                    for stat in reg.assessors_moderators_status_ids:
                        if stat.am_status == 'Recommended':
                            stat_dict.update({stat.id: {'stat': stat.am_status, 'date_updated': stat.am_date}})
                        if stat.am_status == 'Rejected':
                            stat_dict.update({stat.id: {'stat': stat.am_status, 'date_updated': stat.am_date}})

                    # todo: uncomment below and deal with dirty data
                    if not stat_dict:
                        raise Warning(_('missing statuses from assessment: ' + reg.provider_accreditation_ref))
                    elif len(stat_dict) == 2:
                        del stat_dict[max(stat_dict)]
                    else:
                        broken_regs.append(reg.assessors_moderators_ref)
                    # if len(stat_dict) > 1:
                    #     raise Warning(_('there are issues in the statuses of accreditation:' + accred.provider_accreditation_ref))
                    created = datetime.strptime(reg.create_date, '%Y-%m-%d %H:%M:%S').date()
                    recommend_date = stat_dict[min(stat_dict)]['date_updated']
                    recommended = datetime.strptime(recommend_date, '%Y-%m-%d %H:%M:%S').date()

                    delta = recommended - created
                    regs = {'mod_id_no': reg.identification_id,
                            'mod_name':reg.name,
                            'mod_surname':reg.person_last_name,
                            'province':reg.work_province.id,
                            'application_date':reg.create_date,
                            'update_date':recommend_date,
                            'days_to_update':delta.days,
                            'final_state':reg.final_state,
                            'report_id':self.id
                            }
                    self.env['seta.reports.8week.register'].create(regs)
                else:
                    broken_regs.append(reg.assessors_moderators_ref)
        self.headers = pprint.saferepr(headers)
        return "/report_export/mod_ass_register_8week_analysis/%s"

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

    def _late_assessment_accreditation_analysis(self):
        accreds = self.env['provider.accreditation'].search(
            [('create_date', '>=', self.from_date), ('create_date', '<=', self.to_date)])
        # vals = []
        headers = [_('Provider Name'),
                   _('Provider Ref No '),
                   _('Provider SDLNo'),
                   _('alt provider sdl'),
                   _('Province'),
                   _('Date of Provider Accreditation application'),
                   _('Number of days it took for Provider Accreditation application to be assessed (<=140 days)'),
                   _('Date Application Recommended to ETQA / Declined  '),
                   _('final state')]
        broken_accreds = []
        for accred in accreds:
            stat_dict = {}
            if accred.final_state in ['Recommended','Submitted','Approved','Evaluated','Recommended2','Validated','Rejected']:
                dbg(len(accred.provider_accreditation_status_ids))
                if len(accred.provider_accreditation_status_ids) > 2:
                    dbg(accred.provider_accreditation_ref)
                    for stat in accred.provider_accreditation_status_ids:
                        if stat.pa_status == 'Recommended':
                            stat_dict.update({stat.id:{'stat':stat.pa_status,'date_updated':stat.pa_date}})
                        if stat.pa_status == 'Rejected':
                            stat_dict.update({stat.id: {'stat': stat.pa_status, 'date_updated': stat.pa_date}})

                    # todo: uncomment below and deal with dirty data
                    if not stat_dict:
                        raise Warning(_('missing statuses from accreditation: ' + accred.provider_accreditation_ref))
                    elif len(stat_dict) == 2:
                        del stat_dict[max(stat_dict)]
                    else:
                        broken_accreds.append(accred.provider_accreditation_ref)
                    # if len(stat_dict) > 1:
                    #     raise Warning(_('there are issues in the statuses of accreditation:' + accred.provider_accreditation_ref))
                    created = datetime.strptime(accred.create_date, '%Y-%m-%d %H:%M:%S').date()
                    recommend_date = stat_dict[min(stat_dict)]['date_updated']
                    recommended = datetime.strptime(recommend_date, '%Y-%m-%d %H:%M:%S').date()

                    delta = recommended - created
                    # raise Warning(_(delta.days))
                    val = {
                        'provider_name': accred.name,
                        'provider_accreditation_ref': accred.provider_accreditation_ref,
                        'sdl':accred.sequence_num,
                        'alt_sdl':accred.alternate_acc_number,
                        'state_id': accred.state_id.id,
                        'application_date':accred.create_date,
                        'update_date':recommend_date,
                        'days_to_assess':delta.days,
                        'final_state':accred.final_state,
                        'report_id':self.id
                    }

                    self.env['seta.reports.late.accreditations'].create(val)
                else:
                    broken_accreds.append(accred.provider_accreditation_ref)
        dbg(broken_accreds)
        self.headers = pprint.saferepr(headers)

        return "/report_export/late_accreditation_analysis/%s"

    def _assessment_analysis(self):
        domain = [('create_date', '>=', self.from_date), ('create_date', '<=', self.to_date)]
        if self.qual_skill_assessment:
            domain.append(('qual_skill_assessment','=',self.qual_skill_assessment))
        if self.assessment_state:
            domain.append(('state','=',self.assessment_state))
        dbg(domain)
        assessments = self.env['provider.assessment'].search(domain)
        # vals = []
        if self.qual_skill_assessment == 'qual':
            headers = [_('NAME'), _('provider'), _('type'), _('batch'), _('state'), _('province'), _('enrolled learners'), _('learner'), _('rpl'), _('achieved'), _('qualification'), _('qualification id'), ]
        if self.qual_skill_assessment in ['lp','skill']:
            headers = [_('NAME'), _('provider'), _('type'), _('batch'), _('state'), _('province'), _('enrolled learners'), _('learner'), _('rpl'), _('achieved'), _('qualification'), _('qualification id'), ]
        if not self.qual_skill_assessment:
            headers = [_('NAME'), _('provider'), _('type'), _('batch'), _('state'), _('province'), _('enrolled learners'), _('learner'), _('rpl'), _('achieved'), _('qualification'), _('qualification id'),]

        for assessment in assessments:
            val = {
                'assessment':assessment.id,
                'name':assessment.name,
                'provider_id':assessment.provider_id.id,
                'qual_skill_assessment':assessment.qual_skill_assessment,
                'batch_id':assessment.batch_id.id,
                'fiscal_year':assessment.fiscal_year.id,
                'start_date':assessment.start_date,
                'state':assessment.state,
                'provider_province':assessment.provider_province.id,  
                'report_id':self.id
            }

            self.env['seta.reports.assessment'].create(val)
        self.headers = pprint.saferepr(headers)

        return "/report_export/assessment_analysis/%s"

    def _assessment_approval_analysis(self):
        undefined_prov = self.env.ref('hwseta_xlsx_reports.state_UNDEFINED').id
        domain = [('create_date', '>=', self.from_date), ('create_date', '<=', self.to_date),('state','!=','Draft')]
        assessments = self.env['provider.assessment'].search(domain)
        # vals = []
        headers = [_('Province'),
                   _('Number of Learner applications recommended to ETQA'),
                   _('Number of Learners approved for certification'),
                   _('Number of Learners Declined'),
                   _('% Of Learners approved for certification'),
                   _('% Of Declined learners')]
        dbg(assessments)
        provinces = {}
        provinces[undefined_prov] = {'approved_count': 0, 'denied_count': 0, 'approved_perc': 0,
                                     'denied_perc': 0, 'total': 0}
        for assessment in assessments:
            dbg(assessment.state)
            if assessment.provider_province.id not in provinces.keys():
                # raise Warning(_('no prvince selected in ' + str(reg)))
                provinces[assessment.provider_province.id] = {'approved_count':0,'denied_count':0,'approved_perc':0,'denied_perc':0,'total':0}
                if assessment.state == 'achieved':
                    provinces[assessment.provider_province.id]['approved_count'] += 1
                if assessment.state == 'Rejected':
                    provinces[assessment.provider_province.id]['denied_count'] += 1
                provinces[assessment.provider_province.id]['total'] += 1
            else:
                if not assessment.provider_province:
                    if assessment.state == 'achieved':
                        provinces[undefined_prov]['approved_count'] += 1
                    if assessment.state == 'Rejected':
                        provinces[undefined_prov]['denied_count'] += 1
                    provinces[undefined_prov]['total'] += 1
                else:
                    if assessment.state == 'achieved':
                        provinces[assessment.provider_province.id]['approved_count'] += 1
                    if assessment.state == 'Rejected':
                        provinces[assessment.provider_province.id]['denied_count'] += 1
                    provinces[assessment.provider_province.id]['total'] += 1
        dbg(provinces)
        for province in provinces.keys():
            dbg('prov' + str(province))
            dbg('total' + str(provinces[province]['total']))
            if provinces[province]['total'] != 0:
                provinces[province]['denied_perc'] = round(100 * float(provinces[province]['denied_count']) / float(provinces[province]['total']),2)
                provinces[province]['approved_perc'] = round(100 * float(provinces[province]['approved_count']) / float(provinces[province]['total']),2)
            else:
                provinces[province]['denied_perc'] = 0
                provinces[province]['approved_perc'] = 0
            # dbg('prov' + str(province))
            # dbg('denied count' + str(provinces[province]['denied_count']))
            # dbg('approved_count' + str(provinces[province]['approved_count']))
            # dbg('total' + str(provinces[province]['total']))
            # dbg('approved_perc' + str(provinces[province]['approved_perc']))
            # dbg('denied_perc' + str(provinces[province]['denied_perc']))
            # dbg('-----------------------------------')
            prov = {'province':province,
                    'total':provinces[province]['total'],
                    'denied_perc':provinces[province]['denied_perc'],
                    'denied_count':provinces[province]['denied_count'],
                    'approved_perc':provinces[province]['approved_perc'],
                    'approved_count':provinces[province]['approved_count'],
                    'report_id':self.id
                    }
            self.env['seta.reports.assessment.approval'].create(prov)
        self.headers = pprint.saferepr(headers)

        return "/report_export/assessment_approval_analysis/%s"


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


class SETAReportAssessmentApproval(models.TransientModel):
    _name = 'seta.reports.assessment.approval'

    province = fields.Many2one('res.country.state')
    total = fields.Float()
    approved_count = fields.Float()
    denied_count = fields.Float()
    denied_perc = fields.Float()
    approved_perc = fields.Float()
    report_id = fields.Many2one("seta.reports", "Report Id")


class SETAReportLateAccreditations(models.TransientModel):
    _name = 'seta.reports.late.accreditations'

    provider_accreditation_ref = fields.Char("REF")
    provider_name = fields.Char("Name")
    final_state = fields.Char()
    sdl = fields.Char()
    alt_sdl = fields.Char()
    application_date = fields.Datetime()
    update_date = fields.Datetime()
    days_to_assess = fields.Integer()
    state_id = fields.Many2one('res.country.state')

    report_id = fields.Many2one("seta.reports", "Report Id")


class SETAReportAssessment(models.TransientModel):
    _name = 'seta.reports.assessment'

    assessment = fields.Many2one('provider.assessment')
    name = fields.Char()
    provider_id = fields.Many2one('res.partner')
    qual_skill_assessment = fields.Selection([('qual', 'qual'),
                              ('skill', 'skill'),
                              ('lp', 'lp')])
    batch_id = fields.Many2one('batch.master')
    fiscal_year = fields.Many2one('account.fiscalyear')
    start_date = fields.Date()
    state = fields.Selection([('draft', 'Draft'),
                              ('submitted', 'Submitted'),
                              ('learners', 'Learners'),
                              ('verify', 'Verify'),
                              ('evaluate', 'Evaluate'),
                              ('achieved', 'Achieved'),
                              ])
    provider_province = fields.Many2one('res.country.state')
    # learner_ids = fields.One2many('learner.assessment.line',)

    report_id = fields.Many2one("seta.reports", "Report Id")


class SETAReportRegister(models.TransientModel):
    _name = 'seta.reports.register'

    province = fields.Many2one('res.country.state')
    total = fields.Float()
    approved_count = fields.Float()
    denied_count = fields.Float()
    denied_perc = fields.Float()
    approved_perc = fields.Float()
    report_id = fields.Many2one("seta.reports", "Report Id")


class SETAReport8WeekRegister(models.TransientModel):
    _name = 'seta.reports.8week.register'

    mod_id_no = fields.Char()
    mod_name = fields.Char()
    mod_surname = fields.Char()
    province = fields.Many2one('res.country.state')
    application_date = fields.Datetime()
    update_date = fields.Datetime()
    days_to_update = fields.Integer()
    final_state = fields.Char()
    report_id = fields.Many2one("seta.reports", "Report Id")


class SETAReportetqaApprovalAccreditationAnalysis(models.TransientModel):
    _name = 'seta.reports.etqa.approval.accreditation.analysis'

    province = fields.Many2one('res.country.state')
    total = fields.Float()
    approved_count = fields.Float()
    denied_count = fields.Float()
    denied_perc = fields.Float()
    approved_perc = fields.Float()

    report_id = fields.Many2one("seta.reports", "Report Id")


class SETAReportetqaSDPsNoLearners(models.TransientModel):
    _name = 'seta.reports.etqa.sdps.no.learners'

    provider_id = fields.Many2one('res.partner')
    report_id = fields.Many2one("seta.reports", "Report Id")

