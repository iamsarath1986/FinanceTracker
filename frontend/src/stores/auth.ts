import { defineStore } from 'pinia'
import api from '../api/client'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('finance_token') as string | null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(password: string) {
      const res = await api.post('/auth/login', { password })
      this.token = res.data.access_token
      localStorage.setItem('finance_token', this.token!)
    },
    logout() {
      this.token = null
      localStorage.removeItem('finance_token')
    },
  },
})
