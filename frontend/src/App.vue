<script setup lang="ts">
import { Landmark, TrendingUp, WalletCards } from 'lucide-vue-next';
import SummaryCard from './components/SummaryCard.vue';
import TransactionFilters from './components/TransactionFilters.vue';
import TransactionForm from './components/TransactionForm.vue';
import TransactionTable from './components/TransactionTable.vue';
import { transactions } from './data/transactions';

const summary = {
  income: 1200,
  expenses: 450,
  balance: 750,
};
</script>

<template>
  <main class="dashboard-shell">
    <header class="dashboard-header">
      <div>
        <p class="eyebrow">Personal finance dashboard</p>
        <h1>Finance Tracker</h1>
      </div>
    </header>

    <section class="summary-grid" aria-label="Finance summary">
      <SummaryCard title="Income" :amount="summary.income" tone="green" :icon="WalletCards" />
      <SummaryCard title="Expenses" :amount="summary.expenses" tone="red" :icon="TrendingUp" />
      <SummaryCard title="Balance" :amount="summary.balance" tone="blue" :icon="Landmark" />
    </section>

    <TransactionForm />

    <section class="panel transactions-panel" aria-labelledby="transactions-title">
      <div class="transactions-panel__header">
        <h2 id="transactions-title" class="section-title">Transactions</h2>
        <TransactionFilters />
      </div>

      <TransactionTable :transactions="transactions" />
    </section>
  </main>
</template>
