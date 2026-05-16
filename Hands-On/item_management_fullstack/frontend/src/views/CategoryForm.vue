<template>
  <div class="card" style="max-width:500px; margin:0 auto;">
    <div class="card-header"><i :class="'fas '+(isEdit?'fa-pen':'fa-plus')"></i> {{ isEdit ? 'Edit Category' : 'Add Category' }}</div>
    <div class="card-body">
      <div v-if="error" class="error-msg">{{ error }}</div>
      <form @submit.prevent="doSave">
        <div class="form-group"><label>Name</label><input v-model="form.name" required /></div>
        <div class="form-group"><label>Description</label><input v-model="form.description" /></div>
        <div class="d-flex gap-2">
          <button type="submit" class="btn btn-primary" :disabled="saving"><i class="fas fa-save"></i> {{ saving ? 'Saving...' : (isEdit ? 'Update' : 'Create') }}</button>
          <router-link to="/categories" class="btn btn-secondary">Cancel</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../api.js'
export default {
  data() { return { isEdit: false, saving: false, error: null, form: { name: '', description: '' } } },
  async created() {
    const id = this.$route.params.id; this.isEdit = !!id
    if (id) {
      const res = await api.categories({ per_page: 100 })
      const c = (res.categories || []).find(x => x.id == id)
      if (c) this.form = { name: c.name, description: c.description }
    }
  },
  methods: {
    async doSave() {
      this.saving = true; this.error = null
      try {
        if (this.isEdit) await api.updateCategory(this.$route.params.id, this.form)
        else await api.createCategory(this.form)
        this.$router.push('/categories')
      } catch (e) { this.error = e.message }
      finally { this.saving = false }
    },
  },
}
</script>
