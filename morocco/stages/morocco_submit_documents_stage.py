from typing import Dict

from morocco.stages.abstract.morocco_evisa_stage import BaseMoroccoEVisaStage
from morocco.util_types import MoroccoVisaStages, MoroccoPayloadData


class MoroccoSubmitDocumentStage(BaseMoroccoEVisaStage):
    stage = MoroccoVisaStages.SubmitDocuments
    method = 'put'

    def process_data(self, data: MoroccoPayloadData) -> Dict:
        return {"attachableId": data.request.beneficiary_id}
