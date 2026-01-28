from typing import List

from common.variable import Variable, MimicVariable
from tazania.stages.abstract.tanzania_template_stage import TanzaniaTemplateStage
from tazania.util_types import TanzaniaVisaStages, TanzaniaPayloadData, TanzaniaVisaTemplates
from tazania.variables import TanzaniaOptionsVariable, TanzaniaDateVariable


class TanzaniaTravelInfoStage(TanzaniaTemplateStage):
    stage = TanzaniaVisaStages.TravelInfo
    template = TanzaniaVisaTemplates.TravelInfo

    def get_variables(self, data: TanzaniaPayloadData) -> List[Variable]:
        is_first_visit = data.travel.date_of_last_visit is None
        variables = [
            MimicVariable(["EmbassyID"],
                          TanzaniaOptionsVariable(['ApplyingCountryID'], data.passport.issuing_country, self.document)),
            Variable(['isFirstVisit'], is_first_visit),
            TanzaniaDateVariable(["Arrival"], data.travel.date_of_arrival),
            TanzaniaOptionsVariable(['DestinationID'], data.travel.destination, self.document),
            Variable(['StayDuration'], (data.travel.date_of_departure - data.travel.date_of_arrival).days),
            Variable(['ApplicantStayAddress'], data.travel.stay_address)
        ]

        if not is_first_visit:
            variables.append(TanzaniaDateVariable(["LastVisit"], data.travel.date_of_last_visit))
        return variables
