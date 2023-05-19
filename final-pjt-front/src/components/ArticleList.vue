<template>
    <div>
        <h2>ArticleList</h2>
        <hr>
        <ArticleListItem
        v-for="item in items" :key="item.id" :item="item"
        />
    </div>
</template>

<script>
import axios from 'axios'
import ArticleListItem from '@/components/ArticleListItem.vue'
const SERVER_URL = 'http://127.0.0.1:8000'
export default {
    name : 'ArticleList',
    data(){
        return {
            items : []
        }
    },
    components : {
        ArticleListItem
    },
    methods : {
        getArticles(){
            axios({
                method : 'get',
                url :`${SERVER_URL}/movies/articles/`,
                headers :{
                    Authorization : `Bearer ${this.$store.state.token}`
                }
            })
            .then((res)=>{
                console.log(res)
                this.items = res.data
            })
            .catch((err)=>{
                console.log(err)
            })
        }
    },
    created(){
        this.getArticles()
    }
}
</script>

<style>

</style>