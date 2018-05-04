# -*- coding: utf-8 -*-
{
    'name': "Shabaka Website",
    'description': """
        Shabaka website
    """,
    'license': 'LGPL-3',
    'category': 'Website',
    'version': '0.1',
    'depends': ['website_sale', 'nzm_product', 'auth_signup', 'website_blog'],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'templates/webclient_view.xml',
        'templates/replace_header_footer.xml',
        'templates/about.xml',
        'templates/register_view.xml',
        'templates/blog.xml',
        'templates/branches.xml',
        'templates/cart.xml',
        'templates/checkout.xml',
        'templates/contact.xml',
        'templates/events.xml',
        'templates/index.xml',
        'templates/owner.xml',
        'templates/paymentMethod.xml',
        'templates/profile.xml',
        'templates/request.xml',
        'templates/settings.xml',
        'templates/single.xml',
        'templates/terms.xml',
        'templates/shop_inherit.xml',
        'templates/shop_product.xml',
        'views/res_partner_view.xml',
        'views/wishlist_view.xml',
        'views/product_offer_view.xml',
        'views/blog_post_view.xml',
    ],
    'installable': True

}
