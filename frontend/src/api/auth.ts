import { apiClient } from './client';

export interface SetupRequest {
  company_name: string;
  ownership_type: string;
  mobile: string;
  office_phone?: string;
  email: string;
  authorized_person_name: string;
  authorized_person_designation?: string;
  gst_registered: boolean;
  gstin?: string;
  address_line_1: string;
  address_line_2?: string;
  city: string;
  district: string;
  state: string;
  state_code: string;
  pincode: string;
  country: string;
  bank_account_holder_name: string;
  bank_account_number: string;
  bank_ifsc: string;
  bank_name: string;
  bank_branch: string;
  bank_account_type: string;
  pin: string;
  confirm_pin: string;
}

export interface LoginRequest {
  pin: string;
}

export interface PinChangeRequest {
  old_pin: string;
  new_pin: string;
  confirm_pin: string;
}

export const authApi = {
  setup: async (data: SetupRequest) => {
    const response = await apiClient.post('/auth/setup', data);
    return response.data;
  },
  login: async (data: LoginRequest) => {
    const response = await apiClient.post('/auth/login', data);
    return response.data;
  },
  changePin: async (data: PinChangeRequest) => {
    const response = await apiClient.post('/auth/pin-change', data);
    return response.data;
  },
  logout: async () => {
    const response = await apiClient.post('/auth/logout');
    return response.data;
  },
  getMe: async () => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  }
};
