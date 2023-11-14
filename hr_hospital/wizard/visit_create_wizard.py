from odoo import models, fields, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class VisitCreateWizard(models.TransientModel):
    _name = 'visit.create.wizard'
    _description = 'Wizard to create patient visit'

    set_date = fields.Datetime(
        string='Time',
        required=True,
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

    # Action methods
    def action_open_wizard(self):
        return {
            'name': _('New Visit'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'visit.create.wizard',
            'target': 'new',
        }

    def action_create_visit(self):
        self.ensure_one()
        diagnosis_id = self.diagnosis_id.id if self.diagnosis_id else None
        self.env['hospital.visit'].create({
            'set_date': self.set_date.strftime(DATETIME_FORMAT),
            'patient_id': self.patient_id.id,
            'doctor_id': self.doctor_id.id,
            'diagnosis_id': diagnosis_id
        })
        return {
            'name': _('New Visit'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hospital.visit',
            'target': 'current',
        }
