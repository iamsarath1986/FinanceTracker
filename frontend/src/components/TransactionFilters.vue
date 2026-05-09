<template>
  <div class="filters" aria-label="Transaction filters">
    <label class="sr-only" for="type-filter">Type filter</label>
    <select id="type-filter" class="filter-control">
      <option>All types</option>
      <option>Income</option>
      <option>Expense</option>
    </select>

    <label class="sr-only" for="category-filter">Category filter</label>
    <select id="category-filter" class="filter-control">
      <option>All categories</option>
      <option>Salary</option>
      <option>Food</option>
      <option>Utilities</option>
      <option>Transport</option>
      <option>Entertainment</option>
    </select>
  </div>
</template>
