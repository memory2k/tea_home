import { createRouter, createWebHistory } from "vue-router";
import HomePage from "./pages/HomePage.vue";
import LibraryPage from "./pages/LibraryPage.vue";
import ItemDetailPage from "./pages/ItemDetailPage.vue";
import NotFoundPage from "./pages/NotFoundPage.vue";

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior() {
    return { top: 0 };
  },
  routes: [
    {
      path: "/",
      name: "home",
      component: HomePage,
    },
    {
      path: "/library/:categoryId",
      name: "library",
      component: LibraryPage,
      props: true,
    },
    {
      path: "/library/:categoryId/:itemId",
      name: "item-detail",
      component: ItemDetailPage,
      props: true,
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: NotFoundPage,
    },
  ],
});

export default router;
