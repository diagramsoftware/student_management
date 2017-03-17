{
    'name': 'Student Marksheet',
    'version': '1.0',
    'author': 'ITROOTS ODOO',
    'category': 'Odoo Education',
    'icon': "/student_marksheet/static/src/img/icon.png",
    'description':
    """
Odoo Student Marksheet module.
================================================
        """,
    'website': 'https://www.odoo.com/',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_information.xml',
        'views/student_marksheet.xml',
        'views/student_course.xml',
        'views/student_subject.xml',
        'views/marksheet_report.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
