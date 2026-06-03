from odoo import models, fields, api

class LimsSample(models.Model):
    _name = 'lims.sample'
    _description = 'LIMS Sample'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Sample ID', required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')
    external_id = fields.Char(string='External ID')
    patient_name = fields.Char(string='Patient Name')
    collection_date = fields.Datetime(string='Collection Date', default=fields.Datetime.now)
    received_date = fields.Datetime(string='Received Date')
    sample_type = fields.Selection([
        ('blood', 'Blood'),
        ('urine', 'Urine'),
        ('water', 'Water'),
        ('soil', 'Soil'),
        ('other', 'Other')
    ], string='Sample Type', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('received', 'Received'),
        ('testing', 'Testing'),
        ('validated', 'Validated'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Urgent'),
        ('2', 'STAT')
    ], string='Priority', default='0')

    test_ids = fields.One2many('lims.sample.test', 'sample_id', string='Tests')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('lims.sample') or 'New'
        return super(LimsSample, self).create(vals)

    def action_receive(self):
        self.write({
            'state': 'received',
            'received_date': fields.Datetime.now()
        })

    def action_test(self):
        self.write({'state': 'testing'})

    def action_validate(self):
        self.write({'state': 'validated'})

class LimsSampleTest(models.Model):
    _name = 'lims.sample.test'
    _description = 'LIMS Sample Test'

    sample_id = fields.Many2one('lims.sample', string='Sample', ondelete='cascade')
    test_id = fields.Many2one('lims.test', string='Test Type', required=True)
    result = fields.Char(string='Result')
    unit_id = fields.Many2one('uom.uom', string='Unit')
    reference_range = fields.Char(string='Reference Range')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('done', 'Done')
    ], string='Status', default='pending')

class LimsTest(models.Model):
    _name = 'lims.test'
    _description = 'LIMS Test Type'

    name = fields.Char(string='Test Name', required=True)
    code = fields.Char(string='Test Code')
    methodology_id = fields.Many2one('lims.methodology', string='Methodology')
    category = fields.Selection([
        ('hematology', 'Hematology'),
        ('biochemistry', 'Biochemistry'),
        ('microbiology', 'Microbiology')
    ], string='Category')
    default_unit_id = fields.Many2one('uom.uom', string='Default Unit')
