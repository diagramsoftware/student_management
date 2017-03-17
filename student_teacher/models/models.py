# -*- coding: utf-8 -*-
import re
from openerp import fields, models, api


class TecherInformation(models.Model):
    _name = "teacher.information"
    _description = 'Teacher Detail Store Into This class'
    _order = 'employee_id'

    employee_id = fields.Char(string="Employee Id", required=True)
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
    image = fields.Binary(string="Image")
    pan_card = fields.Char(size=64, string='PAN Card')
    bank_acc_num = fields.Char(size=64, string='Bank Acc Number')
    visa_info = fields.Char(size=64, string='Visa Info')
    contact = fields.Char(string="Contact", required=True)
    email = fields.Char(string="Email")
    street = fields.Char()
    street2 = fields.Char()
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state", string="State")
    zip = fields.Char(string="Zip")
    country_id = fields.Many2one("res.country", string="Country")
    faculty_subject_ids = fields.Many2many(
        'student.subject', 'faculty_subject_rel',
        'op_faculty_id', 'op_subject_id', string='Subjects')
    _sql_constraints = [('unique_employee_id', 'unique(employee_id)',
                         'Error! Employee Id Already Exist!')]

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
    def validateContact(self):
        if self.contact:
            if re.match("^[0-9]{6,12}$", self.contact) != None:
                return True
            else:
                raise Warning(("Please enter a valid Phone Number."))
