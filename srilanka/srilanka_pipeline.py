from typing import List

from processing.common.pipeline import EVisaPipeline
from processing.common.stages.evisa_stage import BaseEVisaStage
from processing.common.util_types import TPayloadData, TStage
from processing.srilanka.stages.srilanka_add_beneificary_stage import SriLankaAddBeneficiaryStage
from processing.srilanka.stages.srilanka_confirm_stage import SriLankaConfirmStage
from processing.srilanka.stages.srilanka_contact_stage import SriLankaContactStage
from processing.srilanka.stages.srilanka_terms_stage import SriLankaTermsStage
from processing.srilanka.util_types import SriLankaPayloadData, SriLankaVisaStages


# TODO: Use https://client-services.easysend.app to get city and address options
class SriLankaEVisaPipeline(EVisaPipeline[SriLankaPayloadData, SriLankaVisaStages]):
    def _get_stages(self) -> List[BaseEVisaStage[TPayloadData, TStage]]:
        return [
            # SriLankaInitialStage(),
            SriLankaTermsStage(),
            SriLankaContactStage(),
            SriLankaAddBeneficiaryStage(1),
            SriLankaConfirmStage()
        ]
