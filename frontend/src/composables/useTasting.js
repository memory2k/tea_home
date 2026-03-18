import { ref } from "vue";

const allItems = ref([]);
let itemsLoadPromise = null;

async function fetchAllItems() {
  if (allItems.value.length) return allItems.value;
  if (!itemsLoadPromise) {
    itemsLoadPromise = fetch("/api/items/")
      .then((r) => {
        if (!r.ok) throw new Error(`Failed to load items: ${r.status}`);
        return r.json();
      })
      .then((data) => {
        allItems.value = data;
        return data;
      });
  }
  return itemsLoadPromise;
}

export function useTasting() {
  async function listRecords() {
    const r = await fetch("/api/tasting/records/");
    if (!r.ok) throw new Error(`Failed to load records: ${r.status}`);
    return r.json();
  }

  async function getRecord(id) {
    const r = await fetch(`/api/tasting/records/${id}/`);
    if (!r.ok) throw new Error(`Failed to load record: ${r.status}`);
    return r.json();
  }

  async function createRecord(data) {
    const r = await fetch("/api/tasting/records/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!r.ok) {
      const err = await r.json().catch(() => ({}));
      throw Object.assign(new Error("Create failed"), { errors: err });
    }
    return r.json();
  }

  async function updateRecord(id, data) {
    const r = await fetch(`/api/tasting/records/${id}/`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!r.ok) {
      const err = await r.json().catch(() => ({}));
      throw Object.assign(new Error("Update failed"), { errors: err });
    }
    return r.json();
  }

  async function deleteRecord(id) {
    const r = await fetch(`/api/tasting/records/${id}/`, { method: "DELETE" });
    if (!r.ok) throw new Error(`Delete failed: ${r.status}`);
  }

  return {
    allItems,
    fetchAllItems,
    listRecords,
    getRecord,
    createRecord,
    updateRecord,
    deleteRecord,
  };
}
