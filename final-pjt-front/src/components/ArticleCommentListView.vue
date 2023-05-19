<template>
  <div>
    <h4>ArticleCommentList</h4>
    <!-- <ArticleCommentListItemView
    v-for="comment in comments" :key="comment.id" :comment="comment"
    /> -->
  </div>
</template>

<script>
import ArticleCommentListItemView from '@/components/ArticleCommentListItemView.vue'
import axios from 'axios'
const SERVER_URL = 'http://127.0.0.1:8000'

export default {
    name: 'ArticleCommentList',
    data() {
        return {
            comments: [],
        }
    },
    props: {
        articleid: Number,
    },
    components: {
        ArticleCommentListItemView
    },
    methods: {
        // getComments() {
        //     console.log('getComments')
        //     console.log(this.article)
        //     axios({
        //         method : 'get',
        //         url :`${SERVER_URL}/movies/articles/${this.article.id}/`,
        //         headers :{
        //             Authorization : `Bearer ${this.$store.state.token}`
        //         }
        //     })
        //     .then((res)=>{
        //         console.log(res)
        //         this.comments = res.data.articlecomment_set
        //     })
        //     .catch((err)=>{
        //         console.log(err)
        //     }) 
        // }
    },
    created() {
        console.log('created')
        console.log(this.articleid)
        // this.getComments()
    }
}
</script>

<style>

</style>