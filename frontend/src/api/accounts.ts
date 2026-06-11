import api from './client'
import type { Account } from '../types'

export const getAccounts = () => api.get<Account[]>('/accounts')
export const getAccount = (id: number) => api.get<Account>(`/accounts/${id}`)
export const createAccount = (data: Partial<Account>) => api.post<Account>('/accounts', data)
export const updateAccount = (id: number, data: Partial<Account>) => api.patch<Account>(`/accounts/${id}`, data)
export const deleteAccount = (id: number) => api.delete(`/accounts/${id}`)
