<script setup>
import { computed, ref, watch } from "vue";
import ItemCard from "../components/ItemCard.vue";
import LoadingCards from "../components/LoadingCards.vue";
import { useTeaLibrary } from "../composables/useTeaLibrary";

const props = defineProps({
  categoryId: {
    type: String,
    required: true,
  },
});

const { isLoading, error, ensureLoaded, getCategoryById, getCategoryDetail, getSubcategoryItems } =
  useTeaLibrary();

const activeCategoryDetail = ref(null);
const items = ref([]);

const activeCategory = computed(() => activeCategoryDetail.value || getCategoryById(props.categoryId));

const filteredItems = computed(() => {
  return items.value;
});

async function loadCategoryPage(categoryId) {
  activeCategoryDetail.value = null;
  items.value = [];

  return Promise.all([ensureLoaded(), getCategoryDetail(categoryId)])
    .then(async ([, categoryDetail]) => {
      activeCategoryDetail.value = categoryDetail;
      const results = await Promise.all(
        categoryDetail.subcategories.map((subcategory) => getSubcategoryItems(subcategory.slug)),
      );
      items.value = results.flatMap((result) => result.items);
    })
    .catch((loadError) => {
      console.error(loadError);
    });
}

watch(
  () => props.categoryId,
  (categoryId) => {
    loadCategoryPage(categoryId);
  },
  { immediate: true },
);
</script>

<template>
  <main class="page-stack">
    <section class="section-banner">
      <div>
        <p class="eyebrow">Library Section</p>
        <h2>{{ activeCategory?.name || "资料分类" }}</h2>
        <p class="banner-copy">
          {{ activeCategory?.description || "当前分类不存在，请返回首页重新选择。" }}
        </p>
      </div>
      <div class="banner-side">
        <span class="banner-chip">分类页</span>
        <strong>{{ filteredItems.length || activeCategory?.item_count || 0 }}</strong>
      </div>
    </section>

    <section class="library-layout library-layout-single">
      <div class="library-main">
        <LoadingCards v-if="isLoading" />

        <p v-else-if="error" class="empty-state">{{ error }}</p>

        <div v-else-if="activeCategory" class="card-grid">
          <ItemCard
            v-for="item in filteredItems"
            :key="item.slug"
            :item="item"
            :category-id="activeCategory.slug"
          />
        </div>

        <p v-else class="empty-state">未找到该分类。</p>
      </div>
    </section>
  </main>
</template>
