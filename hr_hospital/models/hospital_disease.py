from odoo import models, fields


class HospitalDisease(models.Model):
    _name = 'hospital.disease'
    _description = 'Hospital Diseases'
    _parent_name = 'parent_id'

    name = fields.Char(
        required=True
    )
    description = fields.Text(
    )
    patient_ids = fields.Many2many(
        comodel_name='hospital.patient',
        string='Patients'
    )
    parent_id = fields.Many2one(
        comodel_name='hospital.disease',
        string='Parent Disease',
        ondelete='cascade',
    )
