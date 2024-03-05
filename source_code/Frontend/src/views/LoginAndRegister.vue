<template>
  <el-dialog v-model="this.openGuide" title="如何查看新手指引" width="900px" top="10vh" style="height: 500px;">
    <el-carousel height="500px">
      <el-carousel-item><el-image :src="require('../assets/guide1.png')" fit="fill"/></el-carousel-item>
      <el-carousel-item><el-image :src="require('../assets/guide2.png')" fit="fill"/></el-carousel-item>
    </el-carousel>
  </el-dialog>
  <el-dialog v-model="this.dialogBool" width="600px">
    <el-form ref="findPasswordRef" :model="findPassword" :rules="findPasswordRules">
        <h2 class="title">找回密码</h2>
        <div class="input-field">
          <i class="fa-solid fa-envelope"></i>
          <el-form-item prop="email">
            <el-input v-model="findPassword.email" placeholder="输入你的邮箱" />
          </el-form-item>
        </div>
        <div class="input-field">
          <i class="fa-solid fa-envelope"></i>
          <el-form-item prop="code">
            <el-input v-model="findPassword.code" placeholder="输入验证码" style="width: auto;"/>
            <el-button type="primary" @click="SendCode(this.findPassword,'Find_Password')" :disabled="codeBool" style="width: 30%;">{{ codeString }}</el-button>
          </el-form-item>
        </div>
        <div class="input-field">
          <i class="fa-solid fa-lock"></i>
          <el-form-item prop="password">
            <el-input v-model="findPassword.password" maxlength="30" type="password" placeholder="8-30位密码" autocomplete="off" show-password />
          </el-form-item>
        </div>
        <div class="input-field">
          <i class="fa-solid fa-lock"></i>
          <el-form-item prop="confirmPassword">
            <el-input v-model="findPassword.confirmPassword" maxlength="30" type="password" placeholder="确认密码" autocomplete="off" show-password />
          </el-form-item>
        </div>
        <el-button type="primary" :loading="findPasswordLoading" @click="FindPassword()" class="btn form" round>
          {{findPasswordLoading ? '重置中' : '重置'}}
        </el-button>
      </el-form>
  </el-dialog>
  <div class="container" id="app">
  <div class="forms-container">
    <div class="signin-signup">
      <el-form ref="loginRef" :model="loginForm" :rules="loginRules" class="sign-in-form">
        <h2 class="title">登录</h2>
        <div class="input-field">
          <i class="fa-solid fa-user"></i>
          <el-form-item prop="name">
            <el-input v-model="loginForm.name" maxlength="25" placeholder="昵称" @keyup.enter="Login(loginForm)" />
          </el-form-item>
        </div>
        <div class="input-field">
          <i class="fa-solid fa-lock"></i>
          <el-form-item prop="password">
            <el-input v-model="loginForm.password" type="password" maxlength="30" placeholder="8-30位密码" autocomplete="off" show-password
              @keyup.enter="Login(loginForm)" />
          </el-form-item>
        </div>
        <el-button type="primary" :loading="loginLoading" @click="Login()" class="btn form" round>
          {{loginLoading ? '登 录 中' : '登 录'}}
        </el-button>
        <el-button type="primary" text="true" @click="ForgetPassword()" class="form" round>
          忘记密码
        </el-button>
      </el-form>
      <el-form ref="signUpRef" :model="signUpForm" :rules="signUpRules" class="sign-up-form">
        <h2 class="title">注册</h2>
        <div class="input-field">
          <i class="fa-solid fa-user"></i>
          <el-form-item prop="name">
            <el-input v-model="signUpForm.name" maxlength="25" placeholder="昵称" />
          </el-form-item>
        </div>
        <div class="input-field">
          <i class="fa-solid fa-lock"></i>
          <el-form-item prop="password">
            <el-input v-model="signUpForm.password" maxlength="30" type="password" placeholder="8-30位密码" autocomplete="off" show-password />
          </el-form-item>
        </div>
        <div class="input-field">
          <i class="fa-solid fa-lock"></i>
          <el-form-item prop="confirmPassword">
            <el-input v-model="signUpForm.confirmPassword" maxlength="30" type="password" placeholder="确认密码" autocomplete="off" show-password />
          </el-form-item>
        </div>
        <div class="input-field">
          <i class="fa-solid fa-envelope"></i>
          <el-form-item prop="email">
            <el-input v-model="signUpForm.email" placeholder="输入你的邮箱" />
          </el-form-item>
        </div>
        <div class="input-field">
          <i class="fa-solid fa-envelope"></i>
          <el-form-item prop="code">
            <el-input v-model="signUpForm.code" placeholder="输入验证码" style="width: auto;"/>
            <el-button type="primary" @click="SendCode(this.signUpForm,'Register')" :disabled="codeBool" style="width: 30%;">{{ codeString }}</el-button>
          </el-form-item>
        </div>
        <el-button type="primary" :loading="signUploading" @click="SignUp()" class="btn form" round>
          {{signUploading ? '注 册 中' : '注 册'}}
        </el-button>
      </el-form>
    </div>
  </div>
  <div class="panels-container">
    <div class="panel left-panel">
      <div class="content">
        <h3>新用户 ?</h3>
        <p>
          输入您的信息成为我们的客户
        </p>
        <button class="btn transparent" id="sign-up-btn">
          注 册
        </button>
      </div>
      <img src="./img/log.svg" class="image" alt="" />
    </div>
    <div class="panel right-panel">
      <div class="content">
        <h3>已有账号 ?</h3>
        <p>
          请登录以享受我们更多的服务
        </p>
        <button class="btn transparent" id="sign-in-btn">
          登 录
        </button>
      </div>
      <img src="./img/register.svg" class="image" alt="" />
    </div>
  </div>
