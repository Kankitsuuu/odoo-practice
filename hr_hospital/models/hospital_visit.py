from odoo import models, fields


class HospitalVisit(models.Model):
    _name = 'hospital.visit'
    _description = 'Hospital Patient Visits'

    date = fields.Datetime(
        string='Visit time',
        required=True
    )
    is_canceled = fields.Boolean(
        string='Visit canceled status',
        default=False
    )
    is_succeed = fields.Boolean(
        string='Visit success status',
    )
    patient_id = fields.Many2one(
        comodel_name='hospital.patient',
        string='Patient',
        required=True
    )
    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Doctor',
        required=True
    )
