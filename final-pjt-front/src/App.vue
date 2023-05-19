<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item @click="goTo('SignUpView')">
          <v-list-item-icon>
            <v-icon>mdi-account-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Sign up</v-list-item-title>
        </v-list-item>
        <v-list-item @click="goTo('ArticleView')">
          <v-list-item-icon>
            <v-icon>mdi-newspaper</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Article</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>My App</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-text-field
        v-model="searchText"
        placeholder="Search"
        hide-details
        solo
        dense
        :append-icon="searchText ? '' : 'mdi-magnify'"
        @click:append="clearSearch"
        class="search-field"
        color="black"
      ></v-text-field>
    </v-app-bar>
    
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
import ArticleView from '@/views/ArticleView.vue'
import axios from 'axios'
const SERVER_URL = 'http://127.0.0.1:8000'
export default {
  name: 'App',
  data() {
    return {
      drawer: false,
      searchText: '',
    }
  },
  components : {
    ArticleView,
  },
  methods: {
    clearSearch() {
      this.searchText = '';
    },
    goTo(routeName) {
      this.$router.push({ name: routeName });
    },
    getUser() {
      axios({
        method : 'get',
        url : `${SERVER_URL}/accounts/userinfo/`
      })
      .then((res)=>{
        this.$store.dispatch('getUsers',res.data)
      }).catch((err)=>{
        console.log(err)
      })
    }
  },
  created() {
    this.$store.dispatch('setToken')
    // 필요한 경우 getUser() 메소드 호출
    this.getUser()
  }
}
</script>

<style>
.search-field .v-text-field__slot {
  background-color: white;
  color: black;
}
</style>
