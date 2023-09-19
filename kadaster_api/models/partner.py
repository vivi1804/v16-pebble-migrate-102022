# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
import requests
from datetime import datetime
import time

class InheritResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    run_on_test = fields.Boolean(string="Run on test")
    api_key_test = fields.Char(string="API Key (test)")
    api_key_live = fields.Char(string="API Key (live)")

    # the set_values function saves the value of the run_on_test field to the ir.config_parameter model. 
    # The get_values function retrieves the value of the run_on_test field from the ir.config_parameter model.
    def set_values(self):
        res = super(InheritResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('kadaster_api.run_on_test', self.run_on_test)
        self.env['ir.config_parameter'].sudo().set_param('kadaster_api.api_key_test', self.api_key_test)
        self.env['ir.config_parameter'].sudo().set_param('kadaster_api.api_key_live', self.api_key_live)
        return res

    @api.model
    def get_values(self):
        res = super(InheritResConfigSettings, self).get_values()
        res.update(
            run_on_test=self.env['ir.config_parameter'].sudo().get_param('kadaster_api.run_on_test'),
            api_key_test=self.env['ir.config_parameter'].sudo().get_param('kadaster_api.api_key_test'),
            api_key_live=self.env['ir.config_parameter'].sudo().get_param('kadaster_api.api_key_live')
        )
        return res

class kadasterPartner(models.Model):
    _inherit = 'res.partner'

    datum = fields.Date(string="Datum")
    verblijfsobject = fields.Char(string="Verblijfsobject")
    gebruiksdoel = fields.Char(string="Gebruiksdoel")

    def action_get_mode(self):
        RUN_ON_TEST = self.env['ir.config_parameter'].sudo().get_param('kadaster_api.run_on_test')
        print (RUN_ON_TEST)
        if RUN_ON_TEST == "True":
            MODE = "TEST"
        else:
            MODE = "LIVE"
        return MODE

    def action_get_kadaster_data(self):

        ##GET THE MODE TEST/LIVE
        MODE = self.action_get_mode()
        print ("KADASTER MODE: ", MODE)

        ##GET THE API BASED ON THE MODE
        if MODE == "TEST": 
            API_KEY = self.env['ir.config_parameter'].sudo().get_param('kadaster_api.api_key_test')
        elif MODE == "LIVE": 
            API_KEY = self.env['ir.config_parameter'].sudo().get_param('kadaster_api.api_key_live')

        print ("API KEY: ", API_KEY)

        ##GET REQUIRED DATA FOR API
        postcode = self.zip
        huisnummer = self.street_number
        date_now = datetime.utcnow().strftime('%Y-%m-%d')
        
        print ("Postcode : ", postcode)
        print ("Huisnummer : ", huisnummer)

        if API_KEY:
            headers = {'Accept': 'application/hal+json', 'X-Api-Key': API_KEY}
            print ("Found api key....")

            if postcode and huisnummer:
                print ("Found postcode and huisnummer for this customer...")

                ##search paramater and get identification id
                params = {'postcode': postcode, 'huisnummer': huisnummer, 'exacteMatch':'true', 'page':'1'}
                
                #url based on mode test/live
                if MODE == "TEST": 
                    url = 'https://api.bag.acceptatie.kadaster.nl/lvbag/individuelebevragingen/v2/adressen'
                elif MODE == "LIVE": 
                    url = 'https://api.bag.kadaster.nl/lvbag/individuelebevragingen/v2/adressen'

                print ("Call api to get identification id...")
                start = time.time()
                response = requests.get(url, headers=headers, params=params)

                if response.status_code == 200:
                    data = response.json()
                    if '_embedded' in data:
                        IDENTIFICATIE = data['_embedded']['adressen'][0]['adresseerbaarObjectIdentificatie']
                    else:
                        raise ValidationError("Kadaster API not returning any data.")
                        IDENTIFICATIE = False
                    
                else:
                    print(f'Error: {response.status_code}')
                    IDENTIFICATIE = False
                    raise ValidationError("Postcode and huisnummer might be wrong.")
                
                if IDENTIFICATIE:
                    print ("Indentificatie id found...")
                    print ("Identificatie : ", IDENTIFICATIE)

                    headers_details = {'accept': 'application/hal+json', 'Accept-Crs': 'epsg:28992', 'X-Api-Key': API_KEY}

                    #url based on mode test/live
                    if MODE == "TEST": 
                        url_details = 'https://api.bag.acceptatie.kadaster.nl/lvbag/individuelebevragingen/v2/adresseerbareobjecten/%s' % IDENTIFICATIE
                    elif MODE == "LIVE": 
                        url_details = 'https://api.bag.kadaster.nl/lvbag/individuelebevragingen/v2/adresseerbareobjecten/%s' % IDENTIFICATIE

                    print ("Call api to get gebruiksdoelen...")
                    response_details = requests.get(url_details, headers=headers_details)

                    if response_details.status_code == 200:
                        data_details = response_details.json()
                        data_gebruiksdoelen = data_details['verblijfsobject']['verblijfsobject']['gebruiksdoelen'][0]
                        print ("gebruiksdoel : ", data_gebruiksdoelen)

                        end = time.time()
                        self.write({'datum': date_now, 'verblijfsobject': IDENTIFICATIE, 'gebruiksdoel': data_gebruiksdoelen})
                        
                        print ("kadaster api job done, it takes ", (end - start) , " seconds")

                    else:
                        print(f'Error: {response_details.status_code}')

            else:
                raise ValidationError("Please make sure you have filled in the postcode and huisnummer")