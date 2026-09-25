<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const openId = ref(null)
const detail = ref(null)
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
async function toggle(id) {
  if (openId.value === id) { openId.value = null; detail.value = null; return }
  openId.value = id
  detail.value = await getJSON(`/api/runs/${id}`)
}
function modeOf(r) { return r.result?.take_max ? '择大' : '面积法' }
function baseOf(r) { return r.result?.base_count ?? r.result?.raw_count }
</script>
<template>
  <div class="page">
    <h1>测算记录</h1>
    <table class="tbl">
      <thead><tr><th>时间</th><th>房间</th><th>砖型</th><th>模式</th><th>片数</th><th></th></tr></thead>
      <tbody>
        <template v-for="r in items" :key="r.id">
          <tr class="run-row">
            <td>{{ r.created_at?.slice(0, 19) }}</td>
            <td>{{ r.room_name }}</td>
            <td>{{ r.tile_name }}</td>
            <td>{{ modeOf(r) }}</td>
            <td>{{ r.result?.order_count }}</td>
            <td><button class="link-btn" @click="toggle(r.id)">{{ openId === r.id ? '收起' : '详情' }}</button></td>
          </tr>
          <tr v-if="openId === r.id && detail" class="run-detail">
            <td colspan="6">
              订货基数 {{ baseOf(detail) }} 片（{{ modeOf(detail) }}），
              面积法净用量 {{ detail.result?.raw_count }} 片，
              网格块数 {{ detail.result?.layout?.grid_count ?? '—' }} 块，
              损耗 {{ detail.result?.waste_pct }}%，
              订货 {{ detail.result?.order_count }} 片
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>
