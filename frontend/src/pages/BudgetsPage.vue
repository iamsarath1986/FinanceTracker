<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppLayout from '../components/layout/AppLayout.vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Select from 'primevue/select'
import ProgressBar from 'primevue/progressbar'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { getBudgets, createBudget, updateBudget, deleteBudget } from '../api/budgets'
import { getCategories } from '../api/categories'
import { getAccounts } from '../api/accounts'
import type { Budget, ScopeType, PeriodType, Category, Account } from '../types'

const toast = useToast()
const confirm = useConfirm()
const budgets = ref<Budget[]>([])
const categories = ref<Category[]>([])
const accounts = ref<Account[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const editing = ref<Budget | null>(null)

const scopeOptions = [{ label: 'Category', value: 'category' }, { label: 'Account', value: 'account' }]
const periodOptions = [{ label: 'Monthly', value: 'monthly' }, { label: 'Annual', value: 'annual' }]
const monthOptions = Array.from({ length: 12 }, (_, i) => ({ label: new Date(0, i).toLocaleString('default', { month: 'long' }), value: i + 1 }))

const form = ref({
  name: '',
  scope_type: 'category' as ScopeType,
  period_type: 'monthly' as PeriodType,
  category_id: null as number | null,
  account_id: null as number | null,
  year: new Date().getFullYear(),
  month: new Date().getMonth() + 1 as number | null,
  limit_amount: 0,
  currency: 'AED',
})

async function load() {
  loading.value = true
  try { budgets.value = (await getBudgets()).data } finally { loading.value = false }
}

function openNew() {
  editing.value = null
  form.value = { name: '', scope_type: 'category', period_type: 'monthly', category_id: null, account_id: null, year: new Date().getFullYear(), month: new Date().getMonth() + 1, limit_amount: 0, currency: 'AED' }
  dialogVisible.value = true
}

function openEdit(b: Budget) {
  editing.value = b
  form.value = { name: b.name, scope_type: b.scope_type, period_type: b.period_type, category_id: b.category_id, account_id: b.account_id, year: b.year, month: b.month, limit_amount: b.limit_amount, currency: b.currency }
  dialogVisible.value = true
}

async function save() {
  try {
    const payload = { ...form.value, month: form.value.period_type === 'annual' ? null : form.value.month }
    if (editing.value) {
      await updateBudget(editing.value.id, { name: payload.name, limit_amount: payload.limit_amount, currency: payload.currency })
      toast.add({ severity: 'success', summary: 'Updated', life: 3000 })
    } else {
      await createBudget(payload)
      toast.add({ severity: 'success', summary: 'Created', life: 3000 })
    }
    dialogVisible.value = false
    await load()
  } catch {
    toast.add({ severity: 'error', summary: 'Error saving budget', life: 3000 })
  }
}

function confirmDelete(b: Budget) {
  confirm.require({
    message: `Delete budget "${b.name}"?`,
    header: 'Confirm',
    icon: 'pi pi-trash',
    acceptClass: 'p-button-danger',
    accept: async () => {
      await deleteBudget(b.id)
      toast.add({ severity: 'success', summary: 'Deleted', life: 3000 })
      await load()
    },
  })
}

function pct(b: Budget) { return Math.min(Math.round((b.spent / b.limit_amount) * 100), 100) }

onMounted(async () => {
  [categories.value, accounts.value] = await Promise.all([
    getCategories().then((r) => r.data),
    getAccounts().then((r) => r.data),
  ])
  await load()
})
</script>

<template>
  <AppLayout title="Budgets">
    <Toast />
    <ConfirmDialog />
    <div class="flex justify-end mb-4">
      <Button label="New Budget" icon="pi pi-plus" @click="openNew" />
    </div>
    <div class="overflow-x-auto">
      <DataTable :value="budgets" :loading="loading" striped-rows>
          <Column field="name" header="Name" />
          <Column field="scope_type" header="Scope" />
          <Column header="Period">
            <template #body="{ data }">{{ data.year }}{{ data.month ? '-' + String(data.month).padStart(2, '0') : '' }}</template>
          </Column>
          <Column header="Progress">
            <template #body="{ data }">
              <div class="min-w-32">
                <div class="flex justify-between text-xs mb-1">
                  <span>{{ data.spent.toFixed(2) }} / {{ data.limit_amount.toFixed(2) }} {{ data.currency }}</span>
                  <span>{{ pct(data) }}%</span>
                </div>
                <ProgressBar :value="pct(data)" :show-value="false" class="h-2" />
              </div>
            </template>
          </Column>
          <Column header="Actions">
            <template #body="{ data }">
              <Button icon="pi pi-pencil" text size="small" @click="openEdit(data)" />
              <Button icon="pi pi-trash" text size="small" severity="danger" @click="confirmDelete(data)" />
            </template>
          </Column>
      </DataTable>
    </div>

    <Dialog v-model:visible="dialogVisible" :header="editing ? 'Edit Budget' : 'New Budget'" modal class="w-full max-w-lg mx-4">
      <div class="flex flex-col gap-4 pt-2">
        <div><label class="block text-sm mb-1">Name *</label><InputText v-model="form.name" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Scope *</label><Select v-model="form.scope_type" :options="scopeOptions" option-label="label" option-value="value" class="w-full" :disabled="!!editing" /></div>
        <div v-if="form.scope_type === 'category'"><label class="block text-sm mb-1">Category *</label><Select v-model="form.category_id" :options="categories" option-label="name" option-value="id" class="w-full" :disabled="!!editing" /></div>
        <div v-if="form.scope_type === 'account'"><label class="block text-sm mb-1">Account *</label><Select v-model="form.account_id" :options="accounts" option-label="name" option-value="id" class="w-full" :disabled="!!editing" /></div>
        <div><label class="block text-sm mb-1">Period *</label><Select v-model="form.period_type" :options="periodOptions" option-label="label" option-value="value" class="w-full" :disabled="!!editing" /></div>
        <div><label class="block text-sm mb-1">Year *</label><InputNumber v-model="form.year" :use-grouping="false" class="w-full" :disabled="!!editing" /></div>
        <div v-if="form.period_type === 'monthly'"><label class="block text-sm mb-1">Month *</label><Select v-model="form.month" :options="monthOptions" option-label="label" option-value="value" class="w-full" :disabled="!!editing" /></div>
        <div><label class="block text-sm mb-1">Limit Amount *</label><InputNumber v-model="form.limit_amount" :min-fraction-digits="2" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Currency *</label><InputText v-model="form.currency" maxlength="3" class="w-full" /></div>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="dialogVisible = false" />
        <Button label="Save" @click="save" />
      </template>
    </Dialog>
  </AppLayout>
</template>
