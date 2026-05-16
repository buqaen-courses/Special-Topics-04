<template>
  <div>
    <h2><i class="fas fa-plus-circle"></i> Create New Order</h2>
    <div v-if="error" class="error-msg">{{ error }}</div>
    <div v-if="success" class="success-msg">Order #{{ createdOrderId }} created!</div>

    <div class="card">
      <div class="card-header"><i class="fas fa-user"></i> Customer</div>
      <div class="card-body">
        <select v-model="customerId" style="max-width:400px;" :disabled="loadingCustomers">
          <option :value="null">&mdash; Choose customer &mdash;</option>
          <option v-for="c in customers" :key="c.id" :value="c.id">{{ c.name }} ({{ c.email }})</option>
        </select>
      </div>
    </div>

    <div class="card">
      <div class="card-header"><i class="fas fa-box"></i> Items</div>
      <div class="card-body">
        <div v-for="(item, idx) in items" :key="idx" class="d-flex gap-2" style="margin-bottom:0.8rem;align-items:end;">
          <div style="flex:2;">
            <label>Product</label>
            <select v-model="item.product_id" @change="updatePrice(idx)">
              <option :value="null">&mdash; Select &mdash;</option>
              <option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }} (${{ p.price.toFixed(2) }}, stock: {{ p.stock }})</option>
            </select>
          </div>
          <div style="flex:1;">
            <label>Qty</label>
            <input v-model.number="item.quantity" type="number" min="1" />
          </div>
          <div style="flex:1;">
            <label>Subtotal</label>
            <div style="padding:0.6rem 0;">${{ calcSubtotal(idx) }}</div>
          </div>
          <div style="align-self:flex-end;">
            <button class="btn btn-danger btn-sm" @click="removeItem(idx)" v-if="items.length>1"><i class="fas fa-times"></i></button>
          </div>
        </div>
        <button class="btn btn-secondary btn-sm" @click="addItem"><i class="fas fa-plus"></i> Add item</button>
      </div>
      <div class="card-body" style="border-top:1px solid #e2e8f0;">
        <strong>Total: ${{ total.toFixed(2) }}</strong>
      </div>
    </div>

    <div class="d-flex gap-2" style="margin-top:1rem;">
      <button class="btn btn-primary" @click="doCreate" :disabled="saving"><i class="fas fa-save"></i> {{ saving ? 'Creating...' : 'Create Order' }}</button>
      <router-link to="/orders" class="btn btn-secondary">Cancel</router-link>
    </div>
  </div>
</template>

<script>
import api from '../api.js'
export default {
  data() {
    return {
      customers: [], products: [], productMap: {},
      customerId: null,
      items: [{ product_id: null, quantity: 1 }],
      error: null, success: false, createdOrderId: null,
      saving: false, loadingCustomers: true,
    }
  },
  computed: {
    total() {
      return this.items.reduce((sum, it) => {
        const p = this.productMap[it.product_id]
        return sum + (p ? p.price * (it.quantity || 0) : 0)
      }, 0)
    },
  },
  async created() {
    try {
      const [custRes, prodRes] = await Promise.all([
        api.customers({ per_page: 100 }), api.products({ per_page: 100 }),
      ])
      this.customers = custRes.customers
      this.products = prodRes.products
      this.products.forEach(p => { this.productMap[p.id] = p })
    } catch (e) { this.error = e.message }
    finally { this.loadingCustomers = false }
  },
  methods: {
    addItem() { this.items.push({ product_id: null, quantity: 1 }) },
    removeItem(idx) { this.items.splice(idx, 1) },
    updatePrice(idx) { /* product name shown via select */ },
    calcSubtotal(idx) {
      const p = this.productMap[this.items[idx].product_id]
      return p ? (p.price * (this.items[idx].quantity || 0)).toFixed(2) : '0.00'
    },
    async doCreate() {
      this.error = null; this.success = false; this.saving = true
      try {
        const orderItems = this.items
          .filter(it => it.product_id && it.quantity > 0)
          .map(it => ({ product_id: it.product_id, quantity: it.quantity }))
        const res = await api.createOrder({ customer_id: this.customerId, items: orderItems })
        this.createdOrderId = res.id
        this.success = true
        setTimeout(() => this.$router.push('/orders/' + res.id), 1000)
      } catch (e) { this.error = e.message }
      finally { this.saving = false }
    },
  },
}
</script>
