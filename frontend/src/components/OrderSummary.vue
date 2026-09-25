<script setup>
defineProps({
  result: { type: Object, default: null },
})
</script>
<template>
  <div v-if="result" class="order-summary">
    <div class="hero">{{ result.order_count }} 片</div>
    <ul>
      <li>
        订货基数 {{ result.base_count }} 片
        <template v-if="result.take_max">（择大：面积法 {{ result.raw_count }} 与网格 {{ result.layout?.grid_count }} 取大）</template>
        <template v-else>（面积法净用量）</template>
        ，损耗 {{ result.waste_pct }}%
      </li>
      <li>净用量 {{ result.raw_count }} 片，网格块数 {{ result.layout?.grid_count }} 块</li>
      <li>地面 {{ result.area_m2 }} m²，单砖 {{ result.piece_m2 }} m²</li>
    </ul>
  </div>
</template>
