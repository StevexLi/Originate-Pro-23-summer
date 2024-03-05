<template>
    <el-container>
        <el-aside width="15%">
            <el-scrollbar>
                <el-button type="primary" v-for="item in this.graph.count" :key="item" :plain="item-1!=this.graph.current" @click="this.SwitchGraph(item-1)" class="scrollbar-item">{{ this.graph.list[item-1].name }}</el-button>
            </el-scrollbar>
        </el-aside>
        <el-aside width="85%">
            <el-image :src="this.url" style="display: flex;" fit="fill"></el-image>
        </el-aside>
    </el-container>
</template>

<style scoped>
.scrollbar-item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80%;
  height: 40px;
  margin: 8px;
  text-align: center;
}
</style>
<script>
import { ElMessage } from 'element-plus';
import { getAllGraph } from '../api/graph'

export default{
    data(){
        return{
            url: '',
            projectid: '',
            graph:{
                list: [],
                count: 0,
                current: 0,
            }
        }
    },
    methods:{
        SwitchGraph(index){
            this.url=this.graph.list[index].file_address;
            this.graph.current=index;
        },
        Load(){
            var promise=getAllGraph(this.projectid);
            promise.then((result) => {
                console.log(result);
                if(result.code!=0){
                    ElMessage({
                        message: '未开放页面',
                        type: 'error',
                    })
                    this.$router.push('/');
                }
                else{
                    console.log(result);
                    this.graph.current=0;
                    this.graph.count=0;
                    this.graph.list=result.data;
                    this.graph.count=this.graph.list.length;
                    this.url=this.graph.list[this.graph.current].file_address;
                    ElMessage({
                        message: '欢迎访问',
                        type: 'success',
                    })
                }
            })
        }
    },
    mounted(){
        this.projectid=this.$route.params.projectid;
        this.Load();
    }
}

</script>