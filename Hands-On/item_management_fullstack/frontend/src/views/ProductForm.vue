<template>
  <div class="card" style="max-width:600px; margin:0 auto;">
    <div class="card-header"><i :class="'fas '+(isEdit?'fa-pen':'fa-plus')"></i> {{ isEdit ? 'Edit Product' : 'Add Product' }}</div>
    <div class="card-body">
      <div v-if="error" class="error-msg">{{ error }}</div>
      <form @submit.prevent="doSave">
        <div class="form-group"><label>Name</label><input v-model="form.name" required /></div>
        <div class="form-group"><label>Description</label><input v-model="form.description" /></div>
        <div class="form-group"><label>Price</label><input v-model.number="form.price" type="number" step="0.01" required /></div>
        <div class="form-group"><label>Stock</label><input v-model.number="form.stock" type="number" min="0" /></div>
        <div class="form-group">
          <label>Category</label>
          <select v-model.number="form.category_id">
            <option :value="null">&mdash; No category &mdash;</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>
        <div class="d-flex gap-2">
          <button type="submit" class="btn btn-primary" :disabled="saving"><i class="fas fa-save"></i> {{ saving ? 'Saving...' : (isEdit ? 'Update' : 'Create') }}</button>
          <router-link to="/products" class="btn btn-secondary">Cancel</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../api.js'
export default {
  data() {
    return {
      isEdit: false, saving: false, error: null,
      form: { name: '', description: '', price: 0, stock: 0, category_id: null },
      categories: [],
    }
  },
  async created() {
    const id = this.$route.params.id
    this.isEdit = !!id
    const catRes = await api.categories({ per_page: 100 })
    this.categories = catRes.categories
    if (id) {
      const p = await api.product(id)
      this.form = { name: p.name, description: p.description, price: p.price, stock: p.stock, category_id: p.category_id }
    }
  },
  methods: {
    async doSave() {
      this.saving = true; this.error = null
      try {
        if (this.isEdit) {
          await api.updateProduct(this.$route.params.id, this.form)
        } else {
          await api.createProduct(this.form)
        }
        this.$router.push('/products')
      } catch (e) { this.error = e.message }
      finally { this.saving = false }
    },
  },
}
</script>
