import { apiClient } from './client';

export interface ReturnOrderLineCreate {
  original_order_line_id: string;
  return_quantity: number;
  condition?: string;
  warehouse_action?: string;
}

export interface ReturnOrderCreateRequest {
  original_order_id: string;
  return_type: string;
  reason?: string;
  lines: ReturnOrderLineCreate[];
}

export interface ReturnOrderLineResponse {
  id: string;
  original_order_line_id: string;
  item_id: string | null;
  item_name_snapshot: string;
  unit_snapshot: string | null;
  original_quantity: number;
  previously_returned_quantity: number;
  return_quantity: number;
  remaining_quantity: number;
  rate: number;
  taxable_value: number;
  gst_rate: number;
  cgst_amount: number;
  sgst_amount: number;
  igst_amount: number;
  line_total: number;
  condition: string;
  warehouse_action: string;
}

export interface ReturnOrderResponse {
  id: string;
  return_number: string | null;
  return_type: string;
  original_order_id: string;
  party_id: string;
  return_date: string;
  status: string;
  financial_status: string;
  reason: string | null;
  subtotal: number;
  taxable_total: number;
  cgst_total: number;
  sgst_total: number;
  igst_total: number;
  grand_total: number;
  created_at: string;
  lines: ReturnOrderLineResponse[];
}

export interface ReturnableLineResponse {
  original_order_line_id: string;
  item_name_snapshot: string;
  unit_symbol_snapshot: string | null;
  rate: number;
  gst_rate: number;
  original_quantity: number;
  previously_returned_quantity: number;
  returnable_quantity: number;
}

export interface ReturnableLinesResponse {
  order_id: string;
  order_type: string;
  tax_treatment: string;
  lines: ReturnableLineResponse[];
}

export const returnsApi = {
  getReturnableLines: async (orderId: string) => {
    const response = await apiClient.get<ReturnableLinesResponse>(`/returns/order/${orderId}/returnable-lines`);
    return response.data;
  },
  create: async (data: ReturnOrderCreateRequest) => {
    const response = await apiClient.post<ReturnOrderResponse>('/returns', data);
    return response.data;
  },
  getAll: async (returnType?: string) => {
    const params = new URLSearchParams();
    if (returnType) params.append('return_type', returnType);
    const response = await apiClient.get<{items: ReturnOrderResponse[], total: number}>(`/returns?${params.toString()}`);
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<ReturnOrderResponse>(`/returns/${id}`);
    return response.data;
  },
  approve: async (id: string) => {
    const response = await apiClient.post<ReturnOrderResponse>(`/returns/${id}/approve`, {});
    return response.data;
  },
  post: async (id: string) => {
    const response = await apiClient.post<ReturnOrderResponse>(`/returns/${id}/post`, {});
    return response.data;
  }
};
