<template>
  <div
    v-if="!isShowAll"
    style="
      position: absolute;
      top: 0;
      min-width: 1200px;
      width: 100%;
      height: 100%;
      z-index: 9999;
    "
  >
    <div
      v-loading="!isShowAll"
      element-loading-text="正在加载..."
      style="height: 100%; width: 100%"
    ></div>
  </div>
  <el-dialog
    v-model="dialogVisible"
    title="Tips"
    width="30%"
    style="z-index: 9999"
  >
    <span>{{ dialogMessage }}</span>
  </el-dialog>
  <el-dialog
    v-model="chooseGroupDialog"
    title="选择聊天"
    style="width: 300px; border-radius: 20px; box-shadow: 4px 4px 10px #409eff"
  >
    <div
      style="
        height: 50px;
        width: 200px;
        border-bottom-style: solid;
        border-bottom-color: #dedfe0;
        border-bottom-width: 1px;
        margin-left: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
      "
      v-for="(item, index) in allGroupArray"
      :key="index"
      @click="transferManyMessageOneAfterOne(item)"
    >
      <p style="text-align: center">
        {{ item.group.name }}
      </p>
    </div>
  </el-dialog>
  <el-dialog v-model="addGroupModel" title="创建群聊">
    <el-form :model="form">
      <el-form-item label="群聊名字" :label-width="formLabelWidth">
        <el-input v-model="newGroupName" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="addGroupModel = false">取消</el-button>
        <el-button type="primary" @click="createGroup"> 确定 </el-button>
      </span>
    </template>
  </el-dialog>

  <div
    class="clickRightMenu"
    v-if="clickRightMenu == true && muchSelectModel == false"
    :style="{ top: topNum + 'px', left: leftNum + 'px' }"
  >
    <el-button
      type="primary"
      plain
      class="messageOptionButton"
      text
      style="margin-left: 0px"
      @click="
        deleteSingleMessage(operateMessage[0]);
        clickRightMenu = false;
      "
      >删除</el-button
    >
    <el-button
      type="primary"
      plain
      class="messageOptionButton"
      text
      style="margin-left: 0px"
      @click="
        openMuchSelectModel();
        clickRightMenu = false;
      "
      >多选</el-button
    >
    <el-button
      type="primary"
      plain
      class="messageOptionButton"
      text
      style="margin-left: 0px"
      @click="
        chooseGroupDialog = true;
        muchSelectModel = false;
        clickRightMenu = false;
      "
      >转发</el-button
    >
  </div>
  <el-dialog
    v-model="inviteMemberDialog"
    title="邀请人员"
    style="width: 300px; border-radius: 20px; box-shadow: 4px 4px 10px #409eff"
  >
    <div
      style="
        height: 50px;
        width: 200px;
        border-bottom-style: solid;
        border-bottom-color: #dedfe0;
        border-bottom-width: 1px;
        margin-left: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
      "
      v-for="(item, index) in privateChat"
      :key="index"
      @click="inviteThisPerson(item)"
    >
      <p style="text-align: center">
        {{ item.username }}
      </p>
    </div>
  </el-dialog>
  <el-dialog
    v-model="isTransferDialogShow"
    title="聊天记录"
    width="30%"
    :before-close="handleClose"
  >
    <div
      class="eachMessageContainer"
      v-for="(item, index) in transferContent"
      :key="index"
      v-if="nowWs != -1 && nowWs != -2"
    >
      <div class="bubble left" v-if="item.name !== $store.state.userName">
        <a class="avatar"><img :src="item.icon" /></a>
        <div class="wrap">
          <div class="nameContainer">{{ item.name }}</div>
          <div class="content">
            {{ item.content }}
          </div>
        </div>
      </div>
      <div class="bubble right" v-if="item.name == $store.state.userName">
        <a class="avatar"><img :src="item.icon" /></a>
        <div class="wrap">
          <div class="nameContainer">{{ item.name }}</div>
          <div class="content">
            {{ item.content }}
          </div>
        </div>
      </div>
    </div>
  </el-dialog>
  <div class="searchContainer" @mousedown="removeMenu">
    <div class="title">
      {{ nowChosenGroup.name }}
      <el-button
        type="primary"
        class="searchChatButton"
        @click="getNeighborChaMessage(-1)"
        style="left: 390px; position: absolute; top: 18px"
        v-if="this.searchPosition !== -1"
        >上一条</el-button
      >
      <el-input
        v-model="searchChatInput"
        placeholder="搜索聊天记录"
        style="
          width: 200px;
          left: 500px;
          position: absolute;
          height: 40px;
          top: 15px;
        "
        clearable
      />
      <el-button
        type="primary"
        class="searchChatButton"
        @click="searchChatMessage"
        style="left: 730px; position: absolute; top: 18px"
        v-if="this.searchPosition === -1"
        >搜索</el-button
      >
      <el-button
        type="primary"
        class="searchChatButton"
        @click="getNeighborChaMessage(1)"
        style="left: 720px; position: absolute; top: 18px"
        v-if="this.searchPosition !== -1"
        >下一条</el-button
      >
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
  <el-scrollbar height="500px" class="GroupList" @mousedown="removeMenu">
    <div
      v-for="(item, i) in nowGroupArray"
      :key="i"
      style="
        flex-direction: column;
        display: flex;
        align-content: start;
        width: 220px;
      "
    >
      <div class="dotDiv" v-if="item.unreadMessage != 0"></div>
      <p
        @click="chooseGroup(item, i)"
        class="scrollbar-demo-item"
        :id="'groupList' + i"
      >
        {{ item.group.name }}
        <span class="unreadSpan" v-if="item.unreadMessage != 0">
          [{{ item.unreadMessage }}条]
        </span>
      </p>
    </div>
  </el-scrollbar>
  <el-dialog v-model="dismissGroupDialogShow" title="解散群聊" width="30%">
    <span>确定要解散该群聊吗</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dismissGroupDialogShow = false">取消</el-button>
        <el-button type="danger" @click="dismissGroupChat()"> 确定 </el-button>
      </span>
    </template>
  </el-dialog>
  <el-button type="primary" class="addGroupButton" @click="addGroupModel = true"
    >创建群聊</el-button
  >
  <el-popover
    :visible="atVisible"
    style="z-index: 999"
    placement="top"
    width="200"
    title="123"
    :popper-options="{
      modifiers: [
        {
          name: 'offset',
          options: {
            offset: [popoverPosition.left, popoverPosition.top],
          },
        },
      ],
    }"
    content="this is content, this is content, this is content"
  >
    <template #reference>
      <div
        class="textarea"
        @scroll="loadMore"
        @mousedown="removeMenu"
        ref="messageInput"
      >
        <div
          class="eachMessageContainer"
          v-for="(item, index) in groupMessage[nowWs].content"
          :key="index"
          v-if="nowWs != -1 && nowWs != -2"
        >
          <div
            class="timeContainer"
            v-if="isTimeDifferenceGreaterThan5Second(index)"
          >
            <div>
              {{ item.time }}
            </div>
          </div>
          <div class="bubble left" v-if="item.name !== $store.state.userName">
            <el-checkbox
              v-model="muchSelect[index]"
              class="mt-2"
              inline-prompt
              :active-icon="Check"
              :inactive-icon="Close"
              style="float: left; margin-right: 15px"
              v-if="muchSelectModel == true"
              @change="chooseThisMessage(item, muchSelect[index])"
            />
            <a class="avatar" @click="jumpPersonalPage(item)"
              ><img
                :src="item.icon"
                @click="jumpPersonalPage(item)"
                style="cursor: pointer"
            /></a>
            <div class="wrap">
              <div class="nameContainer">{{ item.name }}</div>
              <div
                class="content"
                @contextmenu.prevent="rightClick($event, item)"
                v-if="Array.isArray(item.content) == false"
              >
                {{ item.content }}
              </div>
              <div
                class="content"
                v-else
                style="
                  box-shadow: 4px 4px 10px #a0cfff;
                  background-color: #c6e2ff;
                  cursor: pointer;
                "
                :id="'transferContainer' + index"
                @mouseover="transferContainerOverChangeColor(index)"
                @mouseout="transferContainerOutChangeColor(index)"
                @click="
                  isTransferDialogShow = true;
                  jsonForTransferContent(item.content);
                "
              >
                来自{{ item.name }}的转发
              </div>
            </div>
          </div>
          <div class="bubble right" v-if="item.name === $store.state.userName">
            <el-checkbox
              v-model="muchSelect[index]"
              class="mt-2"
              inline-prompt
              :active-icon="Check"
              :inactive-icon="Close"
              style="float: right; margin-left: 15px"
              v-if="muchSelectModel == true"
              @change="chooseThisMessage(item, muchSelect[index])"
            />
            <a class="avatar" @click="jumpPersonalPage(item)"
              ><img
                :src="item.icon"
                @click="jumpPersonalPage(item)"
                style="cursor: pointer"
            /></a>
            <div class="wrap">
              <div class="nameContainer">{{ item.name }}</div>
              <div
                class="content"
                @contextmenu.prevent="rightClick($event, item)"
                v-if="Array.isArray(item.content) == false"
              >
                {{ item.content }}
              </div>
              <div
                class="content"
                v-else
                style="
                  box-shadow: 4px 4px 10px #a0cfff;
                  background-color: #c6e2ff;
                  cursor: pointer;
                "
                :id="'transferContainer' + index"
                @mouseover="transferContainerOverChangeColor(index)"
                @mouseout="transferContainerOutChangeColor(index)"
                @click="
                  isTransferDialogShow = true;
                  jsonForTransferContent(item.content);
                "
              >
                来自{{ item.name }}的转发
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <el-scrollbar max-height="500px">
      <div
        class="notification-item"
        v-for="(item, index) in this.nowChosenGroup.member"
        :key="index"
        :title="item.username"
        @click="atDocument(item.username)"
      >
        {{ item.username }}
      </div>
    </el-scrollbar>
  </el-popover>
  <div @mousemove="getMousePosition_popover">
    <el-input
      v-model="messageInput"
      placeholder=""
      class="messageContainer"
      @mousedown="removeMenu"
      v-if="muchSelectModel == false"
      @keydown="keyListener"
    />
  </div>

  <div
    class="messageContainer"
    @mousedown="removeMenu"
    style="background-color: #ecf5ff; display: flex"
    v-if="muchSelectModel == true"
  >
    <div class="selectModelOption">
      <div
        style="
          background-color: white;
          height: 50px;
          width: 50px;
          margin-left: 25px;
          margin-top: 15px;
          border-radius: 50%;
          margin-bottom: 8px;
          cursor: pointer;
        "
        id="icon1"
        @mouseover="overTochangeIconColor('icon1')"
        @mouseleave="leaveTochangeIconColor('icon1')"
        @click="deleteMuchMessage"
      >
        <el-icon style="margin-left: 18px; margin-top: 18px"
          ><Delete
        /></el-icon>
      </div>
      <span
        style="
          margin-toptop: 15px;
          height: 20px;
          width: 100px;
          margin-left: 37px;
          font-size: 10px;
        "
        >删除</span
      >
    </div>
    <div class="selectModelOption">
      <div
        style="
          background-color: white;
          height: 50px;
          width: 50px;
          margin-left: 25px;
          margin-top: 15px;
          border-radius: 50%;
          margin-bottom: 8px;
          cursor: pointer;
        "
        id="icon2"
        @mouseover="overTochangeIconColor('icon2')"
        @mouseleave="leaveTochangeIconColor('icon2')"
        @click="
          chooseGroupDialog = true;
          muchSelectModel = false;
          clickRightMenu = false;
          eachOrTogether = false;
        "
      >
        <el-icon style="margin-left: 18px; margin-top: 18px"
          ><ArrowRight
        /></el-icon>
      </div>
      <span
        style="
          margin-toptop: 15px;
          height: 20px;
          width: 100px;
          margin-left: 26px;
          font-size: 10px;
        "
        >逐条转发</span
      >
    </div>
    <div class="selectModelOption">
      <div
        style="
          background-color: white;
          height: 50px;
          width: 50px;
          margin-left: 25px;
          margin-top: 15px;
          border-radius: 50%;
          margin-bottom: 8px;
          cursor: pointer;
        "
        id="icon3"
        @mouseover="overTochangeIconColor('icon3')"
        @mouseleave="leaveTochangeIconColor('icon3')"
        @click="
          chooseGroupDialog = true;
          muchSelectModel = false;
          clickRightMenu = false;
          eachOrTogether = true;
        "
      >
        <el-icon style="margin-left: 18px; margin-top: 18px"
          ><Expand
        /></el-icon>
      </div>
      <span
        style="
          margin-toptop: 15px;
          height: 20px;
          width: 100px;
          margin-left: 26px;
          font-size: 10px;
        "
        >合并转发</span
      >
    </div>
    <div class="selectModelOption">
      <div
        style="
          background-color: white;
          height: 50px;
          width: 50px;
          margin-left: 25px;
          margin-top: 15px;
          border-radius: 50%;
          margin-bottom: 8px;
          cursor: pointer;
        "
        id="icon4"
        @mouseover="overTochangeIconColor('icon4')"
        @mouseleave="leaveTochangeIconColor('icon4')"
        @click="returnNomalModel"
      >
        <el-icon style="margin-left: 18px; margin-top: 18px"
          ><CloseBold
        /></el-icon>
      </div>
      <span
        style="
          margin-toptop: 15px;
          height: 20px;
          width: 100px;
          margin-left: 37px;
          font-size: 10px;
        "
        >取消</span
      >
    </div>
  </div>
  <el-button
    type="primary"
    plain
    class="sendButton"
    @click="sendMessage"
    @keydown.enter="enter_up()"
    v-if="muchSelectModel == false"
    >发送</el-button
  >
  <div
    class="teamGroupTitle"
    @mousedown="removeMenu"
    v-if="groupOrPerson == false"
  >
    团队成员
  </div>
  <el-button
    type="danger"
    style="position: absolute; display: flex; left: 1250px; top: 17px"
    v-if="groupOrPerson == false && groupOrTeam == true"
    @click="dismissGroupDialogShow = true"
    >解散群聊</el-button
  >
  <el-button
    type="success"
    style="position: absolute; display: flex; left: 1350px; top: 17px"
    v-if="groupOrPerson == false && groupOrTeam == true"
    @click="
      inviteMemberDialog = true;
      getPrivateChat();
    "
    >邀请成员</el-button
  >
  <div class="personalInfoContainer" v-if="this.groupOrPerson == true">
    <div class="personalIconContainer">
      <img :src="nowPerson.icon_address" style="border-radius: 50%" />
    </div>
    <div class="personDetailInfoContainer">
      <pre class="eachInfoItem">昵称     {{ nowPerson.username }}</pre>
      <pre class="eachInfoItem">名字     {{ nowPerson.true_name }}</pre>
      <pre class="eachInfoItem">电话     {{ nowPerson.phone }}</pre>
      <pre class="eachInfoItem">邮箱     {{ nowPerson.email }}</pre>
      <pre class="eachInfoItem">
