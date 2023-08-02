from odoo import fields, models


class PresaleModel(models.Model):
    _name = "presale.order"
    _description = "Presale order model"

    def _defaultName(self):
        # TODO: Avoid searching the whole table
        number = 1
        record_names = [record.name for record in self.env["presale.order"].search([])]
        while ("PS " + str(number).zfill(3)) in record_names:
            number += 1
        return "PS " + str(number).zfill(3)

    active = fields.Boolean(default=True)
    name = fields.Char(default=_defaultName, required=True)
    partner_id = fields.Many2one("res.partner", string="Customer")
    state = fields.Selection(
        default="new",
        required=True,
        selection=[("new", "Draft"), ("validated", "Validated"), ("cancelled", "Cancelled")],
    )
    order_line_ids = fields.One2many("presale.order.line", "presale_order_id")

    def send_validation_email(self, presale_order):
        # TODO: test with proper email
        mail_template = {
            "subject": presale_order.name,
            "email_to": presale_order.partner_id.email,
            "body_html": f"<h2>Your presale order {presale_order.name} has been validated</h2>",
        }
        msg_id = self.env["mail.mail"].create(mail_template)
        self.env["mail.mail"].send([msg_id])

    def action_validate_preorder(self):
        for record in self:
            if record.state == "new":
                record.state = "validated"
                sale_order = self.env["sale.order"].create(
                    {
                        "name": record.name,
                        "partner_id": record.partner_id.id,
                    }
                )
                sale_order.presale_order = record.id
                for presale_order_line in record.order_line_ids:
                    self.env["sale.order.line"].create(
                        {
                            "order_id": sale_order.id,
                            "product_id": presale_order_line.product_id.id,
                            "product_uom_qty": presale_order_line.quantity,
                            "price_unit": presale_order_line.price,
                        }
                    )
                self.send_validation_email(record)

    def action_cancel_preorder(self):
        for record in self:
            if record.state == "new":
                record.state = "cancelled"

    def archive_confirmed_orders(self):
        for record in self.env["presale.order"].search([]):
            if record.state == "validated":
                record.active = False
