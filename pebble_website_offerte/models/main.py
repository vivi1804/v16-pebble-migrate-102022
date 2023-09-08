# -*- coding: utf-8 -*-
import string
from odoo import models, fields, _

class WebsiteOfferte(models.Model):
    _inherit = 'crm.lead'

    x_studio_titel = fields.Many2one('res.partner.title', string="Titel")
    x_studio_voornaam = fields.Char(string="Voornaam")
    x_studio_achternaam = fields.Char(string="Achternaam")
    x_studio_postcode = fields.Char(string="Postcode")
    x_studio_huisnummer = fields.Char(string="Huisnummer")
    x_studio_dak_orientatie = fields.Selection([
        ("Noord","Noord"),("Oost","Oost"),("Zuid","Zuid"),("West","West"),
        ("Zuid-West","Zuid-West"),("Zuid-Oost","Zuid-Oost"),("Geen idee","Geen idee")])
    x_studio_investeringsredenen = fields.Selection([("Rendement","Rendement"),
                                            ("Eigen energie opwekken, Maandelijkse lasten verminderen","Eigen energie opwekken, Maandelijkse lasten verminderen"),
                                            ("Milieu (duurzaamheid) - Bijdrage aan de wereld","Milieu (duurzaamheid) - Bijdrage aan de wereld"),
                                            ("Groener energielabel","Groener energielabel"),
                                            ("Waarde stijging van mijn woning","Waarde stijging van mijn woning")])
    x_studio_energie_verbruik_per_jaar = fields.Integer(string="Energie verbruik per jaar")
    x_studio_zonnepanelen_= fields.Boolean(string="Zonnepanelen ? ")
    x_studio_infraroodverwarming_ = fields.Boolean(string="Infraroodverwarming ? ")
    x_studio_laadpaal_ = fields.Boolean(string="Laadpaal ? ")


class PartnerExtended(models.Model):
    _inherit = 'res.partner'

    x_first_name = fields.Char(string="Voornaam")