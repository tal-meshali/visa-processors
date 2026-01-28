import re
from typing import Dict

from requests import Session, Response

from processing.morocco.stages.abstract.morocco_evisa_stage import BaseMoroccoEVisaStage
from processing.morocco.util_types import MoroccoVisaStages, MoroccoPayloadData

TOKEN_RE = re.compile(r"access_token=([\.\-\w]+)")


class MoroccoLoginStage(BaseMoroccoEVisaStage):
    stage = MoroccoVisaStages.Login

    def process_data(self, data: MoroccoPayloadData) -> Dict:
        return {"dossier": data.request.request_id, "email": data.contact.email_address}

    def handle(self, session: Session, data: MoroccoPayloadData):
        session.headers.update({
            'User-Agent': self.USER_AGENT
        })
        super().handle(session, data)

    def process_response(self, session: Session, data: MoroccoPayloadData, response: Response):
        token = "Bearer " + re.findall(r"access_token=([\.\-\w]+)", response.text)[0]
        data.request.token = token
        session.headers["Authorization"] = token
