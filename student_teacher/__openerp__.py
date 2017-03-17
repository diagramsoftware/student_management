{
    'name': 'Teacher',
    'version': '1.0',
    'author': 'Kanak Infosystems LLP.',
    'category': 'Odoo Education',
    'icon': "/student_marksheet/static/src/img/icon.png",

    'description':
    """
 This module provide overall education management system over OpenERP
=====================================================================
        """,
    'website': 'https://www.odoo.com/',
    'depends': ['student_marksheet'],
    'data': [
        'views/student_teacher_view.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
