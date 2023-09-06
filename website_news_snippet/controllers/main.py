# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.http_routing.models.ir_http import unslug, slug
from bs4 import BeautifulSoup

class WebBlogSnippet(http.Controller):
    @http.route(['/get_news_posts'], type='json', auth='public', website=True)
    def get_news_posts(self):
        #domain = [('website_published', '=', True),('blog_id.name','=',"News")]
        news_id = http.request.env['ir.config_parameter'].sudo().search([('key','=',"blog_news_id")])
        domain = [('website_published', '=', True),('blog_id.id','=',news_id.value)]
        blogs = http.request.env['blog.blog'].sudo().search([('id','=', news_id.value)])
        posts = http.request.env['blog.post'].sudo().search(domain, limit=1, order='post_date desc')
        p = []

        blog_blog = slug(blogs)
        blog_post = slug(posts)
        post_url = blog_blog + "/post/" + blog_post 

        for post in posts:

            ## CONVERT HTML TO TEXT
            soup = BeautifulSoup(post.content, features='html.parser')
            txt_content = soup.get_text()

            ##GET FIRST IMAGES FOR POST COVER
            images = soup.findAll('img')
            if images:
                if images[0].has_attr('src'):
                    img_cover = images[0]['src']
            else:
                img_cover = "/web/image/website.library_image_07"

            post = {
                "name": post.name,
                "subtitle": post.subtitle,
                "content": txt_content,
                "cover": img_cover,
                "post_url": post_url,
            }
            p.append(post)
        return p
