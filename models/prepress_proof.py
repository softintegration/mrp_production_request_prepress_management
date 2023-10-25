# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import UserError,ValidationError

# if the related manufacturing requests are in one of this states,we have to prevent the canceling of the prepress proof,
# FIXME : here we have added the «planned» state although it is not declared the main parent module «prepress_management» but since doesn't heurt ,contrary it allow to cover all the possible states
AVOIDED_CANCEL_MANUFACTURING_REQUEST_STATES = ['waiting','validated','planned','done']

class PrepressProof(models.Model):
    _inherit = 'prepress.proof'


    def _related_mrp_production_request(self):
        self.ensure_one()
        domain = [('prepress_proof_id','=',self.id)]
        return self.env['mrp.production.request'].search(domain)

    # the check must be added in the 2 phases of canceling/quarantine to overcome to situation where the state of the related manufacturing request
    # can be modified between the displaying of motif wizard and the real action

    # add some constraints to cancel

    def action_cancel_with_motif(self):
        self._check_related_mrp_production_request()
        return super(PrepressProof,self).action_cancel_with_motif()

    def _check_cancel(self):
        super(PrepressProof,self)._check_cancel()
        self._check_related_mrp_production_request()

    def _check_related_mrp_production_request(self):
        for each in self:
            if set(each._related_mrp_production_request().mapped("state")).intersection(set(AVOIDED_CANCEL_MANUFACTURING_REQUEST_STATES)):
                raise ValidationError(_("All related manufacturing requests related to proof %s must be draft or cancelled")%each.name)


    # add some constraints to quarantine

    def quarantine_check(self):
        super(PrepressProof,self).quarantine_check()
        self._check_related_mrp_production_request()

    def action_quarantine_wizard(self):
        self._check_related_mrp_production_request()
        return super(PrepressProof,self).action_quarantine_wizard()
