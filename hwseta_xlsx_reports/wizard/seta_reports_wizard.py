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

def get_transaction_type(this):
    dbg(this)
    #if this.is_existing_provider:
    #    return 'Re registration'
    if this.is_extension_of_scope:
        return 'extention of scope'
        #elif not this.is_extension_of_scope and this.is_existing_provider:
    else:
        return 'New registration'

class SETAReport(models.TransientModel):
    _name = 'seta.reports'

    @api.multi
    def pull_qap(self):
        count = 0
        msg = 'SDP/PROVIDER NAME, contact person, physical address, Tel, Cell, e-mail,Accreditation End Date,Province,QUALIFICATION/S,Number of learners enrolled\n'
        learner_provs = [lnr.provider_id.id for lnr in self.env['learner.registration.qualification'].search([
            ('approval_date', '>=', self.from_date),
            ('approval_date', '<=', self.to_date),
        ])]
        for provider in self.env['res.partner'].search(
                [('provider', '=', True),
                 ('parent_id', '=', None),
                 ('active', '=', True),
                 ('id', 'in', learner_provs),
                 # ('provider_end_date', '>=', self.from_date),
                 # ('provider_end_date', '<=', self.to_date),
                 ]):

            person_name = ''
            count += 1
            dbg(provider)
            for person in provider.provider_master_contact_ids:
                try:
                    person_name = str(person.name).encode('utf8')
                except UnicodeEncodeError:
                    person_name = ''
            address = str(provider.physical_address_1) + ' ' + str(provider.physical_address_2) + ' ' + str(
                provider.physical_address_3) + ' ' + str(provider.provider_physical_suburb.name) + ' ' + str(
                provider.city_physical.name)
            msg += str(provider.name) + ',' + str(person_name) + ',' + str(address) + ',' + str(
                provider.phone) + ',' + str(provider.mobile) + ',' + str(provider.email) + ',' + str(
                provider.provider_end_date) + ',' + str(provider.province_code_physical.name) + '\n'
            for qual in provider.qualification_ids:
                count += 1
                learners = self.env['learner.registration.qualification'].search([
                    ('provider_id', '=', provider.id),
                    ('learner_qualification_parent_id', '=', qual.qualification_id.id),
                    ('approval_date', '>=', self.from_date),
                    ('approval_date', '<=', self.to_date),
                ])
                dbg(learners)
                learner_count = len(learners)
                qual_name = str(qual.qualification_id.name).replace(',', ' ')
                msg += ',,,,,,,,[' + str(qual.saqa_qual_id) + ']' + qual_name + ',' + str(
                    learner_count) + '\n'
            dbg(count)
        raise Warning(msg)

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
    raise_info = fields.Boolean()
    raise_errors = fields.Boolean()
    provider_date = fields.Date("provider date")
    report_type = fields.Selection([('_accreditation_analysis', 'Accreditation Analysis'),
                                    ('_assessment_analysis', 'Assessment Analysis'),
                                    ('_etqa_sdps_no_learners', 'etqa_sdps_no_learners'),
                                    ('_register_approval_analysis', '% of Assessor/Moderators of Registration that were approved or declined per province'),
                                    ('_late_assessment_accreditation_analysis', 'Provider Acreditation application assessed in 140 days per province at Provincial Level'),
                                    ('_mod_ass_register_8week_analysis', 'Assessor/Moderator Registration applications approved/declined within an 8-week period per province'),
                                    ('_assessment_approval_analysis', 'Learner Achievement recommendations from the Provinces Approved/Declined by ETQA Head Office'),
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
        # todo: would be sick if we used a m2o filter in the wiz for selecting a single provider/res.partner
        domain = [('provider_end_date', '>=', self.provider_date), ('provider_end_date', '<=', self.provider_date),('provider','=',True),('parent_id','=',None),('active','=',True)]
        providers = self.env['res.partner'].search(domain)
        start = self.from_date
        end = self.to_date
        dbg(providers)
        headers = [ _('NAME'),_('Provider Accreditation Number'), ('Primary Accrediting Body'),
                    ('Accreditation Start Date'), ('Accreditation End Date'), ('Email Address'),
                    ('Physical Address'), ('Province'), ('Type'), ('Accredited Qualification Title'),
                    ('Qualification ID'),('Skill ID'),('LP ID'),('Learners Enrolled'),('Learners Total')]

        for provider in providers:
            # vestigial: we dont use this anymore because the report should be consolidated
            # has_learners = False
            # for qualification in provider.qualification_ids:
            #     if self.env['learner.registration'].search([('provider_id','=',provider.id),('learner_qualification_ids.learner_qualification_parent_id','=',qualification.id)]):
            #         has_learners = True
            # if not has_learners:
            qual_list = []
            skill_list = []
            lp_list = []
            for qual in provider.qualification_ids:
                qual_list.append(qual.id)
                dbg(qual.read())
            for skill in provider.skills_programme_ids:
                skill_list.append(skill.id)
                dbg(skill.read())
            for lp in provider.learning_programme_ids:
                lp_list.append(lp.id)
                dbg(lp.read())
            dbg(skill_list)
            dbg(lp_list)
            dbg(qual_list)
            val = {
                    'provider_id': provider.id,
                    'start_date': start,
                    'end_date': end,
                    'qualification_ids': [(6,0,qual_list)],
                    'skill_ids': [(6,0,skill_list)],
                    'lp_ids': [(6,0,lp_list)],
                    'report_id': self.id
            }

            rec = self.env['seta.reports.etqa.sdps.no.learners'].create(val)
            # rec.write({'qualification_ids': [(0,0,qual_list)],
            #            'skill_ids': [(0, 0, skill_list)],
            #            'lp_ids': [(0, 0, lp_list)]
            #            })
        self.headers = pprint.saferepr(headers)

        return "/report_export/sdps_no_learners/%s"

    def _register_approval_analysis(self):
        undefined_prov = self.env.ref('hwseta_xlsx_reports.state_UNDEFINED').id
        # domain = [('create_date', '>=', self.from_date), ('create_date', '<=', self.to_date),('final_state','!=','Draft')]
        ass_mod = ''
        if self.register_assessor_or_moderator:
            # domain.append(('assessor_moderator', '=', self.register_assessor_or_moderator))
            if self.register_assessor_or_moderator == 'moderator':
                ass_mod = 'Moderator'
            elif self.register_assessor_or_moderator == 'assessor':
                ass_mod = 'Assessor'
        # registrations = self.env['assessors.moderators.register'].search(domain)
        """"
        build up a dict of unique assessments based on statuses , keeping the first submitted status as the val and the assessment as the key 
        """
        reg_dict = {}
        stats = self.env['assessors.moderators.status'].search(
            [('am_status', '=', 'Submitted'),
             ('am_updation_date', '>=', self.from_date),
             ('am_updation_date', '<=', self.to_date),
             ('assessors_moderators_status_mo_id.assessor_moderator','=',self.register_assessor_or_moderator)]
        )
        for stat in stats:
            if stat not in reg_dict.keys():
                reg_dict.update({stat.assessors_moderators_status_mo_id: stat})
            else:
                if reg_dict.get(stat.assessors_moderators_status_mo_id) < stat.assessors_moderators_status_mo_id:
                    reg_dict.update({stat.assessors_moderators_status_mo_id: stat})
        if self.raise_info:
            msg = 'id,ref,province,Assessor/Moderator Application Date,final state,qualifying line state,line date\n'
            for reg in reg_dict:
                msg += str(reg.id) + ',' + str(reg.assessors_moderators_ref) + ',' \
                       + str(reg.work_province.name) + ',' + reg.assessor_moderator_register_date + ','\
                       + str(reg.final_state) + ',' + str(reg_dict.get(reg).am_status) + ','\
                       + str(reg_dict.get(reg).am_updation_date) + '\n'
            raise Warning(_(msg))
        registrations = reg_dict.keys()
        # vals = []
        headers = [_('Province'),
                   _('Number of applications submitted to Provincial Office'),
                   _('Number of %s Registration Applications Approved ' % ass_mod),
                   _('Number of %s Registration Applications Declined ' % ass_mod),
                   _('Percentage of %s Registration applications approved ' % ass_mod),
                   _('Percentage of %s Registration applications declined ' % ass_mod),
                   _('In progress'),
                   _('New Registration'),
                   _('Re Registration'),
                   _('Extension of scope')]
        dbg(registrations)
        provinces = {}
        provinces[undefined_prov] = {'approved_count': 0, 'denied_count': 0, 'approved_perc': 0,
                                     'denied_perc': 0, 'total': 0, 'new_registration_count': 0, 're_registration_count': 0, 'extension_of_scope_count': 0 }

        for reg in registrations:
            if reg.work_province.id not in provinces.keys():
                # raise Warning(_('no prvince selected in ' + str(reg)))
                provinces[reg.work_province.id] = {'approved_count':0,'denied_count':0,'approved_perc':0,'denied_perc':0,
                                                   'total':0, 'new_registration_count': 0, 're_registration_count': 0, 'extension_of_scope_count': 0}
                if reg.final_state == 'Approved':
                    provinces[reg.work_province.id]['approved_count'] += 1
                if reg.final_state == 'Rejected':
                    provinces[reg.work_province.id]['denied_count'] += 1
                if reg.already_registered:
                    provinces[reg.work_province.id]['re_registration_count'] += 1
                if reg.is_extension_of_scope:
                    provinces[reg.work_province.id]['extension_of_scope_count'] += 1
                if not reg.is_extension_of_scope and not reg.already_registered:
                    provinces[reg.work_province.id]['new_registration_count'] += 1
                provinces[reg.work_province.id]['total'] += 1
            else:
                if not reg.work_province:
                    if reg.final_state == 'Approved':
                        provinces[undefined_prov]['approved_count'] += 1
                    if reg.final_state == 'Rejected':
                        provinces[undefined_prov]['denied_count'] += 1
                    if reg.already_registered:
                        provinces[undefined_prov]['re_registration_count'] += 1
                    if reg.is_extension_of_scope:
                        provinces[undefined_prov]['extension_of_scope_count'] += 1
                    if not reg.is_extension_of_scope and not reg.already_registered:
                        provinces[undefined_prov]['new_registration_count'] += 1
                    provinces[undefined_prov]['total'] += 1
                else:
                    if reg.final_state == 'Approved':
                        provinces[reg.work_province.id]['approved_count'] += 1
                    if reg.final_state == 'Rejected':
                        provinces[reg.work_province.id]['denied_count'] += 1
                    if reg.already_registered:
                        provinces[reg.work_province.id]['re_registration_count'] += 1
                    if reg.is_extension_of_scope:
                        provinces[reg.work_province.id]['extension_of_scope_count'] += 1
                    if not reg.is_extension_of_scope and not reg.already_registered:
                        provinces[reg.work_province.id]['new_registration_count'] += 1
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
                    'new_registration_count': provinces[province]['new_registration_count'],
                    're_registration_count': provinces[province]['re_registration_count'],
                    'extension_of_scope_count': provinces[province]['extension_of_scope_count'],
                    'report_id':self.id
                    }
            dbg(prov)
            self.env['seta.reports.register'].create(prov)
        self.headers = pprint.saferepr(headers)

        return "/report_export/register_approval_analysis/%s"

    def _accreditation_etqa_approval_analysis(self):
        undefined_prov = self.env.ref('hwseta_xlsx_reports.state_UNDEFINED').id
        # accreds = self.env['provider.accreditation'].search(
        #     [('create_date', '>=', self.from_date), ('create_date', '<=', self.to_date)])
        """
                build up a list of unique accreds with the statuses to ensure ommission of non valid accreds and precision of date filters
                """
        accred_dict = {}
        statuses = self.env['provider.accreditation.status'].search(
            [('pa_date', '>=', self.from_date), ('pa_date', '<=', self.to_date), ('pa_status', '=', 'Recommended')])
            # [('pa_date', '>=', self.from_date), ('pa_date', '<=', self.to_date), ('pa_status', '=', 'Submitted')])
        # first time add to dict, all times after, compare the min(id) and add lowest stat
        for stat in statuses:
            if stat.pro_acc_status_ids not in accred_dict.keys():
                accred_dict.update({stat.pro_acc_status_ids: stat})
            else:
                if stat < accred_dict.get(stat.pro_acc_status_ids):
                    accred_dict.update({stat.pro_acc_status_ids: stat})
        if self.raise_info:
            msg = 'id,ref,province,final state,qualifying line state,line date\n'
            for accred in accred_dict:
                msg += str(accred.id) + ',' + str(accred.provider_accreditation_ref) + ',' + str(accred.state_id.name) + ','\
                       + str(accred.final_state) + ',' + str(accred_dict.get(accred).pa_status) \
                       + ',' + str(accred_dict.get(accred).pa_date) + '\n'
            raise Warning(_(msg))
        # vals = []
        headers = [_('Province'),
                   _('Number of Provider Accreditation applications recommended to ETQA '),
                   _('Number Approved by ETQA'),
                   _('Number Declined by ETQA'),
                   _('% approved by ETQA '),
                   _('% Declined by ETQA '),
                   _('In Progress '),
                   _('New Accreditation '),
                   _('New Program Approval'),
                   _('Re Accreditation '),
                   _('Extension of Scope ')
                   ]
        provinces = {}
        provinces[undefined_prov] = {'approved_count': 0, 'denied_count': 0, 'approved_perc': 0,
                                     'denied_perc': 0, 'total': 0, 'new': 0, 'new_prog_approval': 0,
                                     'reaccred': 0, 'extension': 0 }

        for accred in accred_dict.keys():
            dbg(accred.state)
            # if a new prov is found add a key with 0 values on ints
            if accred.state_id.id not in provinces.keys():
                # raise Warning(_('no prvince selected in ' + str(reg)))
                provinces[accred.state_id.id] = {'approved_count': 0,
                                                 'denied_count': 0,
                                                 'approved_perc': 0,
                                                 'denied_perc': 0,
                                                 'total': 0,
                                                 'new': 0,
                                                 'new_prog_approval': 0,
                                                 'reaccred': 0,
                                                 'extension': 0
                                                 }
                if accred.final_state == 'Approved':
                    provinces[accred.state_id.id]['approved_count'] += 1
                if accred.final_state == 'Rejected':
                    provinces[accred.state_id.id]['denied_count'] += 1
                if accred.transaction_type == 'new':
                    provinces[accred.state_id.id]['new'] += 1
                if accred.transaction_type == 'new_prog_approval':
                    provinces[accred.state_id.id]['new_prog_approval'] += 1
                if accred.transaction_type == 'reaccred':
                    provinces[accred.state_id.id]['reaccred'] += 1
                if accred.transaction_type == 'extension':
                    provinces[accred.state_id.id]['extension'] += 1

                provinces[accred.state_id.id]['total'] += 1
            # else it chooses the undefined province from data xml
            else:
                if not accred.state_id:
                    if accred.final_state == 'Approved':
                        provinces[undefined_prov]['approved_count'] += 1
                    if accred.final_state == 'Rejected':
                        provinces[undefined_prov]['denied_count'] += 1
                    if accred.transaction_type == 'new':
                        provinces[accred.state_id.id]['new'] += 1
                    if accred.transaction_type == 'new_prog_approval':
                        provinces[accred.state_id.id]['new_prog_approval'] += 1
                    if accred.transaction_type == 'reaccred':
                        provinces[accred.state_id.id]['reaccred'] += 1
                    if accred.transaction_type == 'extension':
                        provinces[accred.state_id.id]['extension'] += 1
                    provinces[undefined_prov]['total'] += 1
                else:
                    if accred.final_state == 'Approved':
                        provinces[accred.state_id.id]['approved_count'] += 1
                    if accred.final_state == 'Rejected':
                        provinces[accred.state_id.id]['denied_count'] += 1
                    if accred.transaction_type == 'new':
                        provinces[accred.state_id.id]['new'] += 1
                    if accred.transaction_type == 'new_prog_approval':
                        provinces[accred.state_id.id]['new_prog_approval'] += 1
                    if accred.transaction_type == 'reaccred':
                        provinces[accred.state_id.id]['reaccred'] += 1
                    if accred.transaction_type == 'extension':
                        provinces[accred.state_id.id]['extension'] += 1
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
                    'new_accred': provinces[province]['new'],
                    'new_prog_approval': provinces[province]['new_prog_approval'],
                    'reaccred': provinces[province]['reaccred'],
                    'extension': provinces[province]['extension'],
                    'report_id': self.id
                    }
            self.env['seta.reports.etqa.approval.accreditation.analysis'].create(prov)
        self.headers = pprint.saferepr(headers)
        return "/report_export/accreditation_etqa_approval_analysis/%s"


    def _mod_ass_register_8week_analysis(self):
        undefined_prov = self.env.ref('hwseta_xlsx_reports.state_UNDEFINED').id
        # domain = [('create_date', '>=', self.from_date), ('create_date', '<=', self.to_date),('final_state','!=','Draft')]
        ass_mod = ''
        if self.register_assessor_or_moderator:
            # domain.append(('assessor_moderator', '=', self.register_assessor_or_moderator))
            if self.register_assessor_or_moderator == 'moderator':
                ass_mod = 'Moderator'
            elif self.register_assessor_or_moderator == 'assessor':
                ass_mod = 'Assessor'
        # registrations = self.env['assessors.moderators.register'].search(domain)
        reg_dict = {}
        stats = self.env['assessors.moderators.status'].search(
            [('am_status', '=', 'Submitted'),
             ('am_date', '>=', self.from_date),
             ('am_date', '<=', self.to_date),
             ('assessors_moderators_status_mo_id.assessor_moderator', '=', self.register_assessor_or_moderator)]
        )
        for stat in stats:
            if stat not in reg_dict.keys():
                reg_dict.update({stat.assessors_moderators_status_mo_id: stat})
            else:
                if reg_dict.get(stat.assessors_moderators_status_mo_id) < stat.assessors_moderators_status_mo_id:
                    reg_dict.update({stat.assessors_moderators_status_mo_id: stat})

        registrations = reg_dict.keys()
        # vals = []
        headers = [_('%s ID No' % ass_mod),
                   _('%s Name' % ass_mod),
                   _('%s Surname' %ass_mod),
                   _('Province'),
                   _('Date of %s Application Submission' % ass_mod),
                   _('Date Approved/Declined by Provincial Manager '),
                   _('Number of days it took for the Provincial Office to approve/decline(<=8 weeks/35 days) a %s Application' % ass_mod),
                   _('%s Application Status' % ass_mod),
                   _('In Progress'),
                   _('Transaction_type'),
                   ]
        broken_regs = {}
        for reg in registrations:
            dbg(reg)
            stat_dict = {}
            if reg.final_state in ['Recommended', 'Submitted', 'Approved', 'Evaluated', 'Recommended2', 'Validated', 'Rejected']:
                if len(reg.assessors_moderators_status_ids) >= 2:
                    for stat in reg.assessors_moderators_status_ids:
                        if stat.am_status == 'Recommended':
                            stat_dict.update({stat.id: {'stat': stat.am_status, 'date_updated': stat.am_date}})
                        if stat.am_status == 'Rejected':
                            stat_dict.update({stat.id: {'stat': stat.am_status, 'date_updated': stat.am_date}})
                        if stat.am_status == 'Approved':
                            stat_dict.update({stat.id: {'stat': stat.am_status, 'date_updated': stat.am_date}})
                    # todo: uncomment below and deal with dirty data
                    # dbg(stat_dict)
                    if not stat_dict:
                        dbg({reg.assessors_moderators_ref:str(reg.identification_id) + ',' + "had no relevant statuses"})
                        dbg(stat_dict)
                        broken_regs.update({reg.assessors_moderators_ref:str(reg.identification_id) + ',' + "had no relevant statuses"})
                        # raise Warning(_('missing statuses from assessment: ' + reg.provider_accreditation_ref))
                    elif len(stat_dict) < 2:
                        dbg({reg.assessors_moderators_ref:str(reg.identification_id) + ',' + 'too few statuses to choose from'})
                        dbg(stat_dict)
                        broken_regs.update({reg.assessors_moderators_ref:str(reg.identification_id) + ',' + 'too few statuses to choose from'})
                    elif len(stat_dict) == 2:
                        dbg(stat_dict)
                        dbg("deleting :" + str(stat_dict[max(stat_dict)]) + ',' + str(reg.assessors_moderators_ref) + ',' + str(reg.identification_id))
                        del stat_dict[max(stat_dict)]
                    # elif len(stat_dict) == 3:
                    #     del stat_dict[max(stat_dict)]
                    #     del stat_dict[max(stat_dict)]
                    else:
                        dbg({reg.assessors_moderators_ref:str(reg.identification_id) + ',' + 'too many statuses to choose from'})
                        dbg(stat_dict)
                        broken_regs.update({reg.assessors_moderators_ref:str(reg.identification_id) + ',' + 'too many statuses to choose from'})
                    # if len(stat_dict) > 1:
                    #     raise Warning(_('there are issues in the statuses of accreditation:' + accred.provider_accreditation_ref))
                    if not reg.assessors_moderators_ref in broken_regs:
                        created = datetime.strptime(reg.create_date, '%Y-%m-%d %H:%M:%S').date()
                        recommend_date = stat_dict[min(stat_dict)]['date_updated']
                        recommended = datetime.strptime(recommend_date, '%Y-%m-%d %H:%M:%S').date()

                        delta = recommended - created
                        in_process = False
                        if reg.final_state not in ['Approved', 'Rejected']:
                            in_process = True

                        regs = {'mod_id_no': reg.identification_id,
                                'mod_name':reg.name,
                                'mod_surname':reg.person_last_name,
                                'province':reg.work_province.id,
                                'application_date':reg.create_date,
                                'update_date':recommend_date,
                                'days_to_update':delta.days,
                                'final_state':reg.final_state,
                                'in_process': in_process,
                                'transaction_type': get_transaction_type(reg),
                                'report_id':self.id
                                }
                        self.env['seta.reports.8week.register'].create(regs)
                else:
                    # dbg({reg.assessors_moderators_ref:'too few statuses'})
                    broken_regs.update({str(reg.assessors_moderators_ref): ',' + str(reg.identification_id) + 'too few statuses'})
        if self.raise_info:
            msg = 'id,ref,identification_id,province,Assessor/Moderator Application Date,final state,qualifying line state,line date\n'
            for reg in reg_dict:
                if not reg.assessors_moderators_ref in broken_regs:
                    msg += str(reg.id) + ',' + str(reg.assessors_moderators_ref) + ',' + str(reg.identification_id) + ',' \
                           + str(reg.work_province.name) + ',' + reg.assessor_moderator_register_date + ','\
                           + str(reg.final_state) + ',' + str(reg_dict.get(reg).am_status) + ','\
                           + str(reg_dict.get(reg).am_date) + '\n'
            raise Warning(_(msg))
        msg = '\n'
        if self.raise_errors:
            dbg("raise")
            for brk in broken_regs:
                msg += str(brk) + ':' + str(broken_regs[brk]) + '\n'
            raise Warning(_(msg))
        self.headers = pprint.saferepr(headers)
        return "/report_export/mod_ass_register_8week_analysis/%s"

    def _accreditation_analysis(self):
        """
        build up a list of unique accreds with the statuses to ensure ommission of non valid accreds and precision of date filters
        """
        accred_dict = {}
        statuses = self.env['provider.accreditation.status'].search(
            [('pa_date', '>=', self.from_date), ('pa_date', '<=', self.to_date), ('pa_status', '=', 'Recommended')])
            # [('pa_date', '>=', self.from_date), ('pa_date', '<=', self.to_date), ('pa_status', '=', 'Submitted')])
        # first time add to dict, all times after, compare the min(id) and add lowest stat
        for stat in statuses:
            if stat.pro_acc_status_ids not in accred_dict.keys():
                accred_dict.update({stat.pro_acc_status_ids:stat})
            else:
                if stat < accred_dict.get(stat.pro_acc_status_ids):
                    accred_dict.update({stat.pro_acc_status_ids:stat})
        if self.raise_info:
            msg = 'id,ref,province,final state,qualifying line state,line date\n'
            for accred in accred_dict:
                msg += str(accred.id) + ',' + str(accred.state_id.name) + ','\
                       + str(accred.final_state) + ',' + str(accred_dict.get(accred).pa_status) \
                       + ',' + str(accred_dict.get(accred).pa_date) + '\n'
            raise Warning(_(msg))
        headers = [_('REF'), _('NAME'), _('phone'), _('email'), _('reg dt'), _('approve dt'), _('extension'), _('exist'), _('final state')]

        for accred in accred_dict.keys():
            val = {
                'provider_accreditation_ref': accred.provider_accreditation_ref,
                'name':accred.name,
                'phone':accred.phone,
                'email':accred.email,
                # 'provider_register_date':accred.provider_register_date,
                'provider_register_date':accred_dict.get(accred).pa_date,
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
        # accreds = self.env['provider.accreditation'].search(
        #     [('create_date', '>=', self.from_date), ('create_date', '<=', self.to_date)])
        """
                build up a list of unique accreds with the statuses to ensure ommission of non valid accreds and precision of date filters
                """
        accred_dict = {}
        broken_accreds = {}
        statuses = self.env['provider.accreditation.status'].search(
            [('pa_date', '>=', self.from_date), ('pa_date', '<=', self.to_date), ('pa_status', '=', 'Recommended')])
            # [('pa_date', '>=', self.from_date), ('pa_date', '<=', self.to_date), ('pa_status', '=', 'Submitted')])
        # first time add to dict, all times after, compare the min(id) and add lowest stat
        for stat in statuses:
            dbg(stat)
            dbg(stat.pro_acc_status_ids)
            min_found = []
            # checks if attched to an accred rec
            if stat.pro_acc_status_ids:
                # checks if accred is in dict yet
                if stat.pro_acc_status_ids not in accred_dict.keys():
                    # loops through all stats in the attached accred and adds all recommended ones to the min list
                    for stat_line in stat.pro_acc_status_ids.provider_accreditation_status_ids:
                        if stat_line.pa_status == 'Recommended':
                            min_found.append(stat_line)
                    # checks if the min stat found is in the date range and adds if true
                    if min(min_found).pa_date >= self.from_date and min(min_found).pa_date <= self.to_date:
                        accred_dict.update({stat.pro_acc_status_ids: min(min_found)})
                        dbg("not in the stat, adding new")
                        dbg(stat.read())
                    else:
                        dbg("not adding, the min stat thats recommended isnt in the date range:" + str(min(min_found).pa_date))
                # found in dict already so it checks for min and adds
                else:
                    dbg("else:")
                    # finds out if the id is lower and if its in the range. adds if true
                    if stat < accred_dict.get(stat.pro_acc_status_ids) and stat.pa_date >= self.from_date and stat.pa_date <= self.to_date:
                        accred_dict.update({stat.pro_acc_status_ids: stat})
                        dbg("in the stat but lower id found")
            else:
                broken_accreds.update({stat:"this stat line is an orphan. no accred linked to it"})
        if self.raise_info:
            msg = 'id,ref,province,final state,qualifying line state,line date\n'
            for accred in accred_dict:
                msg += str(accred.id) + ',' + str(accred.provider_accreditation_ref) + ',' + str(accred.state_id.name) + ','\
                       + str(accred.final_state) + ',' + str(accred_dict.get(accred).pa_status) \
                       + ',' + str(accred_dict.get(accred).pa_date) + '\n'
            raise Warning(_(msg))
        # vals = []
        headers = [_('Provider Name'),
                   _('Provider Ref No '),
                   _('Provider SDLNo'),
                   _('alt provider sdl'),
                   _('Province'),
                   _('Date of Provider Accreditation application'),
                   _('Number of days it took for Provider Accreditation application to be assessed (<=140 days)'),
                   _('Date Application Recommended to ETQA / Declined  '),
                   _('final state'),
                   _('In Progress'),
                   _('Transaction type')]

        # for accred in accreds:
        for accred in accred_dict.keys():
            stat_dict = {}
            sub = {}
            if accred.final_state in ['Recommended','Submitted','Approved','Evaluated','Recommended2','Validated','Rejected']:
                dbg(len(accred.provider_accreditation_status_ids))
                if len(accred.provider_accreditation_status_ids) > 2:
                    dbg(accred.provider_accreditation_ref)
                    for stat in accred.provider_accreditation_status_ids:
                        if stat.pa_status == 'Submitted':
                            sub.update({'date_updated':stat.pa_date})
                        if stat.pa_status == 'Recommended':
                            stat_dict.update({stat.id:{'stat':stat.pa_status,'date_updated':stat.pa_date}})
                        if stat.pa_status == 'Rejected':
                            stat_dict.update({stat.id: {'stat': stat.pa_status, 'date_updated': stat.pa_date}})

                    dbg(sub)
                    # todo: uncomment below and deal with dirty data
                    if not sub:
                        broken_accreds.update({accred.provider_accreditation_ref:"didnt have a submission line item"})
                    if not stat_dict:
                        broken_accreds.update({accred.provider_accreditation_ref:"had no relevant statuses"})
                        # raise Warning(_('missing statuses from accreditation: ' + accred.provider_accreditation_ref))
                    elif len(stat_dict) == 2:
                        del stat_dict[max(stat_dict)]
                    elif len(stat_dict) == 3:
                        del stat_dict[max(stat_dict)]
                        del stat_dict[max(stat_dict)]
                    else:
                        dbg("toooooooooooo many " + str(stat_dict))
                        broken_accreds.update({accred.provider_accreditation_ref:"found too many statuses to choose from"})
                    # if len(stat_dict) > 1:
                    #     raise Warning(_('there are issues in the statuses of accreditation:' + accred.provider_accreditation_ref))
                    if not accred.provider_accreditation_ref in broken_accreds:
                        created = datetime.strptime(sub['date_updated'], '%Y-%m-%d %H:%M:%S').date()
                        recommend_date = stat_dict[min(stat_dict)]['date_updated']
                        recommended = datetime.strptime(recommend_date, '%Y-%m-%d %H:%M:%S').date()
                        delta = recommended - created
                        # raise Warning(_(delta.days))
                        in_process = False
                        if accred.final_state not in ['Approved', 'Rejected']:
                            in_process = True

                        val = {
                            'provider_name': accred.name,
                            'provider_accreditation_ref': accred.provider_accreditation_ref,
                            'sdl':accred.sequence_num,
                            'alt_sdl':accred.alternate_acc_number,
                            'state_id': accred.state_id.id,
                            # 'application_date':accred.create_date,
                            'application_date':created,
                            'update_date':recommend_date,
                            'days_to_assess':delta.days,
                            'final_state':accred.final_state,
                            'in_process': in_process,
                            'transaction_status': accred.transaction_type,
                            'report_id':self.id
                        }

                        self.env['seta.reports.late.accreditations'].create(val)
                else:
                    broken_accreds.update({accred.provider_accreditation_ref:"not enough statuses to work"})
        msg = '\n'
        if self.raise_errors:
            for brk in broken_accreds:
                msg += str(brk) + ':' + str(broken_accreds[brk]) + '\n'
            raise Warning(_(msg))
        self.headers = pprint.saferepr(headers)

        return "/report_export/late_accreditation_analysis/%s"

    def _assessment_analysis(self):
        domain = [('s_date', '>=', self.from_date), ('s_date', '<=', self.to_date)]
        if self.qual_skill_assessment:
            domain.append(('pro_id.qual_skill_assessment','=',self.qual_skill_assessment))
        if self.assessment_state:
            domain.append(('state','=',self.assessment_state))
        dbg(domain)
        assess_dict = {}
        # stats = self.env['assessment.status'].search([('')])
        stats = self.env['assessment.status'].search(domain)
        dbg(stats)
        for stat in stats:
            if stat.pro_id not in assess_dict.keys():
                assess_dict.update({stat.pro_id: stat})
            else:
                if stat < assess_dict.get(stat.pro_id):
                    assess_dict.update({stat.pro_id: stat})
        if self.raise_info:
            msg = 'id,ref,province,state,qualifying line state,line date\n'
            for assess in assess_dict:
                msg += str(assess.id) + ','+ str(assess.name) + ',' + str(assess.provider_province.name) + ',' \
                       + str(assess.state) + ',' + str(assess_dict.get(assess).state) \
                       + ',' + str(assess_dict.get(assess).s_date) + '\n'
            raise Warning(_(msg))

        # todo: uncomment stats and fill the dict
        # vals = []
        if self.qual_skill_assessment == 'qual':
            headers = [_('NAME'), _('provider'), _('type'), _('batch'),
                       _('state'), _('province'), _('enrolled learners'), 
                       _('learner ID'),_('foreign ID'),
                       _('first name'),_('last name'),_('employed'),_('rpl'),
                       _('achieved'), _('qualification'), _('qualification id'),
                       _('learning programme id'), _('skills programme id') ]
        if self.qual_skill_assessment in ['lp','skill']:
            headers = [_('NAME'), _('provider'), _('type'), _('batch'),
                       _('state'), _('province'), _('enrolled learners'), 
                       _('learner ID'),_('foreign ID'),
                       _('first name'),_('last name'),_('employed'),_('rpl'),
                       _('achieved'), _('qualification'), _('qualification id'),
                       _('learning programme id'), _('skills programme id') ]
        if not self.qual_skill_assessment:
            headers = [_('NAME'), _('provider'), _('type'), _('batch'),
                       _('state'), _('province'), _('enrolled learners'), 
                       _('learner ID'),_('foreign ID'),
                       _('first name'),_('last name'),_('employed'),_('rpl'),
                       _('achieved'), _('qualification'), _('qualification id'),
                       _('learning programme id'), _('skills programme id') ]
        for assessment in assess_dict.keys():
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
        assess_dict = {}
        stats = self.env['assessment.status'].search([('s_date', '>=', self.from_date), ('s_date', '<=', self.to_date),('state','=','evaluate')])
        dbg(stats)
        for stat in stats:
            if stat.pro_id not in assess_dict.keys():
                assess_dict.update({stat.pro_id:stat})
            else:
                if stat < assess_dict.get(stat.pro_id):
                    assess_dict.update({stat.pro_id:stat})
        if self.raise_info:
            msg = 'id,ref,province,state,qualifying line state,line date\n'
            for assess in assess_dict:
                msg += str(assess.id) + ',' + str(assess.name) + ',' + str(assess.provider_province.name) + ',' \
                       + str(assess.state) + ',' + str(assess_dict.get(assess).state) \
                       + ',' + str(assess_dict.get(assess).s_date) + '\n'
            raise Warning(_(msg))
        # vals = []
        headers = [_('Province'),
                   _('Number of Learner applications recommended to ETQA'),
                   _('Number of Learners approved for certification'),
                   _('Number of Learners Declined'),
                   _('% Of Learners approved for certification'),
                   _('% Of Declined learners'),
                   _('In Progress')]
        dbg(assessments)
        provinces = {}
        provinces[undefined_prov] = {'approved_count': 0, 'denied_count': 0, 'approved_perc': 0,
                                     'denied_perc': 0, 'total': 0}
        for assessment in assess_dict.keys():
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
    final_state = fields.Char()
    in_process = fields.Char()
    transaction_status = fields.Char()
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
    new_registration_count = fields.Float()
    re_registration_count = fields.Float()
    extension_of_scope_count = fields.Float()
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
    in_process = fields.Char()
    transaction_type = fields.Char()
    report_id = fields.Many2one("seta.reports", "Report Id")


class SETAReportetqaApprovalAccreditationAnalysis(models.TransientModel):
    _name = 'seta.reports.etqa.approval.accreditation.analysis'

    province = fields.Many2one('res.country.state')
    total = fields.Float()
    approved_count = fields.Float()
    denied_count = fields.Float()
    denied_perc = fields.Float()
    approved_perc = fields.Float()
    new_prog_approval = fields.Float()
    new_accred = fields.Float()
    reaccred = fields.Float()
    extension = fields.Float()

    report_id = fields.Many2one("seta.reports", "Report Id")


class SETAReportetqaSDPsNoLearners(models.TransientModel):
    _name = 'seta.reports.etqa.sdps.no.learners'

    provider_id = fields.Many2one('res.partner')
    start_date = fields.Date()
    end_date = fields.Date()
    qualification_ids = fields.Many2many('provider.master.qualification','report_prov_quals','prov_id','qual_id')
    skill_ids = fields.Many2many('skills.programme.master.rel','report_prov_skills','prov_id','skill_id')
    lp_ids = fields.Many2many('learning.programme.master.rel','report_prov_lps','prov_id','lp_id')
    report_id = fields.Many2one("seta.reports", "Report Id")

