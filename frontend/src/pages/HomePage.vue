<script setup>
import { computed, onMounted } from "vue";
import { useTeaLibrary } from "../composables/useTeaLibrary";

const { categories, ensureLoaded } = useTeaLibrary();
const firstCategorySlug = computed(() => categories.value[0]?.slug || "tea-ware");

onMounted(() => {
  ensureLoaded().catch((error) => {
    console.error(error);
  });
});
</script>

<template>
  <main>
    <section class="home-cover" aria-label="茶文化首页封面">
      <div class="home-cover-image">
        <h2>Memory的茶室</h2>
        <router-link class="cover-entry" :to="`/library/${firstCategorySlug}`">进入茶室</router-link>
      </div>
    </section>
  </main>
</template>
