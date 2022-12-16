# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MrpProductionRequest(models.Model):
    """ Manufacturing Order Request """
    _inherit = 'mrp.production.request'

    prepress_proof_id = fields.Many2one('prepress.proof',string='Prepress proof',readonly=True)

    @api.onchange('product_id','company_id')
    def _onchange_product_id(self):
        res = super(MrpProductionRequest, self)._onchange_product_id()
        self._update_prepress_proof()
        return res

    def _update_prepress_proof(self):
        if not self.product_id:
            return
        prepress_proof = self.env['prepress.proof']._get_by_product(self.product_id)
        self.update({'prepress_proof_id': prepress_proof and prepress_proof.ids[0] or False})

    @api.model
    def create(self,vals):
        production_order_requests = super(MrpProductionRequest, self).create(vals)
        for request in production_order_requests:
            if not request.prepress_proof_id:
                prepress_proof = self.env['prepress.proof']._get_by_product(request.product_id)
                request.prepress_proof_id = prepress_proof and prepress_proof.ids[0] or False
        return production_order_requests











