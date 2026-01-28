from abc import ABC

from common.util_methods import solve_captcha
from tazania.stages.abstract.base_tanzania_stage import BaseTanzaniaEVisaStage


class BaseTanzaniaReCaptchaStage(BaseTanzaniaEVisaStage, ABC):
    def extract_auth_fields_from_document(self):
        extracted_fields = super().extract_auth_fields_from_document()
        recaptcha_site_key = self.document.find("div", {"class": "g-recaptcha"}).get(
            "data-sitekey"
        )
        extracted_fields["g-recaptcha-response"] = solve_captcha(
            recaptcha_site_key, self.stage.value
        )
        return extracted_fields
