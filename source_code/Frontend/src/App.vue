<template style="margin: 0; padding: 0; background-color: black">
  <el-dialog v-model="this.genshinG" width="1200px" style="height: 600px;" title="新手指引" top="10vh">
    <el-container style="display: flex;height: 510px;margin-top: -20px;">
      <el-aside width="18%" style="height: 510px;">
        <el-scrollbar max-height="500px">
          <el-button type="primary" v-for="item in this.guideContent.count" :key="item" :plain="item-1!=this.guideContent.current" class="guide-list" @click="this.GuideSwitch(item-1)">{{ this.guideContent.list[item-1].name }}</el-button>
        </el-scrollbar>
      </el-aside>
      <el-divider direction="vertical" style="height: 510px;"/>
      <el-aside width="82%" style="height: 510px;">
        <el-carousel autoplay="false" trigger="click" height="500px">
          <el-carousel-item v-for="i in this.guideContent.list[this.guideContent.current].count" :key="item">
            <div style="align-items: center;height: 500px;">
              <el-image fit="fill" :src="this.guideContent.list[this.guideContent.current].url[i-1]" style="width: 930px;height: 500px;"/>
            </div>
          </el-carousel-item>
        </el-carousel>
      </el-aside>
    </el-container>
  </el-dialog>
  <el-header v-if="this.$store.state.isLogin" style="height: 48px; background-color:rgb(42, 159, 235);">
    <el-row :gutter="10" style=" color: white;">
    <el-col :span="1" @click="displayDrawer">
      <div class="grid-content header-icon"><el-icon><Menu /></el-icon></div>
    </el-col>
    <el-col :span="6"><div id="site-name" class="grid-content" style="text-align: left;" @click="this.$router.push('/'+this.$store.state.uid+'/GroupPage/0')">Originate Pro</div></el-col>
    <el-col :span="15">
      <!-- <div class="grid-content">    <el-button @click="testNotification(20)">(测试用)添加20条消息</el-button>
      <el-button @click="this.$router.push('/1/1/1/DocumentPage')">(测试用)富文本编辑器</el-button></div> -->
    </el-col>
    <el-col :span="1">
      <div class="grid-content header-icon">
        <el-popover
          placement="bottom"
          title="我的通知"
          :width="300"
          trigger="hover"
          content="进一步分为已读通知和未读通知"
        >
        <template #reference>
          <el-icon v-if="this.$store.state.notificationUnread.length!=0" style="color: orange"><BellFilled /></el-icon>  
          <el-icon v-else><Bell /></el-icon>
        </template>
        <el-menu
          default-active="1"
          class="el-menu-demo"
          mode="horizontal"
          :ellipsis="false"
        >
          <el-menu-item index="1" @click="displayNotification(1)">未读通知</el-menu-item>
          <el-menu-item index="2" @click="displayNotification(2)">已读通知</el-menu-item>
          <div class="flex-grow" />
          <el-menu-item index="3" @click="displayNotification(3)">操作</el-menu-item>
        </el-menu>
        <el-scrollbar max-height="500px" v-if="notificationsDisplay===1">
          <div class="notification-item" 
            v-for="(item, index) in this.$store.state.notificationUnread"
            :key="index">
            <el-row v-if="item.t==='邀请'" style="margin-top: 1px;" justify="start">
              <el-col :span="20" @click="calloutNotification(item,1)" style="text-align: left;">
                <el-button type="primary" plain>邀请</el-button>
              </el-col>
              <el-col :span="2">
                <el-icon class="notification-deal delete-message-btn" @click="deleteNotification(item.id)"><Delete /></el-icon>
              </el-col>
              <el-col :span="2" class="notification-deal">
                <el-icon @click="addReadNotification(item.id)"><CircleCheckFilled /></el-icon>
              </el-col>
            </el-row>
            <el-row v-if="item.t==='邀请'" class="notification-content" @click="calloutNotification(item,1)">
              {{item.c}}
            </el-row>
            <el-row v-if="item.t==='@document' || item.t==='@chat'" style="margin-top: 1px;" justify="start">
              <el-col :span="20" @click="calloutNotification(item,1)" style="text-align: left;">
                <el-button type="danger" plain>@你</el-button>
              </el-col>
              <el-col :span="2">
                <el-icon class="delete-message-btn notification-deal" @click="deleteNotification(item.id)"><Delete /></el-icon>
              </el-col>
              <el-col :span="2" class="notification-deal">
                <el-icon @click="addReadNotification(item.id)"><CircleCheckFilled /></el-icon>
              </el-col>
            </el-row>
            <el-row v-if="item.t==='@document' || item.t==='@chat'" class="notification-content" @click="calloutNotification(item,1)">
              {{item.c}}
            </el-row>
            <el-row v-if="item.t==='普通'" style="margin-top: 1px;" justify="start">
              <el-col :span="20" @click="calloutNotification(item,1)" style="text-align: left;">
                <el-button type="info" plain>普通</el-button>
              </el-col>
              <el-col :span="2">
                <el-icon class="notification-deal delete-message-btn" @click="deleteNotification(item.id)"><Delete /></el-icon>
              </el-col>
              <el-col :span="2" class="notification-deal">
                <el-icon @click="addReadNotification(item.id)"><CircleCheckFilled /></el-icon>
              </el-col>
            </el-row>
            <el-row v-if="item.t==='普通'" class="notification-content" @click="calloutNotification(item,1)">
              {{item.c}}
            </el-row>
          </div>
        </el-scrollbar>
        <el-scrollbar max-height="500px" v-if="notificationsDisplay===2">
          <div class="notification-item" 
            v-for="(item, index) in this.$store.state.notificationRead"
            :key="index">
            <el-row v-if="item.t==='邀请'" style="margin-top: 1px;" justify="start">
              <el-col :span="22" @click="calloutNotification(item,2)" style="text-align: left;">
                <el-button type="primary" plain>邀请</el-button>
              </el-col>
              <el-col :span="2">
                <el-icon class="notification-deal delete-message-btn" @click="deleteNotification(item.id)"><Delete /></el-icon>
              </el-col>
            </el-row>
            <el-row v-if="item.t==='邀请'" class="notification-content" :title="item.c" @click="calloutNotification(item,2)">
              {{item.c}}
            </el-row>
            <el-row v-if="item.t==='@document' || item.t==='@chat'" style="margin-top: 1px;" justify="start">
              <el-col :span="22" @click="calloutNotification(item,2)" style="text-align: left;">
                <el-button type="danger" plain>@你</el-button>
              </el-col>
              <el-col :span="2">
                <el-icon class="delete-message-btn notification-deal" @click="deleteNotification(item.id)"><Delete /></el-icon>
              </el-col>
            </el-row>
            <el-row v-if="item.t==='@document' || item.t==='@chat'" class="notification-content" :title="item.c" @click="calloutNotification(item,2)">
              {{item.c}}
            </el-row>
            <el-row v-if="item.t==='普通'" style="margin-top: 1px;" justify="start">
              <el-col :span="22" @click="calloutNotification(item,2)" style="text-align: left;">
                <el-button type="info" plain>普通</el-button>
              </el-col>
              <el-col :span="2">
                <el-icon class="notification-deal delete-message-btn" @click="deleteNotification(item.id)"><Delete /></el-icon>
              </el-col>
            </el-row>
            <el-row v-if="item.t==='普通'" class="notification-content" :title="item.c" @click="calloutNotification(item,2)">
              {{item.c}}
            </el-row>
          </div>
        </el-scrollbar>
        <el-scrollbar max-height="500px" v-if="notificationsDisplay===3">
          <el-row style="margin-top: 10px;" justify="end">
            <el-button type="primary" :icon="Search" @click="setAllReadNotificationRead()">设置所有通知为已读
              <el-icon class="el-icon--right"><Finished /></el-icon>
            </el-button>
          </el-row>
          <el-row style="margin-top: 10px;" justify="end">
            <el-button type="danger" @click="deleteAllNotificaitonRead()">删除所有的已读通知
              <el-icon class="el-icon--right"><DeleteFilled /></el-icon>
            </el-button>
          </el-row>
        </el-scrollbar>
        </el-popover>
      </div>
    </el-col>
    <el-col :span="1">
      <div class="grid-content header-icon">
        <el-popover
          placement="bottom"
          title=""
          :width="200"
          trigger="hover"
          content="个人信息，修改密码，退出登录"
        >
        <template #reference>
          <el-icon><User /></el-icon>
        </template>
          <div class="drawer-item" @click="this.$router.push('/'+this.$store.state.uid+'/PersonalInfomation');">个人信息</div>
          <div class="drawer-item" @click="resetPassword()">修改密码</div>
          <div id="logout-button" @click="logout()" class="drawer-item">退出登录</div>
        </el-popover>
      </div>
    </el-col>
    </el-row>
  </el-header>
  <el-header v-else style="height: 48px; background-color:rgb(42, 159, 235);">
    <el-row :gutter="10" style=" color: white;">
    <el-col :span="1"></el-col>
    <el-col :span="6"><div class="grid-content" style="text-align: left;">Originate Pro</div></el-col>
    <el-col :span="15"></el-col>
    <el-col :span="1"></el-col>
    <el-col :span="1"></el-col>
    </el-row>
  </el-header>
  <el-main style="overflow: hidden;">
    <div style="height: 10px;"></div>
    <el-scrollbar>
    <router-view/>
    </el-scrollbar>
  </el-main>
  <el-drawer
    v-model="drawer"
    title="Originate Pro"
    direction="ltr"
    size="25%"
  >
    <div class="drawer-item" @click="undisplayDrawer(1)">我的团队</div>
    <div class="drawer-item" @click="undisplayDrawer(2)">我的聊天</div>
    <div class="drawer-item" @click="undisplayDrawer(3)">我的项目</div>
    <div style="cursor: default; background-color: rgba(0,0,0,0); height:40vh"></div>
    <div class="drawer-item" @click="undisplayDrawer(4)">新手教程</div>
  </el-drawer>
  <el-dialog v-model="this.dialogBool" width="600px">
    <el-form ref="findPasswordRef" :model="findPassword" :rules="findPasswordRules">
        <h2 class="title">修改密码</h2>
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
  <el-dialog v-model="centerDialogVisible" title="通知详情" width="35%" center>
    <el-scrollbar max-height="300px">
      <div style="max-width: 100%; word-break: break-all; text-align: center;">{{ localDialogNotification.content }}</div>
    </el-scrollbar>
    <template #footer>
      <span class="dialog-footer">
        <el-button v-if="localDialogNotification.type==='邀请'" type="danger" @click="centerDialogVisible = false; rejectInvitaion()">拒绝</el-button>
        <el-button v-if="localDialogNotification.type==='邀请'" type="success" @click="centerDialogVisible = false; acceptInvitation()">接受</el-button>
        <el-button v-if="localDialogNotification.type==='@document'" type="warning" @click="centerDialogVisible = false; jumpToTeamDocument()">
          跳转
        </el-button>
        <el-button v-if="localDialogNotification.type==='@chat'" type="warning" @click="centerDialogVisible = false; jumpToTeamChat()">
          跳转
        </el-button>
        <el-button v-if="localDialogNotification.type==='@document' || localDialogNotification.type==='@chat'" type="primary" @click="centerDialogVisible = false">
          确定
        </el-button>
        <el-button v-if="localDialogNotification.type==='普通'" type="primary" @click="centerDialogVisible = false">
          确定
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

