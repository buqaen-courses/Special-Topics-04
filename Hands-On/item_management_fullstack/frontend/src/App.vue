<template>
  <div id="app-shell">
    <nav class="navbar" v-if="loggedIn">
      <div class="container">
        <router-link to="/" class="navbar-brand">
          <i class="fas fa-store"></i> Shop Manager
        </router-link>
        <ul class="navbar-nav">
          <li><router-link to="/"><i class="fas fa-chart-pie"></i> Dashboard</router-link></li>
          <li><router-link to="/products"><i class="fas fa-box"></i> Products</router-link></li>
          <li><router-link to="/categories"><i class="fas fa-tags"></i> Categories</router-link></li>
          <li><router-link to="/customers"><i class="fas fa-users"></i> Customers</router-link></li>
          <li><router-link to="/orders"><i class="fas fa-shopping-cart"></i> Orders</router-link></li>
          <li class="nav-right"><a href="#" @click.prevent="doLogout" style="color:#f87171;"><i class="fas fa-sign-out-alt"></i> Logout</a></li>
        </ul>
      </div>
    </nav>
    <main class="container" style="margin-top: 2rem;">
      <router-view />
    </main>
  </div>
</template>

<script>
import api from './api.js'
export default {
  data() { return { loggedIn: false } },
  async created() {
    try { await api.me(); this.loggedIn = true }
    catch { this.loggedIn = false }
  },
  methods: {
    async doLogout() {
      await api.logout()
      this.loggedIn = false
      this.$router.push('/login')
    },
  },
}
</script>
