<script setup lang="ts">
import { Plus } from 'lucide-vue-next';
</script>

<template>
  <section class="panel add-transaction" aria-labelledby="add-transaction-title">
    <h2 id="add-transaction-title" class="section-title">Add Transaction</h2>

    <form class="transaction-form" @submit.prevent>
      <label class="field">
        <span class="field__label">Description</span>
        <input class="control" type="text" placeholder="e.g., Groceries" autocomplete="off" />
      </label>

      <label class="field">
        <span class="field__label">Amount</span>
        <input class="control" type="number" min="0" step="0.01" placeholder="0.00" />
      </label>

      <label class="field">
        <span class="field__label">Type</span>
        <select class="control">
          <option>Expense</option>
          <option>Income</option>
        </select>
      </label>

      <label class="field">
        <span class="field__label">Category</span>
        <select class="control">
          <option>Food</option>
          <option>Salary</option>
          <option>Utilities</option>
          <option>Transport</option>
          <option>Entertainment</option>
        </select>
      </label>

      <button class="add-button" type="submit">
        <Plus :size="18" :stroke-width="2.5" />
        <span>Add</span>
      </button>
    </form>
  </section>
</template>
