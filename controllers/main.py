# -*- coding: utf-8 -*-
import time
import werkzeug
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.website.controllers.main import Website
from odoo.addons.website.models.website import unslug
from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.website_sale.controllers.main import WebsiteSale

import odoo
from odoo import http
from odoo.http import request
from odoo.tools.translate import _


class WebsiteSaleShop(WebsiteSale):
    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res = super(WebsiteSaleShop, self).shop(page=page, category=category, search=search, ppg=ppg, **post)
        qcontext = dict(res.qcontext)
        if post.get('most_selling') == 'true':
            list_of_products = []
            for record in request.env['product.product'].sudo().search([]):
                product_qty = 0
                for line in request.env['sale.order.line'].sudo().search(
                        [('product_id', '=', record.id), ('order_id.state', '=', 'done')]):
                    product_qty += line.product_uom_qty
                list_of_products.append({'product_qty': product_qty, 'product_id': record.id})
            newlist = sorted(list_of_products, key=lambda k: k['product_qty'], reverse=True)
            final_products_list = []
            for item_qty in newlist:
                final_products_list.append(item_qty.get('product_id'))
            qcontext.update({
                'products': request.env['product.product'].sudo().browse(final_products_list)
            })
        return request.render("website_sale.products", qcontext)


WebsiteSaleShop()


class WebsiteHome(Website):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        res = super(WebsiteHome, self).index(**kw)
        qcontext = dict(res.qcontext)
        qcontext.update({
            'featured_products': request.env['product.template'].sudo().search([], order='create_date desc', limit=2),
            'products': request.env['product.template'].sudo().search([], order='create_date desc', limit=10),
            'request': request})
        return request.render('website.homepage', qcontext)


WebsiteHome()


class WebsiteSignUp(AuthSignupHome):
    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        qcontext.update({'city': kw.get('city'), 'phone': kw.get('phone')})
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                return super(AuthSignupHome, self).web_login(*args, **kw)
            except (SignupError, AssertionError), e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    qcontext['error'] = _("Could not create a new account.")

        return request.render('auth_signup.signup', qcontext)

    def do_signup(self, qcontext):
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password', 'phone', 'city')}
        assert values.values(), "The form was not properly filled in."
        assert values.get('password') == qcontext.get('confirm_password'), "Passwords do not match; please retype them."
        supported_langs = [lang['code'] for lang in request.env['res.lang'].sudo().search_read([], ['code'])]
        if request.lang in supported_langs:
            values['lang'] = request.lang
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()


WebsiteSignUp()


class WebsiteAccountEdit(website_account):
    @http.route(['/my/account'], type='http', auth='user', website=True)
    def details(self, redirect=None, **post):
        partner = request.env.user.partner_id
        post.update({'phone': partner.phone or request.env.user.sudo().company_id.phone,
                     'street': partner.street or request.env.user.sudo().company_id.street,
                     'city': partner.city or request.env.user.sudo().company_id.city,
                     'country_id': partner.country_id.id or request.env.user.sudo().company_id.country_id.id})
        res = super(WebsiteAccountEdit, self).details(redirect=redirect, **post)
        if res.qcontext.get('error'):
            res.qcontext['error'] = {}
            res.qcontext['error_message'] = {}
        else:
            if post.get('new_password') != post.get('other_new_password'):
                res.qcontext.update({'error': {'password': 'mismatch'}})
        if post.get('new_password'):
            request.env.user.sudo().write({'password': post.get('new_password')})
            res.qcontext.update({'redirect': '/web/login'})
        return res


WebsiteAccountEdit()


class WebsiteSaleWishlist(odoo.http.Controller):

    @http.route(['/shop/cart/add/<product_id>'], type='http', auth="public", website=True)
    def add_product_to_the_cart(self, product_id, **kw):
        _, product_id = unslug(product_id)
        request.website.sale_get_order(force_create=1)._cart_update(
            product_id=product_id,
            add_qty=kw.get('qty') if kw.get('kw') else 0,
            set_qty=0,
            attributes={},
        )
        return request.redirect("/shop/cart")

    @http.route(['/shop/offer/add/<offer_id>'], type='http', auth="public", website=True)
    def add_offer_to_the_cart(self, offer_id, **kw):
        _, offer_id = unslug(offer_id)
        offer = request.env['product.offer'].sudo().browse(offer_id)
        order = request.website.sale_get_order()
        vals = {
            'price_unit': offer.product_id.list_price,
            'website_description': offer.product_id.name,
            'name': offer.product_id.name,
            'order_id': order.id,
            'product_id': offer.product_id.product_variant_id.id,
            'product_uom_qty': 1,
            'product_uom': offer.product_id.uom_id.id,
            'discount': offer.discount_value,
        }
        order_line = request.env['sale.order.line'].sudo().create(vals)
        return request.redirect("/shop/cart")

    @http.route(['/shop/wishlist/add/<product_id>'], type='http', auth="user", website=True)
    def add_product_to_wishlist(self, product_id, **kw):
        _, product_id = unslug(product_id)
        partner_id = request.env.user.sudo().partner_id
        if partner_id.wishlist_id:
            if product_id not in partner_id.wishlist_id.product_wishlist_ids.ids:
                partner_id.wishlist_id.write({'product_wishlist_ids': [(4, product_id)]})
        else:
            wishlist_id = request.env['product.wishlist'].create(
                {'name': str(partner_id.name) + ' Wishlist', 'product_wishlist_ids': [(4, product_id)]})
            partner_id.write({'wishlist_id': wishlist_id.id})

        return request.redirect("/shop")

    @http.route(['/shop/wishlist/delete/<product_id>'], type='http', auth="user", website=True)
    def delete_product_to_wishlist(self, product_id, **kw):
        _, product_id = unslug(product_id)
        partner_id = request.env.user.sudo().partner_id.wishlist_id
        partner_id.write({'product_wishlist_ids': [(3, product_id)]})
        return request.redirect("/page/profile")

    @http.route(['/page/profile'], type='http', auth="user", website=True)
    def got_to_my_profile(self, **kw):
        partner_id = request.env.user.sudo().partner_id
        values = {'partner_id': partner_id,
                  'wishlist_ids': partner_id.wishlist_id.product_wishlist_ids,
                  'request': request}
        return request.render('shabaka_website.profile', values)

    @http.route(['/page/blog'], type='http', auth="public", website=True)
    def display_my_blogs(self, **kw):
        partner_id = request.env.user.sudo().partner_id
        news_ids = request.env['blog.post'].sudo().search([], order='post_date desc')
        values = {'news': news_ids,
                  'request': request}
        return request.render('shabaka_website.blog_posts_search', values)

    @http.route(['/page/branches'], type='http', auth="public", website=True)
    def go_to_branches(self, **kw):
        partner_id = request.env.user.sudo().partner_id
        offer_ids = request.env['product.offer'].sudo().search([('valid_from', '<=', time.strftime('%Y-%m-%d')),
                                                                ('valid_to', '>=', time.strftime('%Y-%m-%d'))])
        news_ids = request.env['blog.post'].sudo().search([], order='post_date desc')
        product_ids = request.env['product.template'].sudo().search([], order='write_date desc', limit=4)
        values = {'offers': offer_ids,
                  'news': news_ids,
                  'products': product_ids,
                  'request': request}
        return request.render('shabaka_website.our_branches', values)


WebsiteSaleWishlist()
