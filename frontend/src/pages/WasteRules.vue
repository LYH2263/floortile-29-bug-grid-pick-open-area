<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const settings = ref({})
const takeMax = ref(false)
const saveMsg = ref('')
onMounted(async () => {
  settings.value = await getJSON('/api/settings')
  takeMax.value = settings.value.take_max === '1'
})
async function saveTakeMax() {
  saveMsg.value = ''
  settings.value = await postJSON('/api/settings', { take_max: takeMax.value })
  takeMax.value = settings.value.take_max === '1'
  saveMsg.value = '已保存，仅影响新测算，不回溯历史记录'
}
</script>
<template>
  <div class="page">
    <h1>损耗规则</h1>
    <p>默认损耗率按订货基数向上取整后再乘 (1+损耗%)。</p>
    <p>当前默认损耗：<strong>{{ settings.waste_pct }}%</strong></p>
    <p>网格预览块数可能大于面积法片数；开启择大后，订货基数取面积法 raw 与网格块数较大者。</p>
    <label class="take-max-toggle">
      <input type="checkbox" v-model="takeMax" @change="saveTakeMax" /> 默认开启择大订货
    </label>
    <p v-if="saveMsg" class="save-msg">{{ saveMsg }}</p>
  </div>
</template>
