<template>
  <el-container class="user-container" style="">
    <el-aside width="60%" calss="information-container">
      <el-text class="information-title">个人信息</el-text>
      <div class="information-item">
        <el-text class="information-text-left">昵称</el-text>
        <el-text class="information-text-right">{{ this.userInfromation.name }}</el-text>
      </div>
      <div class="information-item">
        <el-text class="information-text-left">邮箱</el-text>
        <el-text class="information-text-right">{{ this.userInfromation.email }}</el-text>
      </div>
      <div class="information-item">
        <el-text class="information-text-left">真实姓名</el-text>
        <el-text class="information-text-right">{{ this.userInfromation.truename }}</el-text>
      </div>
      <div class="information-item">
        <el-text class="information-text-left">性别</el-text>
        <el-text class="information-text-right">{{ this.userInfromation.gender==='M'? '男':'女' }}</el-text>
      </div>
      <div style="display: flex;">
        <el-text class="information-text-left" style="height: 70px;">个人简介</el-text>
        <el-text class="information-text-right" style="height: 70px;">{{ this.userInfromation.introduction }}</el-text>
      </div>
    </el-aside>
    <el-aside width="40%" class="avatar-container">
      <el-container>
        <el-header height="60%" class="avatar-item">
          <el-avatar :size="175" fit="fill" style="margin-top: 100px;" :src="this.userInfromation.avatar" />
        </el-header>
        <el-main class="avatar-item">
          <el-button v-if="this.userid==this.$store.state.uid" size="large" type="primary" @click="this.Open()"><el-icon style="margin-right: 4px;"><Edit /></el-icon>编辑个人信息</el-button>
        </el-main>
      </el-container>
      
    </el-aside>
  </el-container>
  <el-dialog v-model="this.userForm.isOpen" title="编辑个人信息" width="500px">
    <el-form ref="userFormRef" :model="userForm" :rules="userFormRules" label-width="70px">
      <el-form-item prop="name" label="昵称" class="dialog-form-item">
        <el-input type="text" v-model="userForm.name" placeholder="请输入昵称" maxlength="30" class="dialog-input" />
      </el-form-item>
      <el-form-item prop="firstname" label="姓" class="dialog-form-item">
        <el-input type="text" v-model="userForm.firstname" placeholder="请输入姓" maxlength="6" class="dialog-input" />
      </el-form-item>
      <el-form-item prop="lastname" label="名" class="dialog-form-item">
        <el-input type="text" v-model="userForm.lastname" placeholder="请输入名" maxlength="20" class="dialog-input" />
      </el-form-item>
      <el-form-item prop="gender" label="性别" class="dialog-form-item">
        <el-radio-group v-model="userForm.gender">
          <el-radio label="M">男</el-radio>
          <el-radio label="F">女</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item prop="phone" label="电话号码" class="dialog-form-item">
        <el-input type="text" v-model="userForm.phone" placeholder="请输入电话号码" maxlength="30" class="dialog-input" />
      </el-form-item>
      <el-form-item prop="introduction" label="简介" class="dialog-form-item">
        <el-input type="text" v-model="userForm.introduction" placeholder="请输入用户简介" maxlength="30" class="dialog-input" />
      </el-form-item>
      <el-form-item prop="icon" label="头像" class="dialog-form-item">
        <el-input id="avatar" type="file" v-model="userForm.icon" class="dialog-input" />
      </el-form-item>
      <el-form-item >
        <el-button type="primary" @click="this.UpdateUserInformation()" style="width: 100px;">提交修改</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<style>
