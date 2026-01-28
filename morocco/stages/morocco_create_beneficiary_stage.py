from processing.common.variable import ISODateVariable
from processing.morocco.stages.abstract.morocco_template_stage import MoroccoTemplateStage
from processing.morocco.util_types import MoroccoVisaTemplates, MoroccoPayloadData, MoroccoVisaStages


class MoroccoCreateBeneficiaryStage(MoroccoTemplateStage):
    stage = MoroccoVisaStages.InitiateBeneficiary
    template = MoroccoVisaTemplates.Initial

    def get_variables(self, data: MoroccoPayloadData):
        return [ISODateVariable(["dateNaissance"], data.passport.date_of_birth)]
