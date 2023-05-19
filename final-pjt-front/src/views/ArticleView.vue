<template>
  <v-container>
    <h1>ArticleView</h1>
    <ArticleList/>
    <!-- <v-main>
      <router-view/>
    </v-main> -->
  </v-container>
</template>

<script>
import ArticleList from '@/components/ArticleList.vue'
export default {
  name: 'ArticleView',
  components : {
    ArticleList
  },
  data() {
    return {
      searchText: '',
    }
  },
  methods: {
    search() {
      // 검색 기능 구현
      // 검색어: this.searchText
      // 검색 로직을 구현하세요.
    },
  },
}
</script>
<style>
.v-input__prepend-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
}
</style>