</div>
</template>

<style  scoped>
@import url('./css/fontawesome-all.min.css');
</style>
<style  scoped>
.el-button.is-round {
  border-radius: 49px;
}
.el-form-item {
  margin-bottom: 0;
}
.el-form-item.is-error .el-input__inner,
.el-form-item.is-error .el-input__inner:focus,
.el-form-item.is-error .el-select-v2__wrapper,
.el-form-item.is-error .el-select-v2__wrapper:focus,
.el-form-item.is-error .el-textarea__inner,
.el-form-item.is-error .el-textarea__inner:focus {
  box-shadow: none;
}
.el-input {
  align-items: center;
  margin-right: 8px;
}

.el-input .el-input__icon {
font-size: 1.4em;
}
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body,
input {
font-family: "Poppins", sans-serif;
}
.container {
position: relative;
width: 100%;
background-color: #fff;
min-height: 100vh;
overflow: hidden;
}

.forms-container {
position: absolute;
width: 100%;
height: 100%;
top: 0;
left: 0;
}

.signin-signup {
position: absolute;
top: 50%;
transform: translate(-50%, -50%);
left: 75%;
width: 50%;
transition: 1s 0.7s ease-in-out;
display: grid;
grid-template-columns: 1fr;
z-index: 5;
}

form {
display: flex;
align-items: center;
justify-content: center;
flex-direction: column;
padding: 0rem 5rem;
transition: all 0.2s 0.7s;
overflow: hidden;
grid-column: 1 / 2;
grid-row: 1 / 2;
}

form.sign-up-form {
opacity: 0;
z-index: 1;
}

form.sign-in-form {
z-index: 2;
}

.title {
font-size: 2.2rem;
color: #444;
margin-bottom: 10px;
}

.input-field {
max-width: 380px;
width: 100%;
background-color: #f0f0f0;
margin: 10px 0;
height: 55px;
border-radius: 55px;
display: grid;
grid-template-columns: 15% 85%;
padding: 0 0.4rem;
position: relative;
}

.input-field i {
text-align: center;
line-height: 55px;
color: #acacac;
transition: 0.5s;
font-size: 1.1rem;
}

.input-field input {
background: none;
outline: none;
border: none;
line-height: 1;
font-weight: 600;
font-size: 1.1rem;
color: #333;
}

