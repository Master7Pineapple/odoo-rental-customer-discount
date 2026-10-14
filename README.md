# Rental customer discounts for Odoo

Set a fixed discount per customer once, and it's applied to every line of every rental order in **Odoo 19**. Built for Sokoon Rental House in Damascus, where staff used to remember discounts and type them on each line.

Shown on [blasedoesit.com](https://blasedoesit.com/#work) under "Smaller work".

## What it does

- New model `customer.rental.discount`: a customer and a discount percentage.
- A **Customer Discounts** page under **Rental → Configuration**, editable inline.
- When the customer is set or changed on a rental order, every line gets that customer's discount. Lines added later get it too.
- Only rental orders (`is_rental_order = True`) are affected. Normal sales orders are left alone.

## How it's built

The views, action, access rights and menu are created in Python in `post_init_hook` (`hooks.py`) instead of XML. That way the module also installs through **Apps → Import Module** (`base_import_module`), which loads data files before the module's own models are registered and would otherwise fail with "Model not found".

The menu is looked up by name at install time, with a fallback to the Rental root menu, so it doesn't depend on a technical ID that has changed between Odoo versions.

## Tech

Python, Odoo ORM, Odoo Rental (`sale_renting`).

## Install

Requires **Odoo 19 Enterprise** with the Rental app.

1. Copy `rental_customer_discount` into a directory on your Odoo addons path.
2. Restart Odoo, then **Apps → Update Apps List**, and install **Rental Customer Discounts**.
3. Go to **Rental → Configuration → Customer Discounts** and add customers.

## Author

Built by **Kosai Alhafez**, business systems developer.
[blasedoesit.com](https://blasedoesit.com) · kosai@blasedoesit.com

## License

LGPL-3. See [LICENSE](LICENSE).
