from odoo import models, fields, api

class MessageWizard(models.TransientModel):
    _name = 'message.wizard'

    @api.multi
    def action_ok(self):
        """ close wizard"""
        return {'type': 'ir.actions.act_window_close'}