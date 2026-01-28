from typing import List

from common.pipeline import EVisaPipeline
from common.stages.evisa_stage import BaseEVisaStage
from tazania.stages.tanzania_contact_info_stage import TanzaniaContactInfoStage
from tazania.stages.tanzania_declaration_stage import TanzaniaDeclarationStage
from tazania.stages.tanzania_document_info_stage import TanzaniaDocumentsUploadStage
from tazania.stages.tanzania_login_stage import TanzaniaLoginStage
from tazania.stages.tanzania_new_application_stage import TanzaniaNewApplicationStage
from tazania.stages.tanzania_passport_info_stage import TanzaniaPassportInfoStage
from tazania.stages.tanzania_personal_info_stage import TanzaniaPersonalInfoStage
from tazania.stages.tanzania_travel_info_stage import TanzaniaTravelInfoStage
from tazania.util_types import TanzaniaPayloadData, TanzaniaVisaStages


class TanzaniaEVisaPipeline(EVisaPipeline[TanzaniaPayloadData, TanzaniaVisaStages]):
    def _get_stages(self) -> List[BaseEVisaStage[TanzaniaPayloadData, TanzaniaVisaStages]]:
        return [
            TanzaniaLoginStage(),
            TanzaniaNewApplicationStage(),
            TanzaniaPersonalInfoStage(),
            TanzaniaContactInfoStage(),
            TanzaniaPassportInfoStage(),
            TanzaniaTravelInfoStage(),
            TanzaniaDocumentsUploadStage(),
            # TanzaniaDeclarationStage()
        ]
