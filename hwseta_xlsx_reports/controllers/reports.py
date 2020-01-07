from collections import deque
import ast

from openerp import http, _
from openerp.http import request
from openerp.tools import ustr
# from openerp.tools.misc import xlwt
# import xlsxwriter as xlwt
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
        worksheet.write_merge(0, 0, 0, 23, _("accreditation report FROM %s TO %s") % (report.from_date, report.to_date),
                              header_bold_blue)
        worksheet.write_merge(0, 0, 24, 27, _("QUARTERS"), header_bold_yellow)

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
                                                   'attachment; filename=pipeline_analysis.xls;')],
                                         cookies={})
        workbook.save(response.stream)

        return response
