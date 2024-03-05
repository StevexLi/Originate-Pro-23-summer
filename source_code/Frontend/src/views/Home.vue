<template>
    <video autoplay="autoplay" loop="" id="video1" src="../assets/back.mp4" muted style="width: 1500px;"></video>
    <el-link :underline="true" href="./loginandregister" style="position: relative; width: 450px;height: 50px;margin-left: 530px;margin-top: -1200px;font-size: 7ch;color: white;">
        Originate Pro
    </el-link>
    <el-link :underline="true" href="./loginandregister" style="position: relative; width: 450px;height: 50px;margin-left: 530px;margin-top: -980px;font-size: x-large;color: white;">
        一个高效的团队协作办公网站
    </el-link>
    <el-link :underline="true" href="./loginandregister" style="position: relative; width: 170px;height: 50px;margin-left: 670px;margin-top: -900px;font-size: xx-large;color: white;">
        快速使用
        <el-icon size="large" style="margin-left: 10px;margin-top: 5px;"><ArrowRightBold /></el-icon>
    </el-link>
    <el-container style="height: 1400px;">
        <el-main height="1200px">
            <el-container style="height: 400px;margin-bottom: 10px;">
                <el-aside width="720px">
                    <img style="width: 720px;height: 390px;" :src="require('../assets/group.jpg')" fit="fill" />
                </el-aside>
                <el-aside width="720px" style="margin-left: 10px;">
                    <img style="width: 720px;height: 390px;" :src="require('../assets/project.png')" fit="fill" />
                </el-aside>
            </el-container>
            <el-container style="height: 400px;margin-bottom: 10px;">
                <el-aside width="720px">
                    <img style="width: 720px;height: 390px;" :src="require('../assets/chat.jpg')" fit="fill" />
                </el-aside>
                <el-aside width="720px" style="margin-left: 10px;">
                    <img style="width: 720px;height: 390px;" src="" fit="fill" />
                </el-aside>
            </el-container>
            <el-container style="height: 400px;margin-bottom: 10px;">
                <el-aside width="720px">
                    <img style="width: 720px;height: 390px;" src="" fit="fill" />
                </el-aside>
                <el-aside width="720px" style="margin-left: 10px;">
                    <img style="width: 720px;height: 390px;" :src="require('../assets/start.jpg')" fit="fill" />
                </el-aside>
            </el-container>
        </el-main>
    </el-container>
    <el-link href="./loginandregister" style="position: relative;margin-top: -2500px;margin-left: 100px;font-size: 5ch;color: black;">团<br/>队<br/>管<br/>理</el-link>
    <el-link href="./loginandregister" style="position: relative;margin-top: -2500px;margin-left: 850px;font-size: 5ch;color: black;">项目协作</el-link>
    <el-link href="./loginandregister" style="position: relative;margin-top: -1600px;margin-left: 200px;font-size: 5ch;color: black;">多种交流形式</el-link>
    <el-link href="./loginandregister" style="position: relative;margin-top: -1550px;margin-left: 1000px;font-size: 5ch;color: black;">在线文档</el-link>
    <el-link href="./loginandregister" style="position: relative;margin-top: -800px;margin-left: 300px;font-size: 5ch;color: black;">共享设计</el-link>
    <el-link href="./loginandregister" style="position: relative;margin-top: -800px;margin-left: 350px;font-size: 5ch;color: black;" class="start">开<br/>始<br/>体<br/>验<el-icon style="position: relative;margin-top: 5px;"><CaretRight /></el-icon></el-link>
</template>

<style scoped>

</style>

<script>
export default{
    data(){
        return{

        }
    },
    methods:{

    },
    mounted(){

    },
}

</script>