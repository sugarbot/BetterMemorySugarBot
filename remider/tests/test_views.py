from django.test import TestCase, override_settings
from django.shortcuts import reverse

from ..forms import GetSecretForm, TriggerTimeForm, ChangeEnvVariableForm, ChooseLanguageForm


class HomeViewTests(TestCase):
    def test_template_loading(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "remider/home.html")
        self.assertEqual(response.status_code, 200)


class AuthViewTests(TestCase):
    def test_template_loading(self):
        response = self.client.get(reverse("get_secret"))
        self.assertTemplateUsed(response, "remider/auth.html")
        self.assertEqual(response.status_code, 200)

    def test_displays_proper_form(self):
        response = self.client.get(reverse("get_secret"))
        self.assertIsInstance(response.context['form'], GetSecretForm)
        self.assertContains(response, 'type="password"')
        self.assertContains(response, 'type="submit"')


class MenuViewTests(TestCase):
    @override_settings(SECRET_KEY="mycoolsecretkey")
    def test_template_loading(self):
        response = self.client.get(reverse("menu") + "?key=mycoolsecretkey")
        self.assertTemplateUsed(response, "remider/menu.html")
        self.assertEqual(response.status_code, 200)

    @override_settings(SECRET_KEY="mycoolsecretkey")
    def test_template_contex(self):
        response = self.client.get(reverse("menu") + "?key=mycoolsecretkey")
        self.assertEqual(response.context["SECRET_KEY"], "mycoolsecretkey")
        self.assertEqual(response.context["info"], False)
        self.assertEqual(response.context["info2"], False)
        response = self.client.get(reverse("menu") + "?key=mycoolsecretkey&info=1")
        self.assertEqual(response.context["info"], True)

    @override_settings(SECRET_KEY="mycoolsecretkey", NIGTSCOUT_LINK="https://test.com", SENSOR_ALERT_FREQUENCY=1,
                       INFUSION_SET_ALERT_FREQUENCY=2, ATRIGGER_KEY="akey", ATRIGGER_SECRET="asecret",
                       TWILIO_ACCOUNT_SID="tsid", TWILIO_AUTH_TOKEN="ttoken")
    def test_proper_forms(self):
        response = self.client.get(reverse("menu") + "?key=mycoolsecretkey")
        self.assertIsInstance(response.context["language_form"], ChooseLanguageForm)
        self.assertIsInstance(response.context["time_form"], TriggerTimeForm)
        forms = (
            ("NIGHTSCOUT_LINK", "ns_link_button", "https://test.com"),
            ("INFUSION_SET_ALERT_FREQUENCY", "infusion_freq_button", 2),
            ("SENSOR_ALERT_FREQUENCY", "sensor_freq_button", 1),
            ("ATRIGGER_KEY", "atrigger_key_button", "akey"),
            ("ATRIGGER_SECRET", "atrigger_secret_button", "asecret"),
            ("TWILIO_ACCOUNT_SID", "twilio_sid_button", "tsid"),
            ("TWILIO_AUTH_TOKEN", "twilio_token_button", "ttoken"),
        )
        for indx, form in enumerate(response.context["forms_list"]):
            self.assertIsInstance(form, ChangeEnvVariableForm)
            self.assertEqual(form.button_name, forms[indx][1])
            self.assertEqual(form.fields['new_value'].label, forms[indx][0])
            self.assertEqual(form.fields['new_value'].initial, forms[indx][2])
