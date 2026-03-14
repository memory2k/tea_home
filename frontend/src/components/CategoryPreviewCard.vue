<script setup>
defineProps({
  category: {
    type: Object,
    required: true,
  },
});
</script>

<template>
  <article class="category-preview-card">
    <div class="taxonomy-index">0{{ category.order }}</div>
    <p class="eyebrow">{{ category.name }}</p>
    <h3>{{ category.description }}</h3>
    <ul class="preview-list">
      <li v-for="sub in category.subcategories" :key="sub.id">{{ sub.name }}</li>
    </ul>
    <div class="preview-meta">
      <span>{{ category.items.length }} 条条目</span>
      <router-link class="text-link" :to="`/library/${category.id}`">进入分类</router-link>
    </div>
  </article>
</template>
