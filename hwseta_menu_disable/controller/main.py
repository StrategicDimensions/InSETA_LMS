from openerp.addons.web import http
from openerp.http import request
from datetime import datetime
DEBUG = True

if DEBUG:
    import logging

    logger = logging.getLogger(__name__)


    def dbg(msg):
        logger.info(msg)
else:
    def dbg(msg):
        pass

class ActionClass(http.Controller):

    @http.route('/check_expired_menus', type="http", website=True, auth="public", csrf=False)
    def return_actionids(self, **kwargs):
        dbg('return_actionids')
        user = http.request.env['res.users'].sudo()
        user_brw = user.search([('id', '=', http.request.uid)])
        partner_obj = user_brw.partner_id
        provider_end_date = partner_obj.provider_end_date
        today = datetime.now().date()
        todays_date = today.strftime('%Y-%m-%d')
        print "Todays Date======", todays_date
        dbg('-------------------------------provider_end_date :' + str(provider_end_date))
        dbg('-------------------------------provider bool :' + str(partner_obj.provider))
        action_list = []
        if provider_end_date < todays_date and partner_obj.provider == True:
            action_ids1 = request.env.ref(
                'hwseta_etqe.action_providers_form').id
            if action_ids1:
                action_list.append(action_ids1)
            action_ids2 = request.env.ref(
                'hwseta_etqe.action_provider_learner_view').id
            if action_ids2:
                action_list.append(action_ids2)
            action_ids3 = request.env.ref(
                'hwseta_etqe.open_view_assessment_list_my').id
            if action_ids3:
                action_list.append(action_ids3)
            action_ids4 = request.env.ref(
                'hwseta_etqe.learner_registration_action').id
            if action_ids4:
                action_list.append(action_ids4)
        # else:
        #     # add entries for admin menu items
        #     action_ids5 = request.env.ref(
        #         'hwseta_etqe.action_provider_learner_view_admin').id
        #     if action_ids5:
        #         action_list.append(action_ids5)
        #     action_ids6 = request.env.ref(
        #         'hwseta_etqe.action_learner_registration_qualification_view_admin').id
        #     if action_ids6:
        #         action_list.append(action_ids6)
        #     action_ids7 = request.env.ref(
        #         'hwseta_etqe.action_learning_programme_learner_rel_view_admin').id
        #     if action_ids7:
        #         action_list.append(action_ids7)
        #     action_ids8 = request.env.ref(
        #         'hwseta_etqe.action_res_partner_view_admin').id
        #     if action_ids8:
        #         action_list.append(action_ids8)
        print "Action List=====", action_list
        dbg(action_list)
        return str(action_list)