性别     {{ nowPerson.gender == "M" ? "男" : "女" }}</pre
      >
    </div>
  </div>

  <div
    class="searchContainer"
    style="left: 1055px; top: 90px; height: 40px"
    @mousedown="removeMenu"
    v-if="groupOrPerson == false"
  >
    <el-input
      v-model="searchPersonInput"
      placeholder="搜索"
      style="width: 300px; margin-left: 50px"
      clearable
    />
    <el-button type="primary" class="searchButton" @click="searchPerson"
      >搜索</el-button
    >
  </div>
  <el-scrollbar
    height="470px"
    class="GroupList"
    style="left: 1100px; top: 130px"
    @mousedown="removeMenu"
    v-if="groupOrPerson == false"
  >
    <p
      v-for="(item, index) in nowPersonArray.member"
      :key="index"
      class="scrollbar-demo-item"
      style="width: 350px"
      @click="choosePersonChat(item)"
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
import { getUserChatRoom, getUserInformation } from "../api/user";
import {
  createChatGroup,
  breakupChatGroup,
  inviteUserIntoChatGroup,
} from "../api/chat";
export default {
  mounted() {
    this.myId = store.state.uid;
    this.openDB();
    this.judgeSamePerson();
    this.getMygroup();
    this.closeWeb();
    setTimeout(() => {
      this.getAllGroupMember();
      this.prepareGroupMessage();
      this.websocketInit();
      this.websocketOpen();
      this.websocketOnMessage();
      this.isShowAll = true;
    }, 4000);
    window.addEventListener("beforeunload", (e) => this.beforeunloadHandler(e));
    window.addEventListener("keydown", this.enter_up);
    this.scrollToBottom();
  },
  data() {
    return {
      nowPersonArray: {
        type: "",
        member: "",
      },
      searchPersonInput: "",
      chooseGroupDialog: false,
      messageInput: "",
      nowChosenGroup: "",
      searchInput: "",
      count: ref(20),
      tempGroupArray: [],
      nowGroupArray: [],
      allGroupArray: [],
      allGroupMember: [],
      nowGroupMember: {
        type: "",
        member: [],
      },
      nowWs: -1,
      groupMessage: [],
      groupSize: 0,
      wsArray: [],
      searchChatInput: "",
      searchPosition: -1,
      targetBox: [],
      dialogMessage: "",
      dialogVisible: false,
      showDot: true,
      messageStorageDb: "",
      isShowAll: false,
      clickRightMenu: false,
      topNum: 0,
      leftNum: 0,
      operateMessage: [],
      muchSelect: [],
      muchSelectModel: false,
      groupOrPerson: false,
      nowPerson: "",
      personIdWhenBuildNewChat: "",
      zeroWs: "",
      myId: "",
      eachOrTogether: false, //false : each;true : together
      isTransferDialogShow: false,
      transferContent: [],
      addGroupModel: false,
      newGroupName: "",
      groupOrTeam: false, //false : 团队 true :群聊,
      dismissGroupDialogShow: false,
      inviteMemberDialog: false,
      privateChat: [],
      cursorPosition: {
        top: 0,
        left: 0,
      },
      popoverPosition: {
        top: -400,
        left: 0,
      },
      atVisible: false,
      notificationWs : "",
    };
  },
  unmounted() {
    window.removeEventListener("keydown", this.enter_up, false);
  },
  beforeRouteUpdate(to, form, next) {
    this.closeWeb();
    console.log("已关闭")
    setTimeout(() => {
      next();
    }, 500);
  },
  beforeRouteLeave(to, form, next) {
    this.closeWeb();
    console.log("已改变")
    setTimeout(() => {
      next();
    }, 500);
  },
  onBeforeUnmount() {
    this.closeWeb();
  },
  methods: {
    atDocument(name) {
      console.log(this.popoverPosition.top);
      console.log(this.popoverPosition.left);
      this.atVisible = false;
      this.messageInput = this.messageInput + name;
    },
    keyListener(event) {
      console.log("key_push");
      console.log(this.nowChosenGroup);
      console.log(this.atVisible);
      if (event.shiftKey && event.keyCode == 50) {
        console.log("同时按下 shift 和数字2键");
        this.atVisible = true;
      } else if (event.keyCode == 27) {
        event.preventDefault();
        this.atVisible = false;
        console.log("按下 esc 键");
      }
    },
    getMousePosition_popover(event) {
      const popover_positon = this.$refs.messageInput;
      const popover_position_offset = popover_positon.getBoundingClientRect(); // this.cursorPosition.top = event.clientY; // this.cursorPosition.left = event.clientX;
      this.cursorPosition.top = event.clientY - popover_position_offset.top;
      this.cursorPosition.left = event.clientX - popover_position_offset.left; // console.log(this.cursorPosition);
    },
    inviteThisPerson(person) {
      console.log(person);
      var request = inviteUserIntoChatGroup(person.id, this.nowChosenGroup.id);
      request.then((result) => {
        console.log(result);
        if (result.code == 1008) {
          this.dialogMessage = "你不是本群创建者，无权更改本群信息";
          this.dialogVisible = true;
          return;
        }
        this.isShowAll = false;
        this.getAllGroupMember();
        setTimeout(() => {
          this.isShowAll = true;
        }, 1000);
      });
      this.inviteMemberDialog = false;
      this.privateChat = [];
    },
    getPrivateChat() {
      console.log(this.allGroupArray);
      var obj;
      for (var i = 0; i < this.allGroupArray.length; i++) {
        if (this.allGroupArray[i].group.type == "Private") {
          obj =
            this.allGroupArray[i].group.member[0].id == store.state.uid
              ? this.allGroupArray[i].group.member[1]
              : this.allGroupArray[i].group.member[0];
          this.privateChat.push(obj);
          console.log(obj);
        }
      }
      console.log(this.privateChat);
    },
    dismissGroupChat() {
      console.log(this.nowChosenGroup);
      this.dismissGroupDialogShow = false;
      var request = breakupChatGroup(this.nowChosenGroup.id);
      request.then((result) => {
        console.log(result);
        if (result.code == 1006) {
          this.dialogMessage = "你不是本群创建者，无权更改本群信息";
          this.dialogVisible = true;
          return;
        }
        console.log(this.wsArray);
        var index;
        for (var i = 0; i < this.groupMessage.length; i++) {
          if (this.nowChosenGroup.id == this.groupMessage[i].id) {
            index = i;
            break;
          }
        }
        this.wsArray = this.wsArray.filter(function (element, i) {
          return i !== index;
        });
        this.isShowAll = false;
        this.getMygroup();
        console.log(this.allGroupArray);
        setTimeout(() => {
          this.getAllGroupMember();
          this.prepareGroupMessage();
          this.isShowAll = true;
        }, 4000);
      });
    },
    createGroup() {
      if (this.newGroupName == "") {
        console.log("kang");
        this.dialogMessage = "群组名字不能为空哦";
        this.dialogVisible = true;
        return;
      }
      var request = createChatGroup(this.newGroupName);
      request.then((result) => {
        var groupid = result.group_id;
        console.log(result);
        this.getMygroup();
        this.isShowAll = false;
        setTimeout(() => {
          this.getAllGroupMember();
          this.prepareGroupMessage();
          var ws = new WebSocket(
            "ws://8.130.25.189/ws/chat/group/" + groupid + "/"
          );
          console.log(ws);
          this.wsArray.push(ws);
          this.websocketOnMessage();
          this.isShowAll = true;
        }, 4000);
      });
      this.addGroupModel = false;
    },
    jsonForTransferContent(content) {
      for (var i = 0; i < content.length; i++) {
        this.transferContent.push(JSON.parse(content[i]));
      }
    },
    transferContainerOverChangeColor(index) {
      var ele = document.querySelector("#transferContainer" + index);
      ele.style.backgroundColor = "#a0cfff";
    },
    transferContainerOutChangeColor(index) {
      var ele = document.querySelector("#transferContainer" + index);
      ele.style.backgroundColor = "#c6e2ff";
    },
    choosePersonChat(item) {
      if (this.nowWs == -2) return;
      if (item.id == this.myId) {
        this.dialogMessage = "不能给自己发信息哦";
        this.dialogVisible = true;
        return;
      }
      for (var i = 0; i < this.allGroupArray.length; i++) {
        if (
          this.allGroupArray[i].group.type == "Private" &&
          this.allGroupArray[i].group.name == item.username
        ) {
          for (var j = 0; j < this.groupMessage.length; j++) {
            if (this.groupMessage[j].id == this.allGroupArray[i].group.id) {
              this.chooseGroup(this.allGroupArray[i], j);
              return;
            }
          }
        }
      }
      var leaveObj = {
        type: "change",
        change: "leave",
        user_id: store.state.uid,
        group_id: this.nowChosenGroup.id,
      };
      this.wsArray[this.nowWs].send(JSON.stringify(leaveObj));
      var enterobj = {
        type: "change",
        change: "enter",
        user_id: store.state.uid,
        group_id: item.id,
      };
      this.zeroWs.send(JSON.stringify(enterobj));
      this.nowWs = -2;
      this.personIdWhenBuildNewChat = item.id;
    },
    transferManyMessageOneAfterOne(group) {
      if (this.eachOrTogether == false) {
        for (var i = 0; i < this.operateMessage.length; i++) {
          this.transferSingleMessage(this.operateMessage[i], group);
        }
      } else {
        var me;
        console.log(group);
        for (var i = 0; i < this.nowGroupMember.member.length; i++) {
          if (store.state.uid == this.nowGroupMember.member[i].id)
            me = this.nowGroupMember.member[i];
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
            group_id: group.group.id,
            content: [],
            timestamp: timestamp1,
          },
        };
        for (var i = 0; i < this.operateMessage.length; i++) {
          var temp = JSON.stringify(this.operateMessage[i]);
          newObj.data.content.push(temp);
        }
        var index;
        for (var i = 0; i < this.groupMessage.length; i++) {
          if (this.groupMessage[i].id == group.group.id) {
            index = i;
            break;
          }
        }
        try {
          this.wsArray[index].send(JSON.stringify(newObj));
        } catch {
          this.dialogMessage = "网络错误9";
        }
      }
      this.returnNomalModel();
    },
    transferSingleMessage(item, group) {
      var index;
      for (var i = 0; i < this.wsArray.length; i++) {
        const url = this.wsArray[i].url;
        const match = url.match(/\/group\/(\d+)/);
        const teamNumber = match[1];
        if (group.group.id == teamNumber) {
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
              group_id: teamNumber,
              content: item.content,
              timestamp: timestamp1,
            },
          };
          console.log(JSON.stringify(newObj));
          try {
            this.wsArray[i].send(JSON.stringify(newObj));
            this.chooseGroupDialog = false;
          } catch {
            this.dialogMessage = "网络错误1";
            this.dialogVisible = true;
          }
        }
      }
    },
    deleteMuchMessage() {
      for (var i = 0; i < this.operateMessage.length; i++) {
        this.deleteSingleMessage(this.operateMessage[i]);
      }
    },
    returnNomalModel() {
      this.operateMessage = [];
      for (var i = 0; i < this.muchSelect.length; i++) {
        this.muchSelect[i] = false;
      }
      this.muchSelectModel = false;
      this.chooseGroupDialog = false;
    },
    leaveTochangeIconColor(eleId) {
      var ele = document.querySelector("#" + eleId);
      ele.style.backgroundColor = "white";
    },
    overTochangeIconColor(eleId) {
      var ele = document.querySelector("#" + eleId);
      ele.style.backgroundColor = "#c6e2ff";
    },
    chooseThisMessage(item, newVal) {
      if (newVal == true) this.operateMessage.push(item);
      else {
        var temp = this.operateMessage.filter((i) => i.time != item.time);
        this.operateMessage = temp;
      }
    },
    openMuchSelectModel() {
      this.muchSelectModel = true;
      this.operateMessage = [];
      for (var i = 0; i < this.muchSelect.length; i++) {
        this.muchSelect[i] = false;
      }
    },
    deleteSingleMessage(item) {
      this.muchSelectModel = false;
      for (var i = 0; i < this.groupMessage[this.nowWs].content.length; i++) {
        var temp = this.groupMessage[this.nowWs].content.filter(
          (i) => i.time != item.time
        );
        this.groupMessage[this.nowWs].content = temp;
      }
      var objectStore = this.db
        .transaction("message", "readwrite")
        .objectStore("message");
      objectStore.openCursor().onsuccess = function (event) {
        var cursor = event.target.result;
        if (cursor) {
          if (cursor.value.time == item.time) {
            cursor.delete();
          } else {
            cursor.continue();
          }
        } else {
          console.log("没有更多数据了！");
        }
      };
    },
    removeMenu() {
      if (this.muchSelectModel == false) {
        this.clickRightMenu = false;
        this.operateMessage = [];
      }
    },
    rightClick(e, item) {
      this.topNum = e.pageY - 60;
      this.leftNum = e.pageX - 20;
      this.clickRightMenu = true;
      this.operateMessage.push(item);
    },
    websocketOpen() {
      this.notificationWs.onopen = () =>{
        console.log("notificationws已经开启")
      }
      this.zeroWs.onopen = () => {
        console.log("0号ws已经开启");
      };
      var that = this;
      for (let i = 0; i < this.allGroupArray.length; i++) {
        const group = this.allGroupArray[i];
        this.wsArray[i].onopen = () => {
          console.log("websocket " + i + " 已开启");
          const newObj = {
            type: "history",
            user_id: store.state.uid,
            group_id: that.allGroupArray[i].group.id,
          };
          try {
            this.wsArray[i].send(JSON.stringify(newObj));
          } catch {
            this.dialogMessage = "网络错误2";
            this.dialogVisible = true;
          }
        };
      }
    },
    addToDB(item) {
      var request = this.db
        .transaction(["message"], "readwrite")
        .objectStore("message")
        .add({
          groupid: item.id,
          userName: item.userName,
          userIcon: item.userIcon,
          content: item.content,
          time: item.time,
        });
      var that = this;
      request.onsuccess = function (event) {
        console.log("数据写入成功");
      };

      request.onerror = function (event) {
        console.log("数据写入失败");
      };
    },
    openDB() {
      var request = window.indexedDB.open("message");
      request.onupgradeneeded = function (event) {
        this.db = event.target.result;
        var objectStore;
        if (!this.db.objectStoreNames.contains("message")) {
          objectStore = this.db.createObjectStore("message", {
            autoIncrement: true,
          });
          objectStore.createIndex("groupid", "groupid", { unique: false });
        }
      };
      request.onsuccess = function (event) {
        this.db = event.target.result;
      }.bind(this); // Bind the function to the correct 'this' context
    },
    enter_up(e) {
      if (e.keyCode == 13) {
        this.sendMessage();
      }
    },
    async beforeunloadHandler(e) {
      await this.closeWeb(); // 退出登录接口
      window.close();
    },
    closeWeb() {
      if (this.nowWs != -1) {
        var leaveObj = {
          type: "change",
          change: "leave",
          user_id: store.state.uid,
          group_id: this.nowChosenGroup.id,
        };
        try {
          this.wsArray[this.nowWs].send(JSON.stringify(leaveObj));
          console.log(JSON.stringify(leaveObj))
        } catch {
          this.dialogMessage = "网络错误3";
          this.dialogVisible = true;
        }
      }
    },
    findNowchat() {
      for (var i = 0; i < this.groupMessage.length; i++) {
        if (this.groupMessage[i].id == this.nowChosenGroup.id) {
          return this.groupMessage[i];
        }
      }
    },
    getNeighborChaMessage(num) {
      if (this.searchPosition === 0 && num === -1) {
        this.dialogMessage = "这是第一条";
        this.dialogVisible = true;
        return;
      }
      if (this.searchPosition === this.targetBox.length - 1 && num === 1) {
        this.dialogMessage = "这是最后一条";
        this.dialogVisible = true;
        return;
      }
      this.searchPosition += num;
      const container = document.querySelector(".textarea");
      const targetBoxTop = this.targetBox[this.searchPosition].offsetTop;
      const containerTop = container.offsetTop;
    },
    searchChatMessage() {
      if (this.searchChatInput === "") {
        alert("K");
        return;
      }
      var temp = document.querySelector(
        "#app > main > div > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default > div > div.textarea > div:nth-child(1) > div.bubble.left > div > div.content"
      );
      if (temp == null)
        temp = document.querySelector(
          "#app > main > div > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default > div > div.textarea > div:nth-child(1) > div.bubble.right > div > div.content"
        );
      console.log(temp);
      if (temp == null) {
        return;
      }
      console.log(temp);
      var index = 1;
      while (temp != null) {
        if (temp.textContent.includes(this.searchChatInput) === true) {
          this.targetBox.push(
            document.querySelector(
              "#app > main > div > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default > div > div.textarea > div:nth-child(" +
                index +
                ")"
            )
          );
        }
        index++;
        temp = document.querySelector(
          "#app > main > div > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default > div > div.textarea > div:nth-child(" +
            index +
            ") > div.bubble.right > div > div.content"
        );
        if (temp == null) {
          temp = document.querySelector(
            "#app > main > div > div.el-scrollbar__wrap.el-scrollbar__wrap--hidden-default > div > div.textarea > div:nth-child(" +
              index +
              ") > div.bubble.left > div > div.content"
          );
        }
      }
      if (this.targetBox.length === 0) {
        this.dialogMessage = "没有对应消息";
        this.dialogVisible = true;
        return;
      }
      this.searchPosition = 0;
      const container = document.querySelector(".textarea");
      const targetBoxTop = this.targetBox[0].offsetTop;
      const containerTop = container.offsetTop;
    },
    jumpPersonalPage(item) {
      var uid;
      for (var i = 0; i < this.allGroupMember.length; i++) {
        if (this.nowChosenGroup.id === this.allGroupMember[i].groupid) {
          for (var j = 0; j < this.allGroupMember[i].member.length; j++) {
            if (this.allGroupMember[i].member[j].username == item.name)
              uid = this.allGroupMember[i].member[j].id;
          }
        }
      }
      this.$router.push("/" + uid + "/PersonalInfomation");
    },
    prepareGroupMessage() {
      this.groupMessage = [];
      for (var i = 0; i < this.allGroupArray.length; i++) {
        var obj = {
          id: this.allGroupArray[i].group.id,
          content: [],
        };
        this.groupMessage.push(obj);
      }
      var that = this;
      var objectStore = this.db.transaction("message").objectStore("message");
      objectStore.openCursor().onsuccess = function (event) {
        var cursor = event.target.result;
        if (cursor) {
          for (var i = 0; i < that.allGroupArray.length; i++) {
            if (that.groupMessage[i].id == cursor.value.groupid) {
              var newObj = {
                name: cursor.value.userName,
                icon: cursor.value.userIcon,
                content: cursor.value.content,
                time: cursor.value.time,
              };
              that.groupMessage[i].content.push(newObj);
              var judge = false;
              that.muchSelect.push(judge);
            }
          }
          cursor.continue();
        } else {
          console.log("没有更多数据了！");
        }
      };
    },
    getAllGroupMember() {
      this.allGroupMember = [];
      for (var i = 0; i < this.allGroupArray.length; i++) {
        var obj = {
          groupid: this.allGroupArray[i].group.id,
          member: this.allGroupArray[i].group.member,
          type: this.allGroupArray[i].group.type,
        };
        this.allGroupMember.push(obj);
      }
      this.groupSize = this.allGroupArray.length;
    },
    getMygroup() {
      this.allGroupArray = [];
      var request = getUserChatRoom();
      var groupTemp;
      request.then((result) => {
        groupTemp = result.data;
        for (var i = 0; i < groupTemp.length; i++) {
          var obj = {
            group: {
              id: groupTemp[i].group_id,
              name: groupTemp[i].name,
              member: groupTemp[i].member_info,
              type: groupTemp[i].type,
            },
            unreadMessage: 0,
          };
          this.allGroupArray.push(obj);
        }
        this.nowGroupArray = this.allGroupArray;
      });
    },
    judgeSamePerson() {
      if (store.state.isLogin === false) this.$router.push("/");
      var uid = this.$route.params.uid;
      if (uid != store.state.uid)
        this.$router.push("/" + store.state.uid + "/Chatroom");
    },
    isTimeDifferenceGreaterThan5Second(index) {
      if (index === 0) return true;
      var date1 = new Date(this.groupMessage[this.nowWs].content[index].time);
      var date2 = new Date(
        this.groupMessage[this.nowWs].content[index - 1].time
      );
      const timeDifferenceInMilliseconds = date1 - date2;
      const timeDifferenceInSeconds = timeDifferenceInMilliseconds / 1000;
      return timeDifferenceInSeconds > 300;
    },
    // judgeIsTransferTogether(parsedData)
    // {
    //   var judgeThing = parsedData.content;
    //   return Array.isArray(judgeTing)
    // },
    receiveSingleMessage(parsedData) {
      var that = this;
      var uid = parsedData.user_id;
      if (uid) {
        var tid = parsedData.group_id;
        var username;
        var userIcon;
        var j = 0;
        var flag = false;
        for (j = 0; j < that.groupSize; j++) {
          if (that.allGroupMember[j].groupid == tid) {
            for (var k = 0; k < that.allGroupMember[j].member.length; k++) {
              if (that.allGroupMember[j].member[k].id === uid) {
                username = that.allGroupMember[j].member[k].username;
                userIcon = that.allGroupMember[j].member[k].icon_address;
                flag = true;
                break;
              }
            }
          }
          if (flag) break;
        }
        var newObj = {
          name: username,
          icon: userIcon,
          content: parsedData.content,
          time: parsedData.timestamp,
        };
        console.log("这条消息未读");
        for (var m = 0; m < that.groupMessage.length; m++) {
          if (that.groupMessage[m].id == tid) {
            that.groupMessage[m].content.push(newObj);
          }
        }
        for (var m = 0; m < that.allGroupArray.length; m++) {
          if (
            that.allGroupArray[m].group.id === tid &&
            that.allGroupArray[m].group.id != this.nowChosenGroup.id
          ) {
            that.allGroupArray[m].unreadMessage++;
          }
        }
        var dbObj = {
          id: tid,
          userName: username,
          userIcon: userIcon,
          content: parsedData.content,
          time: parsedData.timestamp,
        };
        this.addToDB(dbObj);
      }
    },
    websocketInit() {
      for (var i = 0; i < this.allGroupArray.length; i++) {
        var ws = new WebSocket(
          "ws://8.130.25.189/ws/chat/group/" +
            this.allGroupArray[i].group.id +
            "/"
        );
        this.wsArray.push(ws);
        this.zeroWs = new WebSocket("ws://8.130.25.189/ws/chat/group/0/");
        this.notificationWs = new WebSocket("ws://8.130.25.189/ws/notification/")
      }
    },
    zeroReceiveMessage(parseData) {
      var that = this;
      var person1, person2;
      var request = getUserInformation(store.state.uid);
      request.then((result) => {
        person1 = result.data;
        var request1;
        if (that.personIdWhenBuildNewChat)
          request1 = getUserInformation(that.personIdWhenBuildNewChat);
        else request1 = getUserInformation(parseData.user_id);
        request1.then((result2) => {
          setTimeout(() => {
            person2 = result2.data;
            var name1 =
              store.state.uid == person1.id
                ? person2.username
                : person1.username;
            var obj = {
              unreadMessage: 0,
              group: {
                id: parseData.group_id,
                member: [],
                name: name1,
                type: "Private",
              },
            };
            obj.group.member.push(person1);
            obj.group.member.push(person2);
            that.allGroupArray.push(obj);
            var newObj = {
              content: parseData.content,
              icon:
                store.state.uid == person1.id
                  ? person2.icon_address
                  : person1.icon_address,
              name: name1,
              time: parseData.timestamp,
            };
            var obj2 = {
              id: parseData.group_id,
              content: [],
            };
            var memObj = {
              groupid: parseData.group_id,
              member: [],
              type: "Private",
            };
            memObj.member.push(person1);
            memObj.member.push(person2);
            that.allGroupMember.push(memObj);
            obj2.content.push(newObj);
            that.groupMessage.push(obj2);
            var newWs = new WebSocket(
              "ws://8.130.25.189/ws/chat/group/" + parseData.group_id + "/"
            );
            that.wsArray.push(newWs);
            var num = that.wsArray.length - 1;
          }, 500);
        });
      });
    },
    websocketOnMessage() {
      var that = this;
      this.zeroWs.onmessage = function (message) {
        var parsedData = JSON.parse(message.data);
        that.zeroReceiveMessage(parsedData);
      };
      for (var i = 0; i < this.allGroupArray.length; i++) {
        that.wsArray[i].onmessage = function (message) {
          var parsedData = JSON.parse(message.data);
          if (Array.isArray(parsedData.data) === true) {
            var dataArray = parsedData.data;
            for (var j = 0; j < dataArray.length; j++) {
              that.receiveSingleMessage(dataArray[j]);
            }
          } else that.receiveSingleMessage(parsedData);
        };
        this.wsArray[i].onClose = function () {
          if (this.nowWs != -1) {
            var leaveObj = {
              type: "change",
              change: "leave",
              user_id: store.state.uid,
              group_id: this.nowChosenGroup.id,
            };
            try {
              this.wsArray[this.nowWs].send(JSON.stringify(leaveObj));
            } catch {
              this.dialogMessage = "网络错误4";
              this.dialogVisible = true;
            }
          }
          console.log("websocket i 已关闭");
        };
      }
    },
    judgeMemberName()
    {
      console.log(this.nowChosenGroup)
      for(var i = 0;i < this.nowChosenGroup.member.length;i++)
      {
        var str = "@" + this.nowChosenGroup.member[i].username
        console.log(str)
        if(this.messageInput.includes(str))
        {
          var obj = {
            type : "at_jump",
            at_type : "chat",
            sender_id: store.state.uid,
            user_id : this.nowChosenGroup.member[i].id,
            group_id : this.nowChosenGroup.id
          }
          this.notificationWs.send(JSON.stringify(obj))
          return;
        }
      }
    },
    sendMessage() {
      this.judgeMemberName()
      if (this.nowWs === -1) {
        this.messageInput = "";
        return;
      }
      if (this.messageInput == "") {
        this.dialogMessage = "不能发送空白消息";
        this.dialogVisible = true;
        return;
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
      if (this.nowWs === -2) {
        var newObj = {
          type: "chat",
          data: {
            user_id: store.state.uid,
            group_id: this.personIdWhenBuildNewChat,
            content: this.messageInput,
            timestamp: timestamp1,
          },
        };
        this.zeroWs.send(JSON.stringify(newObj));
        this.messageInput = "";
        return;
      }
      var newObj = {
        type: "chat",
        data: {
          user_id: store.state.uid,
          group_id: this.nowChosenGroup.id,
          content: this.messageInput,
          timestamp: timestamp1,
        },
      };
      try {
        this.wsArray[this.nowWs].send(JSON.stringify(newObj));
      } catch {
        this.dialogMessage = "网络错误5";
        this.dialogVisible = true;
      }
      this.messageInput = "";
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
    searchPerson() {
      var temp = [];
      for (var i = 0; i < this.nowGroupMember.member.length; i++) {
        if (
          this.nowGroupMember.member[i].username.indexOf(
            this.searchPersonInput
          ) >= 0
        ) {
          temp.push(this.nowGroupMember.member[i]);
        }
      }
      this.nowPersonArray.member = temp;
    },
    searchGroup() {
      this.nowGroupArray = [];
      for (var i = 0; i < this.allGroupArray.length; i++) {
        if (this.allGroupArray[i].group.name.indexOf(this.searchInput) >= 0) {
          this.nowGroupArray.push(this.allGroupArray[i]);
        }
      }
    },
    chooseGroup(item, i) {
      this.scrollToBottom();
      if (this.nowWs != -1) {
        var leaveObj = {
          type: "change",
          change: "leave",
          user_id: store.state.uid,
          group_id:
            this.nowWs == -2
              ? this.personIdWhenBuildNewChat
              : this.nowChosenGroup.id,
        };
        try {
          if (this.nowWs != -2)
            this.wsArray[this.nowWs].send(JSON.stringify(leaveObj));
          else this.zeroWs.send(JSON.stringify(leaveObj));
        } catch {
          this.dialogMessage = "网络错误7";
          this.dialogVisible = true;
        }
        console.log("已经leave" + leaveObj);
      }
      item.unreadMessage = 0;
      this.nowWs = i;
      this.nowChosenGroup = item.group;
      for (var k = 0; k < this.nowGroupArray.length; k++) {
        var ele1 = document.getElementById("groupList" + k);
        ele1.style.background = "var(--el-color-primary-light-9)";
        ele1.style.color = "var(--el-color-primary)";
      }
      var ele = document.getElementById("groupList" + i);
      ele.style.background = "#409EFF";
      ele.style.color = "white";
      for (var i = 0; i < this.allGroupMember.length; i++) {
        if (item.group.id === this.allGroupMember[i].groupid) {
          this.nowGroupMember = this.allGroupMember[i];
          this.nowPersonArray.type = this.nowGroupMember.type;
          this.nowPersonArray.member = this.nowGroupMember.member;
          if (
            this.nowGroupMember.type == "Team" ||
            this.nowGroupMember.type == "Group"
          ) {
            this.groupOrPerson = false;
            this.groupOrTeam = this.nowGroupMember.type == "Group";
          } else {
            this.groupOrPerson = true;
            for (var j = 0; j < this.nowGroupMember.member.length; j++) {
              if (this.nowGroupMember.member[j].id != store.state.uid) {
                this.nowPerson = this.nowGroupMember.member[j];
              }
            }
          }
        }
      }
      var enterobj = {
        type: "change",
        change: "enter",
        user_id: store.state.uid,
        group_id: this.nowChosenGroup.id,
      };
      console.log(this.wsArray[this.nowWs]);
      console.log(enterobj);
      this.wsArray[this.nowWs].send(JSON.stringify(enterobj));
      console.log("已发送enter", enterobj);
    },
  },
  watch: {
    // 监视属性名
    searchInput: function (newVal, oldVal) {
      if (oldVal != "" && newVal == "") {
        this.nowGroupArray = this.allGroupArray;
      }
    },
    searchChatInput: function (newVal, oldVal) {
      if (oldVal != newVal) {
        this.searchPosition = -1;
        const scrollableContainer = document.querySelector(".textarea");
        scrollableContainer.scrollTop = scrollableContainer.scrollHeight;
        this.searchPosition = -1;
        this.targetBox = [];
      }
    },
    searchPersonInput: function (newVal, oldVal) {
      if (oldVal != "" && newVal == "") {
        this.nowPersonArray = this.nowGroupMember;
      }
    },
    isTransferDialogShow: function (newVal, oldVal) {
      if (oldVal == true && newVal == false) {
        this.transferContent = [];
      }
    },
  },
};
</script>

