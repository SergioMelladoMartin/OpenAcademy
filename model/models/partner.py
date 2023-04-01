from odoo import models, fields

class Partner(models.Model):
    _inherit = 'res.partner'
    
    is_instructor = fields.Boolean("Instructor", default=False)
    sessions = fields.Many2many('open_academy.session', string="Sessions")
