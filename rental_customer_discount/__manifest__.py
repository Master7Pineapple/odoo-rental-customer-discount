{
    'name': 'Rental Customer Discounts',
    'version': '19.0.1.0.0',
    'category': 'Sales/Rental',
    'summary': 'Fixed per-customer discount, auto-applied on Rental orders',
    'description': """
Rental Customer Discounts
==========================
Lets you configure a fixed discount percentage for specific customers.

- A new "Customer Discounts" page is added under the Rental app's
  Configuration menu, where you pick a customer and set their fixed
  discount (%).
- When that customer is selected on a Rental order (quotation), the
  discount is applied automatically to every order line, and to any
  new line added afterwards.

Notes
-----
* The discount is a PERCENTAGE (0-100), applied through the standard
  order line "Discount" field.
* Only applied to orders where is_rental_order = True, so regular
  Sales orders are not affected.
* If a customer has no discount configured, nothing changes (0%).
* If a line's discount was already set to something else, it will be
  overwritten when the partner changes; a brand-new line only gets
  the auto-discount if its own discount is still 0.
""",
    'author': "Kosai Alhafez",
    "website": "https://blasedoesit.com",
    'depends': ['sale_renting'],
    'data': [],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
