<template>
  <header class="topbar">
    <router-link class="brand-block" to="/">
      <div class="brand-mark" aria-hidden="true">
        <span></span>
        <span></span>
      </div>
      <div>
        <p class="eyebrow">Tea Archive</p>
        <h1>茶录</h1>
      </div>
    </router-link>

    <nav class="topnav" aria-label="主导航">
      <router-link to="/">首页</router-link>
      <router-link to="/library/tea-ware">茶具</router-link>
      <router-link to="/library/tea-leaves">茶叶</router-link>
      <router-link to="/library/water">水</router-link>
      <router-link to="/tasting">记录</router-link>
    </nav>
  </header>
</template>
