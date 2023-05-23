<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>My App</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click="openSearchDialog">
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn v-bind="attrs" v-on="on" icon>
            <v-icon>mdi-account-circle</v-icon>
          </v-btn>
        </template>
        <v-list>
          <!-- 프로필 및 로그아웃 메뉴 항목들 -->
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item @click="goTo('home')">
          <v-list-item-icon>
            <v-icon>mdi-account-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Home</v-list-item-title>
        </v-list-item>
        <v-list-item @click="goTo('LoginView')">
          <v-list-item-icon>
            <v-icon>mdi-account-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Login</v-list-item-title>
        </v-list-item>
         <v-list-item @click="logout">
          <v-list-item-icon>
            <v-icon>mdi-account-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Logout</v-list-item-title>
        </v-list-item>
        <v-list-item @click="goTo('SignUpView')">
          <v-list-item-icon>
            <v-icon>mdi-account-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Sign up</v-list-item-title>
        </v-list-item>
        <v-list-item @click="goToProfile">
          <v-list-item-icon>
            <v-icon>mdi-newspaper</v-icon>
          </v-list-item-icon>
          <v-list-item-title>MyProfile</v-list-item-title>
        </v-list-item>
         <v-list-item @click="goTo('MovieView')">
          <v-list-item-icon>
            <v-icon>mdi-account-plus</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Movie</v-list-item-title>
        </v-list-item>
        <v-list-item @click="goTo('ArticleView')">
          <v-list-item-icon>
            <v-icon>mdi-newspaper</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Article</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view />
    </v-main>

    <v-dialog v-model="showSearchDialog" max-width="500">
      <v-card>
        <v-card-title>
          <v-text-field
            v-model="searchText"
            placeholder="Search"
            hide-details
            solo
            dense
          ></v-text-field>
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text color="primary" @click='searchMovies'>Search</v-btn>
          <v-btn text color="primary" @click="closeSearchDialog">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showSearchResultDialog" max-width="800">
      <v-carousel v-if="searchResults && searchResults.length > 0" hide-delimiters show-arrows v-model="currentCarouselIndex" cycle>
        <v-carousel-item
          v-for="(group, index) in groupedSearchResults"
          :key="index"
          style="text-align: center"
        >
          <v-row justify="center" align="center">
            <v-col
              v-for="(movie, movieIndex) in group"
              :key="movieIndex"
              cols="4"
              sm="3"
              md="2"
              style="padding: 8px"
            >
              <v-card class="movie-card" :width="movieCardWidth">
                <!-- 필요한 영화 카드 내용 표시 -->
                <v-card-text>
                  <img :src="getImageUrl(movie.poster_path)" class="moviePoster movie-item" @click="goDetail(movie)" />
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-carousel-item>
      </v-carousel>
      <v-carousel v-else>
        <h1>검색 결과가 없습니다.</h1>
      </v-carousel>
    </v-dialog>
  </v-app>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      drawer: false,
      searchText: '',
      showSearchDialog: false,
      showSearchResultDialog: false,
      searchResults: [],
      currentCarouselIndex: 0
    }
  },
  computed : {
    groupedSearchResults() {
      const groupSize = 9;
      const groups = [];
      for (let i = 0; i < this.searchResults.length; i += groupSize) {
        groups.push(this.searchResults.slice(i, i + groupSize));
      }
      return groups;
    },
    movieCardWidth() {
      // 카드의 너비를 조정하기 위한 계산된 속성
      const cardMargin = 16; // 카드 사이의 간격
      const carouselWidth = 800; // 캐로셀의 너비
      const groupSize = 9; // 그룹당 영화 수
      const numGroups = Math.ceil(this.searchResults.length / groupSize); // 그룹의 수
      const availableWidth = carouselWidth - (groupSize - 1) * cardMargin; // 사용 가능한 너비
      return `${availableWidth / groupSize}px`;
    }

  },
  methods: {
    getImageUrl(posterPath){
            const size = 'w200'
            return `https://image.tmdb.org/t/p/${size}/${posterPath}`
        },
    // Search(){
    //   axios({
    //     method : 'get',
    //     url : `${process.env.VUE_APP_SERVER_URL}/movies/search/?q=${this.searchText}`,
    //     headers : {
    //       Authorization : `Bearer ${this.$store.state.token}`
    //     }
    //   }).then((res)=>{
    //     console.log(res)
    //     this.showSearchDialog = false
    //     this.searchText = ''
    //   }).catch((err)=>{
    //     console.log(err)
    //   })
    // },
    goDetail(movie){
      const movie_id = movie.id
      this.$router.push({name : 'MovieDetailView', params : {movie_id :movie_id}})
      this.showSearchResultDialog = false
    },
    searchMovies() {
      axios({
        method: 'get',
        url: `${process.env.VUE_APP_SERVER_URL}/movies/search/?q=${this.searchText}`,
        headers: {
          Authorization: `Bearer ${this.$store.state.token}`
        }
      })
        .then((res) => {
          console.log(res);
          this.searchResults = res.data;
          this.showSearchDialog = false;
          this.showSearchResultDialog = true;
          this.searchText = ''
        })
        .catch((err) => {
          console.log(err);
        });
    },
    closeSearchResultDialog() {
      this.showSearchResultDialog = false;
      this.searchResults = [];
    },
    logout(){
      axios({
        method : 'delete',
        url : `${process.env.VUE_APP_SERVER_URL}/accounts/auth/`
      }).then((res)=>{
        localStorage.removeItem('token')
        this.$router.push({name:'LoginView'})
      }).catch((err)=>{
        console.log(err)
      })
    },
    clearSearch() {
      this.searchText = '';
    },
    goTo(routeName) {
      if (this.$route.name !== routeName) {
        this.$router.push({ name: routeName });
      }
    },
    goToProfile() {
      for (const user of this.$store.state.users) {
        if (this.$store.state.user.id == user.id) {
          this.username = user.username
        }
      }
      this.$router.push({name: 'ProfileView', params: {username: this.username}})
    },
    getUser() {
      axios({
        method: 'get',
        url: `${process.env.VUE_APP_SERVER_URL}/accounts/userinfo/`
      })
      .then((res) => {
        console.log(res)
        this.$store.dispatch('getUsers', res.data)
      })
      .catch((err) => {
        console.log(err)
      })
    },
    
    openSearchDialog() {
      this.showSearchDialog = true;
    },
    closeSearchDialog() {
      this.showSearchDialog = false;
      this.clearSearch();
    },
  },
  created() {
    this.$store.dispatch('setToken')
    this.$store.dispatch('getMovies')
    this.$store.dispatch('getArticles')
    // 필요한 경우 getUser() 메소드 호출
    this.getUser()
  }
}
</script>

<style scoped>
/* 이전 스타일 코드 생략 */

.movie-card {
  margin-right: 16px;
  flex-shrink: 0;
  cursor:pointer;
}
</style>