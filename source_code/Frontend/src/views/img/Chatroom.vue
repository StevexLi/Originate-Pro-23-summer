<template>
  <div class="searchContainer">
    <div class="title">
      {{ nowChosenGroup.name }}
    </div>
    <el-input
      v-model="searchInput"
      placeholder="搜索"
      style="width: 150px"
      clearable
    />
    <el-button type="primary" class="searchButton" @click="searchGroup"
      >搜索</el-button
    >
  </div>
  <el-scrollbar height="550px" class="GroupList">
    <p
      v-for="(item, i) in nowGroupArray"
      :key="i"
      @click="chooseGroup(item, i)"
      class="scrollbar-demo-item"
      :id="'groupList' + i"
    >
      {{ item.name }}
    </p>
  </el-scrollbar>
  <div class="textarea" @scroll="loadMore">
    <div
      class="eachMessageContainer"
      v-for="(item, index) in groupMessage[nowWs].content"
      :key="index"
      v-if="nowWs !=-1"
    >
      <div class="timeContainer">
        <div v-if="isTimeDifferenceGreaterThan5Second(index)">
          {{ item.time }}
        </div>
      </div>
      <div class="bubble left" v-if="item.name !== $store.state.userName">
        <a class="avatar" @click="jumpPersonalPage(item)"><img :src="item.icon" @click="jumpPersonalPage(item)" /></a>
        <div class="wrap">
          <div class="nameContainer">{{ item.name }}</div>
          <div class="content">
            {{ item.content }}
          </div>
        </div>
      </div>
      <div class="bubble right" v-else>
        <a class="avatar" @click="jumpPersonalPage(item)"><img :src="item.icon" @click="jumpPersonalPage(item)" /></a>
        <div class="wrap">
          <div class="nameContainer">{{ item.name }}</div>
          <div class="content">
            {{ item.content }}
          </div>
        </div>
      </div>
    </div>
  </div>
  <el-input v-model="messageInput" placeholder="" class="messageContainer" />
  <el-button type="primary" plain class="sendButton" @click="sendMessage"
    >发送</el-button
  >
  <div class="teamGroupTitle">团队成员</div>
  <div class="searchContainer" style="left: 1055px; top: 90px; height: 40px">
    <el-input
      v-model="searchInput"
      placeholder="搜索"
      style="width: 300px; margin-left: 50px"
      clearable
    />
    <el-button type="primary" class="searchButton" @click="searchGroup"
      >搜索</el-button
    >
  </div>
  <el-scrollbar
    height="470px"
    class="GroupList"
    style="left: 1100px; top: 130px"
  >
    <p
      v-for="(item, index) in nowGroupMember"
      :key="index"
      class="scrollbar-demo-item"
      style="width: 350px"
    >
      <img :src="item.icon_address" class="userIcon" />
      <span>
        {{ item.username }}
      </span>
    </p>
  </el-scrollbar>
</template>