#site-name{
  transition: 0.2s;
}

#site-name:hover{
  cursor: pointer;
  scale: 1.05;
  transition: 0.2s;
}

.el-header {
  position: relative;
  width: 100%;
  height: 48px;      
}

.el-main {
  position: absolute;
  left: 0;
  right: 0;
  top: 48px;
  bottom: 0;
  overflow-y: scroll;
}


/* .el-row {
  
} */
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}

.grid-content {
  font-size: 24px;
  min-height: 48px;
  line-height: 48px;
}

.header-icon {
  margin-top: 3px;
  transition: 0.2s;
}

.header-icon:hover {
  cursor: pointer;
  scale: 1.2;
  transition: 0.2s;
}

.drawer-item {
  /* display: flex; */
  align-items: center;
  /*justify-content: center;*/
  height: 50px;
  line-height: 50px;
  margin: 10px;
  /*padding-left: 5px;*/
  text-align: center;
  border-radius: 4px;
  color: black;
  transition: 0.5s;
  overflow: hidden;
}

.drawer-item:hover {
  cursor: pointer;
  background: rgba(125, 125, 125, 0.25);
  /* color: rgb(42, 159, 235); */
  transition: 0.2s;
}

.notifiction-set-holder {
  max-height: 600px;
  overflow: scroll;
  overflow-x: hidden;
}

