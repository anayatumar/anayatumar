from odoo import models, fields, api
from datetime import date

class LimsPatient(models.Model):
    _name = 'lims.patient'
    _description = 'Laboratory Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Patient Name', required=True, tracking=True)
    mr_no = fields.Char(string='MR No.', required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')
    guardian_name = fields.Char(string='Guardian Name')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    dob = fields.Date(string='Date of Birth')
    age = fields.Char(string='Age', compute='_compute_age', store=True)
    contact_no = fields.Char(string='Contact No.')
    email = fields.Char(string='Email ID')
    city = fields.Char(string='City')
    referred_by = fields.Char(string='Referred By')

    @api.depends('dob')
    def _compute_age(self):
        for record in self:
            if record.dob:
                today = date.today()
                age = today.year - record.dob.year - ((today.month, today.day) < (record.dob.month, record.dob.day))
                record.age = str(age)
            else:
                record.age = "Unknown"

    @api.model
    def create(self, vals):
        if vals.get('mr_no', 'New') == 'New':
            vals['mr_no'] = self.env['ir.sequence'].next_by_code('lims.patient') or 'New'
        return super(LimsPatient, self).create(vals)

class LimsTest(models.Model):
    _name = 'lims.test'
    _description = 'LIMS Test Type'

    name = fields.Char(string='Test Name', required=True)
    short_name = fields.Char(string='Short Name')
    code = fields.Char(string='Test ID/Code')
    department = fields.Char(string='Department')
    sample_requirement = fields.Char(string='Sample Requirement')
    reporting_time = fields.Char(string='Reporting Time')
    result_type = fields.Selection([
        ('numeric', 'Numeric'),
        ('text', 'Text/Descriptive'),
        ('selection', 'Selection/Positive-Negative')
    ], string='Result Type', default='numeric')
    report_pattern = fields.Text(string='Report Pattern/Template')
    normal_range = fields.Char(string='Normal/Reference Range')
    methodology_id = fields.Many2one('lims.methodology', string='Methodology')
    category = fields.Selection([
        ('hematology', 'Hematology'),
        ('biochemistry', 'Biochemistry'),
        ('microbiology', 'Microbiology')
    ], string='Category')
    default_unit_id = fields.Many2one('uom.uom', string='Default Unit')

class LimsTestProfile(models.Model):
    _name = 'lims.test.profile'
    _description = 'LIMS Test Profile/Panel'

    name = fields.Char(string='Profile/Panel Name', required=True)
    code = fields.Char(string='Profile Code')
    test_ids = fields.Many2many('lims.test', string='Tests')
    description = fields.Text(string='Description')

class LimsSample(models.Model):
    _name = 'lims.sample'
    _description = 'LIMS Sample'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Lab ID', required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')
    external_id = fields.Char(string='External Panel ID')
    patient_id = fields.Many2one('lims.patient', string='Patient', required=True)
    profile_id = fields.Many2one('lims.test.profile', string='Selected Panel/Profile')

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

    @api.onchange('profile_id')
    def _onchange_profile_id(self):
        if self.profile_id:
            test_lines = []
            for test in self.profile_id.test_ids:
                test_lines.append((0, 0, {
                    'test_id': test.id,
                    'unit_id': test.default_unit_id.id,
                    'reference_range': test.normal_range,
                }))
            self.test_ids = test_lines

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
    _description = 'LIMS Sample Test Result'

    sample_id = fields.Many2one('lims.sample', string='Sample', ondelete='cascade')
    test_id = fields.Many2one('lims.test', string='Test Type', required=True)
    result = fields.Char(string='Result')
    unit_id = fields.Many2one('uom.uom', string='Unit')
    reference_range = fields.Char(string='Reference Range')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('done', 'Done')
    ], string='Status', default='pending')
