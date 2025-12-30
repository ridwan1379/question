{
    'name': 'Move Date Advanced',
    'version': '13.0.1.0.0',
    'category': 'Tools',
    'summary': 'Advanced move date with wizard, log, and security',
    'author': 'Muhamad Ridwan',
    'depends': ['base', 'mail'],
    'data': [
    'security/ir.model.access.csv',

    # VIEW & ACTION HARUS DULU
    'views/movedate_log_view.xml',
    'views/movedate_wizard_view.xml',

    # MENU TERAKHIR
    'views/movedate_menu.xml',
],

    'installable': True,
    'application': True,
}