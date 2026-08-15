from sqlalchemy.orm import Session
from app.models.company import Company, CompanyGSTDetail, CompanyAddress, CompanyBankAccount, CompanyAuth
from app.schemas.auth import CompanySetupRequest
from app.core.security import hash_pin, generate_id
from app.core.exceptions import ValidationException, ConflictException
from app.core.gst import GSTService

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
            mobile_country_code=data.mobile_country_code,
            mobile_e164=data.mobile_e164,
            office_phone=data.office_phone,
            office_phone_country_code=data.office_phone_country_code,
            office_phone_e164=data.office_phone_e164,
            email=data.email,
            website=data.website,
            authorized_person_name=data.authorized_person_name,
            authorized_person_designation=data.authorized_person_designation,
        )
        db.add(company)
        db.flush()
        
        # GST details
        gst_detail = None
        if data.gst_registered and data.gstin:
            gst_validation = GSTService.validate(data.gstin)
            if not gst_validation.valid:
                raise ValidationException("Invalid GSTIN. Please check the 15-character GST number.")
            
            parsed = GSTService.parse(data.gstin)
            
            gst_detail = CompanyGSTDetail(
                company_id=company.id,
                gstin=gst_validation.gstin,
                state_code=parsed.state_code,
                state_name=parsed.state,
                pan=parsed.pan,
                tan=data.tan,
                registration_number=parsed.entity_number,
                gstin_character_14=parsed.default_character,
                checksum=parsed.check_digit,
                gstin_validation_status="VALID",
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
        
        # Bank account — optional, only create if details provided
        if data.bank_account_number and data.bank_ifsc and data.bank_account_holder_name:
            bank = CompanyBankAccount(
                company_id=company.id,
                account_holder_name=data.bank_account_holder_name,
                account_number=data.bank_account_number,
                ifsc=data.bank_ifsc.upper(),
                bank_name=data.bank_name,
                branch=data.bank_branch or "",
                account_type=data.bank_account_type or "CURRENT",
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

    @staticmethod
    def update_company(db: Session, company_id: str, data: dict) -> Company:
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise ValidationException("Company not found")
        
        for key, value in data.items():
            if hasattr(company, key) and value is not None:
                setattr(company, key, value)
                
        db.commit()
        db.refresh(company)
        return company
    
    @staticmethod
    def update_company_logo(db: Session, company_id: str, logo_metadata: dict) -> Company:
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise ValidationException("Company not found")
        
        if not logo_metadata:
            company.logo_asset_id = None
            company.logo_url = None
            db.commit()
            return company

        from app.models.company import CompanyAsset
        # Store in CompanyAsset
        asset = CompanyAsset(
            company_id=company_id,
            asset_type="COMPANY_LOGO",
            file_path=logo_metadata["file_path"],
            mime_type=logo_metadata["mime_type"],
            file_size=logo_metadata["file_size"],
            width=logo_metadata.get("standardized_width"),
            height=logo_metadata.get("standardized_height"),
            original_width=logo_metadata.get("original_width"),
            original_height=logo_metadata.get("original_height"),
            standardized=True
        )
        db.add(asset)
        db.flush()
        
        # Update logo reference on company
        from app.services.file_storage_service import FileStorageService
        company.logo_asset_id = asset.id
        company.logo_url = FileStorageService.get_logo_serve_url(company_id)
        db.commit()
        db.refresh(company)
        return company
        
    @staticmethod
    def change_pin(db: Session, company_id: str, old_pin: str, new_pin: str):
        from app.core.security import verify_pin, hash_pin
        auth = db.query(CompanyAuth).filter(CompanyAuth.company_id == company_id).first()
        if not auth or not verify_pin(old_pin, auth.pin_hash):
            raise ValidationException("Incorrect current PIN")
        
        auth.pin_hash = hash_pin(new_pin)
        db.commit()
