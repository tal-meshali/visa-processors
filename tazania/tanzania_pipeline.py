from typing import List

from processing.common.pipeline import EVisaPipeline
from processing.common.stages.evisa_stage import BaseEVisaStage
from processing.tazania.stages.tanzania_contact_info_stage import TanzaniaContactInfoStage
from processing.tazania.stages.tanzania_declaration_stage import TanzaniaDeclarationStage
from processing.tazania.stages.tanzania_document_info_stage import TanzaniaDocumentsUploadStage
from processing.tazania.stages.tanzania_login_stage import TanzaniaLoginStage
from processing.tazania.stages.tanzania_new_application_stage import TanzaniaNewApplicationStage
from processing.tazania.stages.tanzania_passport_info_stage import TanzaniaPassportInfoStage
from processing.tazania.stages.tanzania_personal_info_stage import TanzaniaPersonalInfoStage
from processing.tazania.stages.tanzania_travel_info_stage import TanzaniaTravelInfoStage
from processing.tazania.util_types import TanzaniaPayloadData, TanzaniaVisaStages


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
