# -*- coding: utf-8 -*-
import re
from datetime import date
from openerp import fields, models, api
from openerp.exceptions import Warning
from openerp.exceptions import UserError
#   from osv import osv


class StudentInfromation(models.Model):
    _name = "student.information"
    _description = 'Student Detail Store Into This class'
    _order = 'rollno'
    name = fields.Char(required=True, string='First Name')
    middle_name = fields.Char(size=128, string='Middle Name', required=True)
    last_name = fields.Char(size=128, string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date', required=True)
    blood_group = fields.Selection([("A+", "A+ve"), ("B+", "B+ve"),
                                    ("O+", "O+ve"), ("AB+", "AB+ve"),
                                    ("A-", "A-ve"), ("B-", "B-ve"),
                                    ("O-", "O-ve"), ("AB-", "AB-ve")],
                                   string='Blood Group')
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'), ('o', 'Other')],
        string='Gender', required=True)
    nationality = fields.Many2one('res.country', string='Nationality')
    language = fields.Many2one('res.lang', string='Mother Tongue')
    rollno = fields.Char(string="Roll No", required=True)
    image = fields.Binary(string="Image")
    contact = fields.Char(string="Contact", required=True)
    email = fields.Char(string="Email", required=True)
    street1 = fields.Char()
    street2 = fields.Char()
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state", string="State")
    zip = fields.Char(string="Zip")
    country_id = fields.Many2one("res.country", string="Country")
    course_id = fields.Many2one(
        'student.course', string='Course', required=True)

    course_subject_id = fields.Many2many(
        'student.subject', 'student_subject_rel',
        'subject_id', 'subject_id_rel')
    # course_subject_id = fields.One2many(
    #     'student.subject', 'subject_id', string="Course Subjects")
    _sql_constraints = [('unique_roll_no', 'unique(rollno)',
                         'Error! Roll Number Already Exist!')]

    # @api.multi
    # @api.onchange('state_id')
    # def onchange_state(self):
    #     if self.state_id:
    #         self.state = self.env["res.country"].browse(self.state_id)
    #     return {'value': {'country_id': self.state.country_id.id}}

    @api.onchange('course_id')
    def course_subject_change(self):
        self.course_subject_id = self.course_id.subject_ids

    @api.one
    @api.constrains('email')
    def ValidationEmail(self):
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", self.email) != None:
            return True
        else:
            raise Warning(
                ("Invalid Email Please enter a valid email address."))

    @api.one
    @api.onchange('contact')
    def ValidationContact(self):
        if self.contact:
            if re.match("^[0-9]{6,12}$", self.contact) != None:
                pass
            else:
                raise Warning(('Please enter a valid Phone Number'))
        else:
            pass


class student_course(models.Model):
    _name = 'student.course'
    name = fields.Char(size=32, string='Name', required=True)
    code = fields.Char(size=8, string='Code', required=True)
    section = fields.Char(size=32, string='Section', required=True)
    subject_ids = fields.Many2many(
        'student.subject', 'student_course_subject_rel',
        'student_course_id', 'student_subject_id', string='Subject(s)')


class student_subject(models.Model):
    _name = 'student.subject'
    subject_id = fields.Many2one('student.information')
    name = fields.Char(size=128, string='Name', required=True)
    code = fields.Char(size=256, string='Code', required=True)
    course_id = fields.Many2one('student.course', string='Course')
    type = fields.Selection([('p', 'Practial'), ('t', 'Theory'),
                             ('pt', 'Both'), ('o', 'Other')],
                            string='Type', required=True)

    _sql_constraints = [('unique_subject_code', 'unique(code)',
                         'Error! Subject Code Already Exist!')]


class StudentMarksheetLine(models.Model):

    _name = 'student.marksheet.line'
    _description = """
    Student Result Information
    """
    stud_id = fields.Many2one('student.marksheet.line', string="Student Id")
    sub_id = fields.Many2one('student.subject', string="Subject Name")
    outof = fields.Integer(string="Out Of")
    marks = fields.Integer(string="Marks")


class StudentMarksheet(models.Model):
    _name = "student.marksheet"
    _description = 'Student Subject Vise Marks Display Hear'
    # _inherits = {'student.subject': 'sub', 'student.information': 'info'}
    rollno = fields.Many2one(
        'student.information', string="Student Name",
        select=True, ondelete='cascade', required=True)
    result = fields.One2many('student.marksheet.line', 'stud_id')
    total = fields.Float(String="Total", compute="_compute_total")
    percentage = fields.Float(
        string="Percentage", compute="_compute_percentage")
    grade = fields.Char(string="Grade", compute="_compute_grade")
    date = date.today().strftime('%d-%m-%Y')
    state = fields.Selection([
        ('draft', 'Unconfirmed'), ('cancel', 'Cancelled'),
        ('confirm', 'Confirmed'), ('done', 'Done')],
        string='Status', default='draft', readonly=True, required=True,
        copy=False)
    # sent = fields.Boolean(readonly=True, default=False, copy=False)

    @api.model
    def create(self, vals):
        res = super(StudentMarksheet, self).create(vals)
        self.button_confirm()
        return res

    @api.multi
    def write(self, vals):
        return super(StudentMarksheet, self).write(vals)

    @api.one
    def button_draft(self):
        self.state = 'done'

    @api.one
    def button_cancel(self):
        if self.state == 'done':
            raise UserError(
                ("You have already set a registration for this event as."))
        self.state = 'cancel'

    @api.one
    def button_confirm(self):
        self.state = 'confirm'

    @api.onchange('result')
    def _compute_total(self):
        for record in self:
            total = 0
            for res in record.result:
                total += res.marks
            record.total = total

    @api.onchange('total')
    def _compute_percentage(self):
        for record in self:
            outof = 0
            for res in record.result:
                outof += res.outof
            try:
                record.percentage = (record.total * 100) / outof
            except ZeroDivisionError:
                print "Zero is Danger"

    @api.onchange('percentage')
    def _compute_grade(self):
        for record in self:
            if record.percentage >= 80:
                record.grade = "A+"
            elif record.percentage >= 70 and record.percentage <= 80:
                record.grade = "A"
            elif record.percentage >= 60 and record.percentage <= 70:
                record.grade = "B+"
            elif record.percentage >= 50 and record.percentage <= 60:
                record.grade = "B"
            elif record.percentage >= 40 and record.percentage <= 50:
                record.grade = "C"
            elif record.percentage >= 35 and record.percentage <= 40:
                record.grade = "D"
            else:
                record.grade = "F"

    @api.multi
    def action_marksheet_sent(self, vals):
        return
