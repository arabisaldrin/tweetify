<template>
  <v-container grid-list-sm>
    <v-layout row>
      <v-flex md8 lg9 sm8>
        <v-toolbar dense class="mb-2">
          <v-icon color="blue">mdi mdi-twitter</v-icon>
          <v-spacer></v-spacer>
          <span v-if="$store.state.socketConnected">
            <v-btn v-if="!$store.state.streaming" icon @click="startStream">
              <v-icon color="blue">mdi mdi-play</v-icon>
            </v-btn>
            <v-btn v-else icon @click="stopStream">
              <v-icon color="red">mdi mdi-stop</v-icon>
            </v-btn>
          </span>
        </v-toolbar>
        <v-alert
          type="warning"
          :value="!$store.state.socketConnected"
          class="mb-4"
        >Conencting Socket...</v-alert>
        <v-alert
          type="success"
          :value="$store.state.socketConnected && !$store.state.tweetReceived"
          class="mb-4"
        >Socket Connected waiting for streams...</v-alert>
        <v-data-iterator
          row
          wrap
          :items="$store.state.tweets"
          :rows-per-page-items="[10,20,30,{text : 'All',value : -1}]"
        >
          <template slot="item" slot-scope="props">
            <v-card class="mb-2 tweet_feed">
              <v-expansion-panel>
                <v-expansion-panel-content expand-icon>
                  <template slot="header">
                    <v-layout row>
                      <v-flex md1>
                        <v-avatar size="40">
                          <img :src="props.item.user_image_url" alt="alt" />
                        </v-avatar>
                      </v-flex>
                      <v-flex>
                        <h5 class="subheading">{{props.item.user_name}}</h5>
                        <div class="body">{{props.item.content}}</div>
                        <div align="right" class="pa-1">
                          <span>{{getSentimentValue(props.item.polarity)}}</span>
                          <v-icon small>arrow_right_alt</v-icon>
                          <span>{{props.item.subjectivity.toFixed(3)}}</span>
                          <v-icon>unfold_more</v-icon>
                        </div>
                      </v-flex>
                    </v-layout>
                  </template>
                  <div class="pa-2 title">{{props.item.full_content}}</div>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-card>
          </template>
        </v-data-iterator>
      </v-flex>
      <v-flex>
        <v-card fixed class="pa-3">
          <h4>Active Filters</h4>
          <v-card-text>
            <v-chip
              v-for="item in items"
              :key="item.text"
              :color="item.color"
              text-color="white"
            >{{item.text}}</v-chip>
          </v-card-text>
        </v-card>
        <v-divider></v-divider>
        <v-card ref="chart">
          <div class="mt-3 pa-3" style="width:300px; height : 400px;margin : auto"></div>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
var echarts = require("echarts");
export default {
  data() {
    const vm = this;
    return {
      items: [],
      colorStack: ["blue", "red", "green"],
      colors: [],
      chartOption: {
        title: {
          text: "Tweet Sentiment Percetage",
          x: "center"
        },
        tooltip: {},
        legend: {
          data: ["Positive", "Negative", "Neutral"],
          y: "bottom"
        },
        series: [
          {
            name: "Sentiment",
            type: "pie",
            itemStyle: {
              normal: {
                label: {
                  formatter: function(params) {
                    if (params.value != 0) {
                      let txt =
                        (
                          (params.value / vm.$store.state.tweets.length) *
                          100
                        ).toFixed(2) + "%";
                      if (params.name != "Neutral")
                        return txt + "\nAverage : " + params.data.average;
                      else return txt;
                    } else return 0 + "%" + "\nAverage : 0";
                  },
                  textStyle: {
                    baseline: "top"
                  }
                }
              }
            },
            data: [
              { name: "Negative", value: 0 },
              { name: "Neutral", value: 0 },
              { name: "Positive", value: 0 }
            ]
          }
        ]
      },
      chart: null
    };
  },
  async created() {
    const vm = this;
    const resposne = await vm.$axios.get("/filter-group");
    if (resposne.status == 200) {
      const groups = resposne.data.results;
      let colorIndex = 0;
      groups.forEach(e => {
        if (colorIndex == vm.colorStack.length) colorIndex = 0;
        const color = vm.colorStack[colorIndex++];
        vm.items = vm.items.concat(
          e.items.map(i => ({
            text: i.content,
            color: color
          }))
        );
        vm.items.sort((a, b) =>
          a.text > b.text ? 1 : a.text < b.text ? -1 : 0
        );
      });
    }

    vm.$bus.$on("onTweet", tweet => {
      let data = vm.chartOption.series[0].data,
        pol = vm.getSentimentValue(tweet.polarity),
        item = data.find(d => d.name == pol);
      item.value += 1;

      const tweets = vm.$store.state.tweets.filter(
        t => vm.getSentimentValue(t.polarity) == pol
      );

      item.average = (
        tweets.reduce((a, b) => ({
          subjectivity: a.subjectivity + b.subjectivity
        })).subjectivity / tweets.length
      ).toFixed(2);
    });

    ["Negative", "Neutral", "Positive"].forEach((v, i) => {
      let pie = vm.chartOption.series[0].data[i];
      const tweets = vm.$store.state.tweets.filter(
        t => vm.getSentimentValue(t.polarity) == v
      );
      pie.name = v;
      pie.value = tweets.length;
      if (pie.length)
        pie.average = (
          tweets.reduce((a, b) => ({
            subjectivity: a.subjectivity + b.subjectivity
          })).subjectivity / tweets.length
        ).toFixed(2);
      else pie.average = 0;
    });

    if (!process.server) {
      const echart = echarts.init(vm.$refs.chart.$el.children[0]);
      echart.setOption(vm.chartOption);

      vm.chart = echart;
    }
  },
  methods: {
    getSentimentValue(polarity) {
      switch (true) {
        case polarity > 0:
          return "Positive";
        case polarity < 0:
          return "Negative";
        case polarity == 0:
          return "Neutral";
      }
    },
    startStream() {
      this.$bus.$emit("socket-command", "start");
    },
    stopStream() {
      this.$bus.$emit("socket-command", "stop");
    }
  },
  watch: {
    chartOption: {
      deep: true,
      handler: function(val) {
        if (this.chart) {
          this.chart.setOption(val);
        }
      }
    }
  }
};
</script>
<style scoped>
.v-expansion-panel__header {
  padding: 0 !important;
}
</style>
