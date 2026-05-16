<template>
  <div class="card" style="max-width:400px; margin:3rem auto;">
    <div class="card-header"><i class="fas fa-lock"></i> Admin Login</div>
    <div class="card-body">
      <div v-if="error" class="error-msg"><i class="fas fa-exclamation-circle"></i> {{ error }}</div>
      <form @submit.prevent="doLogin">
        <div class="form-group">
          <label><i class="fas fa-user"></i> Username</label>
          <input v-model="username" type="text" required autofocus />
        </div>
        <div class="form-group">
          <label><i class="fas fa-key"></i> Password</label>
          <input v-model="password" type="password" required />
        </div>
        <button type="submit" class="btn btn-primary" style="width:100%;" :disabled="loading">
          <i class="fas fa-sign-in-alt"></i> {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../api.js'
export default {
  data() {
    return { username: '', password: '', error: null, loading: false }
  },
  methods: {
    async doLogin() {
      this.loading = true
      this.error = null
      try {
        await api.login(this.username, this.password)
        this.$router.push('/')
      } catch (e) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
