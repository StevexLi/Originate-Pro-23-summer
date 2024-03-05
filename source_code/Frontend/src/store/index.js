import { createStore } from 'vuex'

export default createStore({
  state: {
    isLogin: false,
    token: '',
    uid: 0,
    userName: '',
    userImage: '',
    userGroupList: [],
    hasMessage: false,
    notificationUnread: [],
    notificationRead: [],
    currentGroupList: [],
    currentDocument: '',
  },
  getters: {

  },
  mutations: {
    Logout(state){
      state.isLogin=false;
      state.token='';
      state.uid=0;
      state.userName='';
      state.userImage='';
      state.userGroupList=[];
      state.hasMessage=false;
    },
    Login(state,token){
      var s=token.split('.');
      if(s[1].lenth%4!=0){
        var lenth=s[1].lenth%4;
        for(;lenth<4;lenth++){
          s[1]=s[1]+'=';
        }
      }
      var message=JSON.parse(atob(s[1]));
      console.log(token);
      state.token=token;
      state.uid=message.id;
      state.userName=message.username;
      state.isLogin=true;
    },
    setCurrentDocument(state,name){
      state.currentDocument = name;
    },
    updateGroupList(state,groupList){
      state.userGroupList=groupList;
    },
    getDocumentGroupList(state,list){
      state.currentGroupList = list;
    },
    addNotificationUnread(state,data) {
      var hasMessage = false;
      state.notificationUnread.some(function (value) {
        if (value.id === data.id) {
          hasMessage = true;
          return true;
        }
      });
      if (hasMessage=== false){
        if (data.type==='@document'){
          state.notificationUnread.unshift({ //对象数组
            id: data.id,
            t: data.type,
            b: data.by,
            f: data.forthing,
            c: data.content,
            pid: data.project_id,
            did: data.document_id,
          });
          return;
        }
        if (data.type==='邀请'){
          state.notificationUnread.unshift({ //对象数组
            id: data.id,
            t: data.type,
            b: data.by,
            f: data.forthing,
            c: data.content,
            group_type: data.group_type,
          });
          return;
        }
        state.notificationUnread.unshift({ //对象数组
          id: data.id,
          t: data.type,
          b: data.by,
          f: data.forthing,
          c: data.content,
        });
      }
    },
    addNotificationReadDirect(state,data) {
      var hasMessage = false;
      state.notificationRead.some(function (value) {
        if (value.id === data.id) {
          hasMessage = true;
          return true;
        }
      });
      if (hasMessage === false){
        if (data.type==='@document'){
          state.notificationUnread.unshift({ //对象数组
            id: data.id,
            t: data.type,
            b: data.by,
            f: data.forthing,
            c: data.content,
            pid: data.project_id,
            did: data.document_id,
          });
          return;
        }
        state.notificationRead.unshift({ //对象数组
          id: data.id,
          t: data.type,
          b: data.by,
          f: data.forthing,
          c: data.content,
        });
      }
    },
    addNotificationRead(state,id) {
      state.notificationUnread.some(function (value) {
        if (value.id === id) {
          state.notificationRead.push(value);
          state.notificationUnread.splice(state.notificationUnread.indexOf(value),1);
          return true;
        }
      });
    },
    deleteNotification(state,id) {
      var fromRead = false;
      state.notificationRead.some(function (value) {
        if (value.id === id) {
          state.notificationRead.splice(state.notificationRead.indexOf(value),1);
          fromRead = true;
          return true;
        }
      });
      if (fromRead === false)
        state.notificationUnread.some(function (value) {
          if (value.id === id) {
            state.notificationUnread.splice(state.notificationUnread.indexOf(value),1);
            return true;
          }
      });
    },
    setAllNotificationRead(state) {
      state.notificationUnread.some(function (value) {
          state.notificationRead.push(value);
      });
      state.notificationUnread=[];
    },
    deleteAllNotificationRead(state) {
      state.notificationRead=[];
    },
    searchNotification(state,id) {
      state.notificationRead.some(function (value) {
        if (value.id === id) {
          return true;
        }
      });
      state.notificationUnread.some(function (value) {
        if (value.id === id) {
          return true;
        }
      });
      return false;
    }
  },
  actions: {

  },
  modules: {

  },

})
