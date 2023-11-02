from odoo import models, fields


class HospitalDoctorSpecialty(models.Model):
    _name = 'hospital.doctor.specialty'
    _description = 'Hospital Doctor Specialties'

    name = fields.Char(
        required=True,
    )