#logout-button {
  color: red;
}

#logout-button:hover {
  background: rgba(255, 0, 0, 0.25);
}

.flex-grow {
  flex-grow: 1;
}

.notification-item {
  align-items: center;
  /*justify-content: center;*/
  height: 80px;
  line-height: 40px;
  margin: 10px;
  /*padding-left: 5px;*/
  text-align: center;
  border-radius: 4px;
  color: black;
  transition: 0.5s;
  overflow: hidden;
  border-bottom: rgba(42, 159, 235, 0.5) 1px solid;
}

.notification-item:hover {
  cursor: pointer;
  background: rgba(236, 245, 255, 1);
  /* color: rgb(42, 159, 235); */
  transition: 0.2s;
}

.notification-content {
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
  -o-text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
  display: block;
}

.notification-deal {
  transition: 0.2s;
}

.notification-deal:hover{
  scale: 1.25;
  transition: 0.2s;
  /* color: rgb(42, 159, 235); */
  color: white;
  background-color: rgb(42, 159, 235);
}

.delete-message-btn:hover{
  color: red;
  scale: 1.5;
  background-color: rgba(0,0,0,0);
}

</style>
<style  scoped>
@import url('./views/css/fontawesome-all.min.css');
</style>
<style  scoped>
.guide-list {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80%;
  height: 40px;
  margin: 10px;
  text-align: center;
}
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
let ws;
import { sendVCode, findPassword } from './api/user.js';
import { ElMessage } from 'element-plus';
import { ref, watch } from 'vue';
import store from './store';
import router from './router';
import { ElNotification } from 'element-plus';


