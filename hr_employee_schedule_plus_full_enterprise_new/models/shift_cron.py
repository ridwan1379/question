from odoo import api, fields, models
from datetime import datetime, timedelta


class HrEmployeeShiftCron(models.Model):
    _name = 'hr.employee.shift.cron'
    _description = 'Automatic Weekly Shift Updater'

    @api.model
    def run_weekly_shift_update(self):
        """Dijalankan tiap minggu untuk update shift minggu depan"""
        employees = self.env['hr.employee'].search([('is_scheduled', '=', True)])

        for emp in employees:
            # 1. Ambil shift saat ini
            current_shift = emp.shift_type

            # 2. Rotasi Shift (Contoh sederhana)
            next_shift = self._get_next_shift(current_shift)

            emp.write({'shift_type': next_shift})

            # 3. Buat record schedule baru minggu depan
            self._create_next_week_schedule(emp, next_shift)

            # 4. Hitung otomatis jam kerja & lembur
            self._calculate_working_hours(emp)

            # 5. Kirim notifikasi email
            self._send_notification(emp)

    # ===========================
    # Fungsi bantu
    # ===========================

    def _get_next_shift(self, current_shift):
        """Contoh rotasi shift sederhana"""
        order = ['pagi', 'siang', 'malam']

        if current_shift not in order:
            return 'pagi'

        idx = order.index(current_shift)
        next_idx = (idx + 1) % len(order)
        return order[next_idx]

    def _create_next_week_schedule(self, employee, next_shift):
        """Sinkron data schedule minggu depan"""
        next_monday = datetime.today() + timedelta(days=(7 - datetime.today().weekday()))
        self.env['hr.employee.schedule'].create({
            'employee_id': employee.id,
            'shift_type': next_shift,
            'date': next_monday,
        })

    def _calculate_working_hours(self, employee):
        """Hitung jam kerja dan lembur otomatis"""
        schedules = self.env['hr.employee.schedule'].search([
            ('employee_id', '=', employee.id)
        ])

        total_hours = sum(s.hours_worked for s in schedules)
        employee.weekly_hours = total_hours

        # lembur = jam kerja - 40
        employee.overtime_hours = max(0, total_hours - 40)

    def _send_notification(self, employee):
        """Kirim email reminder ke employee dan manager"""
        template = self.env.ref('hr_employee_schedule_plus.email_template_shift_update')
        if template:
            template.send_mail(employee.id, force_send=True)
