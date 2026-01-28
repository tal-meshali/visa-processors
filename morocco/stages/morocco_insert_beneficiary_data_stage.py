from requests import Session, Response, get

from processing.common.variable import *
from processing.morocco.stages.abstract.morocco_template_stage import MoroccoTemplateStage
from processing.morocco.util_types import MoroccoVisaTemplates, MoroccoPayloadData, MoroccoVisaStages


class MoroccoInsertBeneficiaryDataStage(MoroccoTemplateStage):
    stage = MoroccoVisaStages.UpdateBeneficiary
    template = MoroccoVisaTemplates.Insert
    method = 'put'

    def get_profession(self, data: MoroccoPayloadData):
        underage = (datetime.today() - data.passport.date_of_birth).days / 365 < 18
        return {
            "id": 123 if underage else 55,
            "code": "PR31" if underage else "PR14",
            "libelle": "WITHOUT" if underage else "EMPLOYEE",
            "lang": "en",
            "statut": "Active",
            "active": True,
        }

    def get_variables(self, data: MoroccoPayloadData):
        return [
            Variable(["refInfoBeneficiairesVisa", "refProfession"],
                     data.employment.occupation or self.get_profession(data)),
            Variable(["refInfoBeneficiairesVisa", "lieuNaissance"], data.passport.place_of_birth),
            Variable(["refInfoBeneficiairesVisa", "prenom"], data.passport.first_name),
            Variable(["refInfoBeneficiairesVisa", "nom"], data.passport.last_name),
            Variable(["refInfoPasseport", "numPasseport"], data.passport.passport_number),
            ISODateVariable(["refInfoBeneficiairesVisa", "dateNaissance"], data.passport.date_of_birth),
            DateVariable(["dateNaissance"], data.passport.date_of_birth),
            ISODateVariable(["refInfoPasseport", "dateDelivrance"], data.passport.date_of_issue),
            DateVariable(["dateDelivrPass"], data.passport.date_of_issue),
            ISODateVariable(["refInfoPasseport", "dateExpiration"], data.passport.date_of_expiry),
            DateVariable(["dateExpirPass"], data.passport.date_of_expiry),
            ISODateVariable(["dateArrivee"], data.travel.date_of_arrival),
            DateVariable(["dateArrivePrevue"], data.travel.date_of_arrival),
            ISODateVariable(["dateSortie"], data.travel.date_of_departure),
            DateVariable(["dateSortiePrevue"], data.travel.date_of_departure)
        ]

    def process_data(self, data: MoroccoPayloadData) -> Dict:
        beneficiary_data = super().process_template(data)
        request_data = get(MoroccoVisaStages.GetRequest.value,
                           headers={"Authorization": data.request.token, 'User-Agent': self.USER_AGENT}).json()
        request_data["refsDemandeVisa"].append(beneficiary_data)
        return request_data

    def process_response(self, session: Session, data: MoroccoPayloadData, response: Response):
        response_content = response.json()
        data.request.request_id = response_content["numDossier"]
        print(f"Updated request id: {data.request.request_id}")
        data.request.beneficiary_id = response_content["refsDemandeVisa"][-1]['id']