.input-field input::placeholder {
color: #aaa;
font-weight: 500;
}

.input-field .el-input input {
background: none;
outline: none;
border: none;
line-height: 1;
font-weight: 600;
font-size: 1.1rem;
color: #333;
}

.input-field .el-input input::placeholder {
color: #aaa;
font-weight: 500;
}

.social-text {
padding: 0.7rem 0;
font-size: 1rem;
}

.social-media {
display: flex;
justify-content: center;
}

.social-icon {
height: 46px;
width: 46px;
display: flex;
justify-content: center;
align-items: center;
margin: 0 0.45rem;
color: #333;
border-radius: 50%;
border: 1px solid #333;
text-decoration: none;
font-size: 1.1rem;
transition: 0.3s;
}

.social-icon:hover {
color: #4481eb;
border-color: #4481eb;
}

.btn {
width: 150px;
background-color: #4481eb;
border: none;
outline: none;
height: 49px;
border-radius: 49px;
color: #fff;
text-transform: uppercase;
font-weight: 600;
margin: 10px 0;
cursor: pointer;
transition: 0.5s;
}

.btn:hover {
background-color: #87e0b8;
}

.panels-container {
position: absolute;
height: 100%;
width: 100%;
top: 0;
left: 0;
display: grid;
grid-template-columns: repeat(2, 1fr);
}

