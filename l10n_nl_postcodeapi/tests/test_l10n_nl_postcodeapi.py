# Copyright 2018 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.modules.module import get_module_resource
from odoo.tests.common import TransactionCase


class TestNlPostcodeapi(TransactionCase):
    def setUp(self):
        super(TestNlPostcodeapi, self).setUp()
        # this block of code removes the existing provinces
        # eventually already created by module l10n_nl_country_states
        # to avoid conflicts with tests of l10n_nl_country_states
        is_l10n_nl_country_states_installed = self.env["ir.model"]._get(
            "res.country.state.nl.zip"
        )
        if is_l10n_nl_country_states_installed:
            NlZipStateModel = self.env["res.country.state.nl.zip"]
            NlZipStateModel.search([]).unlink()
            country_nl = self.env["res.country"].search(
                [("code", "like", "NL")], limit=1
            )
            self.assertTrue(country_nl)
            states = self.env["res.country.state"].search(
                [("country_id", "=", country_nl.id)]
            )
            states.unlink()

    def load_nl_provinces(self):
        csv_resource = get_module_resource(
            "l10n_nl_postcodeapi", "examples", "res.country.state.csv",
        )
        csv_file = open(csv_resource, "rb").read()
        import_wizard = self.env["base_import.import"].create(
            {
                "res_model": "res.country.state",
                "file": csv_file,
                "file_type": "text/csv",
            }
        )
        result = import_wizard.parse_preview(
            {"quoting": '"', "separator": ",", "headers": True,}
        )
        self.assertIsNone(result.get("error"))
        results = import_wizard.do(
            ["id", "country_id", "name", "code"],
            ["id", "country_id", "name", "code"],
            {'quoting': '"', 'separator': ',', 'headers': True},
            True
        )
        self.assertFalse(
            results, "results should be empty on successful import"
        )

    def test_01_ir_config_parameter(self):
        config_parameter = self.env["ir.config_parameter"].search(
            [("key", "=", "l10n_nl_postcodeapi.apikey")]
        )
        # Verify l10n_nl_postcodeapi.apikey is created
        self.assertTrue(config_parameter)
        self.assertEqual(config_parameter.value, "Your API key")
        # Verify l10n_nl_postcodeapi.apikey is modified
        config_parameter.write({"value": "KEYXXXXXXXXXXXNOTVALID"})
        self.assertEqual(config_parameter.value, "KEYXXXXXXXXXXXNOTVALID")

    def test_02_res_country_state(self):
        country_nl = self.env["res.country"].search(
            [("code", "like", "NL")], limit=1
        )
        states = self.env["res.country.state"].search(
            [("country_id", "=", country_nl.id)]
        )
        # Verify res.country.state created
        states = self.env["res.country.state"].search(
            [("country_id", "=", country_nl.id)]
        )
        self.assertTrue(states)
        # Verify res.country.state modified
        states[0].write({"name": "test"})
        self.assertEqual(states[0].name, "test")
        # Verify res.country.state unlinked
        states[0].unlink()
        test_states = self.env["res.country.state"].search(
            [("name", "like", "test")]
        )
        self.assertFalse(test_states)

    def test_03_res_partner_with_province(self):
        # Set l10n_nl_postcodeapi.apikey
        config_parameter = self.env["ir.config_parameter"].search(
            [("key", "=", "l10n_nl_postcodeapi.apikey")]
        )
        config_parameter.write(
            {"value": "LWMKElEaEL26pkPGY6Db96vwHrhRZACX9iqbqRYs"}
        )
        country_nl = self.env["res.country"].search(
            [("code", "like", "NL")], limit=1
        )
        partner = self.env["res.partner"].create(
            {"name": "test partner"}
        )
        partner.write({
            "street_name": "Chaussee",
            "country_id": country_nl.id,
            "street_number": 29,
            "street_number2": 29,
            "zip": "6545CA"
        })
        partner.on_change_zip_street_number()
        self.assertEqual(partner.street_name, "Waldeck Pyrmontsingel")
        self.assertEqual(partner.city, "Nijmegen")
        self.assertEqual(partner.state_id.name, "Gelderland")
        self.assertEqual(partner.state_id.code, "GE")

    def test_04_res_partner_no_province(self):
        # Set l10n_nl_postcodeapi.apikey
        config_parameter = self.env["ir.config_parameter"].search(
            [("key", "=", "l10n_nl_postcodeapi.apikey")]
        )
        config_parameter.write(
            {"value": "LWMKElEaEL26pkPGY6Db96vwHrhRZACX9iqbqRYs"}
        )
        country_nl = self.env["res.country"].search(
            [("code", "like", "NL")], limit=1
        )
        partner = self.env["res.partner"].create(
            {"name": "test partner", "country_id": country_nl.id,}
        )
        partner.write({
            "street_name": "Chaussee",
            "country_id": country_nl.id,
            "street_number": 19,
            "street_number2": 19,
            "zip": "1021JT"
        })
        partner.on_change_zip_street_number()
        partner._convert_to_write(partner._cache)
        self.assertEqual(partner.street_name, "Hamerstraat")
        self.assertEqual(partner.city, "Amsterdam")
        self.assertEqual(partner.street, "Hamerstraat 19/19")

    def test_05_res_partner_other_country(self):
        country_it = self.env["res.country"].search(
            [("code", "like", "IT")], limit=1
        )
        partner = self.env["res.partner"].create(
            {"name": "test partner"}
        )
        partner.write({
            "street_name": "Chaussee",
            "country_id": country_it.id,
            "street_number": 17,
            "street_number2": 17,
            "zip": "5038EA1"
        })
        partner.on_change_zip_street_number()
        partner._convert_to_write(partner._cache)
        self.assertFalse(partner.city)
        self.assertFalse(partner.state_id)
        self.assertEqual(partner.street, "17/17 Chaussee")

    def test_06_res_partner_no_key(self):
        country_nl = self.env["res.country"].search(
            [("code", "like", "NL")], limit=1
        )
        partner = self.env["res.partner"].create(
            {
                "name": "test partner",
                "street_number": "10",
                "zip": "4811dj",
                "country_id": country_nl.id,
            }
        )
        partner.on_change_zip_street_number()
        partner._convert_to_write(partner._cache)
        self.assertFalse(partner.street_name)
        self.assertFalse(partner.city)
        self.assertFalse(partner.state_id)
