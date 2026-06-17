<script setup lang="ts">
import { computed } from 'vue'
import Chart from 'primevue/chart'

const props = defineProps<{
  data: { month: string; income: number; expense: number }[]
}>()

const chartData = computed(() => ({
  labels: props.data.map((d) => d.month),
  datasets: [
    {
      label: 'Income',
      data: props.data.map((d) => d.income),
      backgroundColor: '#22c55e',
    },
    {
      label: 'Expense',
      data: props.data.map((d) => d.expense),
      backgroundColor: '#ef4444',
    },
  ],
}))

const chartOptions = {
  responsive: true,
  plugins: { legend: { position: 'top' } },
}
</script>

<template>
  <Chart type="bar" :data="chartData" :options="chartOptions" class="w-full" />
</template>
