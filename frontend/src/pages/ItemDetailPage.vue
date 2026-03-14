<script setup>
import { onMounted, ref } from "vue";
import LoadingCards from "../components/LoadingCards.vue";
import { useTeaLibrary } from "../composables/useTeaLibrary";

const props = defineProps({
  categoryId: {
    type: String,
    required: true,
  },
  itemId: {
    type: String,
    required: true,
  },
});

const { isLoading, error, ensureLoaded, getItemById } = useTeaLibrary();

const item = ref(null);

onMounted(() => {
  Promise.all([ensureLoaded(), getItemById(props.itemId)])
    .then(([, itemDetail]) => {
      item.value = itemDetail;
    })
    .catch((loadError) => {
      console.error(loadError);
    });
});
</script>

<template>
  <main class="page-stack">
    <section class="detail-hero">
      <div class="detail-hero-copy">
        <p class="eyebrow">Archive Entry</p>
        <h2>{{ item?.name || "资料详情" }}</h2>
        <p class="detail-summary large">
          {{ item?.summary || "当前条目不存在，请返回分类页重新选择。" }}
        </p>
        <div class="detail-meta">
          <span>{{ item?.category_name }}</span>
          <span>{{ item?.subcategory_name }}</span>
          <span>{{ item?.origin }}</span>
        </div>
      </div>
      <div class="detail-hero-side">
        <router-link class="button button-secondary" :to="`/library/${categoryId}`">
          返回分类页
        </router-link>
      </div>
    </section>

    <LoadingCards v-if="isLoading" />

    <p v-else-if="error" class="empty-state">{{ error }}</p>

    <section v-else-if="item" class="detail-layout">
      <article class="detail-sheet">
        <dl class="detail-list">
          <div>
            <dt>产地 / 来源</dt>
            <dd>{{ item.origin }}</dd>
          </div>
          <div>
            <dt>核心特征</dt>
            <dd>{{ item.features.join(" / ") }}</dd>
          </div>
          <div>
            <dt>适用场景</dt>
            <dd>{{ item.scene }}</dd>
          </div>
          <div>
            <dt>适配建议</dt>
            <dd>{{ item.pairing }}</dd>
          </div>
          <div>
            <dt>备注</dt>
            <dd>{{ item.notes }}</dd>
          </div>
        </dl>
      </article>

      <aside class="detail-sidebar">
        <article class="side-card">
          <p class="panel-label">关键词</p>
          <div class="tag-list">
            <span v-for="tag in item.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>
        </article>

        <article v-if="item.purchase_links?.length" class="side-card">
          <p class="panel-label">购买链接</p>
          <div class="related-list">
            <a
              v-for="link in item.purchase_links"
              :key="link.url"
              class="related-link"
              :href="link.url"
              target="_blank"
              rel="noreferrer"
            >
              <strong>{{ link.label }}</strong>
              <span>{{ link.platform }}</span>
            </a>
          </div>
        </article>
      </aside>
    </section>

    <p v-else class="empty-state">未找到该条资料。</p>
  </main>
</template>
