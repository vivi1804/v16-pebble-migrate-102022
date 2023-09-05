# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResWijk(models.Model):
    """A register class to create new menu"""
    _name = 'res.wijk'
    _description = "Partner Wijk"

    name = fields.Char('Name')
    cbs_wijkcode = fields.Char('CBS-Wijkcode')
    kaart = fields.Binary('Kaart', attachment=True)
    buurt_ids = fields.One2many('res.buurt','wijk_id','Buurt')
    gemeente_id = fields.Many2one('res.gemeente','Gemeente')

    #def name_get(self):
    #    res = []
    #    for title in self:
    #        name = title.todo_id
    #        res.append((title.id, name))
    #    return res

class ResBuurt(models.Model):
    """A register class to create new menu"""
    _name = 'res.buurt'
    _description = "Partner Buurt"

    name = fields.Char('Name')
    wijk_id = fields.Many2one('res.wijk','Wijk')
    cbs_buurtcode = fields.Char('CBS-Buurtcode')
    inwoner_aantal = fields.Integer('Inwoner Aantal')
    oppvlakte_totaal_ha = fields.Integer('Opp.vlakte Totaal Ha')
    oppvlakte_land = fields.Integer('Opp.vlakte Land')
    kaart = fields.Binary('Kaart', attachment=True)

class ResGemeente(models.Model):
    """A register class to create new menu"""
    _name = 'res.gemeente'
    _description = "Partner Gemeente"

    code = fields.Char('Gemeentecode')
    gm_code = fields.Char('GemeentecodeGM')
    name = fields.Char('Gemeentenaam')
    state_id = fields.Many2one('res.country.state', string="Provincie")
    wijk_ids = fields.One2many('res.wijk','gemeente_id','Wijk')

class ResPartnerExt(models.Model):
    """A register class to create new menu"""
    _inherit = 'res.partner'

    buurt_id = fields.Many2one('res.buurt','Buurt', domain="[('wijk_id', '=?', wijk_id)]")
    wijk_id = fields.Many2one('res.wijk','Wijk', domain="[('gemeente_id', '=?', gemeente_id)]")
    gemeente_id = fields.Many2one('res.gemeente','Gemeente', domain="[('state_id', '=?', state_id)]")

class ResPartnerState(models.Model):
    """A register class to create new menu"""
    _inherit = 'res.country.state'

    prov_code = fields.Char('Provinciecode')
    prov_code_pv = fields.Char('ProvinciecodePV')


        