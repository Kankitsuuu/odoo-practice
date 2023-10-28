from odoo import models, fields, _


class DoctorChangeMultiWizard(models.TransientModel):
    _name = 'doctor.change.multi.wizard'
    _description = 'Wizard to change supervising doctor for patients'

    patient_ids = fields.Many2many(
        comodel_name='hospital.patient',
        string='Patients',
    )

    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Supervising doctor',
    )

    # Action methods
    def action_open_wizard(self) -> dict:
        return {
            'name': _('Change Supervising Doctor Wizard'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'doctor.change.multi.wizard',
            'target': 'new',
            'context': {'default_patient_ids': self.env.context['active_ids']}
        }

    def action_change_doctor(self) -> None:
        for record in self.env['hospital.patient'].browse(self.env.context['active_ids']):
            record.write({'doctor_id': self.doctor_id.id})
