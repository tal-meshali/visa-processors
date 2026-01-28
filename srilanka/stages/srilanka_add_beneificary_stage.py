from typing import List

from processing.common.util_methods import get_country_id
from processing.common.variable import Variable, MimicVariable, DateVariable
from processing.srilanka.stages.abstract.srilanka_template_stage import SriLankaTemplateStage
from processing.srilanka.util_types import SriLankaPayloadData, SriLankaVisaTemplates


class SriLankaAddBeneficiaryStage(SriLankaTemplateStage):

    def __init__(self, beneficiary_index: int):
        self.index = beneficiary_index

    template = SriLankaVisaTemplates.Create

    def get_variables(self, data: SriLankaPayloadData) -> List[Variable]:
        is_male = data.passport.sex == "M"
        return [
            Variable(['hiddenMgenderString'], "Male" if is_male else "Female"),
            Variable(['hiddenGender'], data.passport.sex),  # 01 = Mr. 04 = Ms.
            Variable(['hiddenTitle'], "01" if is_male else "04"),  # 01 = Mr. 04 = Ms.
            Variable(['hiddenOtherNames'], data.passport.first_name),
            Variable(['hiddenSurname'], data.passport.last_name),
            MimicVariable(["hiddenReEnteredPassportNo"], Variable(["hiddenPassportNo"], data.passport.passport_number)),
            MimicVariable(["hiddenReEnteredDobDate"],
                          DateVariable(["hiddenDobDate"], data.passport.date_of_birth, format_str="%m-%d-%Y")),
            DateVariable(["hiddenPassIssueDate"], data.passport.date_of_issue, format_str="%m-%d-%Y"),
            DateVariable(["hiddenPassExDate"], data.passport.date_of_expiry, format_str="%m-%d-%Y"),
            Variable(["otherDecQuesAns"], [f"{data.passport.passport_number}|QN{idx}|0" for idx in range(1, 4)]),
            Variable(['hiddenCob'], get_country_id(data.passport.place_of_birth)),
            Variable(["hiddenMemberNo"], self.index)
        ]
