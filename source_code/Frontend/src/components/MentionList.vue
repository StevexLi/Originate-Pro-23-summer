<template>
    <div class="items">
      <template v-if="items.length">
        <button
          class="item"
          :class="{ 'is-selected': index === selectedIndex }"
          v-for="(item, index) in items"
          :key="index"
          @click="selectItem(index)"
        >
          {{ item.username }}
        </button>
      </template>
      <div class="item" v-else>
        No result
      </div>
    </div>
  </template>
  
  <script>
    import store from "@/store";
    let ws;
  export default {
    props: {
      items: {
        type: Array,
        required: true,
      },
  
      command: {
        type: Function,
        required: true,
      },
    },

    mounted() {
      console.log('in mention list');
      var that = this;
      // ws1 = new WebSocket("ws://8.130.25.189/ws/text/");
      ws = new WebSocket("ws://8.130.25.189/ws/notification/");
      ws.onopen = function () {
        console.log("文档@用websocket已经打开");
      };
      ws.onmessage = function (message) {
        var parsedData = JSON.parse(message.data);
        console.log(parsedData);
      };
      ws.onclose = function () {
        //服务器连接关闭
        console.log("文档@用websocket已关闭");
      };
      var url = this.$route.path;
      var infos = url.split('/');
      this.group_id = parseInt(infos[1]);
      this.project_id = parseInt(infos[2]);
      this.text_id = parseInt(infos[3]);
    },
  
    data() {
      return {
        selectedIndex: 0,
        team_id: 0,
        project_id: 0,
        text_id: 0,
      }
    },
  
    watch: {
      items() {
        this.selectedIndex = 0
      },
    },
  
    methods: {
      onKeyDown({ event }) {
        if (event.key === 'ArrowUp') {
          this.upHandler()
          return true
        }
  
        if (event.key === 'ArrowDown') {
          this.downHandler()
          return true
        }
  
        if (event.key === 'Enter') {
          this.enterHandler()
          return true
        }
  
        return false
      },
  
      upHandler() {
        this.selectedIndex = ((this.selectedIndex + this.items.length) - 1) % this.items.length
      },
  
      downHandler() {
        this.selectedIndex = (this.selectedIndex + 1) % this.items.length
      },
  
      enterHandler() {
        this.selectItem(this.selectedIndex)
      },
  
      selectItem(index) {
        const item = this.items[index]
  
        if (item) {
          var newObj = {
            type: "at_jump",
            at_type: "document",
            sender_id: store.state.uid,
            receiver_id: item.id,
            team_id: this.group_id,
            project_id: this.project_id,
            document_id: this.text_id,
          }
          console.log(newObj);
          console.log("发送前");
          ws.send(JSON.stringify(newObj));
          console.log("发送后");
          this.command({ id: item.username })
        }
      },
    },
  }
  </script>
  
  <style lang="scss">
  .items {
    padding: 0.2rem;
    position: relative;
    border-radius: 0.5rem;
    background: #FFF;
    color: rgba(0, 0, 0, 0.8);
    overflow: hidden;
    font-size: 0.9rem;
    box-shadow:
      0 0 0 1px rgba(0, 0, 0, 0.05),
      0px 10px 20px rgba(0, 0, 0, 0.1),
    ;
  }
  
  .item {
    display: block;
    margin: 0;
    width: 100%;
    text-align: left;
    background: transparent;
    border-radius: 0.4rem;
    border: 1px solid transparent;
    padding: 0.2rem 0.4rem;
  
    &.is-selected {
      border-color: #000;
    }
  }
  </style>