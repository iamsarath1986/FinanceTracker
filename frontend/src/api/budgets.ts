import api from './client'
import type { Budget } from '../types'

export const getBudgets = () => api.get<Budget[]>('/budgets')
export const getBudget = (id: number) => api.get<Budget>(`/budgets/${id}`)
export const createBudget = (data: Partial<Budget>) => api.post<Budget>('/budgets', data)
export const updateBudget = (id: number, data: Partial<Budget>) => api.patch<Budget>(`/budgets/${id}`, data)
export const deleteBudget = (id: number) => api.delete(`/budgets/${id}`)
