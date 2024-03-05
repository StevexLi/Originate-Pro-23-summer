<template>
  <el-container class="first-container">
    <el-aside width="16%" class="left-aside">
      <el-scrollbar height="800px" max-height="640px">
        <el-text class="scrollbar-title">团队列表</el-text>
        <el-button type="primary"  @click="this.OpenDialog(0)" ><el-icon style="margin-right: 4px;"><Plus /></el-icon>新建团队</el-button>
        <el-button type="primary" @click="this.SwithcGroup(item-1)" v-for="item in this.group.length" :key="item" :plain="item-1!=this.group.current" class="scrollbar-item">{{ this.group.list[item-1].name }}</el-button>
      </el-scrollbar>
    </el-aside>
    <el-container class="second-container">
      <el-header height="20%" class="header-content">
        <el-container>
          <el-aside width="10%">
            <el-avatar :size="110" fit="fill" :src="this.currentGroup.avatar"/>
          </el-aside>
          <el-aside width="80%">
            <el-container>
              <el-header height="50%" style="display: flex;justify-content: center;align-items: center;">
                <el-text class="group-title">{{ this.currentGroup.name }}</el-text>
                <el-button v-if="this.currentGroup.id!=0" type="primary" @click="this.OpenDialog(1)" style="height: 50px;"><el-icon style="margin-right: 4px;"><Edit /></el-icon>编辑团队信息</el-button>
                <el-button v-if="this.currentGroup.id!=0" type="primary" @click="this.DeleteGroup(this.currentGroup.id)" style="height: 50px;"><el-icon style="margin-right: 4px;"><Edit /><Close /></el-icon>删除团队</el-button>
              </el-header>
              <el-main>
                <el-text class="group-introduction">团队简介:{{ this.currentGroup.introduction }}</el-text>
              </el-main>
            </el-container>
          </el-aside>
        </el-container>
      </el-header>
      <el-container class="third-container">
        <el-aside v-if="this.listType" width="100%" class="bottom-aside">
          <el-container v-if="this.currentGroup.id!=0" class="forth-container">
            <el-header style="display: flex;justify-content: center;align-items: center;">
              <el-text class="project-title">项目列表</el-text>
              <el-select style="margin-right: 10px;" v-model="this.sorttype" size="large" placeholder="按时间递增排序" @change="this.ProjectSort(this.currentGroup.projectList)">
                <el-option value="0" label="按时间递增排序"/>
                <el-option value="1" label="按时间递减排序"/>
                <el-option value="2" label="按项目名称递增排序"/>
                <el-option value="3" label="按项目名称递减排序"/>
                <el-option value="4" label="按创建者昵称递增排序"/>
                <el-option value="5" label="按创建者昵称递减排序"/>
              </el-select>
              <el-select v-model="this.searchType" size="large" placeholder="项目名称" @change="this.ProjectSearch()">
                <el-option value="0" label="项目名称"/>
                <el-option value="1" label="创建人昵称"/>
                <el-option value="2" label="项目创建时间"/>
              </el-select>
              <el-input v-model="this.searchwords" size="large" style="width: 35%;"></el-input>
              <el-button type="primary" size="large" style="margin-right: 10px;" @click="this.ProjectSearch()"><el-icon><Search /></el-icon></el-button>
              <el-button v-if="this.currentGroup.id!=0" type="primary" @click="this.OpenDialog(2)" style="height: 40px;"><el-icon style="margin-right: 4px;"><Plus /></el-icon>新建项目</el-button>
              <el-button v-if="this.currentGroup.id!=0" type="primary" @click="this.OpenDialog(4)" style="height: 40px;"><el-icon style="margin-right: 4px;"><DeleteFilled /></el-icon>回收站</el-button>
              <el-button v-if="this.currentGroup.id!=0" type="primary" @click="this.ChangeListType()" style="height: 40px;"><el-icon style="margin-right: 4px;"><Switch /></el-icon>查看团队成员列表</el-button>
            </el-header>
            <el-scrollbar>
              <div v-for="item in this.currentGroup.projectCount" :key="item" class="project-list">
                <el-text class="project-name">{{ this.currentGroup.projectList[item-1].name }}</el-text>
                <el-text class="creator-name">{{ this.currentGroup.projectList[item-1].creator_name+" " }}创建</el-text>
                <el-text class="create-time">创建时间：{{ this.currentGroup.projectList[item-1].create_date.substring(0,10)+' '+this.currentGroup.projectList[item-1].create_date.substring(11,19) }}</el-text>
                <el-button @click="this.Jump('/'+this.$store.state.uid+'/'+this.currentGroup.id+'/MyProject/'+this.currentGroup.projectList[item-1].project_id)"><el-icon style="margin-right: 4px;"><Pointer /></el-icon>查看项目</el-button>
                <el-button @click="this.DeleteProject(this.currentGroup.projectList[item-1].project_id)"><el-icon style="margin-right: 4px;"><Delete /></el-icon>删除项目</el-button>
                <el-button @click="this.CopyProject(item-1)"><el-icon style="margin-right: 4px;"><CopyDocument /></el-icon>复制项目</el-button>
              </div>
            </el-scrollbar>
          </el-container>
        </el-aside>
        <el-aside v-else width="100%" class="bottom-aside">
          <el-container v-if="this.currentGroup.id!=0" class="forth-container">
            <el-header style="display: flex;justify-content: center;align-items: center;">
              <el-text class="groupmember-title">成员列表</el-text>
              <el-button v-if="this.currentGroup.id!=0" type="primary" @click="this.OpenDialog(3)" style="height: 40px;"><el-icon style="margin-right: 4px;"><Plus /></el-icon>邀请新成员</el-button>
              <el-button v-if="this.currentGroup.id!=0" type="primary" @click="this.ChangeListType()" style="height: 40px;"><el-icon style="margin-right: 4px;"><Switch /></el-icon>查看团队项目列表</el-button>
            </el-header>
            <el-scrollbar>
              <div v-for="item in this.currentGroup.personCount" :key="item"  class="groupmember-list">
                <el-avatar :size="40" :src="this.currentGroup.personList[item-1].icon_address" fit="fill"/>
                <el-text class="groupmember-name">{{ this.currentGroup.personList[item-1].username }}</el-text>
                <el-text class="groupmember-name">{{ this.currentGroup.personList[item-1].true_name }}</el-text>
                <el-text class="groupmember-email">{{ this.currentGroup.personList[item-1].email }}</el-text>
                <el-button @click="this.Jump('/'+this.currentGroup.personList[item-1].id+'/PersonalInfomation')"><el-icon style="margin-right: 4px;"><Pointer /></el-icon>查看成员</el-button>
                <el-button @click="this.ChangeAuth(this.currentGroup.personList[item-1].id,this.currentGroup.personList[item-1].position==='admin'? 1 : 2)" style="width: 100px;"><el-icon style="margin-right: 4px;"><Avatar /></el-icon>{{ this.currentGroup.authList[item-1] }}</el-button>
                <el-button @click="this.ChangeAuth(this.currentGroup.personList[item-1].id,3)"><el-icon style="margin-right: 4px;"><CircleClose /></el-icon>移除成员</el-button>
              </div>
            </el-scrollbar>
          </el-container>
        </el-aside>
      </el-container>
    </el-container>
  </el-container>
  <el-dialog v-model="this.createGroup.isOpen" title="创建团队" width="500px">
    <el-form ref="createGroupRef" :model="createGroup" :rules="createGroupRules" label-width="70px">
        <el-form-item prop="name" label="团队名称" class="dialog-form-item">
          <el-input type="text" v-model="createGroup.name" placeholder="请输入团队名称" maxlength="30" class="dialog-input" />
        </el-form-item>
        <el-form-item prop="introduction" label="团队简介" class="dialog-form-item">
          <el-input type="textarea" v-model="createGroup.introduction" placeholder="请输入团队介绍" maxlength="200" show-word-limit="true" :autosize="{ minRows: 2, maxRows: 6 }" class="dialog-input" />
        </el-form-item>
        <el-form-item >
          <el-button type="primary" @click="this.CreateGroup()" style="width: 100px;">创建团队</el-button>
        </el-form-item>
    </el-form>
  </el-dialog>
  <el-dialog v-model="this.updateGroup.isOpen" title="修改团队信息" width="500px">
    <el-form ref="updateGroupRef" :model="updateGroup" :rules="updateGroupRules" label-width="70px">
        <el-form-item prop="name" label="团队名称" class="dialog-form-item">
          <el-input type="text" v-model="updateGroup.name" placeholder="请输入团队名称" maxlength="30" class="dialog-input" />
        </el-form-item>
        <el-form-item prop="introduction" label="团队简介" class="dialog-form-item">
          <el-input type="textarea" v-model="updateGroup.introduction" placeholder="请输入团队介绍" maxlength="200" show-word-limit="true" :autosize="{ minRows: 2, maxRows: 6 }" class="dialog-input" />
        </el-form-item>
        <el-form-item prop="avatar" label="团队头像" class="dialog-form-item">
          <el-input id="teamavatar" type="file" v-model="updateGroup.avatar" class="dialog-input" />
        </el-form-item>
        <el-form-item >
          <el-button type="primary" @click="this.UpdateGroup()" style="width: 100px;">上传修改内容</el-button>
        </el-form-item>
    </el-form>
  </el-dialog>
  <el-dialog v-model="this.createProject.isOpen" title="创建项目" width="500px">
    <el-form ref="createProjectRef" :model="createProject" :rules="createProjectRules" label-width="70px">
        <el-form-item prop="name" label="项目名称" class="dialog-form-item">
          <el-input type="text" v-model="createProject.name" placeholder="请输入项目名称" maxlength="30" class="dialog-input" />
        </el-form-item>
        <el-form-item prop="introduction" label="项目简介" class="dialog-form-item">
          <el-input type="textarea" v-model="createProject.introduction" placeholder="请输入项目介绍" maxlength="200" show-word-limit="true" :autosize="{ minRows: 2, maxRows: 6 }" class="dialog-input" />
        </el-form-item>
        <el-form-item >
          <el-button type="primary" @click="this.CreateProject()" style="width: 100px;">创建项目</el-button>
        </el-form-item>
    </el-form>
  </el-dialog>
  <el-dialog v-model="this.addNewMember.isOpen" title="邀请新成员" width="500px">
    <el-form ref="addNewMemberRef" :model="addNewMember" :rules="addNewMemberRules" label-width="70px">
        <el-form-item prop="email" label="邮箱" class="dialog-form-item">
          <el-input type="text" v-model="addNewMember.email" placeholder="请输入用户邮箱" maxlength="30" class="dialog-input" />
        </el-form-item>
        <el-form-item >
          <el-button type="primary" @click="this.AddNewMember()" style="width: 100px;">发送邀请</el-button>
        </el-form-item>
    </el-form>
  </el-dialog>
  <el-dialog v-model="this.restore.isOpen" title="回收站" width="1000px" style="height: 550px;">
    <el-button @click="this.EmptyRestore()" type="primary">清空回收站</el-button>
    <el-scrollbar max-height="400px">
      <div v-for="item in this.restore.count" :key="item" class="project-list">
        <el-text class="project-name">{{ this.restore.list[item-1].name }}</el-text>
        <el-text class="creator-name">{{ this.restore.list[item-1].creator_name }}创建</el-text>
        <el-text class="create-time">创建时间：{{ this.restore.list[item-1].create_date.substring(0,10)+' '+this.restore.list[item-1].create_date.substring(11,19) }}</el-text>
        <el-button @click="this.RestoreProject(this.restore.list[item-1].project_id)"><el-icon style="margin-right: 4px;"><Pointer /></el-icon>恢复项目</el-button>
        <el-button @click="this.RemoveProject(this.restore.list[item-1].project_id)"><el-icon style="margin-right: 4px;"><Delete /></el-icon>彻底删除</el-button>
      </div>
    </el-scrollbar>
  </el-dialog>