export default {
    data () {
      return {
        sitename:"Originate Pro",
        header: false,
        drawer: false,
        notificationsDisplay: 1,
        notificationUnread: {
          type: "",
          by: "",
          content: "",
          ms: [],
        },
        notificationRead: {
          type: "",
          by: "",
          content: "",
          ms: [],
        },
        genshinG: false,
        centerDialogVisible: false,
        localDialogNotification: {
            type: "邀请",
            by: "来自我",
            forthing: "为了爱",
            content: "这是一个示例通知",
            group_id: 0,
            project_id: 0,
            item_id: 0,
            from: 1,
            group_type:'team',
        },
        guideContent:{"count" : 7,
          "current" : 0, 
          "list" : [{
            "name": "侧边栏",
            "count": 2,
            "url": [require('./assets/aside1.png'),require('./assets/aside2.png')],
          },{
            "name": "消息中心与账户",
            "count": 3,
            "url": [require('./assets/message1.png'),require('./assets/message2.png'),require('./assets/message3.png')],
          },{
            "name": "聊天室",
            "count": 3,
            "url": [require('./assets/chat1.png'),require('./assets/chat2.png'),require('./assets/chat3.png')],
          },{
            "name": "团队管理",
            "count": 3,
            "url": [require('./assets/group1.png'),require('./assets/group2.png'),require('./assets/group3.png')],
          },{
            "name": "项目管理",
            "count": 3,
            "url": [require('./assets/project1.png'),require('./assets/project2.png'),require('./assets/project3.png')],
          },{
            "name": "设计页面原型",
            "count": 2,
            "url": [],
          },{
            "name": "在线文档",
            "count": 2,
            "url": [],
          },]
        },
        codeBool: false,
        codeString: '获取验证码',
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
        }
      }
    },

    mounted() {
      // this.websocketInit();
    },

    watch: {
      "$store.state.isLogin" (newStore,oldStore){
        if (newStore===true)
          this.websocketInit();
      },
    },

    methods: {
      GuideSwitch(index){
        this.guideContent.current=index;
      },
      displayDrawer() {
        this.drawer = true;
      },
      undisplayDrawer(jumpto) {
        if (jumpto===1)
          router.push('/'+store.state.uid+'/GroupPage/0');
        else if (jumpto===2)
          router.push('/'+store.state.uid+'/Chatroom');
        else if (jumpto===3)
          router.push('/'+store.state.uid+'/0/MyProject/0');
        else if (jumpto===4)
          this.genshinG = true;
        this.drawer = false;
      },
      displayNotification(type) {
        this.notificationsDisplay = type;
      },
      resetPassword() {
        this.dialogBool=true;
      },
      logout() {
        if (ws)
          ws.close();
        store.commit('Logout');
        router.push('/');
      },
      jumpRouter(to) {
        router.push(to);
      },
      calloutNotification(item,from){
        this.localDialogNotification.type = item.t;
        this.localDialogNotification.by = item.b;
        this.localDialogNotification.forthing = item.f;
        this.localDialogNotification.content = item.c;
        if (item.t==='@document'){
          this.localDialogNotification.group_id = item.f;
          this.localDialogNotification.project_id = item.pid;
          this.localDialogNotification.item_id = item.did;
        }
        if (item.t==='邀请')
          this.localDialogNotification.group_type = item.group_type;
        this.centerDialogVisible = true;
        if (from===1)
          this.addReadNotification(item.id);
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
      },
      addReadNotification(id) {
        store.commit('addNotificationRead',id);
        var newObj = {
          type: "func",
          func: "process",
          data: [id],
        }
        ws.send(JSON.stringify(newObj));
      },
      deleteNotification(id) {
        store.commit('deleteNotification',id);
        var newObj = {
          type: "func",
          func: "delete",
          data: [id],
        }
        ws.send(JSON.stringify(newObj));
      },
      setAllReadNotificationRead() {
        var messageList=[];
        store.state.notificationUnread.some(function (value) {
          messageList.push(value.id);
        });
        var newObj = {
          type: "func",
          func: "process",
          data: messageList,
        }
        ws.send(JSON.stringify(newObj));
        store.commit('setAllNotificationRead');
      },
      deleteAllNotificaitonRead() {
        var messageList=[];
        store.state.notificationRead.some(function (value) {
          messageList.push(value.id);
        });
        var newObj = {
          type: "func",
          func: "delete",
          data: messageList,
        }
        ws.send(JSON.stringify(newObj));
        store.commit('deleteAllNotificationRead');
      },

      websocketInit() {
      var that = this;
      ws = new WebSocket("ws://8.130.25.189/ws/notification/");
      ws.onopen = function () {
        console.log("消息中心的websocket已打开");
        var newObj = {
          type: "func",
          func: "get",
          data: [store.state.uid],
        }
        ws.send(JSON.stringify(newObj));
      };
      ws.onmessage = function (message) {
        var parsedData = JSON.parse(message.data);
        console.log(parsedData);
        if (parsedData.type){
          var isMyMessage = true;
      console.log("single",parsedData);
      if (parsedData.receiver_id && parsedData.receiver_id!=store.state.uid){
        isMyMessage = false;
        console.log("not my message!");
          }
          if (isMyMessage) {
            if (parsedData.type==='invite') {
              var newObj;
              if (parsedData.group_type==='team'){
                newObj = {
                id: parsedData.id,
                type: "邀请",
                by: parsedData.sender_id,
                forthing: parsedData.team_id,
                content: parsedData.content,
                group_type:'team',
              }
              } else {
                newObj = {
                id: parsedData.id,
                type: "邀请",
                by: parsedData.sender_id,
                forthing: parsedData.group_id,
                content: parsedData.content,
                group_type:'group',
                }
              }
              if (parsedData.processed===false){
                store.commit('addNotificationUnread',newObj);
                var flagRepeat = false;
                store.state.notificationRead.some(function (value) {
                  if (value.id===parsedData.id){
                    this.flagRepeat = true
                    return true;
                  }
                });
                if (flagRepeat===false){
                  // store.commit('addNotificationUnread',newObj);
                  // ElNotification({
                  // title: '邀请',
                  // message: parsedData.content,
                  // type: 'warning',
                  // position: 'bottom-right',
                  // });
                }
              } else {
                store.commit('addNotificationReadDirect',newObj);
              }
              console.log(newObj);
            } else if(parsedData.type==='at_document'){
                var newObj = {
                id: parsedData.id,
                type: "@document",
                by: parsedData.sender_id,
                forthing: parsedData.team_id,
                content: parsedData.content,
                project_id: parsedData.project_id,
                document_id: parsedData.document_id,
              };
              
              if (parsedData.processed===false){
                var flagRepeat = false;
                store.state.notificationRead.some(function (value) {
                  if (value.id===parsedData.id){
                    this.flagRepeat = true;
                    return true;
                  }
                });
                  if (flagRepeat===false){
                    store.commit('addNotificationUnread',newObj);
                    // ElNotification({
                    // title: '@你-文档',
                    // message: parsedData.content,
                    // type: 'warning',
                    // position: 'bottom-right',
                    // });
                  }
              } else {
                store.commit('addNotificationReadDirect',newObj);
              }
            } else if (parsedData.type==='at_chat') {
              var newObj = {
                id: parsedData.id,
                type: "@chat",
                by: parsedData.sender_id,
                forthing: parsedData.group_id,
                content: parsedData.content,
              };
              if (parsedData.processed===false){
                var flagRepeat = false;
                store.state.notificationRead.some(function (value) {
                  if (value.id===parsedData.id){
                    this.flagRepeat = true;
                    return true;
                  }
                });
                  if (flagRepeat===false){
                    store.commit('addNotificationUnread',newObj);
                    // ElNotification({
                    // title: '@你-聊天',
                    // message: parsedData.content,
                    // type: 'warning',
                    // position: 'bottom-right',
                    // });
                  }
              } else {
                store.commit('addNotificationReadDirect',newObj);
              }
            } else if (parsedData.type==='normal') {
              var newObj = {
                id: parsedData.id,
                type: "普通",
                by: parsedData.sender_id,
                forthing: "",
                content: parsedData.content,
              };
              if (parsedData.processed===false){
                var flagRepeat = false;
                store.state.notificationRead.some(function (value) {
                  if (value.id===parsedData.id){
                    this.flagRepeat = true;
                    return true;
                  }
                });
                  if (flagRepeat===false){
                    store.commit('addNotificationUnread',newObj);
                    // ElNotification({
                    // title: '通知',
                    // message: parsedData.content,
                    // type: 'info',
                    // position: 'bottom-right',
                    // });
                  }
              } else {
                store.commit('addNotificationReadDirect',newObj);
              }
            }
          }
        }
        else {
          var dataset = parsedData.data.data;
          console.log(dataset[0]);
          for (var i=0;i<dataset.length;i++){
              parsedData = dataset[i];
              console.log("plural",parsedData);
                var isMyMessage = true;
                console.log(parsedData);
                if (parsedData.receiver_id && parsedData.receiver_id!=store.state.uid){
                  isMyMessage = false;
                  console.log("not my message!");
                }
                if (isMyMessage) {
                  if (parsedData.type==='invite') {
                    var newObj;
                    if (parsedData.group_type==='team'){
                      newObj = {
                      id: parsedData.id,
                      type: "邀请",
                      by: parsedData.sender_id,
                      forthing: parsedData.team_id,
                      content: parsedData.content,
                      group_type:'team',
                    }
                    } else {
                      newObj = {
                      id: parsedData.id,
                      type: "邀请",
                      by: parsedData.sender_id,
                      forthing: parsedData.group_id,
                      content: parsedData.content,
                      group_type:'group',
                      }
                    }
                    if (parsedData.processed===false){
                      store.commit('addNotificationUnread',newObj);
                    } else {
                      store.commit('addNotificationReadDirect',newObj);
                    }
                    console.log(newObj);
            } else if(parsedData.type==='at_document'){
              var newObj = {
                id: parsedData.id,
                type: "@document",
                by: parsedData.sender_id,
                forthing: parsedData.team_id,
                content: parsedData.content,
                project_id: parsedData.project_id,
                document_id: parsedData.document_id,
              };
              if (parsedData.processed===false){
                store.commit('addNotificationUnread',newObj);
              } else {
                store.commit('addNotificationReadDirect',newObj);
              }
            } else if (parsedData.type==='at_chat') {
              var newObj = {
                id: parsedData.id,
                type: "@chat",
                by: parsedData.sender_id,
                forthing: parsedData.group_id,
                content: parsedData.content,
              };
              if (parsedData.processed===false){
                store.commit('addNotificationUnread',newObj);
              } else {
                store.commit('addNotificationReadDirect',newObj);
              }
            } else if (parsedData.type==='normal') {
                    var newObj = {
                      id: parsedData.id,
                      type: "普通",
                      by: parsedData.sender_id,
                      forthing: "",
                      content: parsedData.content,
                    };
                    if (parsedData.processed===false){
                      store.commit('addNotificationUnread',newObj);
                    } else {
                      store.commit('addNotificationReadDirect',newObj);
                    }
                  }
                }
          }
        }
      };
      ws.onclose = function () {
        console.log("消息中心的websocket已关闭");
      };
    },

    acceptInvitation() {
      if (this.localDialogNotification.group_type==='team'){
        var newObj = {
        type: "invite.response",
        response: "TRUE",
        group_type: 'team',
        sender_id: store.state.uid,
        receiver_id: this.localDialogNotification.by,
        team_id: this.localDialogNotification.forthing
      }
      ws.send(JSON.stringify(newObj));
      } else {
        var newObj = {
        type: "invite.response",
        response: "TRUE",
        group_type: 'group',
        sender_id: store.state.uid,
        receiver_id: this.localDialogNotification.by,
        group_id: this.localDialogNotification.forthing
      }
      ws.send(JSON.stringify(newObj));
      }
    },
    rejectInvitaion() {
      if (this.localDialogNotification.group_type==='team'){
        var newObj = {
        type: "invite.response",
        response: "FALSE",
        group_type: 'team',
        sender_id: store.state.uid,
        receiver_id: this.localDialogNotification.by,
        team_id: this.localDialogNotification.forthing
      }
      ws.send(JSON.stringify(newObj));
      } else {
        var newObj = {
        type: "invite.response",
        response: "FALSE",
        group_type: 'group',
        sender_id: store.state.uid,
        receiver_id: this.localDialogNotification.by,
        group_id: this.localDialogNotification.forthing
      }
      ws.send(JSON.stringify(newObj));
      }
    },
    jumpToTeamDocument() {
      router.push('/'+this.localDialogNotification.group_id+'/'+this.localDialogNotification.project_id+'/'+this.localDialogNotification.item_id+'/DocumentPage')
    },
    jumpToTeamChat() {
      // 待开发
      router.push('/'+store.state.uid+'/Chatroom');
    },
    sendMessage() {
      const now = new Date();
      console.log(now)
      const year = now.getFullYear();
      const month = now.getMonth() + 1; // 月份从0开始，所以要加1
      const day = now.getDate();
      const hours = now.getHours();
      const minutes = now.getMinutes();
      const seconds = now.getSeconds();
      var newObj = {
        name: "kangjiaqi",
        content: this.messageInput,
        time: `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`,
        realtime : now
      };
      ws.send(JSON.stringify(newObj));
      this.messageInput = "";
    },
      // 下列函数仅供测试
    testNotification(num) {
      for (var i=0;i<num;i++) {
        var j=i.toString();
        console.log(j);
        var data={
          id: i,
          type: "邀请",
          by: "user"+j,
          forthing: "文档"+j,
          content: "user"+j+"邀请你编写文档"+"\""+j+"\"",
        };
        var data2={
          id: i,
          type: "@chat",
          by: "user"+i.toString(),
          forthing: "团队"+i.toString(),
          content: "user"+i.toString()+"在团队"+"\""+i.toString()+"\""+"中@了你",
        }
        var data3={
          id: i,
          type: "普通",
          by: "user"+i.toString(),
          forthing: "团队"+i.toString(),
          content: "user"+i.toString()+"在团队"+"\""+i.toString()+"\""+"发了一个消息",
        }
        if (i%3===0)
          store.commit('addNotificationUnread',data);
        else if (i%3===1)
          store.commit('addNotificationUnread',data2);
        else
          store.commit('addNotificationUnread',data3);
      }
      console.log(store.state.notificationUnread);
    }
  }
}
</script>
