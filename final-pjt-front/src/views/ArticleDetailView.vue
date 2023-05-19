<template>
  <div>
    <h1>ArticleDetailView</h1>
    <p>글 번호 : {{ article?.id }}</p>
    <p>작성자 : {{ username }}</p>
    <p>제목 : {{ article?.title }}</p>
    <p>내용 : {{ article?.content }}</p>
    <p>작성시간 : {{ article?.created_at }}</p>
    <p>수정시간 : {{ article?.updated_at }}</p>
    <ArticleCommentListView :articleid="articleid" />
  </div>
</template>

<script>
import ArticleCommentListView from '@/components/ArticleCommentListView.vue'
import axios from 'axios'
const SERVER_URL = 'http://127.0.0.1:8000'

export default {
    name: 'ArticleDetailView',
    components: {
        ArticleCommentListView
    },
    data() {
        return {
            article: null,
            username: null,
            articleid: null,
        }
    },
    created() {
        this.getArticleDetail()
    },
    methods: {
        getArticleDetail() {
            console.log('getArticleDetail')
            console.log(this.$route.params.articleId)
            axios({
                method: 'get',
                url: `${SERVER_URL}/movies/articles/${ this.$route.params.articleId }/`,
                headers : {
                    Authorization: `Bearer ${ this.$store.state.token}`
                }
            })
            .then((res) => {
                this.article = res.data
                this.articleid = this.$route.params.articleId
                console.log('then')
                console.log(this.articleid)
                for (const user of this.$store.state.users) {
                    if (user.id == this.article.user){
                        this.username = user.username
                    }
                }
            })
            .catch((err) => {
                console.log(err)
            })
        },
    }
}
</script>

<style>

</style>