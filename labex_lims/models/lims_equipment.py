from odoo import models, fields, api

class LimsEquipment(models.Model):
    _name = 'lims.equipment'
    _description = 'LIMS Equipment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Equipment Name', required=True)
    model = fields.Char(string='Model/Serial Number')
    manufacturer = fields.Char(string='Manufacturer')
    installation_date = fields.Date(string='Installation Date')
    last_calibration_date = fields.Date(string='Last Calibration Date')
    next_calibration_date = fields.Date(string='Next Calibration Date')
    state = fields.Selection([
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Maintenance'),
        ('broken', 'Broken')
    ], string='Status', default='available', tracking=True)

class LimsMethodology(models.Model):
    _name = 'lims.methodology'
    _description = 'LIMS Methodology'

    name = fields.Char(string='Method Name', required=True)
    code = fields.Char(string='Method Code')
    description = fields.Text(string='Description/SOP')
    version = fields.Char(string='Version', default='1.0')

class ResCompany(models.Model):
    _inherit = 'res.company'

    lab_tagline = fields.Char(string='Laboratory Tagline')
    lab_license_no = fields.Char(string='Lab License No.')
