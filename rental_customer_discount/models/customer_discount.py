from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CustomerRentalDiscount(models.Model):
    _name = 'customer.rental.discount'
    _description = 'Fixed Rental Discount per Customer'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        ondelete='cascade',
        help='Customer this fixed discount applies to.',
    )
    discount = fields.Float(
        string='Discount (%)',
        required=True,
        default=0.0,
        help='Fixed discount percentage automatically applied to every '
             'line of a Rental order once this customer is selected.',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help='Leave empty to apply this discount regardless of company.',
    )
    note = fields.Char(string='Note')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            'partner_company_uniq',
            'unique(partner_id, company_id)',
            'A discount is already configured for this customer '
            '(in this company).',
        ),
    ]

    @api.constrains('discount')
    def _check_discount_range(self):
        for rec in self:
            if not (0 <= rec.discount <= 100):
                raise ValidationError('The discount must be between 0 and 100.')

    @api.model
    def _get_discount_for_partner(self, partner, company=None):
        """Return the fixed discount (%) configured for a partner, or 0.0.

        Falls back to the partner's commercial entity (company contact)
        if no discount is configured on the contact itself.
        """
        if not partner:
            return 0.0
        company = company or self.env.company
        domain_company = [('company_id', 'in', [company.id, False])]

        rec = self.search(
            [('partner_id', '=', partner.id)] + domain_company, limit=1
        )
        if not rec and partner.commercial_partner_id != partner:
            rec = self.search(
                [('partner_id', '=', partner.commercial_partner_id.id)]
                + domain_company,
                limit=1,
            )
        return rec.discount if rec else 0.0
