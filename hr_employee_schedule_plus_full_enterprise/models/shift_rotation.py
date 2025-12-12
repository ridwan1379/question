# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ShiftRotation(models.Model):
    _name = 'hr.shift.rotation'
    _description = 'Shift Rotation Rule'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    shift_ids = fields.Many2many('hr.shift', 'rotation_shift_rel', 'rotation_id', 'shift_id', string='Rotation Shifts')
    employee_ids = fields.Many2many('hr.employee', 'rotation_employee_rel', 'rotation_id', 'employee_id', string='Employees')
    active = fields.Boolean(default=True)

    def apply_rotation(self):
        for rot in self:
            shifts = rot.shift_ids
            emps = rot.employee_ids
            if not shifts or not emps:
                continue
            idx = 0
            for emp in emps:
                shift = shifts[idx % len(shifts)]
                emp.action_assign_shift(shift.id, notify=True)
                idx += 1
