from typing import List, Dict

from common.pipeline import EVisaPipeline
from common.stages.evisa_stage import BaseEVisaStage
from morocco.extract_visa_request_id import VisaRequestIdExtractor
from morocco.morocco_translator import MoroccoTranslator
from morocco.stages.morocco_create_beneficiary_stage import MoroccoCreateBeneficiaryStage
from morocco.stages.morocco_insert_beneficiary_data_stage import MoroccoInsertBeneficiaryDataStage
from morocco.stages.morocco_login_stage import MoroccoLoginStage
from morocco.stages.morocco_submit_documents_stage import MoroccoSubmitDocumentStage
from morocco.stages.morocco_upload_passport_stage import MoroccoUploadPassportStage
from morocco.stages.morocco_upload_portrait_stage import MoroccoUploadPortraitStage
from morocco.util_types import MoroccoPayloadData, MoroccoVisaStages


class MoroccoEVisaPipeline(EVisaPipeline[MoroccoPayloadData, MoroccoVisaStages]):
    def __init__(self):
        self.visa_request_id_manager = VisaRequestIdExtractor()
        self.request_id = self.visa_request_id_manager.get_and_remove_request_id()
        super().__init__(MoroccoTranslator(self.request_id))

    def _get_stages(self) -> List[BaseEVisaStage[MoroccoPayloadData, MoroccoVisaStages]]:
        return [
            MoroccoLoginStage(),
            MoroccoCreateBeneficiaryStage(),
            MoroccoInsertBeneficiaryDataStage(),
            MoroccoUploadPortraitStage(),
            MoroccoUploadPassportStage(),
            MoroccoSubmitDocumentStage()
        ]

    def run(self, form_data: Dict) -> MoroccoPayloadData:
        data = super().run(form_data)
        self.translator.creation_request_id = data.request.request_id
        return data
