<script setup>
defineProps({
  item: {
    type: Object,
    required: true,
  },
  categoryId: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <article class="info-card">
    <router-link class="card-hitarea" :to="`/library/${categoryId}/${item.slug}`">
      <div class="card-topline">
        <span>{{ item.subcategory_name }}</span>
        <span>{{ item.origin }}</span>
      </div>
      <h3>{{ item.name }}</h3>
      <p>{{ item.summary }}</p>
      <dl>
        <div>
          <dt>关键词</dt>
          <dd>{{ item.tags.join(" · ") }}</dd>
        </div>
        <div>
          <dt>适用场景</dt>
          <dd>{{ item.scene }}</dd>
        </div>
      </dl>
    </router-link>
    <div v-if="item.purchase_links?.length" class="card-actions">
      <a
        v-for="link in item.purchase_links"
        :key="link.url"
        class="buy-link"
        :href="link.url"
        target="_blank"
        rel="noreferrer"
      >
        {{ link.label }}
      </a>
    </div>
  </article>
</template>
