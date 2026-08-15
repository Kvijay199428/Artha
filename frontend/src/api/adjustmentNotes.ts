import { apiClient } from './client';

export interface AdjustmentNoteLineCreate {
  item_id?: string | null;
  item_name_snapshot: string;
  description?: string | null;
  quantity: number;
  unit_id: string;
  unit_snapshot: string;
  rate: number;
  discount_type?: string;
  discount_value?: number;
  gst_rate?: number;
}

export interface AdjustmentNoteCreateRequest {
  note_type: 'CREDIT_NOTE' | 'DEBIT_NOTE';
  source_type?: string | null;
  source_id?: string | null;
  source_number?: string | null;
  party_id: string;
  party_role: 'CUSTOMER' | 'SUPPLIER';
  note_date: string;
  reason_code: string;
  reason_description?: string | null;
  tax_treatment: 'GST' | 'WITHOUT_GST';
  place_of_supply: string;
  lines: AdjustmentNoteLineCreate[];
}

export interface AdjustmentNoteResponse {
  id: string;
  note_number: string;
  note_type: 'CREDIT_NOTE' | 'DEBIT_NOTE';
  source_type?: string | null;
  source_id?: string | null;
  source_number?: string | null;
  party_id: string;
  party_role: 'CUSTOMER' | 'SUPPLIER';
  note_date: string;
  reason_code: string;
  reason_description?: string | null;
  tax_treatment: 'GST' | 'WITHOUT_GST';
  subtotal: number;
  discount_total: number;
  taxable_total: number;
  cgst_total: number;
  sgst_total: number;
  igst_total: number;
  grand_total: number;
  status: string;
  lines: any[];
  created_at: string;
}

export const adjustmentNotesApi = {
  create: async (data: AdjustmentNoteCreateRequest) => {
    const response = await apiClient.post<AdjustmentNoteResponse>('/adjustment-notes', data);
    return response.data;
  },
  getAll: async (note_type?: string) => {
    const params = new URLSearchParams();
    if (note_type) params.append('note_type', note_type);
    const response = await apiClient.get<{items: AdjustmentNoteResponse[], total: number}>(`/adjustment-notes?${params.toString()}`);
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<AdjustmentNoteResponse>(`/adjustment-notes/${id}`);
    return response.data;
  },
  approve: async (id: string) => {
    const response = await apiClient.post<AdjustmentNoteResponse>(`/adjustment-notes/${id}/approve`, {});
    return response.data;
  },
  post: async (id: string) => {
    const response = await apiClient.post<AdjustmentNoteResponse>(`/adjustment-notes/${id}/post`, {});
    return response.data;
  },
  cancel: async (id: string) => {
    const response = await apiClient.post<AdjustmentNoteResponse>(`/adjustment-notes/${id}/cancel`, {});
    return response.data;
  },
  reverse: async (id: string) => {
    const response = await apiClient.post<AdjustmentNoteResponse>(`/adjustment-notes/${id}/reverse`, {});
    return response.data;
  },
  getPdf: async (id: string) => {
    const response = await apiClient.get(`/adjustment-notes/${id}/pdf`, { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
    window.open(url, '_blank');
  }
};
