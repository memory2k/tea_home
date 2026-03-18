import { createRouter, createWebHistory } from "vue-router";
import HomePage from "./pages/HomePage.vue";
import LibraryPage from "./pages/LibraryPage.vue";
import ItemDetailPage from "./pages/ItemDetailPage.vue";
import TastingListPage from "./pages/TastingListPage.vue";
import TastingFormPage from "./pages/TastingFormPage.vue";
import TastingDetailPage from "./pages/TastingDetailPage.vue";
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
      path: "/tasting",
      name: "tasting-list",
      component: TastingListPage,
    },
    {
      path: "/tasting/new",
      name: "tasting-new",
      component: TastingFormPage,
    },
    {
      path: "/tasting/:id",
      name: "tasting-detail",
      component: TastingDetailPage,
      props: true,
    },
    {
      path: "/tasting/:id/edit",
      name: "tasting-edit",
      component: TastingFormPage,
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
