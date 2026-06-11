<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppLayout from '../components/layout/AppLayout.vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { getCategories, createCategory, updateCategory, deleteCategory } from '../api/categories'
import type { Category, CategoryType } from '../types'

const toast = useToast()
const confirm = useConfirm()
const categories = ref<Category[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const editing = ref<Category | null>(null)

const typeOptions = [
  { label: 'Income', value: 'income' },
  { label: 'Expense', value: 'expense' },
]

const form = ref({ name: '', type: 'expense' as CategoryType, color: '#94a3b8', icon: '' })

async function load() {
  loading.value = true
  try { categories.value = (await getCategories()).data } finally { loading.value = false }
}

function openNew() {
  editing.value = null
  form.value = { name: '', type: 'expense', color: '#94a3b8', icon: '' }
  dialogVisible.value = true
}

function openEdit(cat: Category) {
  editing.value = cat
  form.value = { name: cat.name, type: cat.type, color: cat.color ?? '#94a3b8', icon: cat.icon ?? '' }
  dialogVisible.value = true
}

async function save() {
  try {
    const payload = { ...form.value, icon: form.value.icon || null }
    if (editing.value) {
      await updateCategory(editing.value.id, payload)
      toast.add({ severity: 'success', summary: 'Updated', life: 3000 })
    } else {
      await createCategory(payload)
      toast.add({ severity: 'success', summary: 'Created', life: 3000 })
    }
    dialogVisible.value = false
    await load()
  } catch {
    toast.add({ severity: 'error', summary: 'Error saving category', life: 3000 })
  }
}

function confirmDelete(cat: Category) {
  confirm.require({
    message: `Delete category "${cat.name}"?`,
    header: 'Confirm',
    icon: 'pi pi-trash',
    acceptClass: 'p-button-danger',
    accept: async () => {
      await deleteCategory(cat.id)
      toast.add({ severity: 'success', summary: 'Deleted', life: 3000 })
      await load()
    },
  })
}

onMounted(load)
</script>

<template>
  <AppLayout title="Categories">
    <Toast />
    <ConfirmDialog />
    <div class="flex justify-end mb-4">
      <Button label="New Category" icon="pi pi-plus" @click="openNew" />
    </div>
    <div class="overflow-x-auto">
      <DataTable :value="categories" :loading="loading" striped-rows>
          <Column header="Color" style="width: 60px">
            <template #body="{ data }">
              <span class="inline-block w-5 h-5 rounded-full" :style="{ backgroundColor: data.color ?? '#ccc' }" />
            </template>
          </Column>
          <Column field="name" header="Name" />
          <Column field="type" header="Type">
            <template #body="{ data }">
              <span class="px-2 py-0.5 rounded text-xs font-medium"
                :class="data.type === 'income' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
                {{ data.type }}
              </span>
            </template>
          </Column>
          <Column field="icon" header="Icon">
            <template #body="{ data }">
              <i v-if="data.icon" :class="data.icon" />
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

    <Dialog v-model:visible="dialogVisible" :header="editing ? 'Edit Category' : 'New Category'" modal class="w-full max-w-md mx-4">
      <div class="flex flex-col gap-4 pt-2">
        <div><label class="block text-sm mb-1">Name *</label><InputText v-model="form.name" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Type *</label><Select v-model="form.type" :options="typeOptions" option-label="label" option-value="value" class="w-full" /></div>
        <div><label class="block text-sm mb-1">Color</label><input type="color" v-model="form.color" class="h-9 w-full rounded border" /></div>
        <div><label class="block text-sm mb-1">Icon (PrimeIcons class)</label><InputText v-model="form.icon" placeholder="e.g. pi pi-home" class="w-full" /></div>
      </div>
      <template #footer>
        <Button label="Cancel" text @click="dialogVisible = false" />
        <Button label="Save" @click="save" />
      </template>
    </Dialog>
  </AppLayout>
</template>
