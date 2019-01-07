<template>
  <v-app :dark="dark">
    <v-navigation-drawer
      persistent
      :mini-variant="miniVariant"
      v-model="drawer"
      enable-resize-watcher
      fixed
      app
    >
      <v-list class="pa-1">
        <v-list-tile avatar tag="div" class="pb-1">
          <v-list-tile-avatar>
            <img src="https://randomuser.me/api/portraits/men/85.jpg">
          </v-list-tile-avatar>

          <v-list-tile-content>
            <v-list-tile-title>{{$auth.user.username}}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-list class="pt-0" dense>
          <v-divider light></v-divider>
          <v-list-tile to="/dashboard">
            <v-list-tile-action>
              <v-icon>dashboard</v-icon>
            </v-list-tile-action>

            <v-list-tile-content>
              <v-list-tile-title>Dashboard</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile to="/filters/">
            <v-list-tile-action>
              <v-icon>filter_list</v-icon>
            </v-list-tile-action>

            <v-list-tile-content>
              <v-list-tile-title>Filters</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar app :clipped-left="clipped" color="blue" class="white--text">
      <v-tooltip bottom>
        <v-toolbar-side-icon color="white--text" slot="activator" @click.stop="drawer = !drawer"></v-toolbar-side-icon>
        <span>Toggle drawer</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn slot="activator" icon @click.stop="miniVariant = !miniVariant">
          <v-icon color="white" v-html="miniVariant ? 'chevron_right' : 'chevron_left'"></v-icon>
        </v-btn>
        <span>{{miniVariant? 'Expand drawer' : 'Collapse drawer'}}</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn slot="activator" icon @click.stop="clipped = !clipped">
          <v-icon :color="clipped? 'grey' : 'white'">web</v-icon>
        </v-btn>
        <span>{{clipped? 'Unclip drawer' : 'Clip drawer'}}</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn slot="activator" icon @click.stop="fixed = !fixed">
          <v-icon :color="fixed? 'grey' : 'white'">web</v-icon>
        </v-btn>
        <span>{{fixed? 'Scrollable toolbar' : 'Fix toolbar' }}</span>
      </v-tooltip>

      <v-toolbar-title class="hidden-xs-only" v-text="title"></v-toolbar-title>

      <v-spacer></v-spacer>
    </v-toolbar>
    <v-content>
      <nuxt/>
    </v-content>
  </v-app>
</template>

<script>
let channel;

export default {
  asyncData() {
    return {
      drawer: true
    };
  },
  data() {
    return {
      title: "Tweetify",
      dark: false,
      clipped: false,
      drawer: true,
      fixed: false,
      right: true,
      miniVariant: false,
      rightDrawer: false,
      connected: false,
      items: []
    };
  },
  mounted() {
    let vm = this;
    vm.createSocketConnection();
  },
  methods: {
    createSocketConnection() {
      let vm = this,
        userId = vm.$auth.user.id,
        socketUrl = "ws://127.0.0.1:8000/ws/tweet_stream/user/" + userId;

      channel = new WebSocket(socketUrl);
      vm.$store.commit("setSocketConnected", false);
      channel.onopen = e => {
        vm.$store.commit("setSocketConnected", true);
        channel.onmessage = event => {
          const data = JSON.parse(event.data);
          if (data.type == "cmd-response") {
            switch (data.cmd) {
              case "start":
                if (data.result) {
                  vm.$toast.success("Stream started successfuly");
                  vm.$store.commit("setStreamingStatus", true);
                } else {
                  vm.$toast.error("Unable to start straming");
                }
                break;
              case "stop":
                if (data.result) {
                  vm.$toast.success("Stream stopped successfuly");
                  vm.$store.commit("setStreamingStatus", false);
                } else {
                  vm.$toast.error("Unable to stop straming");
                }
                break;
            }
          } else if (data.type == "tweet") {
            vm.$store.commit("onTweet", data.data);
            vm.$bus.$emit("onTweet", data.data);
            if (!vm.$store.state.tweetReceived) {
              vm.$store.commit("tweetReceived");
            }
          }
        };
      };

      channel.onclose = function(e) {
        vm.$store.commit("setSocketConnected", false);
        setTimeout(() => {
          vm.createSocketConnection();
        }, 1000);
      };

      vm.$bus.$on("socket-command", cmd => {
        channel.send(
          JSON.stringify({
            type: "cmd",
            command: cmd
          })
        );
      });
    }
  }
};
</script>
<style lang="scss" scoped>
.v-navigation-drawer {
  ::-webkit-scrollbar {
    width: 0px;
    background: transparent;
  }
  ::-webkit-scrollbar-thumb {
    background: #ff0000;
  }
}
.notifications {
  max-height: 300px;
  overflow: hidden scroll;
}

.v-content__wrap {
  background-color: #ececec !important;
}
</style>
