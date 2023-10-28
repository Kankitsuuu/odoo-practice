from odoo import models, fields, api
from datetime import datetime


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patients'
    _inherit = 'hospital.person'

    birthday_date = fields.Date(
        required=True,
    )
    age = fields.Integer(
        compute='_compute_age',
        readonly=True,
    )
    passport = fields.Char(
        string='Passport(Details)',
        required=True,
    )
    contact_person_id = fields.Many2one(
        comodel_name='hospital.contact.person',
    )
    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Supervising doctor',
    )
    visit_ids = fields.One2many(
        comodel_name='hospital.visit',
        inverse_name='patient_id',
        string='Visits',
    )
    disease_ids = fields.Many2many(
        comodel_name='hospital.disease',
        string='Diseases',
    )

    # Compute methods
    @api.depends('birthday_date')
    def _compute_age(self) -> None:
        today = datetime.today()
        for record in self:
            birthday = record.birthday_date
            if birthday:
                current = (today.month, today.day) < (birthday.month, birthday.day)
                record.age = today.year - birthday.year - current
            else:
                record.age = None

    # CRUD methods
    @api.model
    def create(self, vals_list):
        res = super(HospitalPatient, self).create(vals_list)
        if vals_list.get('doctor_id'):
            record = {
                'time': datetime.now(),
                'doctor_id': vals_list['doctor_id'],
                'patient_id': res.id,
            }
            self.env['hospital.doctor.change'].create(record)
        return res

    def write(self, vals) -> bool:
        if vals.get('doctor_id') and self.doctor_id.id != vals['doctor_id']:
            record = {
                'time': datetime.now(),
                'doctor_id': vals['doctor_id'],
                'patient_id': self._origin.id,
            }
            self.env['hospital.doctor.change'].create(record)
        return super(HospitalPatient, self).write(vals)
