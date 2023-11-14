from odoo import models, fields


class HospitalDoctorChange(models.Model):
    _name = 'hospital.doctor.change'
    _description = 'Hospital history of changes supervising doctor'

    set_time = fields.Datetime(
        string='Time',
        required=True,
        readonly=True,
    )
    patient_id = fields.Many2one(
        comodel_name='hospital.patient',
        required=True,
        readonly=True,
        ondelete='cascade',
    )
    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        readonly=True,
    )

    # Default methods
    def name_get(self):
        data = []
        for rec in self:
            doctor = rec.doctor_id.surname
            patient = rec.patient_id.surname
            date = rec.set_time.date()
            data.append(
                (rec.id, f'{patient} - {doctor} {date}')
            )
        return data
