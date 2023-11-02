from odoo import models, fields, _


class HospitalPatientAnalysis(models.Model):
    _name = 'hospital.patient.analysis'
    _description = 'Hospital patient analyses'

    name = fields.Char(
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
    category_id = fields.Many2one(
        comodel_name='hospital.patient.analysis.category',
        required=True,
    )
    sample_date = fields.Date(
        required=True,
    )
    patient_phone = fields.Char(
        related='patient_id.phone',
        readonly=True,
    )
    is_ready = fields.Boolean(
        string='Ready',
        default=False,
    )
    result = fields.Text()

    # Action methods
    def action_open_analysis(self):
        analysis_id = self.env.context.get('analysis_id')
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        record_url = (base_url + "/web#id=" + str(analysis_id)
                      + "&view_type=form"
                        "&model=hospital.patient.analysis"
                        "&menu_id=131"
                        "&action=201")
        return {
            'name': _('Patient Analysis'),
            'type': 'ir.actions.act_url',
            'url': record_url,
            'target': 'new',
        }
