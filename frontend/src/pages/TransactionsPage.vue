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
import DatePicker from 'primevue/datepicker'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { getTransactions, createTransaction, updateTransaction, deleteTransaction } from '../api/transactions'
import { getAccounts } from '../api/accounts'
import { getCategories } from '../api/categories'
import type { Transaction, TransactionType, Account, Category } from '../types'

const toast = useToast()
const confirm = useConfirm()
const transactions = ref<Transaction[]>([])
const accounts = ref<Account[]>([])
const categories = ref<Category[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const editing = ref<Transaction | null>(null)

const filters = ref({ account_id: null as number | null, category_id: null as number | null, type: null as string | null })

const typeOptions = [{ label: 'Income', value: 'income' }, { label: 'Expense', value: 'expense' }]

const form = ref({
  account_id: null as number | null,
  category_id: null as number | null,
  amount: 0,
  type: 'expense' as TransactionType,
  date: new Date(),
  description: '',
})

function toDateStr(d: Date) {
  return d.toISOString().split('T')[0]
}

async function load() {
  loading.value = true
  try {
    const params: Record<string, unknown> = {}
    if (filters.value.account_id) params.account_id = filters.value.account_id
    if (filters.value.category_id) params.category_id = filters.value.category_id
    if (filters.value.type) params.type = filters.value.type
    transactions.value = (await getTransactions(params)).data
  } finally { loading.value = false }
}

function openNew() {
  editing.value = null
  form.value = { account_id: null, category_id: null, amount: 0, type: 'expense', date: new Date(), description: '' }
  dialogVisible.value = true
}

function openEdit(tx: Transaction) {
  editing.value = tx
  form.value = { account_id: tx.account_id, category_id: tx.category_id, amount: tx.amount, type: tx.type, date: new Date(tx.date), description: tx.description ?? '' }
  dialogVisible.value = true
}

async function save() {
  try {
    const payload = { ...form.value, date: toDateStr(form.value.date), description: form.value.description || null }
    if (editing.value) {
      await updateTransaction(editing.value.id, payload)
      toast.add({ severity: 'success', summary: 'Updated', life: 3000 })
    } else {
      await createTransaction(payload)
      toast.add({ severity: 'success', summary: 'Created', life: 3000 })
    }
    dialogVisible.value = false
    await load()
  } catch {
    toast.add({ severity: 'error', summary: 'Error saving transaction', life: 3000 })
  }
}

function confirmDelete(tx: Transaction) {
  confirm.require({
    message: 'Delete this transaction?',
    header: 'Confirm',
    icon: 'pi pi-trash',
    acceptClass: 'p-button-danger',
    accept: async () => {
      await deleteTransaction(tx.id)
      toast.add({ severity: 'success', summary: 'Deleted', life: 3000 })
      await load()
    },
  })
}

function accountName(id: number) {
  return accounts.value.find((a) => a.id === id)?.name ?? id
}

function categoryName(id: number | null) {
  if (!id) return '—'
  return categories.value.find((c) => c.id === id)?.name ?? id
}

onMounted(async () => {
  [accounts.value, categories.value] = await Promise.all([
    getAccounts().then((r) => r.data),
    getCategories().then((r) => r.data),
  ])
  await load()
})
</script>

<template>
  <AppLayout title="Transactions">
    <Toast />
    <ConfirmDialog />
    <div class="flex flex-wrap gap-3 mb-4 items-end">
          <div>
            <label class="block text-xs mb-1">Account</label>
            <Select v-model="filters.account_id" :options="accounts" option-label="name" option-value="id" placeholder="All" show-clear class="w-40" @change="load" />
          </div>
          <div>
            <label class="block text-xs mb-1">Category</label>
            <Select v-model="filters.category_id" :options="categories" option-label="name" option-value="id" placeholder="All" show-clear class="w-40" @change="load" />
          </div>
          <div>
            <label class="block text-xs mb-1">Type</label>
            <Select v-model="filters.type" :options="typeOptions" option-label="label" option-value="value" placeholder="All" show-clear class="w-32" @change="load" />
          </div>
          <Button label="New Transaction" icon="pi pi-plus" class="ml-auto" @click="openNew" />
        </div>

    <div class="overflow-x-auto">
      <DataTable :value="transactions" :loading="loading" striped-rows>
          <Column field="date" header="Date" />
          <Column header="Account"><template #body="{ data }">{{ accountName(data.account_id) }}</template></Column>
          <Column header="Category"><template #body="{ data }">{{ categoryName(data.category_id) }}</template></Column>
          <Column field="description" header="Description" />
          <Column header="Amount">
            <template #body="{ data }">
              <span :class="data.type === 'income' ? 'text-green-600 font-semibold' : 'text-red-600 font-semibold'">
                {{ data.type === 'expense' ? '-' : '+' }}{{ data.amount.toFixed(2) }}
              </span>
            </template>
          </Column>
          <Column header="Type">
            <template #body="{ data }">
              <span class="px-2 py-0.5 rounded text-xs font-medium"
                :class="data.type === 'income' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
                {{ data.type }}
              </span>
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

    <Dialog v-model:visible="dialogVisible" :header="editing ? 'Edit Transaction' : 'New Transaction'" modal class="w-full max-w-lg mx-4">
      <div class="flex flex-col gap-4 pt-2">
        <div><label class="block text-sm mb-1">Account *</label><Select v-model="form.account_id" :options="accounts" option-label="name" option-value="id" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Category</label><Select v-model="form.category_id" :options="categories" option-label="name" option-value="id" show-clear class="w-full" /></div>
        <div><label class="block text-sm mb-1">Type *</label><Select v-model="form.type" :options="typeOptions" option-label="label" option-value="value" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Amount *</label><InputNumber v-model="form.amount" :min-fraction-digits="2" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Date *</label><DatePicker v-model="form.date" date-format="yy-mm-dd" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Description</label><InputText v-model="form.description" class="w-full" /></div>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="dialogVisible = false" />
        <Button label="Save" @click="save" />
      </template>
    </Dialog>
  </AppLayout>
</template>
