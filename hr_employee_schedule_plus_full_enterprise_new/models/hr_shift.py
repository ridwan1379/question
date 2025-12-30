# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HrShift(models.Model):
    _name = 'hr.shift'
    _description = 'Employee Shift'
    _order = 'start_time'

    name = fields.Char(required=True)
    code = fields.Char(string='Code')
    shift_type = fields.Selection([
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('night', 'Night'),
    ], required=True)
    start_time = fields.Float('Start Time', help='Hour as float, e.g. 8.5 = 08:30')
    end_time = fields.Float('End Time')
    duration = fields.Float(compute='_compute_duration', store=True)
    active = fields.Boolean(default=True)
    allow_overlap = fields.Boolean('Allow Overlap', default=False,
                                   help='Allow employees to have overlapping assignments for this shift')
    color = fields.Integer()

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for r in self:
            if r.start_time is None or r.end_time is None:
                r.duration = 0.0
            else:
                r.duration = (r.end_time - r.start_time) if r.end_time >= r.start_time else (24 - r.start_time + r.end_time)

    @api.constrains('start_time', 'end_time')
    def _check_times(self):
        for r in self:
            if r.start_time is None or r.end_time is None:
                continue
            if r.start_time == r.end_time:
                raise ValidationError(_('Start time and End time cannot be the same.'))