<style scoped>
.notification-item {
  align-items: center;
  /*justify-content: center;*/
  height: 30px;
  line-height: 30px;
  margin: 5px;
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
.addGroupButton {
  position: absolute;
  display: flex;
  top: 570px;
  left: 25px;
  height: 50px;
  width: 150px;
}
.eachInfoItem {
  color: #606266;
  font-size: 15px;
  width: 5px;
  margin-top: 20px;
  width: 300px;
  height: 40px;
}
.personDetailInfoContainer {
  align-items: center;
  align-content: center;
  border-top-style: solid;
  border-top-color: #c6e2ff;
  border-top-width: 2px;
  position: absolute;
  display: flex;
  height: 250px;
  width: 100px;
  top: 200px;
  width: 100%;
  flex-direction: column;
}
.personalInfoContainer {
  position: absolute;
  display: flex;
  height: 500px;
  top: 70px;
  width: 380px;
  left: 1100px;
  border-radius: 20px;
  box-shadow: 4px 4px 10px #409eff;
}
.personalIconContainer {
  position: absolute;
  display: flex;
  left: 120px;
  top: 50px;
  height: 120px;
  width: 120px;
  border-radius: 50%;
}
.selectModelOption {
  height: 100px;
  width: 100px;
  margin-left: 80px;
}
.messageOptionButton {
  position: relative;
  display: flex;
  height: 20px;
  width: 100px;
  margin-top: 10px;
}
.clickRightMenu {
  position: absolute;
  z-index: 9999;
  height: 100px;
  width: 100px;
  border-radius: 5px;
  background-color: #ecf5ff;
}
body {
  margin: 0;
}
.unreadSpan {
  margin-left: 10px;
  font-size: 10px;
  color: gray;
}
.dotDiv {
  position: relative;
  display: flex;
  left: 195px;
  top: 20px;
  height: 10px;
  width: 10px;
  background-color: red;
  border-radius: 50%;
}
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
  box-shadow: 4px 4px 10px #409eff;
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
