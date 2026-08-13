import { apiClient } from './client';

export interface GSTINValidationResponse {
  gstin: string;
  valid: boolean;
  validLength: boolean;
  validStructure: boolean;
  validStateCode: boolean;
  validChecksum: boolean;
  errors: string[];
  level: string;
  parsed?: {
    stateCode: string;
    stateName: string | null;
    pan: string;
    entityNumber: string;
    defaultCharacter: string;
    checkDigit: string;
  };
}

export interface GSTState {
  code: string;
  name: string;
  isUnionTerritory: boolean;
}

export const gstApi = {
  validate: async (gstin: string): Promise<GSTINValidationResponse> => {
    const response = await apiClient.get<{ data: GSTINValidationResponse }>(`/gst/validate/${encodeURIComponent(gstin)}`);
    return (response.data as any).data;
  },
  getStates: async (): Promise<GSTState[]> => {
    const response = await apiClient.get<{ data: GSTState[] }>('/gst/states');
    return (response.data as any).data;
  },
};
