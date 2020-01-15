from collections import deque
import ast
import csv
from openerp import http, _
from openerp.http import request
from openerp.tools import ustr
# from openerp.tools.misc import xlwt
# import xlsxwriter as xlwt
import openpyxl
from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
# wb = load_workbook('filename.xlsx')
# wb = Workbook(write_only=True)
# .
# .
# .
# (make your edits)
# .
# .
# .
# wb.save('new_filename.xlsx')
try:
    import xlwt
except ImportError:
    xlwt = None

DEBUG = True

if DEBUG:
    import logging

    logger = logging.getLogger(__name__)


    def dbg(msg):
        logger.info(msg)
else:
    def dbg(msg):
        pass


class ReportExporter(http.Controller):
    @http.route('/web/pivot/check_xlwt', type='json', auth='none')
    def check_xlwt(self):
        return xlwt is not None

    @http.route(['/report_export/accreditation_analysis/<int:report_id>'], type='http', auth="user")
    def accreditation_analysis(self, report_id, **kw):
        # jdata = json.loads(data)

        report = request.env['seta.reports'].search([('id', '=', report_id)])
        accreds = request.env['seta.reports.accreditations'].search([('report_id', '=', report_id)])
        headers = ast.literal_eval(report.headers)

        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet(report[0].name)
        # worksheet = workbook.add_worksheet(report[0].name)
        header_bold_blue = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour blue; align: vert center, horiz center;")
        header_bold_lightblue = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour blue; align: horiz center;")
        header_bold_yellow = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center;")
        header_bold_lightyellow = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center;")
        header_plain = xlwt.easyxf("pattern: pattern solid, fore_colour blue;")
        bold = xlwt.easyxf("font: bold on;")
        normal_yellow = xlwt.easyxf("pattern: pattern solid, fore_colour yellow; align: horiz right;")
        # Step 1: writing headers
        worksheet.write_merge(0, 0, 0, 7, _("accreditation report FROM %s TO %s") % (report.from_date, report.to_date),
                              header_bold_blue)

        for i, header in enumerate(headers):
            worksheet.write(1, i, header, header_bold_lightblue)

        for i, accred in enumerate(accreds):


            worksheet.write(i + 2, 0, accred.provider_accreditation_ref)
            worksheet.write(i + 2, 1, accred.name)
            worksheet.write(i + 2, 2, accred.phone)
            worksheet.write(i + 2, 3, accred.email)
            worksheet.write(i + 2, 4, accred.provider_register_date)
            worksheet.write(i + 2, 5, accred.provider_approval_date)
            worksheet.write(i + 2, 6, accred.is_extension_of_scope)
            worksheet.write(i + 2, 7, accred.is_existing_provider)

        # num_leads = len(leads)
        # worksheet.write_merge(num_leads + 2, num_leads + 2, 22, 23, "TOTAL", header_bold_blue)
        # worksheet.write(num_leads + 2, 24, xlwt.Formula("SUM($X$3:$X$%s)" % (num_leads + 2)), header_bold_yellow)
        # worksheet.write(num_leads + 2, 25, xlwt.Formula("SUM($Y$3:$Y$%s)" % (num_leads + 2)), header_bold_yellow)
        # worksheet.write(num_leads + 2, 26, xlwt.Formula("SUM($Z$3:$Z$%s)" % (num_leads + 2)), header_bold_yellow)
        # worksheet.write(num_leads + 2, 27, xlwt.Formula("SUM($AA$3:$AA$%s)" % (num_leads + 2)), header_bold_yellow)
        response = request.make_response(None,
                                         headers=[('Content-Type', 'application/vnd.ms-excel'),
                                                  ('Content-Disposition',
                                                   'attachment; filename=accreditation_analysis.xls;')],
                                         cookies={})
        workbook.save(response.stream)

        return response


    @http.route(['/report_export/late_accreditation_analysis/<int:report_id>'], type='http', auth="user")
    def late_accreditation_analysis(self, report_id, **kw):
        # jdata = json.loads(data)

        report = request.env['seta.reports'].search([('id', '=', report_id)])
        accreds = request.env['seta.reports.late.accreditations'].search([('report_id', '=', report_id)])
        headers = ast.literal_eval(report.headers)

        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet(report[0].name)
        # worksheet = workbook.add_worksheet(report[0].name)
        header_bold_blue = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour blue; align: vert center, horiz center;")
        header_bold_lightblue = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour blue; align: horiz center;")
        header_bold_yellow = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center;")
        header_bold_lightyellow = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center;")
        header_plain = xlwt.easyxf("pattern: pattern solid, fore_colour blue;")
        bold = xlwt.easyxf("font: bold on;")
        normal_yellow = xlwt.easyxf("pattern: pattern solid, fore_colour yellow; align: horiz right;")
        # Step 1: writing headers
        worksheet.write_merge(0, 0, 0, 8, _("late accreditation report FROM %s TO %s") % (report.from_date, report.to_date),
                              header_bold_blue)

        for i, header in enumerate(headers):
            worksheet.write(1, i, header, header_bold_lightblue)

        for i, accred in enumerate(accreds):
            worksheet.write(i + 2, 0, accred.provider_name)
            worksheet.write(i + 2, 1, accred.provider_accreditation_ref)
            worksheet.write(i + 2, 2, accred.sdl)
            worksheet.write(i + 2, 3, accred.alt_sdl)
            worksheet.write(i + 2, 4, accred.state_id.name)
            worksheet.write(i + 2, 5, accred.application_date)
            worksheet.write(i + 2, 6, accred.days_to_assess)
            worksheet.write(i + 2, 7, accred.update_date)
            worksheet.write(i + 2, 8, accred.final_state)
            # worksheet.write(i + 2, 7, accred.is_existing_provider)

        # num_leads = len(leads)
        # worksheet.write_merge(num_leads + 2, num_leads + 2, 22, 23, "TOTAL", header_bold_blue)
        # worksheet.write(num_leads + 2, 24, xlwt.Formula("SUM($X$3:$X$%s)" % (num_leads + 2)), header_bold_yellow)
        # worksheet.write(num_leads + 2, 25, xlwt.Formula("SUM($Y$3:$Y$%s)" % (num_leads + 2)), header_bold_yellow)
        # worksheet.write(num_leads + 2, 26, xlwt.Formula("SUM($Z$3:$Z$%s)" % (num_leads + 2)), header_bold_yellow)
        # worksheet.write(num_leads + 2, 27, xlwt.Formula("SUM($AA$3:$AA$%s)" % (num_leads + 2)), header_bold_yellow)
        response = request.make_response(None,
                                         headers=[('Content-Type', 'application/vnd.ms-excel'),
                                                  ('Content-Disposition',
                                                   'attachment; filename=late_accreditation_analysis.xls;')],
                                         cookies={})
        workbook.save(response.stream)

        return response

    @http.route(['/report_export/assessment_analysis/<int:report_id>'], type='http', auth="user")
    def assessment_analysis(self, report_id, **kw):
        report = request.env['seta.reports'].search([('id', '=', report_id)])
        assessments = request.env['seta.reports.assessment'].search([('report_id', '=', report_id)])
        headers = ast.literal_eval(report.headers)
        with open('assessment_analysis.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)

            writer.writeheader()
            for assessment in assessments:
                writer.writerow({'NAME': assessment.assessment.name,
                                 'provider': assessment.provider_id.name,
                                 'type': assessment.qual_skill_assessment,
                                 'batch': assessment.batch_id.batch_name,
                                 'fiscal': assessment.fiscal_year.name,
                                 'start dt': assessment.start_date,
                                 'state': assessment.assessment.state,
                                 'province': assessment.provider_province.name,
                                 'learner': '',
                                 })
                if assessment.qual_skill_assessment == 'qual':
                    for learner in assessment.assessment.learner_ids:
                        rpl = False
                        lnr = learner.learner_id
                        for quals in lnr.learner_qualification_ids:
                            if assessment.batch_id == quals.batch_id:
                                for units in quals.learner_registration_line_ids:
                                    if units.is_rpl_learner:
                                        rpl = True
                                writer.writerow({'NAME': '',
                                                 'provider': '',
                                                 'type': '',
                                                 'batch': '',
                                                 'fiscal': '',
                                                 'start dt': '',
                                                 'state': '',
                                                 'province': '',
                                                 'learner': learner.identification_id,
                                                 'rpl': rpl if rpl else '',
                                                 })
                if assessment.qual_skill_assessment == 'lp':
                    for learner in assessment.assessment.learner_ids_for_lps:
                        rpl = False
                        lnr = learner.learner_id
                        for quals in lnr.learner_qualification_ids:
                            if assessment.batch_id == quals.batch_id:
                                for units in quals.learner_registration_line_ids:
                                    if units.is_rpl_learner:
                                        rpl = True
                                writer.writerow({'NAME': '',
                                                 'provider': '',
                                                 'type': '',
                                                 'batch': '',
                                                 'fiscal': '',
                                                 'start dt': '',
                                                 'state': '',
                                                 'province': '',
                                                 'learner': learner.identification_id,
                                                 'rpl': rpl if rpl else '',
                                                 })


        response = request.make_response(None,
                                         headers=[('Content-Type', 'application/vnd.ms-excel'),
                                                  ('Content-Disposition',
                                                   'attachment; filename=assessment_analysis.csv;')],
                                         cookies={})
        dbg(response)
        with open('assessment_analysis.csv', 'r') as f2:
            data = str.encode(f2.read(), 'utf-8')
            response.response=data


        return response

    @http.route(['/report_export/assessment_approval_analysis/<int:report_id>'], type='http', auth="user")
    def assessment_approval_analysis(self, report_id, **kw):
        # jdata = json.loads(data)

        report = request.env['seta.reports'].search([('id', '=', report_id)])
        assessments = request.env['seta.reports.assessment.approval'].search([('report_id', '=', report_id)])
        headers = ast.literal_eval(report.headers)

        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet(report[0].name)
        # worksheet = workbook.add_worksheet(report[0].name)
        header_bold_blue = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour blue; align: vert center, horiz center;")
        header_bold_lightblue = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour blue; align: horiz center;")
        header_bold_yellow = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center;")
        header_bold_lightyellow = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center;")
        header_plain = xlwt.easyxf("pattern: pattern solid, fore_colour blue;")
        bold = xlwt.easyxf("font: bold on;")
        normal_yellow = xlwt.easyxf("pattern: pattern solid, fore_colour yellow; align: horiz right;")
        # Step 1: writing headers
        worksheet.write_merge(0, 0, 0, 5, _("registrations report FROM %s TO %s") % (report.from_date, report.to_date),
                              header_bold_blue)


        for i, header in enumerate(headers):
            worksheet.write(1, i, header, header_bold_lightblue)

        for i, assessment in enumerate(assessments):

            worksheet.write(i + 2, 0, assessment.province.name)
            worksheet.write(i + 2, 1, assessment.total)
            worksheet.write(i + 2, 2, assessment.approved_count)
            # worksheet.write(i + 2, 3, assessment.denied_count)
            worksheet.write(i + 2, 4, assessment.approved_perc)
            # worksheet.write(i + 2, 5, assessment.denied_perc)


        # num_leads = len(leads)
        # worksheet.write_merge(num_leads + 2, num_leads + 2, 22, 23, "TOTAL", header_bold_blue)
        # worksheet.write(num_leads + 2, 24, xlwt.Formula("SUM($X$3:$X$%s)" % (num_leads + 2)), header_bold_yellow)
        # worksheet.write(num_leads + 2, 25, xlwt.Formula("SUM($Y$3:$Y$%s)" % (num_leads + 2)), header_bold_yellow)
        # worksheet.write(num_leads + 2, 26, xlwt.Formula("SUM($Z$3:$Z$%s)" % (num_leads + 2)), header_bold_yellow)
        # worksheet.write(num_leads + 2, 27, xlwt.Formula("SUM($AA$3:$AA$%s)" % (num_leads + 2)), header_bold_yellow)
        response = request.make_response(None,
                                         headers=[('Content-Type', 'application/vnd.ms-excel'),
                                                  ('Content-Disposition',
                                                   'attachment; filename=assessment_approval_analysis.xls;')],
                                         cookies={})
        workbook.save(response.stream)

        return response

    @http.route(['/report_export/accreditation_etqa_approval_analysis/<int:report_id>'], type='http', auth="user")
    def accreditation_etqa_approval_analysis(self, report_id, **kw):
        # jdata = json.loads(data)

        report = request.env['seta.reports'].search([('id', '=', report_id)])
        assessments = request.env['seta.reports.etqa.approval.accreditation.analysis'].search([('report_id', '=', report_id)])
        headers = ast.literal_eval(report.headers)

        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet(report[0].name)
        # worksheet = workbook.add_worksheet(report[0].name)
        header_bold_blue = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour blue; align: vert center, horiz center;")
        header_bold_lightblue = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour blue; align: horiz center;")
        header_bold_yellow = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center;")
        header_bold_lightyellow = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center;")
        header_plain = xlwt.easyxf("pattern: pattern solid, fore_colour blue;")
        bold = xlwt.easyxf("font: bold on;")
        normal_yellow = xlwt.easyxf("pattern: pattern solid, fore_colour yellow; align: horiz right;")
        # Step 1: writing headers
        worksheet.write_merge(0, 0, 0, 5, _("etqa approval report FROM %s TO %s") % (report.from_date, report.to_date),
                              header_bold_blue)


        for i, header in enumerate(headers):
            worksheet.write(1, i, header, header_bold_lightblue)

        for i, assessment in enumerate(assessments):

            worksheet.write(i + 2, 0, assessment.province.name)
            worksheet.write(i + 2, 1, assessment.total)
            worksheet.write(i + 2, 2, assessment.approved_count)
            worksheet.write(i + 2, 3, assessment.denied_count)
            worksheet.write(i + 2, 4, assessment.approved_perc)
            worksheet.write(i + 2, 5, assessment.denied_perc)


        # num_leads = len(leads)
        # worksheet.write_merge(num_leads + 2, num_leads + 2, 22, 23, "TOTAL", header_bold_blue)
        # worksheet.write(num_leads + 2, 24, xlwt.Formula("SUM($X$3:$X$%s)" % (num_leads + 2)), header_bold_yellow)
        # worksheet.write(num_leads + 2, 25, xlwt.Formula("SUM($Y$3:$Y$%s)" % (num_leads + 2)), header_bold_yellow)
        # worksheet.write(num_leads + 2, 26, xlwt.Formula("SUM($Z$3:$Z$%s)" % (num_leads + 2)), header_bold_yellow)
        # worksheet.write(num_leads + 2, 27, xlwt.Formula("SUM($AA$3:$AA$%s)" % (num_leads + 2)), header_bold_yellow)
        response = request.make_response(None,
                                         headers=[('Content-Type', 'application/vnd.ms-excel'),
                                                  ('Content-Disposition',
                                                   'attachment; filename=accreditation_etqa_approval_analysis.xls;')],
                                         cookies={})
        workbook.save(response.stream)

        return response

    @http.route(['/report_export/register_approval_analysis/<int:report_id>'], type='http', auth="user")
    def register_approval_analysis(self, report_id, **kw):
        # jdata = json.loads(data)

        report = request.env['seta.reports'].search([('id', '=', report_id)])
        registrations = request.env['seta.reports.register'].search([('report_id', '=', report_id)])
        headers = ast.literal_eval(report.headers)

        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet(report[0].name)
        # worksheet = workbook.add_worksheet(report[0].name)
        header_bold_blue = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour blue; align: vert center, horiz center;")
        header_bold_lightblue = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour blue; align: horiz center;")
        header_bold_yellow = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center;")
        header_bold_lightyellow = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center;")
        header_plain = xlwt.easyxf("pattern: pattern solid, fore_colour blue;")
        bold = xlwt.easyxf("font: bold on;")
        normal_yellow = xlwt.easyxf("pattern: pattern solid, fore_colour yellow; align: horiz right;")
        # Step 1: writing headers
        worksheet.write_merge(0, 0, 0, 5, _("registrations report FROM %s TO %s") % (report.from_date, report.to_date),
                              header_bold_blue)


        for i, header in enumerate(headers):
            worksheet.write(1, i, header, header_bold_lightblue)

        for i, reg in enumerate(registrations):
            dbg(reg)
            worksheet.write(i + 2, 0, reg.province.name)
            worksheet.write(i + 2, 1, reg.total)
            worksheet.write(i + 2, 2, reg.approved_count)
            worksheet.write(i + 2, 3, reg.denied_count)
            worksheet.write(i + 2, 4, reg.approved_perc)
            worksheet.write(i + 2, 5, reg.denied_perc)


        # num_leads = len(leads)
        # worksheet.write_merge(num_leads + 2, num_leads + 2, 22, 23, "TOTAL", header_bold_blue)
        # worksheet.write(num_leads + 2, 24, xlwt.Formula("SUM($X$3:$X$%s)" % (num_leads + 2)), header_bold_yellow)
        # worksheet.write(num_leads + 2, 25, xlwt.Formula("SUM($Y$3:$Y$%s)" % (num_leads + 2)), header_bold_yellow)
        # worksheet.write(num_leads + 2, 26, xlwt.Formula("SUM($Z$3:$Z$%s)" % (num_leads + 2)), header_bold_yellow)
        # worksheet.write(num_leads + 2, 27, xlwt.Formula("SUM($AA$3:$AA$%s)" % (num_leads + 2)), header_bold_yellow)
        response = request.make_response(None,
                                         headers=[('Content-Type', 'application/vnd.ms-excel'),
                                                  ('Content-Disposition',
                                                   'attachment; filename=register_approval_analysis.xls;')],
                                         cookies={})
        workbook.save(response.stream)

        return response

    @http.route(['/report_export/mod_ass_register_8week_analysis/<int:report_id>'], type='http', auth="user")
    def mod_ass_register_8week_analysis(self, report_id, **kw):
        # jdata = json.loads(data)

        report = request.env['seta.reports'].search([('id', '=', report_id)])
        registrations = request.env['seta.reports.8week.register'].search([('report_id', '=', report_id)])
        headers = ast.literal_eval(report.headers)

        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet(report[0].name)
        # worksheet = workbook.add_worksheet(report[0].name)
        header_bold_blue = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour blue; align: vert center, horiz center;")
        header_bold_lightblue = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour blue; align: horiz center;")
        header_bold_yellow = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center;")
        header_bold_lightyellow = xlwt.easyxf(
            "font: bold on; pattern: pattern solid, fore_colour yellow; align: horiz center;")
        header_plain = xlwt.easyxf("pattern: pattern solid, fore_colour blue;")
        bold = xlwt.easyxf("font: bold on;")
        normal_yellow = xlwt.easyxf("pattern: pattern solid, fore_colour yellow; align: horiz right;")
        # Step 1: writing headers
        worksheet.write_merge(0, 0, 0, 5, _("registrations report FROM %s TO %s") % (report.from_date, report.to_date),
                              header_bold_blue)

        for i, header in enumerate(headers):
            worksheet.write(1, i, header, header_bold_lightblue)

        for i, reg in enumerate(registrations):
            worksheet.write(i + 2, 0, reg.mod_id_no)
            worksheet.write(i + 2, 1, reg.mod_name)
            worksheet.write(i + 2, 2, reg.mod_surname)
            worksheet.write(i + 2, 3, reg.province.name)
            worksheet.write(i + 2, 4, reg.application_date)
            worksheet.write(i + 2, 5, reg.update_date)
            worksheet.write(i + 2, 6, reg.days_to_update)
            worksheet.write(i + 2, 7, reg.final_state)

        response = request.make_response(None,
                                         headers=[('Content-Type', 'application/vnd.ms-excel'),
                                                  ('Content-Disposition',
                                                   'attachment; filename=mod_ass_register_8week_analysis.xls;')],
                                         cookies={})
        workbook.save(response.stream)

        return response