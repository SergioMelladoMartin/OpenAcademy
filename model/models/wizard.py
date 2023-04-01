from odoo import models, fields

class Wizard(models.TransientModel):
    _name = 'open_academy.wizard'
    _description = "Wizard: Quick Registration of Attendees to Sessions"
    
    session = fields.Many2one('open_academy.session', string="Session", required=True, default=lambda self: self.env['open_academy.session'].browse(self._context.get('active_id')))
    attendees = fields.Many2many('res.partner', string="Attendees")

    def add_attendees(self):
        for r in self.session:
            r.attendees |= self.attendees