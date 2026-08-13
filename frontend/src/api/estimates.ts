import { apiClient } from './client';

export interface EstimateLineCreate {
  item_name_snapshot: string;
  item_type?: string;
  quantity: number;
  unit_snapshot?: string;
  cost_rate?: number;
  markup_percent?: number;
}

export interface EstimateCreateRequest {
  boq_id?: string | null;
  party_id?: string | null;
  estimate_date: string;
  valid_until?: string | null;
  lines: EstimateLineCreate[];
}

export interface EstimateLineResponse {
  id: string;
  item_name_snapshot: string;
  item_type: string;
  quantity: number;
  unit_snapshot: string | null;
  cost_rate: number;
  cost_amount: number;
  markup_percent: number;
  markup_amount: number;
  selling_rate: number;
  selling_amount: number;
}

export interface EstimateResponse {
  id: string;
  estimate_number: string | null;
  boq_id: string | null;
  party_id: string | null;
  estimate_date: string;
  valid_until: string | null;
  version: number;
  status: string;
  material_cost: number;
  labour_cost: number;
  service_cost: number;
  other_cost: number;
  total_cost: number;
  markup_amount: number;
  estimated_selling_value: number;
  gst_total: number;
  grand_total: number;
  created_at: string;
  updated_at: string;
  lines: EstimateLineResponse[];
}

export const estimatesApi = {
  create: async (data: EstimateCreateRequest) => {
    const response = await apiClient.post<EstimateResponse>('/estimates', data);
    return response.data;
  },
  getAll: async () => {
    const response = await apiClient.get<{items: EstimateResponse[], total: number}>('/estimates');
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<EstimateResponse>(`/estimates/${id}`);
    return response.data;
  },
  approve: async (id: string) => {
    const response = await apiClient.post<EstimateResponse>(`/estimates/${id}/approve`, {});
    return response.data;
  }
};
