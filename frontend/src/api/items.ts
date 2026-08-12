import { apiClient } from './client';

export interface Item {
  id: number;
  type: string;
  sku: string | null;
  name: string;
  description: string | null;
  hsn_sac: string | null;
  gst_rate: number;
  cess_rate: number;
  sale_price: number;
  purchase_price: number;
  unit_id: number;
  stock_quantity: number;
  low_stock_warning: number;
  is_active: boolean;
}

export interface ItemCreateRequest {
  type: string;
  sku?: string | null;
  name: string;
  description?: string | null;
  hsn_sac?: string | null;
  gst_rate: number;
  cess_rate?: number;
  sale_price: number;
  purchase_price: number;
  unit_id: number;
  stock_quantity?: number;
  low_stock_warning?: number;
  is_active?: boolean;
}

export const itemsApi = {
  getAll: async () => {
    const response = await apiClient.get<Item[]>('/items');
    return response.data;
  },
  create: async (data: ItemCreateRequest) => {
    const response = await apiClient.post<Item>('/items', data);
    return response.data;
  },
  delete: async (id: number) => {
    const response = await apiClient.delete(`/items/${id}`);
    return response.data;
  }
};
