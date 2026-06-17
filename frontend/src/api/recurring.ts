import api from './client'
import type { RecurringTransaction } from '../types'

export const getRecurring = () => api.get<RecurringTransaction[]>('/recurring')
export const getRecurringById = (id: number) => api.get<RecurringTransaction>(`/recurring/${id}`)
export const createRecurring = (data: Record<string, unknown>) => api.post<RecurringTransaction>('/recurring', data)
export const updateRecurring = (id: number, data: Record<string, unknown>) => api.patch<RecurringTransaction>(`/recurring/${id}`, data)
export const deleteRecurring = (id: number) => api.delete(`/recurring/${id}`)
export const generateRecurring = (id: number) => api.post<{ generated: number }>(`/recurring/${id}/generate`)