.user-container{
  width:800px;
  height: 500px;
  margin-left: 23%;
  margin-right: 23%;
  margin-top: 5%;
  margin-bottom: 5%;
  border-radius: 4px;
  border: 1px solid #409EFF;
}
.information-container{
  display: flex;
  justify-content: center;
  text-align: center;
  border-radius: 4px;
}
.information-title{
  display: flex;
  justify-content: center;
  margin: 10px;
  height: 50px;
  border-radius: 4px;
  font-size: x-large;
  font-weight: 1000;
}
.information-item{
  display: flex;
  margin: 25px;
  height: 30px;
  border-radius: 4px;
}
.information-text-left{
  display: flex;
  justify-content: center;
  width: 45%;
  font-size: large;
  font-weight: 500;
}
.information-text-right{
  width: 55%;
  font-size: large;
  font-weight: 500;
}
.avatar-container{
  display: flex;
  justify-content: center;
  text-align: center;
  border-left: 1px solid #409EFF;
}
.dialog-form-item{
  width: 500px;
  margin-bottom: 30px;
}
.dialog-input{
  width: 400px;
}
</style>

<script>
import store from '@/store';
import { ElMessage } from 'element-plus';
import { getUserInformation, updateUserInformation } from '../api/user.js';

export default{
  data(){
    return{
      userid: '',
      userInfromation:{
        name: '',
        email: '',
        truename: '',
        avatar: '',
        gender: '',
        phone: '',
        introduction: '',
      },
      userForm:{
        isOpen: false,
        name: '',
        email: '',
        firstname: '',
        lastname: '',
        icon: '',
        gender: '',
        phone: '',
        introduction: '',
      },
      userFormRules:{
        name:[{
          validator: (rule, value, callback) => {
            if(value === ''){
              callback("请输入用户昵称");
            }
            callback()
          }, type: 'string', trigger: 'blur'}],
        gender:[{
          validator: (rule, value, callback) => {
            if(value === ''){
              callback("请选择性别");
            }
            callback()
          }, type: 'string', trigger: 'blur'}],
        icon:[{
          validator: (rule, value, callback) => {
            var cover=value.substring(value.lastIndexOf('.'));
            if(cover=='.png'||cover=='.jpg'||cover=='.jpeg'||cover=='.bmp'||cover==''){
                callback();
            }
            else{
                callback(new Error('该文件类型不支持'));
            }
          }, type: 'string', trigger: 'blur'}],
      },
    }
  },
  methods:{
    init(){
      if(store.state.isLogin==false){
        this.$router.push('/');
      }
      else{
        this.userid=this.$route.params.uid;
        var promise=getUserInformation(this.userid);
        promise.then((result) => {
          if(result.code==0){
            this.userInfromation.name=result.data.username;
            this.userInfromation.email=result.data.email;
            this.userInfromation.truename=result.data.true_name;
            this.userInfromation.avatar=result.data.icon_address;
            this.userInfromation.gender=result.data.gender;
            this.userInfromation.phone=result.data.phone;
            this.userInfromation.introduction=result.data.introduction;
          }
          else{
            ElMessage({
              message: "网络连接失败，请刷新页面！",
              group: true,
              type: "error",
            })
          }
        })
      }
    },
    Open(){
      this.userForm.name=this.userInfromation.name;
      this.userForm.gender=this.userInfromation.gender;
      this.userForm.phone=this.userInfromation.phone;
      this.userForm.introduction=this.userInfromation.introduction;
      this.userForm.firstname='';
      this.userForm.lastname='';
      this.userForm.icon='';
      this.userForm.isOpen=true;
    },
    UpdateUserInformation(){
      this.$refs.userFormRef.validate((valid) => {
        if(valid){
          var file1=document.getElementById('avatar').files[0];
          var promise=updateUserInformation(this.userForm.name,this.userForm.firstname,this.userForm.lastname,this.userForm.gender,this.userForm.phone,this.userForm.introduction,file1);
          promise.then((result) => {
            this.MessageCatch(result);
            this.userForm.isOpen=false;
            this.init();
          })
        }
      })
    },
    MessageCatch(data){
      if(data.code!=0){
        ElMessage({
          message: data.msg,
          grouping: true,
          type: 'error',
        })
        return false;
      }
      else{
        ElMessage({
          message: data.msg,
          grouping: true,
          type: 'success',
        })
        return true;
      }
    },
  },
  mounted(){
    this.init();
  }
}
</script>