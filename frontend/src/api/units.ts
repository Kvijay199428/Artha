import { apiClient } from './client';

export interface Unit {
  id: number;
  name: string;
  abbreviation: string;
  category: string;
  is_base_unit: boolean;
  base_unit_id: number | null;
  multiplier: number;
  formula: string | null;
  aliases: string | null;
}

export interface UnitCreateRequest {
  name: string;
  abbreviation: string;
  category: string;
  is_base_unit: boolean;
  base_unit_id?: number | null;
  multiplier?: number;
  formula?: string | null;
  aliases?: string | null;
}

export const unitsApi = {
  getAll: async () => {
    const response = await apiClient.get<Unit[]>('/units');
    return response.data;
  },
  create: async (data: UnitCreateRequest) => {
    const response = await apiClient.post<Unit>('/units', data);
    return response.data;
  },
  delete: async (id: number) => {
    const response = await apiClient.delete(`/units/${id}`);
    return response.data;
  }
};
