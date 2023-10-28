from odoo import models, fields


class HospitalDisease(models.Model):
    _name = 'hospital.disease'
    _description = 'Disease types'

    name = fields.Char(
        string='Disease name',
        required=True
    )
    description = fields.Text(
        string='Disease description'
    )
    patient_ids = fields.Many2many(
        comodel_name='hospital.patient',
        string='Patients'
    )
