{
    'name': "Employee Management",
    'version': '1.0',
    'depends': ['mail', 'sale', 'base', 'hr'],
    'author': "Rookie",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/mail_template.xml',
        'views/employee.xml',
        'views/manager.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
}
