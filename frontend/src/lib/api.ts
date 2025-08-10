import axios from 'axios'
import type { AxiosResponse } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || (
  // In production, use the same domain for API calls
  typeof window !== 'undefined' && window.location.origin.includes('vercel.app') 
    ? window.location.origin 
    : 'http://localhost:8000'
)

export const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Business API
export const businessApi = {
  list: (): Promise<AxiosResponse<any>> => api.get('/businesses/'),
  get: (id: number): Promise<AxiosResponse<any>> => api.get(`/businesses/${id}/`),
  create: (data: any): Promise<AxiosResponse<any>> => api.post('/businesses/', data),
  update: (id: number, data: any): Promise<AxiosResponse<any>> => api.put(`/businesses/${id}/`, data),
  delete: (id: number): Promise<AxiosResponse<any>> => api.delete(`/businesses/${id}/`),
}

// Content API
export const contentApi = {
  list: (params?: any): Promise<AxiosResponse<any>> => api.get('/content/', { params }),
  get: (id: number): Promise<AxiosResponse<any>> => api.get(`/content/${id}/`),
  generate: (data: {
    business_id: number
    content_type: string
    topic: string
    keywords?: string[]
  }): Promise<AxiosResponse<any>> => api.post('/content/generate/', data),
  update: (id: number, data: any): Promise<AxiosResponse<any>> => api.put(`/content/${id}/`, data),
  approve: (id: number): Promise<AxiosResponse<any>> => api.put(`/content/${id}/approve/`),
  saveDraft: (id: number): Promise<AxiosResponse<any>> => api.put(`/content/${id}/draft/`),
  delete: (id: number): Promise<AxiosResponse<any>> => api.delete(`/content/${id}/`),
}

// Industry API
export const industryApi = {
  list: (params?: { active_only?: boolean; search?: string }): Promise<AxiosResponse<any>> => api.get('/industries/', { params }),
  get: (id: number): Promise<AxiosResponse<any>> => api.get(`/industries/${id}/`),
  getBySlug: (slug: string): Promise<AxiosResponse<any>> => api.get(`/industries/slug/${slug}/`),
  create: (data: {
    name: string
    slug: string
    description?: string
    icon?: string
    color?: string
    sort_order?: number
  }): Promise<AxiosResponse<any>> => api.post('/industries/', data),
  update: (id: number, data: any): Promise<AxiosResponse<any>> => api.put(`/industries/${id}/`, data),
  delete: (id: number, force?: boolean): Promise<AxiosResponse<any>> => api.delete(`/industries/${id}/`, { params: { force } }),
  activate: (id: number): Promise<AxiosResponse<any>> => api.put(`/industries/${id}/activate/`),
}

// Suggestions API
export const suggestionsApi = {
  topics: (data: {
    business_id: number
    content_type: string
    category?: string
    description?: string
  }): Promise<AxiosResponse<any>> => api.post('/suggestions/topics/', data),
  keywords: (data: {
    business_id: number
    content_type: string
    category?: string
    topic?: string
    description?: string
  }): Promise<AxiosResponse<any>> => api.post('/suggestions/keywords/', data),
}

// Health check
export const healthApi = {
  check: (): Promise<AxiosResponse<any>> => api.get('/health', { baseURL: API_BASE_URL }),
}