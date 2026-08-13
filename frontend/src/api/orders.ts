import { apiClient } from './client';

export interface SupplyOrderLineCreate {
  item_id?: string | null;
  item_name: string;
  sku?: string | null;
  hsn_sac?: string | null;
  unit_id: string;
  unit_name: string;
  unit_symbol: string;
  quantity: number;
  rate: number;
  discount_type?: string;
  discount_value?: number;
  gst_rate?: number;
  description?: string | null;
}

export interface SupplyOrderCreateRequest {
  order_type: 'PURCHASE' | 'SALES';
  tax_treatment: 'GST' | 'WITHOUT_GST';
  party_id: string;
  order_date: string;
  expected_date?: string | null;
  place_of_supply: string;
  lines: SupplyOrderLineCreate[];
  quotation_id?: string;
  notes?: string | null;
  terms?: string | null;
}

export interface SupplyOrderCalculateRequest {
  tax_treatment: 'GST' | 'WITHOUT_GST';
  party_id?: string | null;
  place_of_supply: string;
  lines: SupplyOrderLineCreate[];
}

export interface SupplyOrderResponse {
  id: string;
  order_type: 'PURCHASE' | 'SALES';
  tax_treatment: 'GST' | 'WITHOUT_GST';
  order_number?: string | null;
  order_date: string;
  expected_date?: string | null;
  party_id: string;
  place_of_supply: string;
  status: string;
  revision: number;
  subtotal: number;
  discount_total: number;
  taxable_total: number;
  cgst_total: number;
  sgst_total: number;
  igst_total: number;
  cess_total: number;
  other_charges: number;
  round_off: number;
  grand_total: number;
  amount_in_words?: string | null;
  notes?: string | null;
  terms?: string | null;
  lines: any[];
}

export const ordersApi = {
  calculate: async (data: SupplyOrderCalculateRequest) => {
    const response = await apiClient.post<any>('/orders/calculate', data);
    return response.data;
  },
  create: async (data: SupplyOrderCreateRequest) => {
    const response = await apiClient.post<SupplyOrderResponse>('/orders', data);
    return response.data;
  },
  getAll: async (order_type?: string) => {
    const params = new URLSearchParams();
    if (order_type) params.append('order_type', order_type);
    const response = await apiClient.get<{items: SupplyOrderResponse[], total: number}>(`/orders?${params.toString()}`);
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<SupplyOrderResponse>(`/orders/${id}`);
    return response.data;
  },
  confirm: async (id: string) => {
    const response = await apiClient.post<SupplyOrderResponse>(`/orders/${id}/confirm`, {});
    return response.data;
  },
  convert: async (id: string) => {
    const response = await apiClient.post<any>(`/orders/${id}/convert`, {});
    return response.data;
  }
};
