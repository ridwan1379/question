# -*- coding: utf-8 -*-
from odoo import api, fields, models

class HrShiftHistory(models.Model):
    _name = 'hr.shift.history'
    _description = 'Employee Shift History'
    _order = 'date_from desc'

    employee_id = fields.Many2one('hr.employee', required=True, ondelete='cascade')
    shift_id = fields.Many2one('hr.shift', required=True)
    date_from = fields.Date(required=True, default=fields.Date.context_today)
    date_to = fields.Date()
    note = fields.Text()
