<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useTasting } from "../composables/useTasting";

const props = defineProps({
  id: { type: String, default: null },
});

const router = useRouter();
const { allItems, fetchAllItems, getRecord, createRecord, updateRecord } = useTasting();

const isEdit = computed(() => !!props.id);
const isLoading = ref(true);
const isSaving = ref(false);
const loadError = ref("");
const saveErrors = ref({});

const form = ref({
  date: "",
  water_temp: "",
  steep_time: "",
  tea_amount: "",
  water_type: "",
  aroma: "",
  taste: "",
  color: "",
  rating: null,
  notes: "",
  weather: "",
  location: "",
  participants: "",
});

const selectedItemIds = ref(new Set());

const groupedItems = computed(() => {
  const groups = {};
  for (const item of allItems.value) {
    const key = item.category_name;
    if (!groups[key]) groups[key] = [];
    groups[key].push(item);
  }
  return groups;
});

function toLocalDatetimeInput(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  const pad = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

function nowLocalDatetimeInput() {
  return toLocalDatetimeInput(new Date().toISOString());
}

onMounted(async () => {
  try {
    await fetchAllItems();
    if (isEdit.value) {
      const record = await getRecord(props.id);
      form.value = {
        date: toLocalDatetimeInput(record.date),
        water_temp: record.water_temp ?? "",
        steep_time: record.steep_time ?? "",
        tea_amount: record.tea_amount,
        water_type: record.water_type,
        aroma: record.aroma,
        taste: record.taste,
        color: record.color,
        rating: record.rating,
        notes: record.notes,
        weather: record.weather,
        location: record.location,
        participants: record.participants,
      };
      selectedItemIds.value = new Set(record.items.map((i) => i.id));
    } else {
      form.value.date = nowLocalDatetimeInput();
    }
  } catch {
    loadError.value = "数据读取失败，请检查后端服务。";
  } finally {
    isLoading.value = false;
  }
});

function toggleItem(id) {
  const s = new Set(selectedItemIds.value);
  if (s.has(id)) s.delete(id);
  else s.add(id);
  selectedItemIds.value = s;
}

function buildPayload() {
  const p = { ...form.value };
  if (!p.water_temp) delete p.water_temp;
  else p.water_temp = Number(p.water_temp);
  if (!p.steep_time) delete p.steep_time;
  else p.steep_time = Number(p.steep_time);
  if (!p.rating) p.rating = null;
  p.item_ids = [...selectedItemIds.value];
  return p;
}

async function handleSubmit() {
  saveErrors.value = {};
  isSaving.value = true;
  try {
    const payload = buildPayload();
    if (isEdit.value) {
      await updateRecord(props.id, payload);
      router.push(`/tasting/${props.id}`);
    } else {
      const record = await createRecord(payload);
      router.push(`/tasting/${record.id}`);
    }
  } catch (e) {
    saveErrors.value = e.errors || { detail: "保存失败，请重试。" };
  } finally {
    isSaving.value = false;
  }
}

function setRating(val) {
  form.value.rating = form.value.rating === val ? null : val;
}
</script>

<template>
  <main class="page-stack">
    <section class="detail-hero">
      <div class="detail-hero-copy">
        <p class="eyebrow">Tasting Journal</p>
        <h2>{{ isEdit ? "编辑记录" : "新建品茗记录" }}</h2>
      </div>
      <div class="detail-hero-side">
        <router-link class="button button-secondary" to="/tasting">返回列表</router-link>
      </div>
    </section>

    <div v-if="isLoading" class="loading-state">
      <div class="loading-card" style="height: 120px"></div>
    </div>

    <p v-else-if="loadError" class="empty-state">{{ loadError }}</p>

    <form v-else class="tasting-form" @submit.prevent="handleSubmit">
      <div v-if="Object.keys(saveErrors).length" class="form-errors">
        <p v-for="(msgs, field) in saveErrors" :key="field" class="form-error-line">
          <strong v-if="field !== 'detail'">{{ field }}：</strong>{{ Array.isArray(msgs) ? msgs.join(" ") : msgs }}
        </p>
      </div>

      <!-- 基本信息 -->
      <div class="form-section">
        <p class="form-section-title">基本信息</p>
        <div class="form-row">
          <label class="form-label" for="date">品茗时间</label>
          <input id="date" v-model="form.date" type="datetime-local" class="form-input" required />
        </div>
      </div>

      <!-- 条目选择（按分类多选） -->
      <div v-for="(items, category) in groupedItems" :key="category" class="form-section">
        <p class="form-section-title">{{ category }}</p>
        <div class="item-checkbox-grid">
          <label
            v-for="item in items"
            :key="item.id"
            class="item-checkbox-label"
            :class="{ selected: selectedItemIds.has(item.id) }"
          >
            <input
              type="checkbox"
              :value="item.id"
              :checked="selectedItemIds.has(item.id)"
              @change="toggleItem(item.id)"
              class="item-checkbox-input"
            />
            <span class="item-checkbox-sub">{{ item.subcategory_name }}</span>
            <span class="item-checkbox-name">{{ item.name }}</span>
          </label>
        </div>
      </div>

      <!-- 冲泡参数 -->
      <div class="form-section">
        <p class="form-section-title">冲泡参数</p>
        <div class="form-grid">
          <div class="form-row">
            <label class="form-label" for="water_temp">水温（℃）</label>
            <input id="water_temp" v-model="form.water_temp" type="number" min="50" max="100" class="form-input" placeholder="如 95" />
          </div>
          <div class="form-row">
            <label class="form-label" for="steep_time">浸泡时长（秒）</label>
            <input id="steep_time" v-model="form.steep_time" type="number" min="5" class="form-input" placeholder="如 30" />
          </div>
          <div class="form-row">
            <label class="form-label" for="tea_amount">用茶量</label>
            <input id="tea_amount" v-model="form.tea_amount" type="text" class="form-input" placeholder="如 5g" />
          </div>
          <div class="form-row">
            <label class="form-label" for="water_type">用水</label>
            <input id="water_type" v-model="form.water_type" type="text" class="form-input" placeholder="如 农夫山泉" />
          </div>
        </div>
      </div>

      <!-- 品评 -->
      <div class="form-section">
        <p class="form-section-title">品评</p>
        <div class="form-row">
          <label class="form-label">评分</label>
          <div class="star-picker">
            <button
              v-for="n in 5"
              :key="n"
              type="button"
              class="star-btn"
              :class="{ active: form.rating !== null && n <= form.rating }"
              @click="setRating(n)"
              :aria-label="`${n} 星`"
            >★</button>
          </div>
        </div>
        <div class="form-row">
          <label class="form-label" for="color">汤色</label>
          <input id="color" v-model="form.color" type="text" class="form-input" placeholder="如 橙黄透亮" />
        </div>
        <div class="form-row">
          <label class="form-label" for="aroma">香气</label>
          <textarea id="aroma" v-model="form.aroma" class="form-input form-textarea" placeholder="描述茶香"></textarea>
        </div>
        <div class="form-row">
          <label class="form-label" for="taste">口感</label>
          <textarea id="taste" v-model="form.taste" class="form-input form-textarea" placeholder="描述入口感受"></textarea>
        </div>
      </div>

      <!-- 附记 -->
      <div class="form-section">
        <p class="form-section-title">附记</p>
        <div class="form-grid">
          <div class="form-row">
            <label class="form-label" for="location">地点</label>
            <input id="location" v-model="form.location" type="text" class="form-input" placeholder="如 家中书房" />
          </div>
          <div class="form-row">
            <label class="form-label" for="weather">天气</label>
            <input id="weather" v-model="form.weather" type="text" class="form-input" placeholder="如 晴，微风" />
          </div>
        </div>
        <div class="form-row">
          <label class="form-label" for="participants">参与人</label>
          <input id="participants" v-model="form.participants" type="text" class="form-input" placeholder="如 张三、李四" />
        </div>
        <div class="form-row">
          <label class="form-label" for="notes">备注</label>
          <textarea id="notes" v-model="form.notes" class="form-input form-textarea" placeholder="其他想记录的内容"></textarea>
        </div>
      </div>

      <div class="form-actions">
        <router-link class="button button-secondary" to="/tasting">取消</router-link>
        <button type="submit" class="button button-primary" :disabled="isSaving">
          {{ isSaving ? "保存中…" : isEdit ? "保存修改" : "创建记录" }}
        </button>
      </div>
    </form>
  </main>
</template>

<style scoped>
.tasting-form {
  display: grid;
  gap: 18px;
}

.form-section {
  padding: 24px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--line);
  background: var(--paper);
  backdrop-filter: blur(18px);
  box-shadow: var(--shadow-soft);
}

