from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def _onchange_partner_id_rental_discount(self):
        self._apply_customer_rental_discount()

    def write(self, vals):
        res = super().write(vals)
        if 'partner_id' in vals:
            self._apply_customer_rental_discount()
        return res

    def _apply_customer_rental_discount(self):
        Discount = self.env['customer.rental.discount']
        for order in self:
            if not order.partner_id:
                continue
            # Only touch actual Rental orders, not regular Sales orders.
            if 'is_rental_order' in order._fields and not order.is_rental_order:
                continue
            discount = Discount._get_discount_for_partner(
                order.partner_id, order.company_id
            )
            if discount:
                for line in order.order_line:
                    if not line.display_type:
                        line.discount = discount


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        lines._apply_customer_rental_discount_on_create()
        return lines

    def _apply_customer_rental_discount_on_create(self):
        Discount = self.env['customer.rental.discount']
        for line in self:
            if line.display_type:
                continue
            order = line.order_id
            if not order.partner_id:
                continue
            if 'is_rental_order' in order._fields and not order.is_rental_order:
                continue
            if line.discount:
                # Don't override a discount that was explicitly set
                # (e.g. copied from a pricelist rule or set manually).
                continue
            discount = Discount._get_discount_for_partner(
                order.partner_id, order.company_id
            )
            if discount:
                line.discount = discount
