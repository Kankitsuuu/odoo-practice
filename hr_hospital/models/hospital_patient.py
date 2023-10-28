from odoo import models, fields


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patients'

    name = fields.Char(
        string='Name',
        required=True
    )
    phone = fields.Char(
        string='Phone number'
    )
    address = fields.Char(
        string='Address'
    )
    email = fields.Char(
        string='Email'
    )
    age = fields.Integer(
        string='Patient`s age'
    )
    gender = fields.Selection(
        selection=[('male', 'Male'),
                   ('female', 'Female'),
                   ('other', 'Other')],
        string='Gender',
        required=True
    )
    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Supervising doctor',
        required=True
    )
    visit_ids = fields.One2many(
        comodel_name='hospital.visit',
        inverse_name='patient_id',
        string='Patient visits',
    )
    disease_ids = fields.Many2many(
        comodel_name='hospital.disease',
        string='Patient diseases',
    )
