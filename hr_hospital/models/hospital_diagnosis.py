from odoo import models, fields


class HospitalDiagnosis(models.Model):
    _name = 'hospital.diagnosis'
    _description = 'Hospital Diagnoses'
    _inherit = ['mail.thread']

    set_date = fields.Date(
        required=True,
    )
    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        required=True,
    )
    patient_id = fields.Many2one(
        comodel_name='hospital.patient',
        required=True,
    )
    disease_id = fields.Many2one(
        comodel_name='hospital.disease',
        required=True,
    )
    disease_category = fields.Char(
        string='Disease Category',
        related='disease_id.category_id.name',
        store=True,
    )
    treatment = fields.Text()

    # Default methods
    def name_get(self):
        return [(
            rec.id, f'Patient {rec.patient_id.surname} - {rec.disease_id.name}'
        ) for rec in self
        ]
