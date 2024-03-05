<template>
  <el-dialog v-for="item in this.dialog.count" v-model="this.dialog.list[item-1].isOpen">
    <el-text>{{ this.dialog.list[item-1].name }}</el-text>
    <el-button type="primary" @click="this.Test()">test</el-button>
  </el-dialog>
  <div id="app">
    <ng-form-design :imp="false" :basic-item="false" :personal-item="false" :layout-item="false" ref="formDesign" />
    <ng-form-build :disabled="false" ef="formBuild" />
  </div>
</template>

<script>
export default{
  data(){
    return{
      dialog:{
        count: 1,
        list: [{
          "name" : "1",
          "isOpen" : true,
        }]
      },
    }
  }, 
  methods:{
    Test(){
      this.dialog.list.push({"name" : "2","isOpen" : true});
      this.dialog.count++;
    }
  },
  mounted(){
    
  },
}
</script>