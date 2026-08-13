-- Phase 10: Business Identity & GST Validation
-- Run this if you have an existing database

ALTER TABLE companies ADD COLUMN mobile_country_code VARCHAR(5) DEFAULT '+91';
ALTER TABLE companies ADD COLUMN mobile_e164 VARCHAR(20);
ALTER TABLE companies ADD COLUMN office_phone_country_code VARCHAR(5);
ALTER TABLE companies ADD COLUMN office_phone_e164 VARCHAR(20);
ALTER TABLE companies ADD COLUMN logo_url VARCHAR(500);

ALTER TABLE company_gst_details ADD COLUMN tan VARCHAR(10);

ALTER TABLE company_bank_accounts RENAME COLUMN account_type TO account_type_old;
ALTER TABLE company_bank_accounts ADD COLUMN account_type VARCHAR(30) DEFAULT 'CURRENT';

ALTER TABLE company_assets ADD COLUMN original_width INTEGER;
ALTER TABLE company_assets ADD COLUMN original_height INTEGER;
ALTER TABLE company_assets ADD COLUMN standardized BOOLEAN DEFAULT 0;

ALTER TABLE parties ADD COLUMN tan VARCHAR(10);
ALTER TABLE parties ADD COLUMN mobile_country_code VARCHAR(5) DEFAULT '+91';
ALTER TABLE parties ADD COLUMN mobile_e164 VARCHAR(20);
ALTER TABLE parties ADD COLUMN office_phone VARCHAR(20);
ALTER TABLE parties ADD COLUMN office_phone_country_code VARCHAR(5);
ALTER TABLE parties ADD COLUMN office_phone_e164 VARCHAR(20);

ALTER TABLE party_bank_accounts ADD COLUMN account_type VARCHAR(30) DEFAULT 'CURRENT';
