from sqlalchemy.orm import Session
from app.models.party import Party, PartyAddress, PartyBankAccount
from app.core.exceptions import NotFoundException, ValidationException
from app.services.audit_service import AuditService
from app.core.gst import GSTService

class PartyService:
    @staticmethod
    def create_party(db: Session, company_id: str, data: dict) -> Party:
        if data.get("gstin"):
            gst_result = GSTService.validate(data["gstin"])
            if not gst_result.valid:
                raise ValidationException("Invalid GSTIN format")
            parsed = GSTService.parse(data["gstin"])
            data["gstin"] = gst_result.gstin
            data["pan"] = parsed.pan
            if not data.get("state_code"):
                data["state_code"] = parsed.state_code
            if not data.get("state"):
                data["state"] = parsed.state

        party = Party(
            company_id=company_id,
            legal_name=data["legal_name"],
            trade_name=data.get("trade_name"),
            party_type=data.get("party_type", "Proprietorship"),
            account_type=data["account_type"],
            contact_person=data.get("contact_person"),
            mobile_country_code=data.get("mobile_country_code"),
            mobile=data.get("mobile"),
            mobile_e164=data.get("mobile_e164"),
            alternate_mobile=data.get("alternate_mobile"),
            office_phone_country_code=data.get("office_phone_country_code"),
            office_phone=data.get("office_phone"),
            office_phone_e164=data.get("office_phone_e164"),
            email=data.get("email"),
            website=data.get("website"),
            gstin=data.get("gstin"),
            gst_registration_type=data.get("gst_registration_type", "Regular"),
            pan=data.get("pan"),
            tan=data.get("tan"),
            state=data.get("state"),
            state_code=data.get("state_code"),
            place_of_supply=data.get("place_of_supply"),
            credit_limit=data.get("credit_limit"),
            credit_days=data.get("credit_days"),
            payment_terms=data.get("payment_terms"),
            notes=data.get("notes"),
        )
        db.add(party)
        db.flush()
        
        for addr_data in data.get("addresses", []):
            addr = PartyAddress(party_id=party.id, **addr_data)
            db.add(addr)
        
        for bank_data in data.get("bank_accounts", []):
            bank = PartyBankAccount(party_id=party.id, **bank_data)
            db.add(bank)
        
        db.commit()
        db.refresh(party)
        AuditService.log(db, company_id, "PARTY", party.id, "CREATED")
        return party
    
    @staticmethod
    def update_party(db: Session, company_id: str, party_id: str, data: dict) -> Party:
        party = db.query(Party).filter(Party.id == party_id, Party.company_id == company_id).first()
        if not party:
            raise NotFoundException("Party not found")
        
        if data.get("gstin") and data.get("gstin") != party.gstin:
            gst_result = GSTService.validate(data["gstin"])
            if not gst_result.valid:
                raise ValidationException("Invalid GSTIN format")
            parsed = GSTService.parse(data["gstin"])
            data["gstin"] = gst_result.gstin
            if not data.get("pan"):
                data["pan"] = parsed.pan
            if not data.get("state_code"):
                data["state_code"] = parsed.state_code
            if not data.get("state"):
                data["state"] = parsed.state

        for field in ["legal_name", "trade_name", "party_type", "account_type", "contact_person",
                      "mobile_country_code", "mobile", "mobile_e164", "alternate_mobile",
                      "office_phone_country_code", "office_phone", "office_phone_e164",
                      "email", "website", "gstin", "gst_registration_type", "pan", "tan", "state", 
                      "state_code", "place_of_supply", "credit_limit", "credit_days", 
                      "payment_terms", "notes", "status"]:
            if field in data:
                setattr(party, field, data[field])
        
        db.commit()
        db.refresh(party)
        AuditService.log(db, company_id, "PARTY", party.id, "UPDATED")
        return party
    
    @staticmethod
    def list_parties(db: Session, company_id: str, account_type: str = None, search: str = None):
        query = db.query(Party).filter(Party.company_id == company_id)
        if account_type:
            query = query.filter(Party.account_type.in_([account_type, "BOTH"]))
        if search:
            query = query.filter(
                Party.legal_name.ilike(f"%{search}%") | 
                Party.gstin.ilike(f"%{search}%")
            )
        return query.order_by(Party.legal_name).all()
    
    @staticmethod
    def get_party(db: Session, company_id: str, party_id: str):
        party = db.query(Party).filter(Party.id == party_id, Party.company_id == company_id).first()
        if not party:
            raise NotFoundException("Party not found")
        return party
