<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const password = ref('')
const error = ref('')
const loading = ref(false)

async function login() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(password.value)
    router.push('/dashboard')
  } catch {
    error.value = 'Invalid password. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-surface-100">
    <Card class="w-full max-w-sm shadow-lg">
      <template #title>
        <div class="text-center">
          <i class="pi pi-chart-pie text-4xl text-primary-500 mb-2 block" />
          <span>FinanceTracker</span>
        </div>
      </template>
      <template #content>
        <form class="flex flex-col gap-4" @submit.prevent="login">
          <div class="flex flex-col gap-1">
            <label class="text-sm font-medium text-surface-700">Password</label>
            <InputText
              v-model="password"
              type="password"
              placeholder="Enter your PIN / password"
              class="w-full"
              autofocus
            />
          </div>
          <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
          <Button type="submit" label="Login" class="w-full" :loading="loading" />
        </form>
      </template>
    </Card>
  </div>
</template>
