import { apiClient } from './client';

export interface InvoiceLineCreate {
  item_id?: string | null;
  item_name: string;
  description?: string | null;
  hsn_sac?: string | null;
  quantity: number;
  unit_id: string;
  unit_name: string;
  unit_symbol: string;
  rate: number;
  discount_type?: string;
  discount_value?: number;
  gst_rate?: number;
}

export interface InvoiceCreateRequest {
  invoice_type?: string;
  invoice_date: string;
  customer_id: string;
  place_of_supply: string;
  lines: InvoiceLineCreate[];
  notes?: string | null;
  terms?: string | null;
}

export interface InvoiceCalculateRequest {
  customer_id?: string | null;
  place_of_supply: string;
  lines: InvoiceLineCreate[];
}

export interface InvoiceCalculateResponse {
  subtotal: number;
  discount_total: number;
  taxable_total: number;
  cgst_total: number;
  sgst_total: number;
  igst_total: number;
  grand_total: number;
  amount_in_words?: string | null;
  lines: any[];
}

export interface InvoiceResponse {
  id: string;
  invoice_number: string;
  invoice_type: string;
  invoice_date: string;
  customer_name_snapshot: string;
  place_of_supply: string;
  subtotal: number;
  discount_total: number;
  taxable_total: number;
  cgst_total: number;
  sgst_total: number;
  igst_total: number;
  grand_total: number;
  amount_in_words?: string | null;
  invoice_status: string;
  payment_status: string;
  notes?: string | null;
  lines: any[];
  created_at: string;
}

export const invoicesApi = {
  calculate: async (data: InvoiceCalculateRequest) => {
    const response = await apiClient.post<InvoiceCalculateResponse>('/invoices/calculate', data);
    return response.data;
  },
  create: async (data: InvoiceCreateRequest) => {
    const response = await apiClient.post<InvoiceResponse>('/invoices', data);
    return response.data;
  },
  getAll: async () => {
    const response = await apiClient.get<{items: InvoiceResponse[], total: number}>('/invoices');
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<InvoiceResponse>(`/invoices/${id}`);
    return response.data;
  },
  finalize: async (id: string) => {
    const response = await apiClient.post<InvoiceResponse>(`/invoices/${id}/finalize`, {});
    return response.data;
  },
  cancel: async (id: string, reason: string) => {
    const response = await apiClient.post<InvoiceResponse>(`/invoices/${id}/cancel`, { cancel_reason: reason });
    return response.data;
  },
  getPdf: async (id: string) => {
    const response = await apiClient.get(`/invoices/${id}/pdf`, { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
    window.open(url, '_blank');
  }
};
