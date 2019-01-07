import Vue from 'vue'
import Router from 'vue-router'
import { interopDefault } from './utils'

const _2092c629 = () => interopDefault(import('../pages/dashboard/index.vue' /* webpackChunkName: "pages/dashboard/index" */))
const _7a864150 = () => interopDefault(import('../pages/filters/index.vue' /* webpackChunkName: "pages/filters/index" */))
const _0ed08bd3 = () => interopDefault(import('../pages/filters/index/index.vue' /* webpackChunkName: "pages/filters/index/index" */))
const _53e9a262 = () => interopDefault(import('../pages/filters/index/add.vue' /* webpackChunkName: "pages/filters/index/add" */))
const _1508a2ee = () => interopDefault(import('../pages/filters/index/group/_id/index.vue' /* webpackChunkName: "pages/filters/index/group/_id/index" */))
const _97872ac4 = () => interopDefault(import('../pages/filters/index/group/_id/edit.vue' /* webpackChunkName: "pages/filters/index/group/_id/edit" */))
const _85ec1424 = () => interopDefault(import('../pages/filters/index/group/_id/items/add.vue' /* webpackChunkName: "pages/filters/index/group/_id/items/add" */))
const _0e42d90a = () => interopDefault(import('../pages/login.vue' /* webpackChunkName: "pages/login" */))
const _2dfbddb8 = () => interopDefault(import('../pages/administration/users/index.vue' /* webpackChunkName: "pages/administration/users/index" */))
const _60293a3b = () => interopDefault(import('../pages/administration/users/index/index.vue' /* webpackChunkName: "pages/administration/users/index/index" */))
const _3e2a6a6c = () => interopDefault(import('../pages/administration/users/index/add.vue' /* webpackChunkName: "pages/administration/users/index/add" */))
const _61d680b4 = () => interopDefault(import('../pages/administration/users/index/_id/index.vue' /* webpackChunkName: "pages/administration/users/index/_id/index" */))
const _3e5dd6e6 = () => interopDefault(import('../pages/administration/users/index/_id/edit.vue' /* webpackChunkName: "pages/administration/users/index/_id/edit" */))
const _252e3863 = () => interopDefault(import('../pages/auth/logout.vue' /* webpackChunkName: "pages/auth/logout" */))
const _2f36f064 = () => interopDefault(import('../pages/index.vue' /* webpackChunkName: "pages/index" */))

Vue.use(Router)

if (process.client) {
  window.history.scrollRestoration = 'manual'
}
const scrollBehavior = function (to, from, savedPosition) {
  // if the returned position is falsy or an empty object,
  // will retain current scroll position.
  let position = false

  // if no children detected
  if (to.matched.length < 2) {
    // scroll to the top of the page
    position = { x: 0, y: 0 }
  } else if (to.matched.some(r => r.components.default.options.scrollToTop)) {
    // if one of the children has scrollToTop option set to true
    position = { x: 0, y: 0 }
  }

  // savedPosition is only available for popstate navigations (back button)
  if (savedPosition) {
    position = savedPosition
  }

  return new Promise((resolve) => {
    // wait for the out transition to complete (if necessary)
    window.$nuxt.$once('triggerScroll', () => {
      // coords will be used if no selector is provided,
      // or if the selector didn't match any element.
      if (to.hash) {
        let hash = to.hash
        // CSS.escape() is not supported with IE and Edge.
        if (typeof window.CSS !== 'undefined' && typeof window.CSS.escape !== 'undefined') {
          hash = '#' + window.CSS.escape(hash.substr(1))
        }
        try {
          if (document.querySelector(hash)) {
            // scroll to anchor by returning the selector
            position = { selector: hash }
          }
        } catch (e) {
          console.warn('Failed to save scroll position. Please add CSS.escape() polyfill (https://github.com/mathiasbynens/CSS.escape).')
        }
      }
      resolve(position)
    })
  })
}

export function createRouter() {
  return new Router({
    mode: 'history',
    base: '/',
    linkActiveClass: 'nuxt-link-active',
    linkExactActiveClass: 'nuxt-link-exact-active',
    scrollBehavior,

    routes: [{
      path: "/dashboard",
      component: _2092c629,
      name: "dashboard"
    }, {
      path: "/filters",
      component: _7a864150,
      children: [{
        path: "",
        component: _0ed08bd3,
        name: "filters-index"
      }, {
        path: "add",
        component: _53e9a262,
        name: "filters-index-add"
      }, {
        path: "group/:id?",
        component: _1508a2ee,
        name: "filters-index-group-id"
      }, {
        path: "group/:id?/edit",
        component: _97872ac4,
        name: "filters-index-group-id-edit"
      }, {
        path: "group/:id?/items/add",
        component: _85ec1424,
        name: "filters-index-group-id-items-add"
      }]
    }, {
      path: "/login",
      component: _0e42d90a,
      name: "login"
    }, {
      path: "/administration/users",
      component: _2dfbddb8,
      children: [{
        path: "",
        component: _60293a3b,
        name: "administration-users-index"
      }, {
        path: "add",
        component: _3e2a6a6c,
        name: "administration-users-index-add"
      }, {
        path: ":id",
        component: _61d680b4,
        name: "administration-users-index-id"
      }, {
        path: ":id/edit",
        component: _3e5dd6e6,
        name: "administration-users-index-id-edit"
      }]
    }, {
      path: "/auth/logout",
      component: _252e3863,
      name: "auth-logout"
    }, {
      path: "/",
      component: _2f36f064,
      name: "index"
    }],

    fallback: false
  })
}
