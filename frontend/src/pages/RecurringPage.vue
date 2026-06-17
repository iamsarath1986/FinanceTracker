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
import ToggleSwitch from 'primevue/toggleswitch'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { getRecurring, createRecurring, updateRecurring, deleteRecurring, generateRecurring } from '../api/recurring'
import { getAccounts } from '../api/accounts'
import { getCategories } from '../api/categories'
import type { RecurringTransaction, TransactionType, Frequency, Account, Category } from '../types'

const toast = useToast()
const confirm = useConfirm()
const items = ref<RecurringTransaction[]>([])
const accounts = ref<Account[]>([])
const categories = ref<Category[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const editing = ref<RecurringTransaction | null>(null)

const typeOptions = [{ label: 'Income', value: 'income' }, { label: 'Expense', value: 'expense' }]
const freqOptions = [{ label: 'Daily', value: 'daily' }, { label: 'Weekly', value: 'weekly' }, { label: 'Monthly', value: 'monthly' }, { label: 'Yearly', value: 'yearly' }]

const form = ref({
  account_id: null as number | null,
  category_id: null as number | null,
  amount: 0,
  type: 'expense' as TransactionType,
  description: '',
  frequency: 'monthly' as Frequency,
  start_date: new Date(),
  end_date: null as Date | null,
  is_active: true,
})

function toDateStr(d: Date | null) {
  return d ? d.toISOString().split('T')[0] : null
}

async function load() {
  loading.value = true
  try { items.value = (await getRecurring()).data } finally { loading.value = false }
}

function openNew() {
  editing.value = null
  form.value = { account_id: null, category_id: null, amount: 0, type: 'expense', description: '', frequency: 'monthly', start_date: new Date(), end_date: null, is_active: true }
  dialogVisible.value = true
}

function openEdit(item: RecurringTransaction) {
  editing.value = item
  form.value = { account_id: item.account_id, category_id: item.category_id, amount: item.amount, type: item.type, description: item.description ?? '', frequency: item.frequency, start_date: new Date(item.start_date), end_date: item.end_date ? new Date(item.end_date) : null, is_active: item.is_active }
  dialogVisible.value = true
}

async function save() {
  try {
    const payload = { ...form.value, start_date: toDateStr(form.value.start_date) as string, end_date: toDateStr(form.value.end_date), description: form.value.description || null }
    if (editing.value) {
      await updateRecurring(editing.value.id, payload)
      toast.add({ severity: 'success', summary: 'Updated', life: 3000 })
    } else {
      await createRecurring(payload)
      toast.add({ severity: 'success', summary: 'Created', life: 3000 })
    }
    dialogVisible.value = false
    await load()
  } catch {
    toast.add({ severity: 'error', summary: 'Error saving', life: 3000 })
  }
}

async function generate(item: RecurringTransaction) {
  try {
    const res = await generateRecurring(item.id)
    toast.add({ severity: 'success', summary: `Generated ${res.data.generated} transaction(s)`, life: 3000 })
    await load()
  } catch {
    toast.add({ severity: 'error', summary: 'Generate failed', life: 3000 })
  }
}

function confirmDelete(item: RecurringTransaction) {
  confirm.require({
    message: 'Delete this recurring transaction?',
    header: 'Confirm',
    icon: 'pi pi-trash',
    acceptClass: 'p-button-danger',
    accept: async () => {
      await deleteRecurring(item.id)
      toast.add({ severity: 'success', summary: 'Deleted', life: 3000 })
      await load()
    },
  })
}

function accountName(id: number) { return accounts.value.find((a) => a.id === id)?.name ?? id }
function categoryName(id: number | null) { return id ? (categories.value.find((c) => c.id === id)?.name ?? id) : '—' }

onMounted(async () => {
  [accounts.value, categories.value] = await Promise.all([
    getAccounts().then((r) => r.data),
    getCategories().then((r) => r.data),
  ])
  await load()
})
</script>

<template>
  <AppLayout title="Recurring Transactions">
    <Toast />
    <ConfirmDialog />
    <div class="flex justify-end mb-4">
      <Button label="New Recurring" icon="pi pi-plus" @click="openNew" />
    </div>
    <div class="overflow-x-auto">
      <DataTable :value="items" :loading="loading" striped-rows>
          <Column header="Account"><template #body="{ data }">{{ accountName(data.account_id) }}</template></Column>
          <Column header="Category"><template #body="{ data }">{{ categoryName(data.category_id) }}</template></Column>
          <Column field="description" header="Description" />
          <Column field="amount" header="Amount" />
          <Column field="type" header="Type" />
          <Column field="frequency" header="Frequency" />
          <Column field="start_date" header="Start" />
          <Column field="is_active" header="Active">
            <template #body="{ data }">
              <span :class="data.is_active ? 'text-green-600' : 'text-surface-400'">
                {{ data.is_active ? 'Yes' : 'No' }}
              </span>
            </template>
          </Column>
          <Column header="Actions">
            <template #body="{ data }">
              <Button icon="pi pi-play" text size="small" title="Generate" @click="generate(data)" />
              <Button icon="pi pi-pencil" text size="small" @click="openEdit(data)" />
              <Button icon="pi pi-trash" text size="small" severity="danger" @click="confirmDelete(data)" />
            </template>
          </Column>
      </DataTable>
    </div>

    <Dialog v-model:visible="dialogVisible" :header="editing ? 'Edit Recurring' : 'New Recurring'" modal class="w-full max-w-lg mx-4">
      <div class="flex flex-col gap-4 pt-2">
        <div><label class="block text-sm mb-1">Account *</label><Select v-model="form.account_id" :options="accounts" option-label="name" option-value="id" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Category</label><Select v-model="form.category_id" :options="categories" option-label="name" option-value="id" show-clear class="w-full" /></div>
        <div><label class="block text-sm mb-1">Type *</label><Select v-model="form.type" :options="typeOptions" option-label="label" option-value="value" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Amount *</label><InputNumber v-model="form.amount" :min-fraction-digits="2" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Description</label><InputText v-model="form.description" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Frequency *</label><Select v-model="form.frequency" :options="freqOptions" option-label="label" option-value="value" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Start Date *</label><DatePicker v-model="form.start_date" date-format="yy-mm-dd" class="w-full" /></div>
        <div><label class="block text-sm mb-1">End Date</label><DatePicker v-model="form.end_date" date-format="yy-mm-dd" show-clear class="w-full" /></div>
        <div class="flex items-center gap-3"><label class="text-sm">Active</label><ToggleSwitch v-model="form.is_active" /></div>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="dialogVisible = false" />
        <Button label="Save" @click="save" />
      </template>
    </Dialog>
  </AppLayout>
</template>
