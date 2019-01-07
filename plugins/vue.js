import Vue from "vue";
import Modal from "~/components/Modal";
import ECharts from "vue-echarts/components/ECharts";

import "@mdi/font/css/materialdesignicons.css";

// import ECharts modules manually to reduce bundle size
import "echarts/lib/chart/pie";
import "echarts/lib/component/tooltip";

Vue.component("v-chart", ECharts);

Vue.component("modal", Modal);

Vue.use({
	install() {
		Vue.prototype.$bus = new Vue();
	}
});
