import { apiClient } from './client';

export interface CompanyDetail {
  id: string;
  company_name: string;
  legal_name?: string;
  trade_name?: string;
  ownership_type: string;
  status: string;
  mobile: string;
  mobile_country_code?: string;
  office_phone?: string;
  office_phone_country_code?: string;
  email: string;
  website?: string;
  authorized_person_name: string;
  logo_url?: string;
  gst_details?: {
    id: string;
    gstin?: string;
    state_code?: string;
    state_name?: string;
    pan?: string;
    tan?: string;
    gstin_validation_status: string;
  };
  bank_accounts: Array<{
    id: string;
    account_holder_name: string;
    account_number: string;
    ifsc: string;
    bank_name?: string;
    branch: string;
    account_type: string;
    is_primary: boolean;
  }>;
}

export const companyApi = {
  get: async (): Promise<CompanyDetail> => {
    const response = await apiClient.get<{ data: CompanyDetail }>('/company/');
    return (response.data as any).data;
  },
  update: async (data: Partial<CompanyDetail>): Promise<CompanyDetail> => {
    const response = await apiClient.put<{ data: CompanyDetail }>('/company/', data);
    return (response.data as any).data;
  },
  uploadLogo: async (file: File): Promise<{ logo_url: string; asset_id: string }> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post<{ data: { logo_url: string; asset_id: string } }>('/company/logo', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return (response.data as any).data;
  },
};
