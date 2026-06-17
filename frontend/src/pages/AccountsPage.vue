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
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import { getAccounts, createAccount, updateAccount, deleteAccount } from '../api/accounts'
import type { Account, AccountType } from '../types'

const toast = useToast()
const confirm = useConfirm()
const accounts = ref<Account[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const editing = ref<Account | null>(null)

const typeOptions = [
  { label: 'Savings', value: 'savings' },
  { label: 'Checking', value: 'checking' },
  { label: 'Investments', value: 'investments' },
  { label: 'Credit Card', value: 'credit_card' },
  { label: 'Cash', value: 'cash' },
]

const form = ref({
  name: '', type: 'checking' as AccountType, bank_name: '', country: '', currency: 'USD', opening_balance: 0,
})

async function load() {
  loading.value = true
  try { accounts.value = (await getAccounts()).data } finally { loading.value = false }
}

function openNew() {
  editing.value = null
  form.value = { name: '', type: 'checking', bank_name: '', country: '', currency: 'USD', opening_balance: 0 }
  dialogVisible.value = true
}

function openEdit(account: Account) {
  editing.value = account
  form.value = { name: account.name, type: account.type, bank_name: account.bank_name ?? '', country: account.country ?? '', currency: account.currency, opening_balance: account.opening_balance }
  dialogVisible.value = true
}

async function save() {
  try {
    const payload = { ...form.value, bank_name: form.value.bank_name || null, country: form.value.country || null }
    if (editing.value) {
      await updateAccount(editing.value.id, payload)
      toast.add({ severity: 'success', summary: 'Updated', life: 3000 })
    } else {
      await createAccount(payload)
      toast.add({ severity: 'success', summary: 'Created', life: 3000 })
    }
    dialogVisible.value = false
    await load()
  } catch {
    toast.add({ severity: 'error', summary: 'Error saving account', life: 3000 })
  }
}

function confirmDelete(account: Account) {
  confirm.require({
    message: `Delete account "${account.name}"?`,
    header: 'Confirm',
    icon: 'pi pi-trash',
    acceptClass: 'p-button-danger',
    accept: async () => {
      await deleteAccount(account.id)
      toast.add({ severity: 'success', summary: 'Deleted', life: 3000 })
      await load()
    },
  })
}

onMounted(load)
</script>

<template>
  <AppLayout title="Accounts">
    <Toast />
    <ConfirmDialog />
    <div class="flex justify-end mb-4">
      <Button label="New Account" icon="pi pi-plus" @click="openNew" />
    </div>
    <div class="overflow-x-auto">
      <DataTable :value="accounts" :loading="loading" striped-rows>
          <Column field="name" header="Name" />
          <Column field="type" header="Type" />
          <Column field="bank_name" header="Bank" />
          <Column field="currency" header="Currency" />
          <Column field="current_balance" header="Balance">
            <template #body="{ data }">
              <span :class="data.current_balance >= 0 ? 'text-green-600' : 'text-red-600'" class="font-semibold">
                {{ data.current_balance.toFixed(2) }}
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

    <Dialog v-model:visible="dialogVisible" :header="editing ? 'Edit Account' : 'New Account'" modal class="w-full max-w-lg mx-4">
      <div class="flex flex-col gap-4 pt-2">
        <div><label class="block text-sm mb-1">Name *</label><InputText v-model="form.name" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Type *</label><Select v-model="form.type" :options="typeOptions" option-label="label" option-value="value" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Bank</label><InputText v-model="form.bank_name" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Country (2-letter)</label><InputText v-model="form.country" maxlength="2" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Currency *</label><InputText v-model="form.currency" maxlength="3" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Opening Balance</label><InputNumber v-model="form.opening_balance" :min-fraction-digits="2" class="w-full" /></div>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="dialogVisible = false" />
        <Button label="Save" @click="save" />
      </template>
    </Dialog>
  </AppLayout>
</template>
