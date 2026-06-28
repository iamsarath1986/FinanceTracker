<script setup lang="ts">
import type { LegacyTransaction as Transaction } from '../types/legacy';

defineProps<{
  transactions: Transaction[];
}>();

const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
});
</script>

<template>
  <div class="table-wrap">
    <table class="transactions-table">
      <thead>
        <tr>
          <th scope="col">Date</th>
          <th scope="col">Description</th>
          <th scope="col">Category</th>
          <th scope="col">Amount</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="transaction in transactions" :key="transaction.id">
          <td>{{ transaction.date }}</td>
          <td class="description-cell">{{ transaction.description }}</td>
          <td>
            <span class="badge" :class="`badge--${transaction.category.toLowerCase()}`">
              {{ transaction.category }}
            </span>
          </td>
          <td
            class="amount-cell"
            :class="transaction.type === 'income' ? 'amount-cell--income' : 'amount-cell--expense'"
          >
            {{ currencyFormatter.format(transaction.amount) }}
          </td>
          <td>
            <div class="action-buttons" :aria-label="`Actions for ${transaction.description}`">
              <button class="icon-button icon-button--edit" type="button" aria-label="Edit transaction">
                <i class="pi pi-pencil" aria-hidden="true" />
              </button>
              <button class="icon-button icon-button--delete" type="button" aria-label="Delete transaction">
                <i class="pi pi-trash" aria-hidden="true" />
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
