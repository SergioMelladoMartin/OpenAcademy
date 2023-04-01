from odoo import models, fields, api

class Course(models.Model):
    _name = "open_academy.course"
    _description = "OpenAcademy Courses"
    _sql_constraints = [
        ('name_description_check', 'CHECK(title != description)', "The title of the course should not be the description"),
        ('name_unique', 'UNIQUE(title)', "The course title must be unique"),
    ]

    title = fields.Char(string="title", required=True)
    name = fields.Char(compute='_get_name', store=True)
    description = fields.Text()
    sessions = fields.One2many('open_academy.session', 'course', string='Sessions')
    sessions_count = fields.Integer(compute='_get_sessions_count', string='Sessions count')
    responsible = fields.Many2one('res.users', string="Responsible", required=True)
    type = fields.Selection([('online', 'Online'), ('presential', 'Presential')], string="Type", default='online')
    
    @api.depends('title', 'responsible')
    def _get_name(self):
        for r in self:
            r.name = r.title + ' - ' + r.responsible.name
            
    @api.depends('sessions')
    def _get_sessions_count(self):
        for r in self:
            r.sessions_count = len(r.sessions)

    def copy(self):
        return super().copy(default={'title': self.title + ' (copy)'})