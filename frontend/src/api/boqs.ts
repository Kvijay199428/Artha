import { apiClient } from './client';

export interface BOQLineCreate {
  parent_line_id?: string | null;
  section?: string | null;
  item_type: string;
  item_id?: string | null;
  description: string;
  specification?: string | null;
  quantity: number;
  unit_id?: string | null;
  unit_snapshot?: string | null;
  quantity_formula?: string | null;
  estimated_rate?: number;
  remarks?: string | null;
  sort_order?: number;
}

export interface BOQCreateRequest {
  project_name?: string | null;
  party_id?: string | null;
  boq_date: string;
  notes?: string | null;
  lines: BOQLineCreate[];
}

export interface BOQLineResponse {
  id: string;
  parent_line_id: string | null;
  section: string | null;
  item_type: string;
  item_id: string | null;
  description: string;
  specification: string | null;
  quantity: number;
  unit_id: string | null;
  unit_snapshot: string | null;
  quantity_formula: string | null;
  estimated_rate: number;
  estimated_amount: number;
  remarks: string | null;
  sort_order: number;
}

export interface BOQResponse {
  id: string;
  boq_number: string | null;
  project_name: string | null;
  party_id: string | null;
  boq_date: string;
  version: number;
  status: string;
  notes: string | null;
  created_at: string;
  updated_at: string;
  lines: BOQLineResponse[];
}

export const boqsApi = {
  create: async (data: BOQCreateRequest) => {
    const response = await apiClient.post<BOQResponse>('/boqs', data);
    return response.data;
  },
  getAll: async () => {
    const response = await apiClient.get<{items: BOQResponse[], total: number}>('/boqs');
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<BOQResponse>(`/boqs/${id}`);
    return response.data;
  },
  approve: async (id: string) => {
    const response = await apiClient.post<BOQResponse>(`/boqs/${id}/approve`, {});
    return response.data;
  }
};
