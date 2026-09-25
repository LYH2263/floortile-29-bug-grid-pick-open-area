<script setup>
defineProps({
  cols: { type: Number, default: 0 },
  rows: { type: Number, default: 0 },
  gridCount: { type: Number, default: 0 },
  rawCount: { type: Number, default: 0 },
  baseCount: { type: Number, default: 0 },
  takeMax: { type: Boolean, default: false },
})
</script>
<template>
  <div class="grid-preview">
    <p>铺砖网格预览：{{ cols }} 列 × {{ rows }} 行，共 {{ gridCount }} 块（含裁切格）</p>
    <p v-if="takeMax" class="grid-compare">
      择大对照：面积法 {{ rawCount }} 片 / 网格 {{ gridCount }} 块，订货基数取 <strong>{{ baseCount }}</strong>
    </p>
    <p v-else class="grid-compare">未开启择大，订货基数按面积法 {{ rawCount }} 片（网格 {{ gridCount }} 块仅作预览）</p>
    <div class="mini-grid" :style="{ gridTemplateColumns: `repeat(${Math.min(cols, 12)}, 1fr)` }">
      <span v-for="n in Math.min(cols * rows, 48)" :key="n" class="cell"></span>
    </div>
  </div>
</template>
