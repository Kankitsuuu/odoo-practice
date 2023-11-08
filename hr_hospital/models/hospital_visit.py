import pprint
from typing import NoReturn, Optional
from pytz import timezone
from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class HospitalVisit(models.Model):
    _name = 'hospital.visit'
    _description = 'Hospital Visits'

    set_date = fields.Datetime(
        string='Time',
        required=True,
    )
    is_canceled = fields.Boolean(
        string='Canceled',
        default=False,
    )
    is_succeed = fields.Boolean(
        string='Success',
    )
    patient_id = fields.Many2one(
        comodel_name='hospital.patient',
        required=True,
    )
    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        required=True,
    )
    diagnosis_id = fields.Many2one(
        comodel_name='hospital.diagnosis',
    )

    # Default methods
    def name_get(self):
        data = []
        for rec in self:
            patient = rec.patient_id.surname
            doctor = rec.doctor_id.surname
            data.append(
                (rec.id, f'{patient}-{doctor} {rec.set_date.date()}')
            )
        return data

    # Constraints and onchanges
    @api.onchange('date', 'patient_id', 'doctor_id', 'diagnosis_id')
    def _onchange_visit_data(self):
        for visit in self:
            if visit.set_date and (datetime.now() > visit.set_date):
                raise ValidationError(_(
                    'You cannot change this field.'
                ))

    # CRUD methods
    @api.model
    def create(self, vals):
        visit_time = datetime.strptime(vals['set_date'], DATETIME_FORMAT)
        doctor_id = vals['doctor_id']
        self.check_time_exists(visit_time, doctor_id)
        self.check_doctor_schedule(visit_time, doctor_id)
        return super(HospitalVisit, self).create(vals)

    def write(self, vals):
        if vals.get('patient_id'):
            raise UserError(_('You cannot change patient for visit.'))

        for visit in self:
            if vals.get('is_canceled') and visit.is_succeed is True:
                raise UserError(_('You cannot set canceled status for successful visit.'))

            elif vals.get('set_date') or vals.get('doctor_id'):
                visit_time = datetime.strptime(vals['set_date'], DATETIME_FORMAT) \
                    if vals.get('set_date') else visit.set_date
                doctor_id = vals['doctor_id'] if vals.get('doctor_id') else visit.doctor_id.id
                self.check_time_exists(visit_time, doctor_id)
                self.check_doctor_schedule(visit.set_date, doctor_id)

        return super(HospitalVisit, self).write(vals)

    def unlink(self):
        if self.diagnosis_id:
            raise UserError(_(
                'You cannot delete records with diagnosis.'
            ))
        return super(HospitalVisit, self).unlink()

    # Custom methods
    @api.model
    def check_time_exists(self, visit_time: datetime, doctor_id: int) -> Optional[NoReturn]:
        visit = self.search([
            ('set_date', '<=', visit_time + timedelta(minutes=15)),
            ('set_date', '>=', visit_time - timedelta(minutes=15)),
            ('doctor_id', '=', doctor_id),
            ('patient_id', '!=', self.patient_id.id),
            ('is_canceled', '=', False)
        ])
        if visit:
            raise UserError(_(
                'An appointment for this time already exists.'
                'Try to choose a different time.'
            ))

    @api.model
    def check_doctor_schedule(self, visit_time: datetime, doctor_id: int) -> Optional[NoReturn]:
        visit_date = visit_time.date()
        doctor_schedules = self.env['hospital.doctor.schedule'].search([
            ('doctor_id', '=', doctor_id),
            ('work_date', '=', visit_date)
        ])
        if doctor_schedules:
            visit_time = visit_time.astimezone(timezone(self._context['tz']))
            for schedule in doctor_schedules:
                visit_time_value: float = visit_time.time().hour + visit_time.time().minute/60
                if schedule.start_time <= visit_time_value <= schedule.end_time:
                    return
        raise UserError(_("There are no doctor's office hours at this time."))
