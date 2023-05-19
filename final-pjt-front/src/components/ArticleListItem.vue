<template>
  <div>
    <p>{{item.title}}</p>
    <p>작성자 : {{item.user}}</p>
    <router-link :to="{name: 'ArticleDetailView', params: {articleId: item.id}}">[Detail]</router-link>
    <hr>
  </div>
</template>

<script>
import axios from 'axios'
const SERVER_URL = 'http://127.0.0.1:8000'
export default {
    name : 'ArticleListItem',
    data(){
      return {
      
      }
    },
    props : {
      item : Object
    },
    methods : {
      getArticle(){
        axios({
          method : 'get',
          url : `${SERVER_URL}/movies/articles/${this.item.id}`,
          headers : {
            Authorization : `Bearer ${this.$store.state.token}`
          }
        })
        .then((res)=>{
          for (const user of this.$store.state.users){
            if (user.id == this.item.user){
              this.item.user = user.username
            }
          }
        })
      }
    },
    created(){
      this.getArticle()
    } 
}
</script>

<style>

</style>