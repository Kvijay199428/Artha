import { apiClient } from './client';

export interface QuotationLineCreate {
  item_id?: string;
  item_name_snapshot: string;
  description?: string;
  hsn_sac_snapshot?: string;
  sku_snapshot?: string;
  quantity: number;
  unit_id?: string;
  unit_snapshot?: string;
  rate: number;
  discount_type?: string;
  discount_value?: number;
  gst_rate?: number;
}

export interface QuotationCreateRequest {
  quotation_type: string;
  tax_treatment: string;
  party_id: string;
  valid_until: string;
  place_of_supply: string;
  notes?: string;
  terms?: string;
  lines: QuotationLineCreate[];
}

export interface QuotationLineResponse {
  id: string;
  item_id: string | null;
  item_name_snapshot: string;
  description: string | null;
  hsn_sac_snapshot: string | null;
  sku_snapshot: string | null;
  quantity: number;
  converted_quantity: number;
  unit_id: string | null;
  unit_snapshot: string | null;
  rate: number;
  discount_type: string | null;
  discount_value: number;
  discount_amount: number;
  tax_treatment: string;
  gst_rate: number;
  taxable_value: number;
  cgst_amount: number;
  sgst_amount: number;
  igst_amount: number;
  cess_amount: number;
  line_total: number;
}

export interface QuotationResponse {
  id: string;
  quotation_number: string | null;
  quotation_type: string;
  tax_treatment: string;
  party_id: string;
  quotation_date: string;
  valid_until: string;
  status: string;
  revision: number;
  place_of_supply: string;
  subtotal: number;
  discount_total: number;
  taxable_total: number;
  cgst_total: number;
  sgst_total: number;
  igst_total: number;
  cess_total: number;
  round_off: number;
  grand_total: number;
  notes: string | null;
  terms: string | null;
  accepted_at: string | null;
  accepted_by: string | null;
  acceptance_method: string | null;
  fully_converted: boolean;
  created_at: string;
  lines: QuotationLineResponse[];
}

export const quotationsApi = {
  create: async (data: QuotationCreateRequest) => {
    const response = await apiClient.post<QuotationResponse>('/quotations', data);
    return response.data;
  },
  getAll: async (quotationType?: string) => {
    const params = new URLSearchParams();
    if (quotationType) params.append('quotation_type', quotationType);
    const response = await apiClient.get<{items: QuotationResponse[], total: number}>(`/quotations?${params.toString()}`);
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<QuotationResponse>(`/quotations/${id}`);
    return response.data;
  },
  approve: async (id: string) => {
    const response = await apiClient.post<QuotationResponse>(`/quotations/${id}/approve`, {});
    return response.data;
  },
  accept: async (id: string, acceptanceMethod: string = "USER_ACCEPTED") => {
    const response = await apiClient.post<QuotationResponse>(`/quotations/${id}/accept`, {
      acceptance_method: acceptanceMethod
    });
    return response.data;
  }
};
