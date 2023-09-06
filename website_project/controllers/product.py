# -*- coding: utf-8 -*-
import werkzeug.urls
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.http_routing.models.ir_http import unslug, slug

class WebsiteProduct(http.Controller):
    _references_per_page = 5

    @http.route([
        '/product_info',
        '/product_info/page/<int:page>',
    ], type='http', auth="public", website=True)
    def website_product_portal(self, page=0, **post):
        Product = request.env['product.template']
        Category = request.env['website.product.category']
        search_value = post.get('search')

        domain = [('published', '=', True)]
        if search_value:
            domain += [
                '|','|','|','|',
                ('name', 'ilike', search_value),
                ('default_code', 'ilike', search_value),
                ('short_description', 'ilike', search_value),
                ('html_product_details', 'ilike', search_value),
                ('html_product_details_2', 'ilike', search_value),
            ]
        
        category_id = post.get('category_id')
        if category_id:
            category_id = unslug(category_id)[1] or 0
            domain += [('website_category_ids', 'in', category_id)]

        product_count = Product.sudo().search_count(domain)

        # pager
        url = '/product_info'
        pager = request.website.pager(
            url=url, total=product_count, page=page, step=self._references_per_page,
            scope=7, url_args=post
        )

        products = Product.sudo().search(domain, offset=pager['offset'], limit=self._references_per_page)

        categories = Category.search([('product_ids', 'in', products.ids)], order='name ASC')
        category = category_id and Category.browse(category_id) or False

        values = {
            'products': products,
            'post': post,
            'search_path': "?%s" % werkzeug.url_encode(post),
            'pager': pager,
            'category': category,
            'categories': categories,
        }
        return request.render("website_project.product_index", values)
    
    @http.route(['/product_info/<product_id>'], type='http', auth="public", website=True)
    def products_detail(self, product_id, **post):
        _, product_id = unslug(product_id)
        if product_id:
            product = request.env['product.template'].sudo().browse(product_id)
            if product.exists():
                values = {}
                values['main_object'] = values['product'] = product
                return request.render("website_project.product_details", values)
        return self.product(**post)