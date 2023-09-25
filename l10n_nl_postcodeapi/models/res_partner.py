# Copyright 2013-2015 Therp BV <https://therp.nl>
# @autors: Stefan Rijnhart, Ronald Portier
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.tools import ormcache
import requests


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    @ormcache(skiparg=2)
    def get_province(self, province):
        """ Return the province or empty recordset """
        if not province:
            return self.env["res.country.state"]
        return self.env["res.country.state"].search(
            [("name", "=", province)], limit=1
        )

    @api.onchange("zip", "street_number", "country_id")
    def on_change_zip_street_number(self):
        """
        Normalize the zip code, check on the partner's country and
        if all is well, request address autocompletion data.

        NB. postal_code is named 'zip' in Odoo, but is this a reserved
        keyword in Python
        """
        postal_code = self.zip and self.zip.replace(" ", "")
        country = self.country_id
        if (
            not (postal_code and self.street_number)
            or country
            and country != self.env.ref("base.nl")
        ):
            return {}
        auth_key = self.env["ir.config_parameter"].sudo().get_param(
            "l10n_nl_postcodeapi.apikey", ""
        )
        base_url = ("https://api.postcodeapi.nu/v3/lookup/%s/%s" % (
            postal_code, self.street_number
        ))
        headers = {
            'X-Api-Key': str(auth_key)
        }
        resp = requests.request(method='GET', url=base_url, headers=headers,
                                timeout=60)
        resp_data = resp.json()
        err_msg = resp_data.get('title', False)
        if err_msg:
            return {"warning": {"title": _("Warning"), "message": err_msg}}
        self.street_name = resp_data.get('street', False)
        self.city = resp_data.get('city', False)
        self.state_id = self.get_province(resp_data.get('province', False))
