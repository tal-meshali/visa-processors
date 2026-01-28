from typing import List

from processing.common.variable import Variable, DateVariable, MimicVariable
from processing.srilanka.stages.abstract.srilanka_template_stage import SriLankaTemplateStage
from processing.srilanka.util_types import SriLankaVisaTemplates, SriLankaPayloadData


class SriLankaContactStage(SriLankaTemplateStage):
    template = SriLankaVisaTemplates.Contact

    def get_variables(self, data: SriLankaPayloadData) -> List[Variable]:
        return [
            DateVariable(["arrivalDate"], data.travel.date_of_arrival, format_str="%m-%d-%Y"),
            Variable(["conAddOne"], data.contact.address),
            Variable(["RequestedVisaDays"], data.request.amount_of_days),
            Variable(["contCity"], data.contact.city),
            Variable(["contPhoneNo"], data.contact.phone_number),
            MimicVariable(["reEnterEmail"], Variable(["contEmail"], data.contact.email_address)),
        ]
