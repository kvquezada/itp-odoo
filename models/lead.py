from odoo import models, fields


class LeadsList(models.Model):
    _name = 'leads.list'

    name = fields.Char("Name")
    email = fields.Char("Email")
    phone = fields.Char("Phone")
