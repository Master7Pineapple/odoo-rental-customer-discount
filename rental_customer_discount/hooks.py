from odoo import api, SUPERUSER_ID


LIST_ARCH = """<list string="Customer Rental Discounts" editable="bottom">
    <field name="partner_id"/>
    <field name="discount"/>
    <field name="company_id" groups="base.group_multi_company"/>
    <field name="note"/>
</list>"""

FORM_ARCH = """<form string="Customer Rental Discount">
    <sheet>
        <group>
            <field name="partner_id"/>
            <field name="discount"/>
            <field name="company_id" groups="base.group_multi_company"/>
            <field name="note"/>
            <field name="active"/>
        </group>
    </sheet>
</form>"""


def post_init_hook(env):
    """Set up everything (views, action, access rights, menu) in Python
    instead of via data files.

    Some install paths (e.g. uploading this module as a zip through
    Apps > Import Module) load data files before the module's own
    models have been registered in the active registry, which makes
    any XML/CSV file that references 'customer.rental.discount' fail
    with "Model not found" or similar. post_init_hook always runs
    after the module (and its models) are fully loaded, regardless of
    install path, so building everything here avoids that ordering
    problem entirely.
    """
    # Odoo < 17 compatibility: hook used to receive (cr, registry).
    if not isinstance(env, api.Environment):
        cr = env
        env = api.Environment(cr, SUPERUSER_ID, {})

    if 'customer.rental.discount' not in env:
        # Model still not available for some reason - nothing more we
        # can safely do here.
        return

    action = _setup_views_and_action(env)
    _setup_access_rights(env)
    if action:
        _setup_menu(env, action)


def _setup_views_and_action(env):
    View = env['ir.ui.view']
    Action = env['ir.actions.act_window']

    list_view = View.search([
        ('model', '=', 'customer.rental.discount'), ('type', '=', 'list'),
    ], limit=1)
    if not list_view:
        list_view = View.create({
            'name': 'customer.rental.discount.list',
            'model': 'customer.rental.discount',
            'type': 'list',
            'arch': LIST_ARCH,
        })

    form_view = View.search([
        ('model', '=', 'customer.rental.discount'), ('type', '=', 'form'),
    ], limit=1)
    if not form_view:
        form_view = View.create({
            'name': 'customer.rental.discount.form',
            'model': 'customer.rental.discount',
            'type': 'form',
            'arch': FORM_ARCH,
        })

    action = Action.search([
        ('res_model', '=', 'customer.rental.discount'),
    ], limit=1)
    if not action:
        action = Action.create({
            'name': 'Customer Discounts',
            'res_model': 'customer.rental.discount',
            'view_mode': 'list,form',
        })
    return action


def _setup_access_rights(env):
    IrModel = env['ir.model']
    Access = env['ir.model.access']

    model = IrModel.search([('model', '=', 'customer.rental.discount')], limit=1)
    if not model:
        return

    access_defs = [
        {
            'name': 'customer.rental.discount.user',
            'group_ref': 'sales_team.group_sale_salesman',
            'perm_read': True,
            'perm_write': False,
            'perm_create': False,
            'perm_unlink': False,
        },
        {
            'name': 'customer.rental.discount.manager',
            'group_ref': 'sales_team.group_sale_manager',
            'perm_read': True,
            'perm_write': True,
            'perm_create': True,
            'perm_unlink': True,
        },
    ]

    for definition in access_defs:
        if Access.search([('name', '=', definition['name'])], limit=1):
            continue
        group = env.ref(definition['group_ref'], raise_if_not_found=False)
        Access.create({
            'name': definition['name'],
            'model_id': model.id,
            'group_id': group.id if group else False,
            'perm_read': definition['perm_read'],
            'perm_write': definition['perm_write'],
            'perm_create': definition['perm_create'],
            'perm_unlink': definition['perm_unlink'],
        })


def _setup_menu(env, action):
    Menu = env['ir.ui.menu']

    existing = Menu.search(
        [('action', '=', 'ir.actions.act_window,%d' % action.id)], limit=1
    )
    if existing:
        return

    rental_root = Menu.search(
        [('name', '=', 'Rental'), ('parent_id', '=', False)], limit=1
    )

    config_menu = False
    if rental_root:
        config_menu = Menu.search(
            [('name', '=', 'Configuration'), ('parent_id', '=', rental_root.id)],
            limit=1,
        )

    parent = config_menu or rental_root

    Menu.create({
        'name': 'Customer Discounts',
        'action': 'ir.actions.act_window,%d' % action.id,
        'parent_id': parent.id if parent else False,
        'sequence': 100,
    })
