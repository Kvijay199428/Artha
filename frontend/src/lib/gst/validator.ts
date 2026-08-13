import { GST_STATE_CODES } from './stateCodes';

const GSTIN_REGEX = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/;


export interface GSTINValidation {
  valid: boolean;
  validLength: boolean;
  validStructure: boolean;
  validStateCode: boolean;
  validChecksum: boolean;
  errors: string[];
  normalized: string;
}

export interface GSTINParseResult {
  gstin: string;
  stateCode: string;
  stateName: string | null;
  isUnionTerritory: boolean;
  pan: string;
  panHolderType: string;
  entityNumber: string;
  defaultCharacter: string;
  checkDigit: string;
}

function computeChecksum(gstin: string): string {
  const body = gstin.slice(0, 14);
  const vals = body.split('').map((c) =>
    c >= '0' && c <= '9' ? parseInt(c) : c.charCodeAt(0) - 55
  );
  const weighted = vals.map((v, i) => v * ((i % 2) + 1));
  const reduced = weighted.map((x) => Math.floor(x / 36) + (x % 36));
  const sum = reduced.reduce((a, b) => a + b, 0);
  const csum = 36 - (sum % 36);
  if (csum >= 36) return '0';
  return csum < 10 ? String(csum) : String.fromCharCode(csum + 55);
}

export function validateGSTIN(raw: string): GSTINValidation {
  const normalized = raw.toUpperCase().replace(/\s+/g, '');
  const errors: string[] = [];
  let validLength = false;
  let validStructure = false;
  let validStateCode = false;
  let validChecksum = false;

  if (normalized.length !== 15) {
    errors.push(`GSTIN must be exactly 15 characters (currently ${normalized.length})`);
  } else {
    validLength = true;
  }

  if (validLength) {
    if (!GSTIN_REGEX.test(normalized)) {
      errors.push('GSTIN format is invalid. Expected: SSAAAAANNNNAS(Z)D');
    } else {
      validStructure = true;
    }
  }

  if (validLength) {
    const stateCode = normalized.slice(0, 2);
    if (!GST_STATE_CODES[stateCode]) {
      errors.push(`Invalid state code: ${stateCode}`);
    } else {
      validStateCode = true;
    }
  }

  if (validLength) {
    const expected = computeChecksum(normalized);
    if (normalized[14] !== expected) {
      errors.push(`Invalid checksum digit. Expected: ${expected}`);
    } else {
      validChecksum = true;
    }
  }

  const valid = validLength && validStructure && validStateCode && validChecksum;

  return { valid, validLength, validStructure, validStateCode, validChecksum, errors, normalized };
}

export function parseGSTIN(raw: string): GSTINParseResult | null {
  const validation = validateGSTIN(raw);
  if (!validation.validLength) return null;
  const gstin = validation.normalized;
  const stateCode = gstin.slice(0, 2);
  const state = GST_STATE_CODES[stateCode] ?? null;
  return {
    gstin,
    stateCode,
    stateName: state?.name ?? null,
    isUnionTerritory: state?.isUnionTerritory ?? false,
    pan: gstin.slice(2, 12),
    panHolderType: gstin[11],
    entityNumber: gstin[12],
    defaultCharacter: gstin[13],
    checkDigit: gstin[14],
  };
}
