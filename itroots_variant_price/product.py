# -*- coding: utf-8 -*-

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class product_product(models.Model):
    _inherit = 'product.product'

    # price_extra - valoarea extra pret in functie de atribute
    # list_price - pretul de lista a produsului
    # lst_price - pretul de lista a produsului + pretul exta
    # price_extra_variant - valoarea extra de pret a variantei
    # lst_price = list_price + price_extra + price_extra_variant
    # price_extra_variant = lst_price - list_price - price_extra
    # list_price = fields.Float()
    # price_extra = fields.Float()

    price_extra_variant = fields.Float(string="Variant Public Price", digits=dp.get_precision('Product Price'))
    lst_price = fields.Float(compute="_get_product_lst_price", inverse="_set_product_lst_price")
    # fields.function(_product_lst_price, fnct_inv=_set_product_lst_price, type='float', string='Public Price', digits_compute=dp.get_precision('Product Price')),

    @api.multi
    def _get_product_lst_price(self):
        print "get price"
        for product in self:
            price = product.list_price
            if not price:
                price = product.product_tmpl_id.list_price
            if 'uom' in self.env.context:
                uom = product.uos_id or product.uom_id
                price = self.env['product.uom']._compute_price(uom.id, price, self.env.context['uom'])

            product.lst_price = price + product.price_extra + product.price_extra_variant

    @api.multi
    def _set_product_lst_price(self):
        print "set price"
        for product in self:
            if 'uom' in self.env.context:
                uom = product.uos_id or product.uom_id
                lst_price = self.env['product.uom']._compute_price(self.env.context['uom'], product.lst_price, uom.id)
            else:
                lst_price = product.lst_price
            self.price_extra_variant = lst_price - product.list_price - product.price_extra
