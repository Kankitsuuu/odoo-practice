from typing import NoReturn, Optional, Union
from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class HospitalVisit(models.Model):
    _name = 'hospital.visit'
    _description = 'Hospital Visits'

    date = fields.Datetime(
        string='Time',
        required=True,
    )
    is_canceled = fields.Boolean(
        string='Canceled status',
        default=False,
    )
    is_succeed = fields.Boolean(
        string='Success status',
    )
    patient_id = fields.Many2one(
        comodel_name='hospital.patient',
        string='Patient',
        required=True,
    )
    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Doctor',
        required=True,
    )
    diagnosis_id = fields.Many2one(
        comodel_name='hospital.diagnosis',
        string='Diagnosis',
    )

    # Default methods
    def name_get(self) -> list:
        return [
            (rec.id, f'{rec.patient_id.surname} {rec.date.date()}') for rec in self
        ]

    # Constraints and onchanges
    @api.onchange('date', 'patient_id', 'doctor_id', 'diagnosis_id')
    def _onchange_visit_data(self) -> Optional[NoReturn]:
        if self.date and (datetime.now() > self.date):
            raise UserError(_('You cannot change this field.'))

    # CRUD methods
    @api.model
    def create(self, vals_list):
        print(self.patient_id.id)
        visit_time = datetime.strptime(vals_list['date'], DATETIME_FORMAT)
        doctor_id = vals_list['doctor_id']
        self.check_time_exists(visit_time, doctor_id)
        self.check_doctor_schedule(visit_time, doctor_id)
        return super(HospitalVisit, self).create(vals_list)

    def write(self, vals) -> Union[bool, NoReturn]:
        if vals.get('patient_id'):
            raise UserError(_('You cannot change patient for visit.'))

        elif vals.get('is_canceled') and self.is_succeed is True:
            raise UserError(_('You cannot set canceled status for successful visit.'))

        elif vals.get('date') or vals.get('doctor_id'):
            visit_time = datetime.strptime(vals['date'], DATETIME_FORMAT) if vals.get('date') else self.date
            doctor_id = vals['doctor_id'] if vals.get('doctor_id') else self.doctor_id.id
            self.check_time_exists(visit_time, doctor_id)
            self.check_doctor_schedule(self.date, doctor_id)

        return super(HospitalVisit, self).write(vals)

    def unlink(self):
        if self.diagnosis_id:
            raise UserError(_('You cannot delete records with diagnosis.'))
        return super(HospitalVisit, self).unlink()

    # Custom methods
    def check_time_exists(self, visit_time: datetime, doctor_id: int) -> Optional[NoReturn]:
        record = self.search([
            ('date', '<=', visit_time + timedelta(minutes=15)),
            ('date', '>=', visit_time - timedelta(minutes=15)),
            ('doctor_id', '=', doctor_id),
            ('patient_id', '!=', self.patient_id.id),
            ('is_canceled', '=', False)
        ])
        if record:
            raise UserError(_(
                'An appointment for this time already exists.'
                'Try to choose a different time.'
            ))

    def check_doctor_schedule(self, visit_time: datetime, doctor_id: int) -> Optional[NoReturn]:
        visit_date = visit_time.date()
        doctor_schedules = self.env['hospital.doctor.schedule'].search([
            ('doctor_id', '=', doctor_id),
            ('date', '=', visit_date)
        ])
        print(doctor_schedules)
        if doctor_schedules:
            for schedule in doctor_schedules:
                visit_time_value: float = visit_time.time().hour + visit_time.time().minute/60
                if schedule.start_time <= visit_time_value <= schedule.end_time:
                    return
        raise UserError(_("There are no doctor's office hours at this time."))
