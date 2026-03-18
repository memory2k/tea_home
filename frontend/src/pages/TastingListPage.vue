<script setup>
import { onMounted, ref } from "vue";
import { useTasting } from "../composables/useTasting";

const { listRecords } = useTasting();

const records = ref([]);
const isLoading = ref(true);
const error = ref("");

onMounted(() => {
  listRecords()
    .then((data) => {
      records.value = data;
    })
    .catch(() => {
      error.value = "记录读取失败，请检查后端服务。";
    })
    .finally(() => {
      isLoading.value = false;
    });
});

function formatDate(iso) {
  return new Date(iso).toLocaleDateString("zh-CN", { year: "numeric", month: "long", day: "numeric" });
}

function formatTime(iso) {
  return new Date(iso).toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" });
}

function starLabel(rating) {
  return "★".repeat(rating) + "☆".repeat(5 - rating);
}

function itemsByCategory(items) {
  const groups = {};
  for (const item of items) {
    const k = item.category_name;
    if (!groups[k]) groups[k] = [];
    groups[k].push(item.name);
  }
  return groups;
}
</script>

<template>
  <main class="page-stack">
    <section class="detail-hero">
      <div class="detail-hero-copy">
        <p class="eyebrow">Tasting Journal</p>
        <h2>品茗记录</h2>
        <p class="detail-summary large">记录每一次与茶的相遇。</p>
      </div>
      <div class="detail-hero-side">
        <router-link class="button button-primary" to="/tasting/new">+ 新记录</router-link>
      </div>
    </section>

    <div v-if="isLoading" class="loading-state">
      <div class="loading-card" style="height: 100px"></div>
      <div class="loading-card" style="height: 100px"></div>
      <div class="loading-card" style="height: 100px"></div>
    </div>

    <p v-else-if="error" class="empty-state">{{ error }}</p>

    <p v-else-if="records.length === 0" class="empty-state">
      尚无品茗记录。点击右上方「+ 新记录」开始记录。
    </p>

    <section v-else class="tasting-timeline">
      <router-link
        v-for="record in records"
        :key="record.id"
        class="tasting-card"
        :to="`/tasting/${record.id}`"
      >
        <div class="tasting-card-date">
          <span class="tasting-date-day">{{ formatDate(record.date) }}</span>
          <span class="tasting-date-time">{{ formatTime(record.date) }}</span>
        </div>
        <div class="tasting-card-body">
          <div class="tasting-card-top">
            <span v-if="record.rating" class="tasting-rating">{{ starLabel(record.rating) }}</span>
            <span v-if="record.location" class="tasting-meta-chip">{{ record.location }}</span>
            <span v-if="record.participants" class="tasting-meta-chip">{{ record.participants }}</span>
          </div>
          <div v-if="record.items.length" class="tasting-items-row">
            <template v-for="(names, cat) in itemsByCategory(record.items)" :key="cat">
              <span class="tasting-cat-label">{{ cat }}</span>
              <span class="tasting-item-names">{{ names.join("、") }}</span>
            </template>
          </div>
          <p v-if="record.taste" class="tasting-card-taste">{{ record.taste }}</p>
        </div>
      </router-link>
    </section>
  </main>
</template>

<style scoped>
.tasting-timeline {
  display: grid;
  gap: 14px;
}

.tasting-card {
  display: flex;
  gap: 20px;
  align-items: start;
  padding: 20px 24px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--line);
  background: var(--paper);
  backdrop-filter: blur(18px);
  box-shadow: var(--shadow-soft);
  color: inherit;
  text-decoration: none;
  transition:
    transform 220ms ease-out,
    box-shadow 220ms ease-out,
    border-color 220ms ease-out;
}

.tasting-card:hover {
  transform: translateY(-2px);
  border-color: rgba(53, 95, 74, 0.2);
  box-shadow: var(--shadow);
}

.tasting-card-date {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 120px;
  padding-top: 2px;
}

.tasting-date-day {
  font-size: 0.92rem;
  font-weight: 500;
  color: var(--primary);
}

.tasting-date-time {
  font-size: 0.82rem;
  color: var(--muted);
}

.tasting-card-body {
  flex: 1;
  min-width: 0;
}

.tasting-card-top {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.tasting-rating {
  font-size: 0.9rem;
  color: var(--accent);
  letter-spacing: 0.05em;
}

.tasting-meta-chip {
  font-size: 0.82rem;
  color: var(--muted);
  padding: 2px 10px;
  border-radius: 999px;
  background: rgba(83, 63, 39, 0.07);
}

.tasting-items-row {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 6px 10px;
  margin-bottom: 8px;
}

.tasting-cat-label {
  font-size: 0.78rem;
  color: var(--muted);
  background: rgba(53, 95, 74, 0.08);
  padding: 1px 8px;
  border-radius: 999px;
}

.tasting-item-names {
  font-size: 0.92rem;
  font-weight: 500;
  color: var(--primary-deep);
  font-family: "Noto Serif SC", serif;
}

.tasting-card-taste {
  margin: 0;
  font-size: 0.92rem;
  color: var(--muted);
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@media (max-width: 600px) {
  .tasting-card {
    flex-direction: column;
    gap: 10px;
  }
  .tasting-card-date {
    flex-direction: row;
    gap: 10px;
    min-width: unset;
  }
}
</style>
