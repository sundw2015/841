/**
 * Created by qssec on 2017/6/9.
 */
import aside from './Aside.vue'
import adminPassword from './admin-password.vue'
import ysSelect from './select.vue'
import ysModal from './modal.vue'
import ysInfo from './info.vue'
import tableData from './table-data.vue'
import ysPoptip from './poptip.vue'
import ysSwitch from './switch.vue'
import ysSwitchTab from './switch-tab.vue'
import loadingMini from './loading-mini.vue'
import loadingNormal from './loading-normal.vue'
import loadingGlobal from './loading-global.vue'
import LineChart from './line-chart.vue'
import valid from './valid.vue'
import ysValid from './ys-valid.vue'
import tooltip from './tooltip.vue'
import tagator from './tagator.vue'
import checkbox from './checkbox.vue'
import radio from './radio.vue'
import percent from './td/percent.vue'
import stepAll from './step-all.vue'
import guide from './guide.vue'
import guides from './guides.vue'
import calendar from './calendar.vue'
import pieChart from './pie-chart.vue'
import ringChart from './ring-chart.vue'
import lineChart from './line-chart.vue'
import lingBarChart from './ling-bar-chart.vue'
import fengBarChart from './bar-chart.vue'
import tag from './tag.vue'
import ysTab from './tab.vue'
import noData from './no-data.vue'
import cirqueChart from './cirque-chart.vue'

const components = [
  aside,
  adminPassword,
  ysSelect,
  ysModal,
  ysInfo,
  tableData,
  ysPoptip,
  ysSwitch,
  ysSwitchTab,
  loadingMini,
  loadingNormal,
  loadingGlobal,
  LineChart,
  valid,
  ysValid,
  tagator,
  tooltip,
  checkbox,
  radio,
  percent,
  stepAll,
  guide,
  guides,
  calendar,
  pieChart,
  ringChart,
  lineChart,
  lingBarChart,
  fengBarChart,
  tag,
  noData,
  ysTab,
  cirqueChart
]

const install = function (Vue, opts={}) {
   components.map(component => {
    Vue.component(component.name, component)
  })
}
module.exports = {
  install
}