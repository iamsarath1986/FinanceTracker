import api from './client'
import type { Category } from '../types'

export const getCategories = () => api.get<Category[]>('/categories')
export const getCategory = (id: number) => api.get<Category>(`/categories/${id}`)
export const createCategory = (data: Partial<Category>) => api.post<Category>('/categories', data)
export const updateCategory = (id: number, data: Partial<Category>) => api.patch<Category>(`/categories/${id}`, data)
export const deleteCategory = (id: number) => api.delete(`/categories/${id}`)
