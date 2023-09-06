# -*- coding: utf-8 -*-

import werkzeug.urls
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.http_routing.models.ir_http import unslug, slug

class WebsiteCustomer(http.Controller):
    _references_per_page = 20

    @http.route([
        '/references',
        '/references/page/<int:page>',
        '/references/gemeente/<model("res.gemeente"):gemeente>',
        '/references/gemeente/<model("res.gemeente"):gemeente>/page/<int:page>',
        '/references/wijk/<model("res.wijk"):wijk>',
        '/references/wijk/<model("res.wijk"):wijk>/page/<int:page>',
        '/references/buurt/<model("res.buurt"):buurt>',
        '/references/buurt/<model("res.buurt"):buurt>/page/<int:page>',
    ], type='http', auth="public", website=True)
    def website_project_portal(self, gemeente=None, wijk=None, buurt=None, page=0, **post):
        Project = request.env['website.project.customer']
        Tag = request.env['website.project.tag']
        search_value = post.get('search')

        domain = [('post_state','=','st_publish')]
        if search_value:
            domain += [
                '|','|','|','|','|',
                ('name', 'ilike', search_value),
                ('short_description', 'ilike', search_value),
                ('long_description', 'ilike', search_value),
                ('gemeente_id.name', 'ilike', search_value),
                ('wijk_id.name', 'ilike', search_value),
                ('buurt_id.name', 'ilike', search_value),
            ]
        
        tag_id = post.get('tag_id')
        if tag_id:
            tag_id = unslug(tag_id)[1] or 0
            domain += [('tag_ids', 'in', tag_id)]

        # group by gemeente, based on customers found with the search(domain)
        gemeentes = Project.sudo().read_group(domain, ["id", "gemeente_id"], groupby="gemeente_id", orderby="gemeente_id")
        gemeente_count = Project.sudo().search_count(domain)

        if gemeente:
            domain += [('gemeente_id', '=', gemeente.id)]
            if gemeente.id not in (x['gemeente_id'][0] for x in gemeentes if x['gemeente_id']):
                if gemeente.exists():
                    gemeentes.append({
                        'gemeente_id_count': 0,
                        'gementee_id': (gemeente.id, gemeente.name)
                    })
                    gemeentes.sort(key=lambda d: (d['gemeente_id'] or (0, ""))[1])

        gemeentes.insert(0, {
            'gemeente_id_count': gemeente_count,
            'gemeente_id': (0, _("Alle Gemeentes"))
        })

        # group by wijk, based on customers found with the search(domain)
        wijks = Project.sudo().read_group(domain, ["id", "wijk_id"], groupby="wijk_id", orderby="wijk_id")
        wijk_count = Project.sudo().search_count(domain)

        if wijk:
            domain += [('wijk_id', '=', wijk.id)]
            if wijk.id not in (x['wijk_id'][0] for x in wijks if x['wijk_id']):
                if wijk.exists():
                    wijks.append({
                        'wijk_id_count': 0,
                        'wijk_id': (wijk.id, wijk.name)
                    })
                    wijks.sort(key=lambda d: (d['wijk_id'] or (0, ""))[1])

        wijks.insert(0, {
            'wijk_id_count': wijk_count,
            'wijk_id': (0, _("Alle Wijken"))
        })

        # group by wijk, based on customers found with the search(domain)
        buurts = Project.sudo().read_group(domain, ["id", "buurt_id"], groupby="buurt_id", orderby="buurt_id")
        buurt_count = Project.sudo().search_count(domain)

        if buurt:
            domain += [('buurt_id', '=', buurt.id)]
            if buurt.id not in (x['buurt_id'][0] for x in buurts if x['buurt_id']):
                if buurt.exists():
                    buurts.append({
                        'buurt_id_count': 0,
                        'buurt_id': (buurt.id, buurt.name)
                    })
                    buurts.sort(key=lambda d: (d['buurt_id'] or (0, ""))[1])

        buurts.insert(0, {
            'buurt_id_count': buurt_count,
            'buurt_id': (0, _("Alle Buurten"))
        })

        project_count = Project.sudo().search_count(domain)

        # pager
        url = '/references'
        if gemeente:
            url += '/gemeente/%s' % gemeente.id
        if wijk:
            url += '/wijk/%s' % wijk.id
        if buurt:
            url += '/buurt/%s' % buurt.id
        pager = request.website.pager(
            url=url, total=project_count, page=page, step=self._references_per_page,
            scope=7, url_args=post
        )

        projects = Project.sudo().search(domain, offset=pager['offset'], limit=self._references_per_page, order='create_date DESC')

        tags = Tag.search([('project_ids', 'in', projects.ids)], order='create_date DESC')
        tag = tag_id and Tag.browse(tag_id) or False

        values = {
            'gemeentes': gemeentes,
            'current_gemeente_id': gemeente.id if gemeente else 0,
            'current_gemeente': gemeente or False,
            'wijks': wijks,
            'current_wijk_id': wijk.id if wijk else 0,
            'current_wijk': wijk or False,
            'buurts': buurts,
            'current_buurt_id': buurt.id if buurt else 0,
            'current_buurt': buurt or False,
            'projects': projects,
            'post': post,
            'search_path': "?%s" % werkzeug.url_encode(post),
            'pager': pager,
            'tag': tag,
            'tags': tags,
        }
        return request.render("website_project.index", values)
    
    @http.route(['/references/<project_id>'], type='http', auth="public", website=True)
    def projects_detail(self, project_id, **post):
        _, project_id = unslug(project_id)
        if project_id:
            project = request.env['website.project.customer'].sudo().browse(project_id)
            if project.exists():
                values = {}
                values['main_object'] = values['project'] = project
                return request.render("website_project.details", values)
        return self.customers(**post)