from typing import NoReturn, Optional
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HospitalDoctorSchedule(models.Model):
    _name = 'hospital.doctor.schedule'
    _description = 'Hospital Doctor Schedule'

    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        required=True,
    )
    work_date = fields.Date(
        string='Date',
        required=True,
    )
    start_time = fields.Float(
        string='From',
        required=True,
        default=9,
    )
    end_time = fields.Float(
        string='To',
        required=True,
        default=17,
    )

    # Default methods
    def name_get(self):
        data = []
        for rec in self:
            doctor = rec.doctor_id.surname
            data.append(
                (rec.id, f'Doctor {doctor} {rec.work_date}')
            )
        return data

    # CRUD methods
    @api.model
    def create(self, vals):
        self.check_time_conditions(vals)
        return super(HospitalDoctorSchedule, self).create(vals)

    # Custom methods
    def check_time_conditions(self, vals) -> Optional[NoReturn]:
        domain = [
            ('work_date', '=', vals['work_date']),
            ('doctor_id', '=', vals['doctor_id'])
        ]
        start, end = vals['start_time'], vals['end_time']

        if not 0 <= start < end < 24:
            raise UserError(_('Wrong time data.'))

        for record in self.search(domain):
            conditions = [
                record.start_time <= start <= record.end_time,
                record.start_time <= end <= record.end_time,
                start <= record.start_time < record.end_time <= end
            ]
            if any(conditions):
                raise UserError(
                    _('You cannot set a schedule with existing office hours')
                )
