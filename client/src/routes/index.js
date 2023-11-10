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
      // meta: {
      //   requiresAuth: true
      // }
    },
    {
      path: "/welcome",
      name: "welcome",
      component: () => import("../components/Landing.vue"),
    },
    {
      path: "/dashboard/:name/:email/:role",
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
    {
      path: "/profile/:name/:email/:role",
      name: "profile",
      component: () => import("../components/Profile.vue"),
    }, 
    // {
    //   path: "/settings",
    //   name: "settings",
    //   component: () => import("../components/Settings.vue"),
    // },
  ],
});

// router.beforeEach((to, from, next) => {
//   if (to.matched.some((record) => record.meta.requiresAuth)) {
//     // La ruta requiere autenticación
//     if (isAuthenticated()) {
//       // El usuario está autenticado, permitir el acceso
//       next();
//     } else {
//       // El usuario no está autenticado, redirigir a la página de inicio de sesión
//       next("/login");
//     }
//   } else {
//     // La ruta no requiere autenticación, permitir el acceso sin verificar
//     next();
//   }
// });

export default router;