.form-section-title {
  margin: 0 0 20px;
  font-family: "Noto Serif SC", serif;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--primary-deep);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.form-row {
  display: grid;
  gap: 6px;
}

.form-row + .form-row {
  margin-top: 14px;
}

.form-label {
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--text);
}

.form-input {
  width: 100%;
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid rgba(83, 63, 39, 0.18);
  background: rgba(255, 252, 247, 0.9);
  color: var(--text);
  font: inherit;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 200ms;
}

.form-input:focus {
  border-color: rgba(53, 95, 74, 0.4);
}

.form-textarea {
  min-height: 90px;
  resize: vertical;
}

/* 条目多选卡片 */
.item-checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 10px;
}

.item-checkbox-label {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: 12px 14px;
  border-radius: 14px;
  border: 1px solid rgba(83, 63, 39, 0.14);
  background: rgba(255, 252, 247, 0.8);
  cursor: pointer;
  transition:
    border-color 180ms,
    background-color 180ms,
    transform 180ms;
}

.item-checkbox-label:hover {
  border-color: rgba(53, 95, 74, 0.25);
  transform: translateY(-1px);
}

.item-checkbox-label.selected {
  border-color: rgba(53, 95, 74, 0.5);
  background: rgba(53, 95, 74, 0.1);
}

.item-checkbox-input {
  position: absolute;
  top: 10px;
  right: 12px;
  accent-color: var(--primary);
  width: 16px;
  height: 16px;
}

.item-checkbox-sub {
  font-size: 0.78rem;
  color: var(--muted);
  padding-right: 20px;
}

.item-checkbox-name {
  font-size: 0.92rem;
  font-weight: 500;
  color: var(--primary-deep);
  padding-right: 20px;
}

/* 星级 */
.star-picker {
  display: flex;
  gap: 4px;
}

.star-btn {
  font-size: 1.6rem;
  color: rgba(83, 63, 39, 0.22);
  cursor: pointer;
  padding: 0 2px;
  transition: color 150ms, transform 150ms;
  background: none;
  border: none;
  line-height: 1;
}

.star-btn.active {
  color: var(--accent);
}

.star-btn:hover {
  color: var(--accent);
  transform: scale(1.15);
}

.form-errors {
  padding: 16px 20px;
  border-radius: var(--radius-md);
  border: 1px solid rgba(192, 57, 43, 0.2);
  background: rgba(255, 235, 235, 0.6);
}

.form-error-line {
  margin: 0;
  font-size: 0.9rem;
  color: #c0392b;
}

.form-error-line + .form-error-line {
  margin-top: 6px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

@media (max-width: 600px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  .item-checkbox-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