<script scoped>
import { ref } from "vue";
import store from "@/store";
import { getGroupInformation } from "../api/group";
export default {
  mounted() {
    this.judgeSamePerson();
    this.getMygroup();
    this.getAllGroupMember();
    this.prepareGroupMessage();
    this.scrollToBottom();
    this.websocketInit();
    console.log(store.state.userName)
  },
  data() {
    return {
      messageInput: "",
      nowChosenGroup: "",
      searchInput: "",
      count: ref(20),
      tempGroupArray: [],
      nowGroupArray: [],
      allGroupArray: [],
      allGroupMember: [],
      nowGroupMember: [],
      nowWs: -1,
      groupMessage: [],
      groupSize: 0,
      wsArray: [],
    };
  },
  methods: {
    jumpPersonalPage(item){
      var uid;
      for(var i = 0;i < this.allGroupMember.length;i++)
      {
        console.log(this.allGroupMember[i])
        if(this.nowChosenGroup.id === this.allGroupMember[i].groupid)
        {
          for(var j = 0;j < this.allGroupMember[i].member.length;j++)
          {
            if(this.allGroupMember[i].member[j].username == item.name)
            uid = this.allGroupMember[i].member[j].id
          }
        }
      }
      this.$router.push("/" + uid + "/PersonalInfomation");
    },
    prepareGroupMessage() {
      for (var i = 0; i < this.allGroupArray.length; i++) {
        {
          var obj = {
            id: this.allGroupArray[i].id,
            content: [],
          };
          this.groupMessage.push(obj);
        }
      }
    },
    getAllGroupMember() {
      for (var i = 0; i < this.allGroupArray.length; i++) {
        // var that = this;
        var groupInformation = getGroupInformation(this.allGroupArray[i].id);
        groupInformation.then((result) => {
          var groupInfo = result.data;
          var obj = {
            groupid: groupInfo.id,
            member: groupInfo.user_list,
          };
          this.allGroupMember.push(obj);
        });
      }
      this.groupSize = this.allGroupArray.length;
    },
    getMygroup() {
      this.allGroupArray = store.state.userGroupList;
      this.nowGroupArray = this.allGroupArray;
    },
    judgeSamePerson() {
      // if(store.state.isLogin === false)
      // this.$router.push('/')
      // var uid = this.$route.params.uid;
      // if(uid != store.state.uid)
      // this.$router.push('/' + store.state.uid + '/Chatroom')
    },
    isTimeDifferenceGreaterThan5Second(index) {
      if (index === 0) return true;
      var date1 = new Date(this.groupMessage[this.nowWs].content[index].time);
      var date2 = new Date(this.groupMessage[this.nowWs].content[index - 1].time);
      const timeDifferenceInMilliseconds = date1 - date2;
      const timeDifferenceInSeconds = timeDifferenceInMilliseconds / 1000;
      return timeDifferenceInSeconds > 300;
    },
    websocketInit() {
      for (var i = 0; i < this.allGroupArray.length; i++) {
        var ws = new WebSocket(
          "ws://8.130.25.189/ws/chat/team/" + this.allGroupArray[i].id + "/"
        );
        this.wsArray.push(ws);
      }
      var that = this;
      for (var i = 0; i < this.allGroupArray.length; i++) {
        that.wsArray[i].onopen = function () {
          //服务器连接关闭
          console.log("websocket i 已开启");
        };
        that.wsArray[i].onmessage = function (message) {
          var parsedData = JSON.parse(message.data);
          var uid = parsedData.user_id;
          if (uid) {
            var tid = parsedData.team_id;
            var username;
            var userIcon;
            var j = 0;
            if (tid) console.log(tid);
            var flag = false;
            var teamNum;
            for (j = 0; j < that.groupSize; j++) {
              if (that.allGroupMember[j].groupid === tid) {
                for (var k = 0; k < that.allGroupMember[j].member.length; k++) {
                  console.log(that.allGroupMember[j].member[k].id);
                  if (that.allGroupMember[j].member[k].id === uid) {
                    console.log("kangjaiqi");
                    username = that.allGroupMember[j].member[k].username;
                    userIcon = that.allGroupMember[j].member[k].icon_address;
                    flag = true;
                    teamNum = j;
                    break;
                  }
                }
              }
              if (flag) break;
            }
            console.log(username);
            console.log(userIcon);
            var newObj = {
              name: username,
              icon: userIcon,
              content: parsedData.content,
              time: parsedData.timestamp,
            };
            console.log(teamNum);
            that.groupMessage[j].content.push(newObj);
            console.log(newObj);
          }
        };
        this.wsArray[i].onclose = function () {
          //服务器连接关闭
          console.log("websocket i 已关闭");
        };
      }
    },
    sendMessage() {
      if(this.nowWs === -1)
      {
        this.messageInput = ""
        return
      }
      const now = new Date();
      const year = now.getFullYear();
      const month = now.getMonth() + 1; // 月份从0开始，所以要加1
      const day = now.getDate();
      const hours = now.getHours();
      const minutes = now.getMinutes();
      const seconds = now.getSeconds();
      var timestamp1 =
        year +
        "-" +
        month +
        "-" +
        day +
        " " +
        hours +
        ":" +
        minutes +
        ":" +
        seconds;
      var newObj = {
        type: "chat",
        data: {
          user_id: store.state.uid,
          team_id: this.nowChosenGroup.id,
          content: this.messageInput,
          timestamp: timestamp1,
        },
      };
      this.wsArray[this.nowWs].send(JSON.stringify(newObj));
      console.log(JSON.stringify(newObj));
      this.messageInput = ""
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const scrollableContainer = document.querySelector(".textarea");
        scrollableContainer.scrollTop = scrollableContainer.scrollHeight;
      });
    },
    loadMore() {
      let scrollingElement = document.querySelector(".textarea");
      if (scrollingElement.scrollTop === 0) {
        // 执行加载操作
      }
    },
    load() {},
    searchGroup() {
      this.nowGroupArray = [];
      for (var i = 0; i < this.allGroupArray.length; i++) {
        if (this.allGroupArray[i].name.indexOf(this.searchInput) >= 0) {
          this.nowGroupArray.push(this.allGroupArray[i]);
        }
      }
    },
    chooseGroup(item, i) {
      if (this.nowWs != -1) {
        var leaveObj = {
          type: "change",
          change: "leave",
          user_id: store.state.uid,
          team_id: this.nowChosenGroup.id,
        };
        this.wsArray[this.nowWs].send(JSON.stringify(leaveObj));
        console.log(JSON.stringify(leaveObj));
      }
      this.nowWs = i;
      this.nowChosenGroup = item;
      for (var k = 0; k < this.nowGroupArray.length; k++) {
        var ele1 = document.getElementById("groupList" + k);
        ele1.style.background = "var(--el-color-primary-light-9)";
        ele1.style.color = "var(--el-color-primary)";
      }
      var ele = document.getElementById("groupList" + i);
      ele.style.background = "#409EFF";
      ele.style.color = "white";
      for (var i = 0; i < this.allGroupMember.length; i++) {
        if (item.id === this.allGroupMember[i].groupid)
          this.nowGroupMember = this.allGroupMember[i].member;
      }
      var enterobj = {
        type: "change",
        change: "enter",
        user_id: store.state.uid,
        team_id: this.nowChosenGroup.id,
      };
      this.wsArray[this.nowWs].send(JSON.stringify(enterobj));
      console.log(JSON.stringify(enterobj));
    },
  },
  watch: {
    // 监视属性名
    searchInput: function (newVal, oldVal) {
      if (oldVal != "" && newVal == "") {
        this.nowGroupArray = this.allGroupArray;
      }
    },
  },
};
</script>

