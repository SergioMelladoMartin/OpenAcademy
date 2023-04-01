from odoo import models, fields, api

class Session(models.Model):
    _name = "open_academy.session"
    _description = "OpenAcademy Sessions"
    
    name = fields.Char(string="Name", required=True)
    initial_date = fields.Date(string="Initial Date", required=True, default=fields.Date.today)
    duration = fields.Float(string="Duration", required=True)
    number_of_seats = fields.Integer(string="Number of Seats", required=True)
    course = fields.Many2one('open_academy.course', string='Course')
    course_title = fields.Char(string="Course Title", related='course.title')
    instructor = fields.Many2one('res.partner', domain=[
            '|',
            ('is_instructor', '=', True),
            '&',
            ('category_id.name', 'ilike', 'level%'),
            ('category_id.parent_id.name', 'ilike', 'teacher')
        ]
    )
    attendees = fields.Many2many('res.partner', string='Attendees', required=True) 
    attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count',  store=True)
    taken_seats = fields.Float(string="Taken Seats", compute='_taken_seats')
    color = fields.Integer(compute='_define_color')

    @api.depends('attendees')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendees)
    
    @api.depends('number_of_seats', 'attendees')
    def _taken_seats(self):
        for r in self:
            if r.number_of_seats == 0:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendees) / r.number_of_seats
                
    @api.depends('duration')
    def _define_color(self):
        for r in self:
            if r.duration < 5:
                r.color = 1
            elif r.duration < 15:
                r.color = 2
            else:
                r.color = 3
                
    @api.onchange('number_of_seats', 'attendees')
    def _verify_valid_seats(self):
        if self.number_of_seats < 0:
            self.number_of_seats = 0
            return {
                'warning': {
                    'title': "Number of seats must be positive",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.number_of_seats < len(self.attendees):
            self.number_of_seats = len(self.attendees)
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }
    
    @api.constrains('instructor', 'attendees')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor in r.attendees:
                raise models.ValidationError("A session's instructor can't be an attendee")
