<template>
  <div class="loading-state" aria-live="polite">
    <div v-for="n in 3" :key="n" class="loading-card"></div>
  </div>
</template>
