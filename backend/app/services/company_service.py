from sqlalchemy.orm import Session
from app.models.company import Company, CompanyGSTDetail, CompanyAddress, CompanyBankAccount, CompanyAuth
from app.schemas.auth import CompanySetupRequest
from app.core.security import hash_pin, generate_id
from app.core.exceptions import ValidationException, ConflictException
from app.utils.gstin import validate_gstin

class CompanyService:
    @staticmethod
    def create_company(db: Session, data: CompanySetupRequest) -> Company:
        if data.pin != data.confirm_pin:
            raise ValidationException("PIN and confirmation PIN do not match")
        
        # Check existing
        existing = db.query(Company).first()
        if existing:
            raise ConflictException("A company account already exists. Please log in.")
        
        company = Company(
            company_name=data.company_name,
            legal_name=data.company_name,
            ownership_type=data.ownership_type,
            status="ACTIVE",
            mobile=data.mobile,
            office_phone=data.office_phone,
            email=data.email,
            authorized_person_name=data.authorized_person_name,
            authorized_person_designation=data.authorized_person_designation,
        )
        db.add(company)
        db.flush()
        
        # GST details
        gst_detail = None
        if data.gst_registered and data.gstin:
            gst_validation = validate_gstin(data.gstin)
            if not gst_validation["valid"]:
                raise ValidationException("Invalid GSTIN. Please check the 15-character GST number.")
            
            gst_detail = CompanyGSTDetail(
                company_id=company.id,
                gstin=gst_validation["normalized"],
                state_code=gst_validation["state_code"],
                pan=gst_validation["pan"],
                registration_number=gst_validation["registration_number"],
                gstin_character_14=gst_validation["default_code"],
                checksum=gst_validation["checksum"],
                gstin_validation_status="VALID" if gst_validation["valid"] else "INVALID",
            )
            db.add(gst_detail)
        
        # Address
        address = CompanyAddress(
            company_id=company.id,
            address_type="REGISTERED",
            address_line_1=data.address_line_1,
            address_line_2=data.address_line_2,
            city=data.city,
            district=data.district,
            state=data.state,
            state_code=data.state_code,
            pincode=data.pincode,
            country=data.country,
            is_default=True,
        )
        db.add(address)
        
        # Bank account
        bank = CompanyBankAccount(
            company_id=company.id,
            account_holder_name=data.bank_account_holder_name,
            account_number=data.bank_account_number,
            ifsc=data.bank_ifsc.upper(),
            bank_name=data.bank_name,
            branch=data.bank_branch,
            account_type=data.bank_account_type,
            is_primary=True,
        )
        db.add(bank)
        
        # Auth
        auth = CompanyAuth(
            company_id=company.id,
            pin_hash=hash_pin(data.pin),
            failed_attempts=0,
        )
        db.add(auth)
        
        db.commit()
        db.refresh(company)
        return company
    
    @staticmethod
    def get_company(db: Session, company_id: str) -> Company:
        return db.query(Company).filter(Company.id == company_id).first()
    
    @staticmethod
    def get_company_detail(db: Session, company_id: str):
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            return None
        return company
