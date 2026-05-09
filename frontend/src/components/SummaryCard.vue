<script setup lang="ts">
import type { Component } from 'vue';

defineProps<{
  title: string;
  amount: number;
  tone: 'green' | 'red' | 'blue';
  icon: Component;
}>();

const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
});
</script>

<template>
  <article class="summary-card" :class="`summary-card--${tone}`">
    <div class="summary-card__icon" aria-hidden="true">
      <component :is="icon" :size="38" :stroke-width="2.3" />
    </div>
    <div class="summary-card__content">
      <p class="summary-card__title">{{ title }}</p>
      <p class="summary-card__amount">{{ currencyFormatter.format(amount) }}</p>
    </div>
  </article>
</template>