</template>

<style scoped>
.dialog-form-item{
  width: 500px;
  margin-bottom: 30px;
}
.dialog-input{
  width: 400px;
}
.first-container{
  min-width: 1200px;
  height: 630px;
  min-height: 630px;
}
.second-container{
  height: 100%;
}
.third-container{
  height: 80%;
}
.left-aside{
  height: 100%;
}
.bottom-aside{
  margin-top: 20px;
  margin-right: 20px;
  height: 100%;
}
.header-content{
  border-bottom: 1px solid #409EFF;
}
.scrollbar-title {
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  font-size: x-large;
  font-weight: 1000;
  color: black;
}
.scrollbar-item {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80%;
  height: 40px;
  margin: 8px;
  text-align: center;
}
.group-title{
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 50px;
  margin: 10px;
  border-radius: 4px;
  font-size: xx-large;
  font-weight: 1000;
  color: black;
}
.group-introduction{
  align-items: center;
  justify-content: center;
  height: 50px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  font-size:medium;
  font-weight: 500;
  color: black;
}
.groupmember-title{
  align-items: center;
  width: 90%;
  height: 50px;
  border-radius: 4px;
  font-size:3ch;
  font-weight: 500;
  color: black;
}
.groupmember-list{
  display: flex;
  align-items: center;
  height: 50px;
  margin: 5px;
  border-radius: 4px;
  border-bottom: 1px solid #409EFF;
}
.groupmember-name{
  width: 18%;
  margin-left: 20px;
  display: flex;
  text-align: center;
  font-size:1ch;
  font-weight: 500;
  color: black;
}
.groupmember-email{
  width: 25%;
  margin-left: 20px;
  display: flex;
  text-align: center;
  font-size:1ch;
  font-weight: 500;
  color: black;
}
.project-title{
  align-items: center;
  width: 40%;
  height: 50px;
  border-radius: 4px;
  font-size:3ch;
  font-weight: 500;
  color: black;
}
.project-list{
  display: flex;
  align-items: center;
  height: 50px;
  margin: 5px;
  border-radius: 4px;
  border-bottom: 1px solid #409EFF;
}
.project-name{
  width: 18%;
  margin-left: 20px;
  display: flex;
  text-align: center;
  font-size:1ch;
  font-weight: 500;
  color: black;
}
.creator-name{
  width: 18%;
  margin-left: 20px;
  display: flex;
  text-align: center;
  font-size:1ch;
  font-weight: 500;
  color: black;
}
.create-time{
  width: 25%;
  margin-left: 20px;
  display: flex;
  text-align: center;
  font-size:1ch;
  font-weight: 500;
  color: black;
}
</style>


