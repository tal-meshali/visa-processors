from typing import List

from common.pipeline import EVisaPipeline
from common.stages.evisa_stage import BaseEVisaStage
from morocco.stages.morocco_create_beneficiary_stage import MoroccoCreateBeneficiaryStage
from morocco.stages.morocco_insert_beneficiary_data_stage import MoroccoInsertBeneficiaryDataStage
from morocco.stages.morocco_login_stage import MoroccoLoginStage
from morocco.stages.morocco_submit_documents_stage import MoroccoSubmitDocumentStage
from morocco.stages.morocco_upload_passport_stage import MoroccoUploadPassportStage
from morocco.stages.morocco_upload_portrait_stage import MoroccoUploadPortraitStage
from morocco.util_types import MoroccoPayloadData, MoroccoVisaStages


class MoroccoEVisaPipeline(EVisaPipeline[MoroccoPayloadData, MoroccoVisaStages]):
    def _get_stages(self) -> List[BaseEVisaStage[MoroccoPayloadData, MoroccoVisaStages]]:
        return [
            MoroccoLoginStage(),
            MoroccoCreateBeneficiaryStage(),
            MoroccoInsertBeneficiaryDataStage(),
            MoroccoUploadPortraitStage(),
            MoroccoUploadPassportStage(),
            MoroccoSubmitDocumentStage()
        ]