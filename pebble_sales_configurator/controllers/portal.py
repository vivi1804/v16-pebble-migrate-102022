# -*- coding: utf-8 -*-

import base64
from odoo import http
import werkzeug
from odoo.http import request
from odoo.addons.website.controllers import form

class WebsiteForm(form.WebsiteForm):

    @http.route(['/enphase', '/paneel/ref=<int:paneel_id>',
                '/frame/ref=<int:frame_id>','/roof/ref=<int:roof_id>'], type='http', auth="public", website=True)
    def website_sales_config_enphase(self, paneel_id=None, frame_id=None, roof_id=None, **post):
        default_values = {}
        values = {}
        if request.env.user:
            default_values['user_id'] = request.env.user.id
        
        ## Check if there is draft order
        ## If no draft create new, if found draft then check the last saved step 
        MODE = "new"
        opportunity = False
        sales_order = False
        attachments_ids = False
        types = request.env['sales.configurator.type'].search([('name','=',"Enphase")])
        sales = request.env['sales.configurator'].search(['&','&',('verkoper.id','=', request.env.user.id ),('state','=',"draft"),
        ('sales_configurator_type.id','=', types.id)], limit=1)

        ## Checking and determine the mode of the record 
        if sales:
            ## search opportunity
            ## if found opportunity then show the existing data 
            ## if not found then create new.
            if sales.opportunity:
                opportunity = sales.opportunity.id
                sales.write({'opportunity' : opportunity, 'powercon': sales.opportunity.x_studio_energie_verbruik_per_jaar})
                sales_order = request.env['sale.order'].search(['&',('opportunity_id','=', opportunity),('state','in',['draft','sent'])], order="create_date desc", limit=1) 
                MODE = "show_opportunity"
            else:
                MODE = "no_opportunity"

            if sales.opportunity_page == True and sales.step_2 == False:
                MODE = "step2"
                ## load record attachments
                attachments_ids = request.env['ir.attachment'].search([('res_id','=', sales.id)])
            elif sales.step_2 == True and sales.step_3 == False:
                MODE = "step3"
            elif sales.step_3 and sales.step_4 == False:
                MODE = "step4"
        
        ## If opportunity not found then create one
        ## Checking if user have created the opportunity 
        ## if system found new created opportunity then update sales configuration and assign the mode back to step2
        if MODE  == "no_opportunity":
            opportunities = request.env['crm.lead'].search([('name','ilike', sales.name)], limit=1)
            if opportunities:
                for line in opportunities:
                    ## system found the opprtunity. update the sales record to add the opportunity
                    sales.write({'opportunity': line.id, 'powercon': line.x_studio_energie_verbruik_per_jaar})

                    ## Get sales order 
                    opportunity = line.id
                    sales_order = request.env['sale.order'].search(['&',('opportunity_id','=', opportunities.id),('state','=',"draft")], limit=1)
                    
                    ### automatic action will take next action: create sales and copy attachments to partner_id
                    
                    MODE = "show_opportunity"

        ##data for selection fields        
        products_paneel = request.env['sales.configurator.type_paneel'].search([])
        products_frame = request.env['sales.configurator.type_frame'].search([])

        ##load instruction
        company_id = request.env.user.company_id

        ##load sales condition
        sales_condition =  request.env['sale.template.conditions'].search([('is_sales_configurator','=',True)])

        ##IF THERE IS PANEEL ID THEN DELETE PANEEL
        if paneel_id:
            rec_paneel = request.env['sales.configurator.paneel'].search([('id','=', paneel_id)])
            rec_paneel.unlink()

        ##IF THERE IS FRAME ID THEN DELETE FRAME
        if frame_id:
            rec_frame = request.env['sales.configurator.frame'].search([('id','=', frame_id)])
            rec_frame.unlink()

        ##IF THERE IS ROOF ID THEN DELETE ROOF
        if roof_id:
            rec_roof = request.env['sales.configurator.roof'].search([('id','=', roof_id)])
            rec_roof.unlink()
    
        values = {
            'default_values': default_values,
            'mode': MODE,
            'products_paneel': products_paneel,
            'products_frame': products_frame,
            'opportunity': opportunity,
            'sales_order': sales_order,
            'company_id': company_id,
            'sales': sales,
            'types': types,
            'sales_condition':sales_condition,
            'attachments_ids': attachments_ids}

        return request.render("pebble_sales_configurator.enphase_form", values )

    ##STEP 1: Create the draft sales configurator record. 
    ##And pass some value to the fields.
    @http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
    def website_form(self, model_name, **kwargs):
        if model_name == "sales.configurator":
            param_postcode = request.params.get('postcode')
            param_huisnummer = request.params.get('huisnummer')
            huisnummer = param_huisnummer.strip()
            request.params['name'] = "-".join([param_postcode,huisnummer])
            request.params['step_1'] = True
            request.params['energycost'] = 0.4
            request.params['klein_materiaal'] = "ja"
            request.params['klein_aantal_dagen'] = 1
            request.params['steiger'] = "ja"
            request.params['steiger_aantal_dagen'] = 1
            request.params['aansluitwaarde'] = "25"
            request.params['kabeltrace'] = "Dit wordt bepaald tijdens de opname door de monteur."
            
        return super(WebsiteForm, self).website_form(model_name, **kwargs) 
    
    ## Update opportunity pages.
    @http.route('/step_opp', type='json', auth="public", website=True, csrf=False)
    def step_opp_json(self, **post): 
        ## get the value from js
        if post:
            id = post['id']
            dak_orientatie = post['dak_orientatie']
            investeringsredenen = post['investeringsredenen']
            energie_verbruik = post['energie_verbruik']
            medium_id = post['medium_id']
            
            if post['zonnepanelen'] == "True":
                zonnepanelen = True
            else: 
                zonnepanelen = False

            if post['infraroodverwarming'] == "True":
                infraroodverwarming = True
            else: 
                infraroodverwarming = False

            if post['laadpaal'] == "True":
                laadpaal = True
            else: 
                laadpaal = False

            description = post['description']
            title = post['title']
            voornaam = post['voornaam']
            phone = post['phone']
            achternaam = post['achternaam']
            email_from = post['email_from']

            vals = {
                    'x_studio_dak_orientatie' : dak_orientatie,
                    'x_studio_investeringsredenen' : investeringsredenen,
                    'x_studio_energie_verbruik_per_jaar' : energie_verbruik,
                    'medium_id' : medium_id,
                    'x_studio_zonnepanelen_' : zonnepanelen,
                    'x_studio_infraroodverwarming_' : infraroodverwarming,
                    'x_studio_laadpaal_' : laadpaal,
                    'description' : description,
                    'x_studio_title' : title,
                    'x_studio_voornaam' : voornaam,
                    'phone' : phone,
                    'x_studio_achternaam' : achternaam,
                    'email_from' : email_from,
            }
        
        ## update opportunity records.
        opportunity = request.env['crm.lead'].search([('id','=', id)], limit=1)
        opportunity.write(vals)

        ## change state on sales configuration
        for line in  opportunity.sale_configuration:
            if line.state == "draft" and line.sales_configurator_type.name == "Enphase":
                sale_configuration = line

        sales = request.env['sales.configurator'].search([('id','=', sale_configuration.id)], limit=1)
        sales.write({'opportunity_page': True})

        args = {'success': True}
        return args 

    #STEP 2: Update the draft record.
    @http.route('/step2', type='json', auth="public", website=True, csrf=False)
    def step2_json(self, **post):  
        ## get value from js
        if post:
            id = post['id']
            aansluiting = post['aansluiting']
            aantal_eindstoppen = post['aantal_eindstoppen']
            enyoy = post['enyoy']
            powercon = post['powercon']
            desireprod = post['desireprod']
            energycost = post['energycost']
            grondkabel = post['grondkabel']
            elecprod = post['elecprod']
            condition_id = post['condition_id']
            aansluitwaarde = post['aansluitwaarde']
            kabeltrace = post['kabeltrace']
            extra_dakvlakken_eenvoudig = post['extra_dakvlakken_eenvoudig']
            extra_dakvlakken_complex = post['extra_dakvlakken_complex']
            
            if post['dakdoorvoer'] == "True":
                dakdoorvoer = True
            else: 
                dakdoorvoer = False

            ## text replace for condition text
            condition = request.env['sale.template.conditions'].search([('id','=', condition_id)], limit=1)
            txt_replace = condition.sale_condition.replace("[aansluitwaarde]", aansluitwaarde ).replace("[route ac kabel]", kabeltrace )

            vals = {
                    'aansluiting': aansluiting,
                    'aantal_eindstoppen': aantal_eindstoppen,
                    'enyoy': enyoy,
                    'powercon': powercon,
                    'desireprod': desireprod,
                    'energycost': energycost,
                    'grondkabel': grondkabel,
                    'elecprod': elecprod,
                    'sales_condition_id':condition_id,
                    'condition_txt': txt_replace,
                    'aansluitwaarde': aansluitwaarde,
                    'kabeltrace': kabeltrace,
                    'extra_dakvlakken_eenvoudig': extra_dakvlakken_eenvoudig,
                    'extra_dakvlakken_complex': extra_dakvlakken_complex,
                    'dakdoorvoer': dakdoorvoer,
                    'step_2': True}

            ## condition for attachment 
            if "legplan" in post:
                legplan = post['legplan']['file']
                vals["legplan"] = legplan

            if "materkast" in post.keys():
                materkast =  post['materkast']['file']
                vals["foto_materkast"] = materkast

            ## update sales configurator records
            sales = request.env['sales.configurator'].search([('id','=', id)], limit=1)
            sales.write(vals)

            ##get attachments files and name
            attchs = []
            for key in post:
                if key == "attachments":
                    for line in post[key]:
                        filename = line['filename']
                        file = line['file']

                        ##CREATE ATTACHMENTS
                        attch = request.env['ir.attachment'].sudo().create({
                        'name': filename, 
                        'type': "binary", 
                        'res_model': "sales.configurator", 
                        'res_id': id, 
                        'datas': file, 
                        'mimetype': 'image/png'})
                        attchs.append(attch.id)

                        ##CREATE ATTACHMENT FOR PARTNER
                        partner_attch = request.env['ir.attachment'].sudo().create({
                        'name': filename, 
                        'type': "binary", 
                        'res_model': "res.partner", 
                        'res_id': sales.opportunity.partner_id.id, 
                        'datas': file, 
                        'mimetype': 'image/png'})
                        sales.write({'copy_attachment': True})

                    #POST MESSAGE
                    if attchs:
                        msg_id = sales.sudo().message_post(body="Attached Files", message_type="comment")
                        for file_id in attchs:
                            msg_id.sudo().write({'attachment_ids': [(4, file_id)]})

        args = {'success': True}
        return args
    
    #STEP 3: Update the draft record.
    @http.route('/step3', type='json', auth="public", website=True, csrf=False)
    def step3_json(self, **post):  
        ## get data from js
        if post:
            id = post['id']
            steiger = post['steiger']
            steiger_aantal_dagen = post['steiger_aantal_dagen']
            ladderlift = post['ladderlift']
            ladderlift_aantal_dagen = post['ladderlift_aantal_dagen']
            dakrandbeveiliging = post['dakrandbeveiliging']
            dak_aantal_dagen = post['dak_aantal_dagen']
            dak_aantal_meter = post['dak_aantal_meter']
            verrijker = post['verrijker']
            verrijker_aantal_dagen = post['verrijker_aantal_dagen']
            notes = post['notes']

            ## Update records 
            sales = request.env['sales.configurator'].search([('id','=', id)], limit=1)
            sales.write({
                'steiger': steiger,
                'steiger_aantal_dagen': steiger_aantal_dagen,
                'ladderlift': ladderlift,
                'ladderlift_aantal_dagen': ladderlift_aantal_dagen,
                'dakrandbeveiliging':  dakrandbeveiliging,
                'dak_aantal_dagen': dak_aantal_dagen,
                'dak_aantal_meter': dak_aantal_meter,
                'verrijker': verrijker,
                'verrijker_aantal_dagen':verrijker_aantal_dagen,
                'notes': notes,
                'step_3': True
                })

        args2 = {'success': True}
        return args2

    #STEP 4: Update the draft record and confirm the record.
    ## In this step, must have opportunity that connect to sales order
    ## Mark as done
    @http.route('/confirm', type='json', auth="public", website=True, csrf=False)
    def confirm_json(self, **post):  
        ## get value from js
        if post:
            id = post['id']

            ## update records 
            sales = request.env['sales.configurator'].search([('id','=', id)], limit=1)
            sales.write({'state': "confirm", 'step_4': True})

        args2 = {'success': True}
        return args2

    # Getting the sale order report.
    ## In this step, the sales order need to be "sent"
    @http.route('/enphase/report/<enphase_id>', methods=['POST', 'GET'], csrf=False, type='http', auth="user", website=True)
    def print_id(self, enphase_id, **kw):
        sales = request.env['sale.order'].sudo().search([('id', '=', enphase_id)], limit=1)
        if not sales:
            return None
        pdf, _ = request.env['ir.actions.report']._get_report_from_name(
            'sale.report_saleorder').sudo().render_qweb_pdf(
            [int(enphase_id)])
        pdf_http_headers = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        return request.make_response(pdf, headers=pdf_http_headers)
    
    #PREVIOUS BUTTON
    ## Back to step opportunity
    @http.route('/back_step_opp', type='json', auth="public", website=True, csrf=False)
    def back_step_opp(self, **post): 
        if post:
            id = post['id']

            sales = request.env['sales.configurator'].search([('id','=', id)], limit=1)
            sales.write({'opportunity_page': False})

        args2 = {'success': True}
        return args2

    ## Back to step 2
    @http.route('/back_step2', type='json', auth="public", website=True, csrf=False)
    def back_step2(self, **post): 
        if post:
            id = post['id']

            sales = request.env['sales.configurator'].search([('id','=', id)], limit=1)
            sales.write({'step_2': False})

        args2 = {'success': True}
        return args2

    #PREVIOUS BUTTON
    ## Back to step 3
    @http.route('/back_step3', type='json', auth="public", website=True, csrf=False)
    def back_step3(self, **post): 
        if post:
            id = post['id']

            sales = request.env['sales.configurator'].search([('id','=', id)], limit=1)
            sales.write({'step_3': False})

        args3 = {'success': True}
        return args3

    ## adding paneel line 
    @http.route('/add_paneel', type='json', auth="public", website=True, csrf=False)
    def add_paneel(self, **post): 
        if post:
            id = post['id']
            paneel = post['paneel']
            aantal_panelen = post['aantal_panelen']

            sales = request.env['sales.configurator'].search([('id','=', id)], limit=1)
            sales.write({'paneel_ids': [(0,0, {'type_paneel':paneel,'aantal_panelen':aantal_panelen})]})

        args = {'success': True}
        return args

    ## adding frame lines
    @http.route('/add_frame', type='json', auth="public", website=True, csrf=False)
    def add_frame(self, **post): 
        if post:
            id = post['id']
            frame = post['frame']
            aantal_frame = post['aantal_frame']

            sales = request.env['sales.configurator'].search([('id','=', id)], limit=1)
            sales.write({'frame_ids': [(0,0, {'type_frame':frame,'aantal_frame':aantal_frame})]})

        args = {'success': True}
        return args

    ## adding roof lines
    @http.route('/add_roof', type='json', auth="public", website=True, csrf=False)
    def add_roof(self, **post): 
        if post:
            id = post['id']
            type = post['roof']
            name = post['roof_name']

            sales = request.env['sales.configurator'].search([('id','=', id)], limit=1)
            sales.write({'roof_ids': [(0,0, {'type':type,'name':name})]})

        args = {'success': True}
        return args

    ## discard sales configuration
    @http.route(['/discard','/discard_opp'], type='json', auth="public", website=True, csrf=False)
    def discard(self, **post): 
        ## get value from js
        if post:
            id = post['id']

            sales = request.env['sales.configurator'].search([('id','=', id)], limit=1)
            sales.write({'state': "cancel"})
            if sales.opportunity:
                OPPORTUNITY = sales.opportunity.id
                sales.write({'opportunity': [(2, OPPORTUNITY)] })

        args = {'success': True}
        return args
    
    ## SEND QUOTATION
    @http.route('/send_quotation', type='json', auth="public", website=True, csrf=False)
    def send_quotation(self, **post):
        if post:
            id = post['id']

        sale_id = request.env['sale.order'].sudo().search([('id','=', id)], limit=1)

        pdf, pdf_name = request.env['ir.actions.report']._get_report_from_name('sale.report_saleorder').sudo().render_qweb_pdf([int(id)])
        pdf = base64.b64encode(pdf)
        attachment_id = request.env['ir.attachment'].sudo().create({
            'name': sale_id.name + ".pdf",
            'datas': pdf,
            'res_model': 'sale.order',
            'res_id': sale_id.id,
        })

        param_template_id = request.env['ir.config_parameter'].sudo().search([('key','=', "pebble_so_mail_template_id")])
        template_id = int(param_template_id.value)
        template =  request.env['mail.template'].sudo().browse(template_id)
        if template:
            template.sudo().send_mail(sale_id.id, force_send=True)
            msg_id = sale_id.sudo().message_post(body="Email sent to customer")
            msg_id.sudo().write({'attachment_ids': [(4, attachment_id.id)]})
            
            sale_id.write({'state': "sent"})

        args = {'success': True}
        return args