<script>
import store from '@/store';
import { ElMessage } from 'element-plus';
import { getUserGroup } from '../api/user.js';
import { createGroup, deleteGroup, changeAuth, inviteMember, getGroupInformation, updateGroup} from '../api/group.js';
import { createProject, deleteProject, restoreProject, removeProject, emptyRestore, getRestoreList, copyProject } from '../api/project.js';
import { Search } from '@element-plus/icons-vue';

export default{
  data(){
    return{
      uid: store.state.uid,
      listType: true,
      sorttype: '',
      searchwords: '',
      searchType: '',
      createGroup:{
        isOpen: false,
        name: '',
        introduction: '',
      },
      updateGroup:{
        isOpen: false,
        name: '',
        introduction: '',
        avatar: '',
      },
      createProject:{
        isOpen: false,
        name: '',
        introduction: '',
      },
      addNewMember:{
        isOpen: false,
        email: '',
      },
      group:{
        list: [],
        length: 0,
        current: 0,
      },
      currentGroup:{
        id: '',
        avatar: 'https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png',
        name: '您还没有任何团队',
        introduction: '快去创建或加入一个团队吧',
        personCount: 0,
        personList: [],
        authList: [],
        projectCount: 0,
        projectList: [],
        projectListBeforeSearch: [],
        projectCountBeforeSearch: 0,
      },
      restore:{
        isOpen: false,
        list: [],
        count: 0,
      },
      createGroupRules:{
        name:[{
          validator: (rule, value, callback) => {
            if(value === ''){
              callback("请输入团队名称");
            }
            callback();
          }, type: 'string', trigger: 'blur'}],
        introduction:[{
          validator: (rule, value, callback) => {
            if(value === ''){
              callback("请输入团队介绍");
            }
            callback();
          }, type: 'string', trigger: 'blur'}],
      },
      updateGroupRules:{
        name:[{
          validator: (rule, value, callback) => {
            if(value === ''){
              callback("请输入团队名称");
            }
            callback()
          }, type: 'string', trigger: 'blur'}],
        introduction:[{
          validator: (rule, value, callback) => {
            if(value === ''){
              callback("请输入团队介绍");
            }
            callback();
          }, type: 'string', trigger: 'blur'}],
        avatar:[{
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
      createProjectRules:{
        name:[{
          validator: (rule, value, callback) => {
            if(value === ''){
              callback("请输入项目名称");
            }
            for(var i=0;i<this.currentGroup.projectCount;i++){
              if(value==this.currentGroup.projectList[i].name){
                callback("同一个团队项目名称唯一");
              }
            }
            callback()
          }, type: 'string', trigger: 'blur'}],
        introduction:[{
          validator: (rule, value, callback) => {
            if(value === ''){
              callback("请输入项目介绍");
            }
            callback()
          }, type: 'string', trigger: 'blur'}],
      },
      addNewMemberRules:{
        email:[{
          validator: (rule, value, callback) => {
            if(value === ''){
              callback("请输入用户邮箱");
            }
            callback()
          }, type: 'string', trigger: 'blur'}],
      },
    }
  },
  methods:{
    ChangeListType(){
      this.listType=!this.listType;
    },
    CreateGroup(){
      this.$refs.createGroupRef.validate((valid) => {
        if(valid){
          var promise1=createGroup(this.createGroup.name,this.createGroup.introduction);
          promise1.then((result)=>{
            if(this.MessageCatch(result,true)){
              this.Load(this.currentGroup.id);
            }
          })
        }
      })
    },
    UpdateGroup(){
      this.$refs.updateGroupRef.validate((valid) => {
        if(valid){
          var promise1=updateGroup(this.currentGroup.id, this.updateGroup.name, this.updateGroup.introduction, document.getElementById('teamavatar').files[0]);
          promise1.then((result) => {
            if(this.MessageCatch(result, true)){
              this.Load(this.currentGroup.id);
              this.updateGroup.isOpen=false;
            }
          })
        }
      })
    },
    CreateProject(){
      this.$refs.createProjectRef.validate((valid) => {
        if(valid){
          var promise=createProject(this.createProject.name,this.currentGroup.id,this.createProject.introduction);
          promise.then((result)=>{
            if(this.MessageCatch(result,true)){
              this.Load(this.currentGroup.id);
            }
          });
        }
      })
    },
    AddNewMember(){
      this.$refs.addNewMemberRef.validate((valid) => {
        if(valid){
          var promise=inviteMember(this.currentGroup.id,this.addNewMember.email);
          promise.then((result) => {
            this.MessageCatch(result,true);
          })
        }
      })
    },
    DeleteGroup(groupid){
      var promise1=deleteGroup(groupid);
      promise1.then((result) => {
        if(this.MessageCatch(result,true)){
          this.Load(this.currentGroup.id);
        }
      })
    },
    DeleteProject(projectid){
      var promise=deleteProject(projectid);
      promise.then((result) => {
        if(this.MessageCatch(result,true)){
          this.Load(this.currentGroup.id);
        }
      })
    },
    CopyProject(index){
      var newname=this.currentGroup.projectList[index].name+'副本';
      var tmpname=newname;
      for(var i=0,j=1;i<this.currentGroup.projectCount;i++){
        console.log(this.currentGroup.projectList[i].name+' '+tmpname);
        if(this.currentGroup.projectList[i].name==tmpname){
          tmpname=newname+j;
          j++;
          i=0;
        }
      }
      newname=tmpname;
      var promise=copyProject(this.currentGroup.projectList[index].project_id, newname);
      promise.then((result) => {
        if(this.MessageCatch(result,true)){
          this.Load(this.currentGroup.id);
        }
      })
    },
    ChangeAuth(userid,opcode){
      var ownPosition;
      var userPosition;
      if(userid==store.state.uid){
        ElMessage({
          message: "不能对自己进行操作",
          grouping: true,
          type: 'error',
        })
      }
      else{
        for(var i=0;i<this.currentGroup.personCount;i++){
          if(this.currentGroup.personList[i].id==store.state.uid){
            ownPosition=this.currentGroup.personList[i].position;
          }
          if(this.currentGroup.personList[i].id==userid){
            userPosition=this.currentGroup.personList[i].position;
          }
        }
        if(opcode==1){
          if(ownPosition==='creator'){
            var promise1=changeAuth(userid,this.currentGroup.id,opcode);
            promise1.then((result)=>{
              if(this.MessageCatch(result,true)){
                this.GetCurrenGroup(this.currentGroup.id);
              }
            })
          }
          else{
            ElMessage({
              message: "只有创建者可以将管理员降为普通成员",
              grouping: true,
              type: 'warning',
            })
          }
        }
        else if(opcode==2){
          if(ownPosition==='creator'||ownPosition==='admin'){
            var promise1=changeAuth(userid,this.currentGroup.id,opcode);
            promise1.then((result)=>{
              if(this.MessageCatch(result,true)){
                this.GetCurrenGroup(this.currentGroup.id);
              }
            })
          }
          else{
            ElMessage({
              message: "普通成员不能修改其他人的权限",
              grouping: true,
              type: 'warning',
            })
          }
        }
        else{
          if(ownPosition==='creator'||(ownPosition==='admin'&&userPosition==='member')){
            var promise1=changeAuth(userid,this.currentGroup.id,opcode);
            promise1.then((result)=>{
              if(this.MessageCatch(result,true)){
                this.GetCurrenGroup(this.currentGroup.id);
              }
            })
          }
          else if(ownPosition==='admin'){
            ElMessage({
              message: "管理员不能移除管理员",
              grouping: true,
              type: 'warning',
            })
          }
          else{
            ElMessage({
              message: "普通成员不能移除其他人",
              grouping: true,
              type: 'warning',
            })
          }
        }
      }
      this.Load(this.currentGroup.id);
    },
    SwithcGroup(index){
      this.Load(this.group.list[index].id);
    //   var promise=getUserGroup();
    //   promise.then((result)=>{
    //     if(result.code==0){
    //       store.commit("updateGroupList",result.data);
    //       if(result.data.length==0){
    //         this.currentGroup.id=0;
    //         this.currentGroup.avatar='https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png';
    //         this.currentGroup.name='您还没有任何团队';
    //         this.currentGroup.introduction='快去创建或加入一个团队吧';
    //         this.currentGroup.personCount=0;
    //         this.currentGroup.projectCount=0
    //         this.currentGroup.personList=[];
    //         this.currentGroup.projectList=[];
    //         this.currentGroup.authList=[];
    //       }
    //       else{
    //         for(var i=0;i<result.data.length;i++){
    //           if(result.data[i].id==this.group.list[index].id){
    //             this.group.current=i;
    //             this.currentGroup.id=result.data[i].id;
    //             break;
    //           }
    //           if(this.group.length-i==1){
    //             this.group.current=0;
    //             this.currentGroup.id=result.data[0].id;
    //           }
    //         }
    //       }
    //       this.group.list=result.data;
    //       this.group.length=this.group.list.length;
    //       if(this.currentGroup.id!=0){
    //         this.GetCurrenGroup(this.currentGroup.id);
    //       }
    //       this.$router.push('/'+store.state.uid+'/GroupPage/'+this.currentGroup.id);
    //     }
    //     else{

    //     }
    //   })
    },
    Jump(url){
      this.$router.push(url);
    },
    OpenDialog(index){
      if(index==0){
        this.createGroup.isOpen=true;
      }
      else if(index==1){
        this.updateGroup.name=this.currentGroup.name;
        this.updateGroup.introduction=this.currentGroup.introduction;
        this.updateGroup.isOpen=true;
      }
      else if(index==2){
        this.createProject.isOpen=true;
      }
      else if(index==3){
        this.addNewMember.isOpen=true;
      }
      else{
        this.GetRestoreList();
      }
    },
    GetRestoreList(){
      var promise1=getRestoreList(this.currentGroup.id);
      promise1.then((result) => {
        if(this.MessageCatch(result, false)){
          this.restore.list=result.data.deleted_projects;
          this.restore.count=this.restore.list.length;
          this.restore.isOpen=true;
        }
      })
    },
    EmptyRestore(){
      var promise1=emptyRestore(this.currentGroup.id);
      promise1.then((result) => {
        if(this.MessageCatch(result,true)){
          this.restore.isOpen=false;
        }
      })
    },
    RestoreProject(projectid){
      var promise1=restoreProject(projectid);
      promise1.then((result) => {
        if(this.MessageCatch(result, true)){
          this.GetRestoreList();
        }
      })
    },
    RemoveProject(projectid){
      var promise1=removeProject(projectid);
      promise1.then((result) => {
        if(this.MessageCatch(result, true)){
          this.GetRestoreList();
        }
      })
    },
    ProjectSort(newList){
      if(this.sorttype==0||this.sorttype===''){
        newList.sort((a,b)=>a.id-b.id);
      }
      else if(this.sorttype==1){
        newList.sort((a,b)=>b.id-a.id);
      }
      else if(this.sorttype==2){
        newList.sort((a,b)=>{
          if(a.name>b.name){
            return 1;
          }
          else{
            return -1;
          }});
      }
      else if(this.sorttype==3){
        newList.sort((a,b)=>{
          if(b.name>a.name){
            return 1;
          }
          else{
            return -1;
          }});
      }
      else if(this.sorttype==4){
        newList.sort((a,b)=>{
          if(a.creator_name>b.creator_name){
            return 1;
          }
          else{
            return -1;
          }});
      }
      else if(this.sorttype==5){
        newList.sort((a,b)=>{
          if(b.creator_name>a.creator_name){
            return 1;
          }
          else{
            return -1;
          }});
      }
      this.currentGroup.projectList=newList;
      this.currentGroup.projectCount=newList.length;
    },
    ProjectSearch(){
      var newList=[];
      if(this.searchwords===''){
        newList=this.currentGroup.projectListBeforeSearch;
      }
      else{
        if(this.searchType==0||this.searchType===''){
          for(var i=0;i<this.currentGroup.projectCountBeforeSearch;i++){
            if(this.currentGroup.projectListBeforeSearch[i].name.search(this.searchwords)!=-1){
              newList.push(this.currentGroup.projectListBeforeSearch[i]);
            }
          }
        }
        else if(this.searchType==1){
          for(var i=0;i<this.currentGroup.projectCountBeforeSearch;i++){
            if(this.currentGroup.projectListBeforeSearch[i].creator_name.search(this.searchwords)!=-1){
              newList.push(this.currentGroup.projectListBeforeSearch[i]);
            }
          }
        }
        else if(this.searchType==2){
          for(var i=0;i<this.currentGroup.projectCountBeforeSearch;i++){
            if(this.currentGroup.projectListBeforeSearch[i].create_date.search(this.searchwords)!=-1){
              newList.push(this.currentGroup.projectListBeforeSearch[i]);
            }
          }
        }
      }
      this.ProjectSort(newList);
    },
    Load(groupid){
      var promise1=getUserGroup();
      promise1.then((result) => {
        if(this.MessageCatch(result,false)){
          this.group.list=result.data;
          this.group.length=this.group.list.length;
          for(var i=0;i<this.group.length;i++){
            if(this.group.list[i].id==groupid){
              this.group.current=i;
              this.currentGroup.id=this.group.list[i].id;
              break;
            }
            if(this.group.length-i==1){
              if(groupid>0){
                ElMessage({
                  message: '您不在该团队中，已重新加载您所在团队',
                  grouping: true,
                  type: 'warning',
                })
              }
              this.group.current=0;
              this.currentGroup.id=this.group.list[0].id;
            }
          }
          if(this.group.length>0){
            this.GetCurrenGroup(this.currentGroup.id);
            this.Jump('/'+this.uid+'/GroupPage/'+this.currentGroup.id);
          }
          else{
            this.group.current=0
            this.currentGroup.id=0;
            this.currentGroup.avatar='https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png';
            this.currentGroup.name='您还没有任何团队';
            this.currentGroup.introduction='快去创建或加入一个团队吧';
            this.currentGroup.personCount=0;
            this.currentGroup.projectCount=0;
            this.currentGroup.personList=[];
            this.currentGroup.projectList=[];
            this.currentGroup.authList=[];
            this.Jump('/'+this.uid+'/GroupPage/'+this.currentGroup.id);
          }
        }
      })
    },
    GetCurrenGroup(groupId){
      var promise=getGroupInformation(groupId);
      promise.then((result)=>{
        this.currentGroup.id=groupId;
        this.currentGroup.name=result.data.name;
        this.currentGroup.introduction=result.data.introduction;
        this.currentGroup.avatar=result.data.icon_address;
        this.currentGroup.personList=result.data.user_list;
        this.currentGroup.personCount=this.currentGroup.personList.length;
        this.currentGroup.projectListBeforeSearch=result.data.project_list;
        this.currentGroup.projectCountBeforeSearch=this.currentGroup.projectListBeforeSearch.length;
        this.currentGroup.authList=[];
        for(var i=0;i<this.currentGroup.personCount;i++){
          if(this.currentGroup.personList[i].position==='creator'){
            this.currentGroup.authList.push('创建者')
          }
          else if(this.currentGroup.personList[i].position==='admin'){
            this.currentGroup.authList.push('管理员')
          }
          else{
            this.currentGroup.authList.push('成员')
          }
        }
        this.ProjectSearch();
      })
    },
    MessageCatch(data,opcode){
      if(data.code!=0){
        ElMessage({
          message: data.msg,
          grouping: true,
          type: 'error',
        })
        return false;
      }
      if(opcode==true&&data.code==0){
        ElMessage({
          message: data.msg,
          grouping: true,
          type: 'success',
        })
      }
      return true;
    },
  },
  mounted(){
    this.uid=this.$route.params.uid;
    var groupid=this.$route.params.groupid;
    if(store.state.isLogin==false){
      this.$router.push('/');
    }
    else if(store.state.uid!=this.uid){
      this.$router.push('/'+store.state.uid+'/GroupPage/'+groupid);
      this.uid=store.state.uid;
    }
    this.Load(groupid);
    // addEventListener("keydown",);
  }
}
</script>