.container:before {
content: "";
position: absolute;
height: 2000px;
width: 2000px;
top: -10%;
right: 48%;
transform: translateY(-50%);
background-image: linear-gradient(-45deg, #4481eb 0%, #4481eb 100%);
transition: 1.8s ease-in-out;
border-radius: 50%;
z-index: 6;
}

.image {
width: 100%;
transition: transform 1.1s ease-in-out;
transition-delay: 0.4s;
}

.panel {
display: flex;
flex-direction: column;
align-items: flex-end;
justify-content: space-around;
align-items: center;
text-align: center;
z-index: 6;
}

.left-panel {
pointer-events: all;
padding: 3rem 17% 2rem 12%;
}

.right-panel {
pointer-events: none;
padding: 3rem 12% 2rem 17%;
}

.panel .content {
color: #fff;
transition: transform 0.9s ease-in-out;
transition-delay: 0.6s;
}

.panel h3 {
font-weight: 600;
line-height: 1;
font-size: 1.5rem;
}

.panel p {
font-size: 0.95rem;
padding: 0.7rem 0;
}

.btn.transparent {
margin: 0;
background: none;
border: 2px solid #fff;
width: 130px;
height: 41px;
font-weight: 600;
font-size: 0.8rem;
}

.btn.transparent:hover {
background: #fff;
color: #42b983;
}

.right-panel .image,
.right-panel .content {
transform: translateX(800px);
}

/* ANIMATION */

.container.sign-up-mode:before {
transform: translate(100%, -50%);
right: 52%;
}

.container.sign-up-mode .left-panel .image,
.container.sign-up-mode .left-panel .content {
transform: translateX(-800px);
}

.container.sign-up-mode .signin-signup {
left: 25%;
}

.container.sign-up-mode form.sign-up-form {
opacity: 1;
z-index: 2;
}

.container.sign-up-mode form.sign-in-form {
opacity: 0;
z-index: 1;
}

.container.sign-up-mode .right-panel .image,
.container.sign-up-mode .right-panel .content {
transform: translateX(0%);
}

.container.sign-up-mode .left-panel {
pointer-events: none;
}

.container.sign-up-mode .right-panel {
pointer-events: all;
}

@media (max-width: 870px) {
.container {
  min-height: 800px;
  height: 100vh;
}

.signin-signup {
  width: 100%;
  top: 95%;
  transform: translate(-50%, -100%);
  transition: 1s 0.8s ease-in-out;
}

.signin-signup,
.container.sign-up-mode .signin-signup {
  left: 50%;
}

.panels-container {
  grid-template-columns: 1fr;
  grid-template-rows: 1fr 2fr 1fr;
}

.panel {
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  padding: 2.5rem 8%;
  grid-column: 1 / 2;
}

.right-panel {
  grid-row: 3 / 4;
}

.left-panel {
  grid-row: 1 / 2;
}

.image {
  width: 200px;
  transition: transform 0.9s ease-in-out;
  transition-delay: 0.6s;
}

.panel .content {
  padding-right: 15%;
  transition: transform 0.9s ease-in-out;
  transition-delay: 0.8s;
}

.panel h3 {
  font-size: 1.2rem;
}

.panel p {
  font-size: 0.7rem;
  padding: 0.5rem 0;
}

.btn.transparent {
  width: 110px;
  height: 35px;
  font-size: 0.7rem;
}

.container:before {
  width: 1500px;
  height: 1500px;
  transform: translateX(-50%);
  left: 30%;
  bottom: 68%;
  right: initial;
  top: initial;
  transition: 2s ease-in-out;
}

.container.sign-up-mode:before {
  transform: translate(-50%, 100%);
  bottom: 32%;
  right: initial;
}

.container.sign-up-mode .left-panel .image,
.container.sign-up-mode .left-panel .content {
  transform: translateY(-300px);
}

.container.sign-up-mode .right-panel .image,
.container.sign-up-mode .right-panel .content {
  transform: translateY(0px);
}

.right-panel .image,
.right-panel .content {
  transform: translateY(300px);
}

.container.sign-up-mode .signin-signup {
  top: 5%;
  transform: translate(-50%, 0);
}
}

@media (max-width: 570px) {
form {
  padding: 0 1.5rem;
}

.image {
  display: none;
}

.panel .content {
  padding: 0.5rem 1rem;
}

.container {
  padding: 1.5rem;
}

.container:before {
  bottom: 72%;
  left: 50%;
}

.container.sign-up-mode:before {
  bottom: 28%;
  left: 50%;
}
}
</style>

<script>
import store from '@/store';
import { ref, watch } from 'vue';
import { ElMessage } from 'element-plus';
import { userRister, userLogin, sendVCode, findPassword, getUserGroup } from '../api/user.js';

export default{
  data() {
    return {
      openGuide: false,
      codeBool: false,
      codeString: '获取验证码',
      loginLoading: false,
      signUploading: false,
      loginForm: {
        name: '',
        password: ''
      },
      signUpForm: {
        name: '',
        password: '',
        confirmPassword: '',
        email: '',
        code: ''
      },
      dialogBool: false,
      findPasswordLoading: false,
      findPassword:{
        email: '',
        code: '',
        password: '',
        confirmPassword: '',
      },
      findPasswordRules: {
        email: [{
          validator: (rule, value, callback) => {
            if (value === '') {
              callback(new Error('请输入邮箱'));
            } else {
              callback();
            }
          }, type: 'string', trigger: 'blur'}],
        code: [{
          validator: (rule, value, callback) => {
            if (value === '') {
              callback(new Error('请输入验证码'));
            } else {
              callback();
            }
          }, type: 'string', trigger: 'blur'}],
        password: [{ 
          validator: (rule, value, callback) => {
            if (value.length<8) {
              callback(new Error('请输入至少8位密码'));
            } else {
              callback();
            }
          },type: 'string', trigger: 'blur' }],
        confirmPassword: [{
          validator: (rule, value, callback) => {
            if (value === '') {
              callback(new Error('请再次输入密码'));
            } else if (value !== this.findPassword.password) {
              callback(new Error('两次输入密码不一致!'));
            } else {
              callback();
            }
          }, type: 'string', trigger: 'blur'}]
      },
      loginRules: {
        name: [{ required: true, message: '请输入用户名', type: 'string', trigger: 'blur' }],
        password: [{ 
          validator: (rule, value, callback) => {
            if (value.length<8) {
              callback(new Error('请输入至少8位密码'));
            } else {
              callback();
            }
          },type: 'string', trigger: 'blur' }],
      },
      signUpRules: {
        name: [{ required: true, message: '请输入用户名', type: 'string', trigger: 'blur' }],
        password: [{ 
          validator: (rule, value, callback) => {
            if (value.length<8) {
              callback(new Error('请输入至少8位密码'));
            } else {
              callback();
            }
          },type: 'string', trigger: 'blur' }],
        confirmPassword: [{
          validator: (rule, value, callback) => {
            if (value === '') {
              callback(new Error('请再次输入密码'));
            } else if (value !== this.signUpForm.password) {
              callback(new Error('两次输入密码不一致!'));
            } else {
              callback();
            }
          }, type: 'string', trigger: 'blur'}],
        email: [{
          validator: (rule, value, callback) => {
            if (value === '') {
              callback(new Error('请输入邮箱'));
            } else {
              callback();
            }
          }, type: 'string', trigger: 'blur'}],
        code: [{
          validator: (rule, value, callback) => {
            if (value === '') {
              callback(new Error('请输入验证码'));
            } else {
              callback();
            }
          }, type: 'string', trigger: 'blur'}]
      },
    }
},
    created() {
      this.loginLoading = false
      this.signUploading = false
    },
    mounted() {
      if(store.state.isLogin==true){
        this.$router.push('/'+store.state.uid+'/GroupPage')
      }
      const sign_in_btn = document.querySelector("#sign-in-btn")
      const sign_up_btn = document.querySelector("#sign-up-btn")
      const container = document.querySelector(".container")
      sign_up_btn.addEventListener("click", () => {
      container.classList.add("sign-up-mode")
      })
      sign_in_btn.addEventListener("click", () => {
        container.classList.remove("sign-up-mode")
      })
    },
    methods: {
        Login() {
          this.$refs.loginRef.validate((valid) => {
            if (valid) {
              var promise1=userLogin(this.loginForm.name,this.loginForm.password);
              promise1.then((result)=>{
                if(this.MessageCatch(result)){
                  store.commit('Login',result.token);
                  var promise2=getUserGroup();
                  promise2.then((result)=>{
                    if(this.MessageCatch(result)){
                      store.commit('updateGroupList',result.data);
                      if(store.state.userGroupList.length==0){
                        this.$router.push('/'+store.state.uid+'/GroupPage/0');
                      }
                      else{
                        this.$router.push('/'+store.state.uid+'/GroupPage/'+store.state.userGroupList[0].id);
                      }
                    }
                    else{
                      ElMessage({
                        message: "获取信息失败，已退出登录",
                        grouping: true,
                        type: 'error',
                      })
                      store.commit('Logout');
                    }
                  })
                }
              })
            }
          })
        },
        SignUp() {
          this.$refs.signUpRef.validate((valid) => {
            if (valid) {
              var promise=userRister(this.signUpForm.name, this.signUpForm.password, this.signUpForm.confirmPassword, this.signUpForm.email, this.signUpForm.code);
              promise.then((result)=>{
                if(this.MessageCatch(result)){
                  this.openGuide=true;
                }
              })
            }
          })
        },
        ForgetPassword(){
          this.dialogBool=true;
        },
        FindPassword(){
          this.$refs.findPasswordRef.validate((valid) => {
            if(valid){
              var promise=findPassword(this.findPassword.email, this.findPassword.code, this.findPassword.password, this.findPassword.confirmPassword);
              promise.then((result)=>{
                this.MessageCatch(result);
                this.dialogBool=false;
              })
            }
          })
        },
        SendCode(form,type){
          if(form.email==''){
            ElMessage({
              message: '请输入您的邮箱',
              grouping: true,
              type: 'warning',
            })
          }
          else{
            var promise=sendVCode(form.email,type);
            promise.then((result)=>{
              if(this.MessageCatch(result)){
                this.codeBool=true;
                const num=ref(60);
                watch(()=>num.value,(newValue)=>{
                  this.codeString=newValue;
                });
                let timer=setInterval(function(){
                  num.value--;
                  if(num.value==0){
                    this.codeString='获取验证码';
                    this.codeBool=false;
                    clearInterval(timer);
                  }
                },1000);
              }
            });
          }
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
        }
    }
}
</script>