# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    is_scheduled = fields.Boolean(string="Is Scheduled")
    is_scheduled = fields.Boolean('Is Scheduled', default=False)
    shift_type = fields.Selection([
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('night', 'Night'),
    ], string='Primary Shift')
    cuti_total = fields.Float(
        string="Total Cuti",
        help="Total jatah cuti tahunan karyawan."
    )

    cuti_terpakai = fields.Float(
        string="Cuti Terpakai",
        help="Jumlah cuti yang sudah dipakai."
    )

    cuti_sisa = fields.Float(
        string="Sisa Cuti",
        compute="_compute_cuti_sisa",
        store=True
    )

    def _compute_cuti_sisa(self):
        for rec in self:
            rec.cuti_sisa = rec.cuti_total - rec.cuti_terpakai

    shift_ids = fields.Many2many('hr.shift', 'hr_employee_shift_rel', 'employee_id', 'shift_id', string='Assigned Shifts')
    current_shift_id = fields.Many2one('hr.shift', string='Current Shift')
    shift_history_ids = fields.One2many('hr.shift.history', 'employee_id', string='Shift History')

    shift_conflict = fields.Boolean(compute='_compute_shift_conflict', string='Has Shift Conflict')

    @api.depends('shift_ids')
    def _compute_shift_conflict(self):
        for rec in self:
            rec.shift_conflict = False
            shifts = rec.shift_ids
            for i in range(len(shifts)):
                for j in range(i+1, len(shifts)):
                    s1 = shifts[i]
                    s2 = shifts[j]
                    if s1.allow_overlap:
                        continue
                    if _time_overlap(s1.start_time, s1.end_time, s2.start_time, s2.end_time):
                        rec.shift_conflict = True

    def action_assign_shift(self, shift_id, date_from=False, date_to=False, notify=False, force=False):
        self.ensure_one()
        shift = self.env['hr.shift'].browse(shift_id)
        if not shift:
            raise ValidationError(_('Shift not found'))
        if not shift.allow_overlap and not force:
            for s in self.shift_ids:
                if _time_overlap(shift.start_time, shift.end_time, s.start_time, s.end_time):
                    raise ValidationError(_('This assignment would create a conflict with %s') % s.name)
        if shift not in self.shift_ids:
            self.write({'shift_ids': [(4, shift.id)]})
        self.write({'current_shift_id': shift.id, 'shift_type': shift.shift_type, 'is_scheduled': True})
        vals = {'employee_id': self.id, 'shift_id': shift.id}
        if date_from:
            vals['date_from'] = date_from
        if date_to:
            vals['date_to'] = date_to
        self.env['hr.shift.history'].create(vals)
        if notify:
            template = self.env.ref('hr_employee_schedule_plus.email_shift_assignment', False)
            if template:
                template.send_mail(self.id, force_send=True)

    def action_unassign_shift(self, shift_id, date_to=False):
        self.ensure_one()
        shift = self.env['hr.shift'].browse(shift_id)
        if shift in self.shift_ids:
            self.write({'shift_ids': [(3, shift.id)]})
        if date_to:
            last = self.env['hr.shift.history'].search([('employee_id', '=', self.id), ('shift_id', '=', shift.id)], order='date_from desc', limit=1)
            if last:
                last.date_to = date_to

def _time_overlap(a1, a2, b1, b2):
    if a1 is None or a2 is None or b1 is None or b2 is None:
        return False
    def norm(x):
        return float(x)
    a1, a2, b1, b2 = norm(a1), norm(a2), norm(b1), norm(b2)
    def ranges(s, e):
        if e >= s:
            return [(s, e)]
        else:
            return [(s, 24.0), (0.0, e)]
    for r1 in ranges(a1, a2):
        for r2 in ranges(b1, b2):
            if r1[0] < r2[1] and r2[0] < r1[1]:
                return True
    return False