<style>
.userIcon {
  height: 40px;
  width: 40px;
  border-radius: 50%;
  margin-right: 50px;
  left: 10px;
}
.nameContainer {
  margin-bottom: 5px;
  color: #c6c6c6;
  font-size: 13px;
}
.teamGroupTitle {
  text-align: center;
  position: absolute;
  display: flex;
  height: 60px;
  width: 400px;
  top: 10px;
  left: 1100px;
  border-bottom-style: solid;
  border-bottom-color: #79bbff;
  border-bottom-width: 2px;
  font-size: 30px;
}
.GroupList {
  position: absolute;
  top: 60px;
}
.scrollbar-demo-item {
  cursor: pointer;
  width: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
  border-style: solid;
  border-color: #79bbff;
  border-radius: 5px;
  border-width: 1px;
}
.timeContainer {
  text-align: center;

  align-items: center;
  align-content: center;
  height: 30px;
  width: 100%;
  margin-top: 20px;
}

.title {
  font-size: 30px;
  position: absolute;
  display: flex;
  height: 60px;
  width: 800px;
  left: 260px;
  top: 0px;

  border-bottom-style: solid;
  border-bottom-color: #79bbff;
  border-bottom-width: 2px;
}

.bubble {
  padding: 6px;
  overflow: hidden;
  position: relative;
}

.bubble:after {
  clear: both;
  content: "";
}

.bubble a.avatar {
  display: block;
  height: 44px;
  width: 44px;
  border-radius: 2px;
  overflow: hidden;
}

.bubble a.avatar > img {
  width: 100%;
  height: 100%;
}

.bubble.left a.avatar {
  float: left;
}

.bubble.right a.avatar {
  float: right;
}

.bubble .content {
  width: auto;
  padding: 0.7em 0.5em;
  font-size: 16px;
  border-radius: 6px;
  border: 1px solid;
  position: relative;
  display: inline-block;
  word-wrap: break-word; /* 允许单词内换行 */
  max-width: 250px;
}

.bubble .content:before {
  content: "";
  display: inline-block;
  box-sizing: border-box;
  width: 12px;
  height: 12px;
  border: 1px solid transparent;
  border-radius: 3px;
  position: absolute;
  background-color: inherit;
  border-right-color: inherit;
  border-bottom-color: inherit;
}

.bubble.left {
  text-align: left;
}

.bubble.right {
  text-align: right;
}

.bubble.left .wrap {
  margin-left: 56px;
  margin-right: 56px;
}

.bubble.left .content {
  background: #fafafa;
  border-color: #c6c6c6;
}

.bubble.left .content:before {
  left: -6px;
  top: 16px;
  transform: rotate(135deg);
}

.bubble.right .wrap {
  margin-right: 56px;
  margin-left: 56px;
}

.bubble.right .content {
  background: #b3e866;
  border-color: #9ab96b;
  text-align: left;
}

.bubble.right .content:before {
  right: -6px;
  top: 16px;
  transform: rotate(-45deg);
}

.eachMessageContainer {
  height: 90px;
  width: 100%;
}

.sendButton {
  position: absolute;
  display: flex;
  top: 585px;
  left: 1000px;
}

.messageContainer {
  position: absolute;
  display: flex;
  height: 100px;
  width: 800px;
  left: 255px;
  top: 480px;
}

.textarea {
  flex-direction: column;
  position: absolute;
  overflow: auto;
  /* 启用垂直滚动 */
  left: 255px;
  top: 85px;
  display: flex;
  height: 380px;
  width: 800px;
  border-radius: 5px;
  border-color: #79bbff;
  border-width: 1px;
  border-style: solid;
}

.searchButton {
  margin-left: 20px;
  margin-top: 10px;
}

.searchContainer {
  position: absolute;
  display: flex;
  left: 0px;
  top: 10px;
  height: 50px;
  width: 415px;
  margin-left: 0px;
}

.infinite-list {
  position: absolute;
  top: 70px;
  left: -40px;
  height: 1000px;
  list-style: none;
  text-align: center;
}

.infinite-list .infinite-list-item {
  flex-direction: column;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 70px;
  width: 350px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}
</style>
