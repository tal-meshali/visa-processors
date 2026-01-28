from typing import Dict

from processing.morocco.stages.abstract.morocco_evisa_stage import BaseMoroccoEVisaStage
from processing.morocco.util_types import MoroccoVisaStages, MoroccoPayloadData


class MoroccoSubmitDocumentStage(BaseMoroccoEVisaStage):
    stage = MoroccoVisaStages.SubmitDocuments
    method = 'put'

    def process_data(self, data: MoroccoPayloadData) -> Dict:
        return {"attachableId": data.request.beneficiary_id}
