from odoo import models, fields


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctors'

    name = fields.Char(
        string='Name',
        required=True
    )
    phone = fields.Char(
        string='Phone'
    )
    email = fields.Char(
        string='Email'
    )
    address = fields.Char(
        string='Address'
    )
    age = fields.Integer(
        string='Age'
    )
    gender = fields.Selection(
        selection=[('male', 'Male'),
                   ('female', 'Female'),
                   ('other', 'Other')],
        string='Gender',
        required=True
    )
    patient_ids = fields.One2many(
        comodel_name='hospital.patient',
        inverse_name='doctor_id',
        string='Patients'
    )
    visit_ids = fields.One2many(
        comodel_name='hospital.visit',
        inverse_name='doctor_id',
        string='Patient visits'
    )
