import { createRouter, createWebHistory } from "vue-router";

// function isAuthenticated() {
//   const userEmail = localStorage.getItem("email");
//   return userEmail !== null && userEmail !== undefined;
// }

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [ {
      path: "/",
      name: "/",
      component: () => import("../components/Login.vue"),
    },
    {
      path: "/welcome",
      name: "welcome",
      component: () => import("../components/Landing.vue"),
    },
    {
      path: "/dashboard/:tid/:code/:role",
      name: "dashboard",
      component: () => import("../components/ViewLogged.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../components/Login.vue"),
    }, 
    {
      path: "/recommendation",
      name: "recommendation",
      component: () => import("../components/Recommendation.vue"),
    }, 
  ],
});

export default router;