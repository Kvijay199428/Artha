-- Phase 11: Schema additions
-- SQLite-compatible ALTER TABLE statements
-- Run ONCE on existing databases to add new columns added in Phase 10-11
-- Fresh installs: create_all() handles this automatically

-- Company: new contact/logo fields
ALTER TABLE companies ADD COLUMN mobile_country_code VARCHAR(5) DEFAULT '+91';
ALTER TABLE companies ADD COLUMN mobile_e164 VARCHAR(25);
ALTER TABLE companies ADD COLUMN office_phone_country_code VARCHAR(5);
ALTER TABLE companies ADD COLUMN office_phone_e164 VARCHAR(25);
ALTER TABLE companies ADD COLUMN website VARCHAR(300);
ALTER TABLE companies ADD COLUMN logo_url VARCHAR(500);
ALTER TABLE companies ADD COLUMN logo_asset_id VARCHAR(36);

-- Company GST: TAN field
ALTER TABLE company_gst_details ADD COLUMN tan VARCHAR(10);

-- Parties: new contact fields
ALTER TABLE parties ADD COLUMN tan VARCHAR(10);
ALTER TABLE parties ADD COLUMN mobile_country_code VARCHAR(5) DEFAULT '+91';
ALTER TABLE parties ADD COLUMN mobile_e164 VARCHAR(25);
ALTER TABLE parties ADD COLUMN office_phone VARCHAR(20);
ALTER TABLE parties ADD COLUMN office_phone_country_code VARCHAR(5);
ALTER TABLE parties ADD COLUMN office_phone_e164 VARCHAR(25);

-- Party bank accounts: account type
ALTER TABLE party_bank_accounts ADD COLUMN account_type VARCHAR(30) DEFAULT 'CURRENT';

-- Company assets: standardization metadata
ALTER TABLE company_assets ADD COLUMN original_width INTEGER;
ALTER TABLE company_assets ADD COLUMN original_height INTEGER;
ALTER TABLE company_assets ADD COLUMN standardized BOOLEAN DEFAULT 0;
