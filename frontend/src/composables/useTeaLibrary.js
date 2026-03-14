import { computed, ref } from "vue";

const isLoading = ref(false);
const error = ref("");
const categories = ref([]);

let loadPromise;

async function ensureLoaded() {
  if (categories.value.length) {
    return categories.value;
  }

  if (!loadPromise) {
    isLoading.value = true;
    error.value = "";
    loadPromise = fetch("/api/categories/")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Failed to load data: ${response.status}`);
        }

        return response.json();
      })
      .then((payload) => {
        categories.value = payload;
        return categories.value;
      })
      .catch((loadError) => {
        error.value = "资料库读取失败，请检查后端服务。";
        throw loadError;
      })
      .finally(() => {
        isLoading.value = false;
      });
  }

  return loadPromise;
}

export function useTeaLibrary() {
  const summary = computed(() => {
    const categoryCount = categories.value.length;
    const subcategoryCount = categories.value.reduce((total, item) => total + (item.subcategory_count || 0), 0);
    const totalItems = categories.value.reduce((total, item) => total + (item.item_count || 0), 0);

    return {
      categoryCount,
      subcategoryCount,
      totalItems,
    };
  });

  function getCategoryById(categoryId) {
    return categories.value.find((category) => category.slug === categoryId) || null;
  }

  async function getCategoryDetail(categoryId) {
    const response = await fetch(`/api/categories/${categoryId}/`);
    if (!response.ok) {
      throw new Error(`Failed to load category detail: ${response.status}`);
    }
    return response.json();
  }

  async function getSubcategoryItems(subcategoryId) {
    const response = await fetch(`/api/subcategories/${subcategoryId}/items/`);
    if (!response.ok) {
      throw new Error(`Failed to load subcategory items: ${response.status}`);
    }
    return response.json();
  }

  async function getItemById(itemId) {
    const response = await fetch(`/api/items/${itemId}/`);
    if (!response.ok) {
      throw new Error(`Failed to load item detail: ${response.status}`);
    }
    return response.json();
  }

  return {
    isLoading,
    error,
    categories,
    summary,
    ensureLoaded,
    getCategoryById,
    getCategoryDetail,
    getSubcategoryItems,
    getItemById,
  };
}
