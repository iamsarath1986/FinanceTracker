<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Card from 'primevue/card'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import ProgressSpinner from 'primevue/progressspinner'
import AppLayout from '../components/layout/AppLayout.vue'
import BalanceCard from '../components/dashboard/BalanceCard.vue'
import CashFlowChart from '../components/dashboard/CashFlowChart.vue'
import BudgetProgress from '../components/dashboard/BudgetProgress.vue'
import { getDashboardSummary } from '../api/dashboard'
import type { DashboardSummary } from '../types'

const summary = ref<DashboardSummary | null>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await getDashboardSummary()
    summary.value = res.data
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <AppLayout title="Dashboard">
    <template #default>
        <div v-if="loading" class="flex justify-center items-center h-64">
          <ProgressSpinner />
        </div>
        <div v-else-if="summary" class="flex flex-col gap-6">
          <section>
            <h2 class="text-lg font-semibold mb-3 text-surface-700">Accounts</h2>
            <div class="flex flex-wrap gap-4">
              <BalanceCard
                v-for="a in summary.accounts"
                :key="a.id"
                :name="a.name"
                :currency="a.currency"
                :current_balance="a.current_balance"
              />
              <p v-if="!summary.accounts.length" class="text-surface-400 text-sm">No accounts yet.</p>
            </div>
          </section>

          <section>
            <h2 class="text-lg font-semibold mb-3 text-surface-700">Cash Flow</h2>
            <Card>
              <template #content>
                <CashFlowChart :data="summary.monthly_cashflow" />
              </template>
            </Card>
          </section>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <section>
              <h2 class="text-lg font-semibold mb-3 text-surface-700">Budget Progress</h2>
              <Card>
                <template #content>
                  <BudgetProgress :items="summary.budget_progress" />
                </template>
              </Card>
            </section>

            <section>
              <h2 class="text-lg font-semibold mb-3 text-surface-700">Recent Transactions</h2>
              <Card>
                <template #content>
                  <div class="overflow-x-auto">
                    <DataTable :value="summary.recent_transactions" size="small">
                      <Column field="date" header="Date" />
                      <Column field="description" header="Description" />
                      <Column field="amount" header="Amount">
                        <template #body="{ data }">
                          <span :class="data.type === 'income' ? 'text-green-600' : 'text-red-600'">
                            {{ data.type === 'expense' ? '-' : '+' }}{{ data.amount.toFixed(2) }}
                          </span>
                        </template>
                      </Column>
                      <Column field="type" header="Type">
                        <template #body="{ data }">
                          <span
                            class="px-2 py-0.5 rounded text-xs font-medium"
                            :class="data.type === 'income' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                          >{{ data.type }}</span>
                        </template>
                      </Column>
                    </DataTable>
                  </div>
                </template>
              </Card>
            </section>
          </div>
        </div>
    </template>
  </AppLayout>
</template>
