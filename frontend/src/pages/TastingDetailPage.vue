<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useTasting } from "../composables/useTasting";

const props = defineProps({
  id: { type: String, required: true },
});

const router = useRouter();
const { getRecord, deleteRecord } = useTasting();

const record = ref(null);
const isLoading = ref(true);
const error = ref("");
const isDeleting = ref(false);

onMounted(() => {
  getRecord(props.id)
    .then((data) => { record.value = data; })
    .catch(() => { error.value = "记录读取失败，请检查后端服务。"; })
    .finally(() => { isLoading.value = false; });
});

const itemsByCategory = computed(() => {
  if (!record.value) return {};
  const groups = {};
  for (const item of record.value.items) {
    const k = item.category_name;
    if (!groups[k]) groups[k] = [];
    groups[k].push(item);
  }
  return groups;
});

function formatDatetime(iso) {
  if (!iso) return "";
  return new Date(iso).toLocaleString("zh-CN", {
    year: "numeric", month: "long", day: "numeric",
    hour: "2-digit", minute: "2-digit",
  });
}

function starLabel(rating) {
  if (!rating) return "";
  return "★".repeat(rating) + "☆".repeat(5 - rating);
}

async function handleDelete() {
  if (!confirm("确认删除这条品茗记录？此操作无法撤销。")) return;
  isDeleting.value = true;
  try {
    await deleteRecord(props.id);
    router.push("/tasting");
  } catch {
    alert("删除失败，请重试。");
    isDeleting.value = false;
  }
}
</script>

<template>
  <main class="page-stack">
    <div v-if="isLoading" class="loading-state">
      <div class="loading-card" style="height: 120px"></div>
    </div>

    <p v-else-if="error" class="empty-state">{{ error }}</p>

    <template v-else-if="record">
      <section class="detail-hero">
        <div class="detail-hero-copy">
          <p class="eyebrow">{{ formatDatetime(record.date) }}</p>
          <h2>{{ record.items.length ? record.items.map(i => i.name).join(" · ") : "品茗记录" }}</h2>
          <div class="detail-meta" v-if="record.rating">
            <span class="tasting-rating">{{ starLabel(record.rating) }}</span>
          </div>
        </div>
        <div class="detail-hero-side">
          <div class="detail-actions">
            <router-link class="button button-secondary" :to="`/tasting/${id}/edit`">编辑</router-link>
            <button class="button button-danger" :disabled="isDeleting" @click="handleDelete">
              {{ isDeleting ? "删除中…" : "删除" }}
            </button>
          </div>
        </div>
      </section>

      <section class="detail-layout">
        <article class="detail-sheet">
          <dl class="detail-list">
            <div v-if="record.color">
              <dt>汤色</dt>
              <dd>{{ record.color }}</dd>
            </div>
            <div v-if="record.aroma">
              <dt>香气</dt>
              <dd>{{ record.aroma }}</dd>
            </div>
            <div v-if="record.taste">
              <dt>口感</dt>
              <dd>{{ record.taste }}</dd>
            </div>
            <div v-if="record.notes">
              <dt>备注</dt>
              <dd>{{ record.notes }}</dd>
            </div>
          </dl>
        </article>

        <aside class="detail-sidebar">
          <!-- 条目（按分类分组） -->
          <article v-if="record.items.length" class="side-card">
            <p class="panel-label">本次使用</p>
            <div v-for="(items, cat) in itemsByCategory" :key="cat" class="item-group">
              <p class="item-group-cat">{{ cat }}</p>
              <router-link
                v-for="item in items"
                :key="item.id"
                class="related-link"
                :to="`/library/${item.category_slug}/${item.slug}`"
              >
                <strong>{{ item.name }}</strong>
                <span>{{ item.subcategory_name }}</span>
              </router-link>
            </div>
          </article>

          <!-- 冲泡参数 -->
          <article class="side-card">
            <p class="panel-label">冲泡参数</p>
            <dl class="detail-list">
              <div v-if="record.water_temp">
                <dt>水温</dt>
                <dd>{{ record.water_temp }} ℃</dd>
              </div>
              <div v-if="record.steep_time">
                <dt>浸泡时长</dt>
                <dd>{{ record.steep_time }} 秒</dd>
              </div>
              <div v-if="record.tea_amount">
                <dt>用茶量</dt>
                <dd>{{ record.tea_amount }}</dd>
              </div>
              <div v-if="record.water_type">
                <dt>用水</dt>
                <dd>{{ record.water_type }}</dd>
              </div>
            </dl>
          </article>

          <!-- 环境 -->
          <article class="side-card">
            <p class="panel-label">环境</p>
            <dl class="detail-list">
              <div v-if="record.location">
                <dt>地点</dt>
                <dd>{{ record.location }}</dd>
              </div>
              <div v-if="record.weather">
                <dt>天气</dt>
                <dd>{{ record.weather }}</dd>
              </div>
              <div v-if="record.participants">
                <dt>参与人</dt>
                <dd>{{ record.participants }}</dd>
              </div>
            </dl>
          </article>
        </aside>
      </section>

      <div class="tasting-back">
        <router-link class="text-link" to="/tasting">← 返回品茗记录</router-link>
      </div>
    </template>

    <p v-else class="empty-state">未找到该条记录。</p>
  </main>
</template>

<style scoped>
.detail-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.button-danger {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  padding: 0 20px;
  border-radius: 999px;
  border: 1px solid rgba(192, 57, 43, 0.2);
  background: rgba(255, 235, 235, 0.6);
  color: #c0392b;
  cursor: pointer;
  font: inherit;
  transition: background-color 220ms ease-out, transform 220ms ease-out;
}

.button-danger:hover:not(:disabled) {
  background: rgba(192, 57, 43, 0.12);
  transform: translateY(-1px);
}

.button-danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.tasting-rating {
  font-size: 1rem;
  color: var(--accent);
  letter-spacing: 0.06em;
}

.item-group {
  margin-top: 14px;
}

.item-group:first-child {
  margin-top: 10px;
}

.item-group-cat {
  margin: 0 0 8px;
  font-size: 0.8rem;
  color: var(--muted);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.related-link {
  display: grid;
  gap: 4px;
  padding: 14px;
  border-radius: 16px;
  background: rgba(255, 252, 247, 0.84);
  border: 1px solid rgba(83, 63, 39, 0.08);
  color: inherit;
  text-decoration: none;
  transition: transform 220ms ease-out, border-color 220ms ease-out;
}

.related-link + .related-link {
  margin-top: 8px;
}

.related-link:hover {
  transform: translateY(-1px);
  border-color: rgba(53, 95, 74, 0.2);
}

.related-link span {
  color: var(--muted);
  font-size: 0.92rem;
}

.tasting-back {
  padding: 8px 0;
}

.text-link {
  color: var(--primary);
  text-decoration: none;
  font-size: 0.9rem;
}

.text-link:hover {
  text-decoration: underline;
}
</style>
