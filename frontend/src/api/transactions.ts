import api from './client'
import type { Transaction } from '../types'

export const getTransactions = (params?: Record<string, unknown>) => api.get<Transaction[]>('/transactions', { params })
export const getTransaction = (id: number) => api.get<Transaction>(`/transactions/${id}`)
export const createTransaction = (data: Record<string, unknown>) => api.post<Transaction>('/transactions', data)
export const updateTransaction = (id: number, data: Record<string, unknown>) => api.patch<Transaction>(`/transactions/${id}`, data)
export const deleteTransaction = (id: number) => api.delete(`/transactions/${id}`)
