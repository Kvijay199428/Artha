import { apiClient } from './client';

export interface Address {
  id?: string;
  address_type: string;
  address_line_1: string;
  address_line_2?: string;
  city: string;
  state: string;
  state_code: string;
  pincode: string;
  is_default: boolean;
}

export interface Party {
  id: string;
  party_code?: string;
  legal_name: string;
  trade_name?: string | null;
  party_type: string;
  account_type: string;
  contact_person?: string | null;
  mobile?: string | null;
  email?: string | null;
  gstin?: string | null;
  gst_registration_type?: string | null;
  pan?: string | null;
  state: string;
  state_code: string;
  place_of_supply?: string | null;
  status: string;
  addresses: Address[];
}

export interface PartyCreateRequest {
  legal_name: string;
  trade_name?: string;
  party_type: string;
  account_type: string;
  contact_person?: string;
  mobile?: string;
  email?: string;
  gstin?: string;
  gst_registration_type?: string;
  pan?: string;
  state: string;
  state_code: string;
  place_of_supply?: string;
  addresses?: Address[];
}

export const partiesApi = {
  getAll: async (account_type?: string, search?: string) => {
    const params = new URLSearchParams();
    if (account_type) params.append('account_type', account_type);
    if (search) params.append('search', search);
    const response = await apiClient.get<{items: Party[]}>(`/parties?${params.toString()}`);
    return response.data.items;
  },
  create: async (data: PartyCreateRequest) => {
    const response = await apiClient.post<Party>('/parties', data);
    return response.data;
  },
  update: async (id: string, data: Partial<PartyCreateRequest>) => {
    const response = await apiClient.put<Party>(`/parties/${id}`, data);
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<Party>(`/parties/${id}`);
    return response.data;
  }
};
