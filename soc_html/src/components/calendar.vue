<style scoped>
    .calendar-box {
        position: relative;
        display: inline-block;
    }

    .calendar {
        width: 220px;
        padding: 10px;
        background: linear-gradient(to right, #1c1c2d 0%, #2d2831 100%);
        position: absolute;
        z-index: 9999;
        border-radius: 3px;
        opacity: .95;
        transition: all .5s ease;
        color: #9bbced;
    }

    .calendar.left {
        left: 0px;
    }

    .calendar.right {
        right: 0px;
    }

    .calendar-enter, .calendar-leave {
        opacity: 0;
        transform: translate3d(0, -10px, 0);
    }

    .calendar:before {
        position: absolute;
        top: -10px;
        content: "";
        border: 5px solid rgba(0, 0, 0, 0);
        border-bottom-color: #2d2831;
    }

    .calendar:after {
        position: absolute;
        top: -9px;
        content: "";
        border: 5px solid rgba(0, 0, 0, 0);
        border-bottom-color: #2d2831;
    }

    .calendar.left:before {
        left: 30px;
    }

    .calendar.left:after {
        left: 30px;
    }

    .calendar.right:before {
        right: 30px;
    }

    .calendar.right:after {
        right: 30px;
    }

    .calendar-tools {
        height: 32px;
        font-size: 14px;
        position: relative;
    }

    .calendar-tools input {
        width: 50px;
        text-align: center;
        border: none;
        background-color: transparent;
    }

    .calendar-tools span {
        cursor: pointer;
    }

    .calendar-tools .text {
        text-align: center;
    }

    .calendar-prev {
        font-size: 20px;
        position: absolute;
        top: -5px;
        left: 0px;
    }

    .calendar-next {
        font-size: 20px;
        position: absolute;
        top: -5px;
        right: 0px;
    }

    .calendar table {
        clear: both;
        width: 100%;
        margin-bottom: 10px;
        border-collapse: collapse;
    }

    .calendar table tr td:first-child {
        padding-left: 0px !important;
    }

    .calendar td {
        margin: 2px !important;
        padding: 0px 0;
        width: 14.28571429%;
        height: 26px;
        text-align: center;
        vertical-align: middle;
        line-height: 26px;
        cursor: pointer;
        border: none !important;
    }

    .calendar td.week {
        pointer-events: none !important;
        cursor: default !important;
    }

    .calendar td.disable {
        color: rgba(126, 159, 208, 0.5);
        pointer-events: none !important;
        cursor: default !important;
    }

    .calendar td span {
        display: block;
        height: 26px;
        line-height: 26px;
        margin: 2px;
        border-radius: 2px;
        border: 1px solid rgba(0, 0, 0, 0);
    }

    .calendar td span:hover {
        background: none;
        border: 1px solid #4a92ff;
    }

    .calendar td.selected span {
        background-color: #4a92ff;
        color: #fff;
    }

    .calendar td.selected span:hover {
        background-color: #4a92ff;
        color: #fff;
    }

    .calendar thead {
        background: none;
    }

    .calendar thead td {
        text-transform: uppercase;
    }

    .calendar .timer {
        margin: 10px 0;
        text-align: center;
    }

    .calendar .timer input {
        width: 45px;
    }

    .calendar-button {
        text-align: center;
        padding-top: 10px;
        padding-bottom: 5px;
    }

    .calendar .lunar {
        font-size: 11px;
        line-height: 150%;
        color: #aaa;
    }

    .calendar td.selected .lunar {
        color: #fff;
    }
</style>
<template>
    <div class="calendar-box">
        <input class="ys-input"
               @click.stop="startOpen($event)"
               v-model="value"
               readonly
               :placeholder="text"
               v-bind:style="{ width: width + 'px' }">
        <div class="calendar"
             v-show="show"
             :style="{'top':y+'px'}"
             v-bind:class="[place=='left' ? 'left' : 'right']"
             transition="calendar"
             transition-mode="out-in">
            <div v-if="type!='time'">
                <div class="calendar-tools">
                <span class="calendar-prev" @click="prev">
                    <i class="md md-navigate-before"></i>
                </span>
                    <span class="calendar-next" @click="next">
                    <i class="md md-navigate-next"></i>
                </span>
                    <div class="text center">
                        <input type="text" v-model="year" value="{{year}}" @change="render(year,month)" min="1970"
                               max="2100" maxlength="4">
                        <span>/</span>
                        <input type="text" v-model="monthString" value="{{monthString}}" readonly>
                    </div>
                </div>
                <table cellpadding="5">
                    <thead>
                    <tr>
                        <td v-for="week in weeks" class="week">{{week}}</td>
                    </tr>
                    </thead>
                    <tr v-for="(k1,day) in days">
                        <td
                                v-for="(k2,child) in day"
                                :class="{'selected':child.selected,'disable':child.disabled}"
                                @click="select(k1,k2,$event)" @touchstart="select(k1,k2,$event)">
                            <span>{{child.day}}</span>
                            <div class="lunar" v-if="showLunar">{{child.lunar}}</div>
                        </td>
                    </tr>
                </table>
            </div>
            <div class="calendar-time" v-show="type=='datetime'||type=='time'">
                <div class="timer">
                    <input type="number" v-model="hour" @change="change('hour',23)" min="0" max="23" maxlength="2"
                           class="ys-input">
                    <span style="color:#444">:</span>
                    <input type="number" v-model="minute" @change="change('minute',59)" min="0" max="59" maxlength="2"
                           class="ys-input">
                    <span style="color:#444">:</span>
                    <input type="number" v-model="second" @change="change('second',59)" min="0" max="59" maxlength="2"
                           class="ys-input">

                </div>
            </div>
            <div class="calendar-button" v-show="type=='datetime'||type=='time'||range">
                <button class="ys-btn ys-btn-blue m-r-10" @click="ok">确定</button>
                <button class="ys-btn ys-btn-white" @click="cancel">取消</button>
            </div>
        </div>
    </div>
</template>
<script>
    import clickoutside from 'src/directives/clickoutside';

    export default {
        name: "calendar",
        directives: {clickoutside},
        props: {
            show: {
                type: Boolean,
                twoWay: true,
                default: false
            },
            type: {
                type: String,
                default: "date"
            },
            text: {
                type: String,
                default: "选择日期时间"
            },
            width: {
                type: Number,
                default: 130
            },
            value: {
                type: String,
                twoWay: true,
                default: ""
            },
            x: {
                type: Number,
                default: 0
            },
            y: {
                type: Number,
                default: 0
            },
            place: {
                type: String,
                default: "left"
            },
            begin: {
                type: String,
                twoWay: true,
                default: ""
            },
            end: {
                type: String,
                default: ""
            },
            range: {
                type: Boolean,
                default: false
            },
            rangeBegin: {
                type: Array,
                default: Array
            },
            rangeEnd: {
                type: Array,
                default: Array
            },
            sep: {
                type: String,
                twoWay: true,
                default: "-"
            },
            weeks: {
                type: Array,
                default: function () {
                    return ['日', '一', '二', '三', '四', '五', '六']
                }
            },
            months: {
                type: Array,
                default: function () {
                    return ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
                }
            }
        },
        data() {
            return {
                year: 0,
                month: 0,
                day: 0,
                hour: 12,
                minute: 0,
                second: 0,
                days: [],
                today: [],
                currentMonth: Number,
                monthString: "",
            }
        },
        created() {
            this.init()
        },
        ready() {
            let self = this;
            $(".calendar-box").click(function (event) {
                event = event || window.event;
                event.stopPropagation();
            });
            $(document).click(function (e) {
                self.close();
            });
        },
        watch: {
            show() {
                this.init()
            },
            value() {
                this.init()
            }
        },
        methods: {
            startOpen(e) {
                $(".calendar").hide();
                this.show = true;
                this.x = e.target.offsetLeft;
                this.y = e.target.offsetTop + e.target.offsetHeight + 8;
            },
            zero(n) {
                return n < 10 ? '0' + n : n
            },// 日期补零
            init() {
                var now = new Date();
                if (this.value != "") {
                    if (this.value.indexOf("-") != -1) this.sep = "-"
                    if (this.value.indexOf(".") != -1) this.sep = "."
                    if (this.value.indexOf("/") != -1) this.sep = "/"
                    if (this.type == "date") {
                        var split = this.value.split(this.sep)
                        this.year = parseInt(split[0])
                        this.month = parseInt(split[1]) - 1
                        this.day = parseInt(split[2])
                    } else if (this.type == "datetime") {
                        var split = this.value.split(" ")
                        var splitDate = split[0].split(this.sep)
                        this.year = parseInt(splitDate[0])
                        this.month = parseInt(splitDate[1]) - 1
                        this.day = parseInt(splitDate[2])
                        if (split.length > 1) {
                            var splitTime = split[1].split(":")
                            this.hour = splitTime[0]
                            this.minute = splitTime[1]
                            this.second = splitTime[2]
                        }
                    } else if (this.type == "time") {
                        var splitTime = this.value.split(":")
                        this.hour = splitTime[0]
                        this.minute = splitTime[1]
                        this.second = splitTime[2]
                    }
                    if (this.range) {
                        var split = this.value.split(" ~ ")
                        if (split.length > 1) {
                            var beginSplit = split[0].split(this.sep)
                            var endSplit = split[1].split(this.sep)
                            this.rangeBegin = [parseInt(beginSplit[0]), parseInt(beginSplit[1] - 1), parseInt(beginSplit[2])]
                            this.rangeEnd = [parseInt(endSplit[0]), parseInt(endSplit[1] - 1), parseInt(endSplit[2])]
                        }
                    }
                } else {
                    if (this.sep == "") this.sep = "/"
                    this.year = now.getFullYear()
                    this.month = now.getMonth()
                    this.day = now.getDate()
                    this.hour = this.zero(now.getHours())
                    this.minute = this.zero(now.getMinutes())
                    this.second = this.zero(now.getSeconds())
                    if (this.range) {
                        this.rangeBegin = Array
                        this.rangeEnd = Array
                    }
                }
                this.monthString = this.months[this.month]
                this.render(this.year, this.month)
            },// 初始化一些东西
            render(y, m) {
                if (!this.range) {
                    this.rangeBegin = []
                    this.rangeEnd = []
                }
                var firstDayOfMonth = new Date(y, m, 1).getDay()         //当月第一天
                var lastDateOfMonth = new Date(y, m + 1, 0).getDate()    //当月最后一天
                var lastDayOfLastMonth = new Date(y, m, 0).getDate()     //最后一月的最后一天
                this.year = y
                this.currentMonth = this.months[m]
                var seletSplit = this.value.split(" ")[0].split(this.sep)

                var i, line = 0, temp = []
                for (i = 1; i <= lastDateOfMonth; i++) {
                    var dow = new Date(y, m, i).getDay()
                    // 第一行
                    if (dow == 0) {
                        temp[line] = []
                    } else if (i == 1) {
                        temp[line] = []
                        var k = lastDayOfLastMonth - firstDayOfMonth + 1
                        for (var j = 0; j < firstDayOfMonth; j++) {
                            temp[line].push({
                                day: k,
                                disabled: true
                            })
                            k++;
                        }
                    }

                    // 如果是日期范围
                    if (this.range) {
                        var options = {
                            day: i
                        }
                        if (this.rangeBegin.length > 0) {
                            var beginTime = Number(new Date(this.rangeBegin[0], this.rangeBegin[1], this.rangeBegin[2]))
                            var endTime = Number(new Date(this.rangeEnd[0], this.rangeEnd[1], this.rangeEnd[2]))
                            var thisTime = Number(new Date(this.year, this.month, i))
                            if (beginTime <= thisTime && endTime >= thisTime) {
                                options.selected = true
                            }
                        }
                        temp[line].push(options)
                    } else {
                        // 单选模式
                        var chk = new Date()
                        var chkY = chk.getFullYear()
                        var chkM = chk.getMonth()
                        // 匹配上次选中的日期
                        if (
                            parseInt(seletSplit[0]) == this.year &&
                            parseInt(seletSplit[1]) - 1 == this.month &&
                            parseInt(seletSplit[2]) == i) {
                            temp[line].push({
                                day: i,
                                selected: true
                            })
                            this.today = [line, temp[line].length - 1]
                        }

                        // 没有默认值的时候显示选中今天日期
                        else if (chkY == this.year && chkM == this.month && i == this.day && this.value == "") {
                            temp[line].push({
                                day: i,
                                selected: true
                            })
                            this.today = [line, temp[line].length - 1]
                        } else {
                            // 设置可选范围
                            // console.log(this.begin,this.end);
                            var options = {
                                day: i,
                                selected: false,
                            }
                            if (this.begin != "") {

                                var beginSplit = this.begin.split(this.sep)
                                var beginTime = Number(new Date(
                                    parseInt(beginSplit[0]),
                                    parseInt(beginSplit[1]) - 1,
                                    parseInt(beginSplit[2])
                                ))
                                if (beginTime > Number(new Date(this.year, this.month, i))) options.disabled = true
                            }
                            if (this.end != "") {
                                var endSplit = this.end.split(this.sep)
                                var endTime = Number(new Date(
                                    parseInt(endSplit[0]),
                                    parseInt(endSplit[1]) - 1,
                                    parseInt(endSplit[2])
                                ))
                                if (endTime < Number(new Date(this.year, this.month, i))) options.disabled = true
                            }
                            temp[line].push(options)
                        }
                    }

                    // 最后一行
                    if (dow == 6) {
                        line++
                    } else if (i == lastDateOfMonth) {
                        var k = 1
                        for (dow; dow < 6; dow++) {
                            temp[line].push({
                                day: k,
                                disabled: true
                            })
                            k++
                        }
                    }
                } //end for

                this.days = temp
            },// 渲染日期
            prev(e) {
                e.stopPropagation()
                if (this.month == 0) {
                    this.month = 11
                    this.year = parseInt(this.year) - 1
                } else {
                    this.month = parseInt(this.month) - 1
                }
                this.monthString = this.months[this.month]
                this.render(this.year, this.month)
            },// 上月
            next(e) {
                e.stopPropagation()
                if (this.month == 11) {
                    this.month = 0
                    this.year = parseInt(this.year) + 1
                } else {
                    this.month = parseInt(this.month) + 1
                }
                this.monthString = this.months[this.month]
                this.render(this.year, this.month)
            },//  下月
            select(k1, k2, e) {
                if (e != undefined) e.stopPropagation()
                // 日期范围
                if (this.range) {
                    if (this.rangeBegin.length == 0 || this.rangeEndTemp != 0) {
                        this.rangeBegin = [this.year, this.month, this.days[k1][k2].day, this.hour, this.minute, this.second]
                        this.rangeBeginTemp = this.rangeBegin
                        this.rangeEnd = [this.year, this.month, this.days[k1][k2].day, this.hour, this.minute, this.second]
                        this.rangeEndTemp = 0
                    } else {
                        this.rangeEnd = [this.year, this.month, this.days[k1][k2].day, this.hour, this.minute, this.second]
                        this.rangeEndTemp = 1
                        // 判断结束日期小于开始日期则自动颠倒过来
                        if (+new Date(this.rangeEnd[0], this.rangeEnd[1], this.rangeEnd[2]) < +new Date(this.rangeBegin[0], this.rangeBegin[1], this.rangeBegin[2])) {
                            this.rangeBegin = this.rangeEnd
                            this.rangeEnd = this.rangeBeginTemp
                        }
                    }
                    this.render(this.year, this.month)
                } else {
                    // 取消上次选中
                    if (this.today.length > 0) {
                        this.days[this.today[0]][this.today[1]].selected = false
                    }
                    // 设置当前选中天
                    this.days[k1][k2].selected = true
                    this.day = this.days[k1][k2].day
                    this.today = [k1, k2]
                    if (this.type == 'date') {
                        this.value = this.year + this.sep + this.zero(this.month + 1) + this.sep + this.zero(this.days[k1][k2].day)
                        this.show = false
                    }
                }

            },// 选中日期
            ok() {
                // 只有有日期的时候才执行
                if (this.type != "time") {
                    let isSelected = false;
                    this.days.forEach(v => {
                        v.forEach(vv => {
                            if (vv.selected) {
                                isSelected = true
                            }
                        })
                    })
                    if (!isSelected) return false
                }

                if (this.range) {
                    this.value = this.output(this.rangeBegin) + " ~ " + this.output(this.rangeEnd)
                } else {
                    this.value = this.output([
                        this.year,
                        this.month,
                        this.day,
                        parseInt(this.hour),
                        parseInt(this.minute),
                        parseInt(this.second)
                    ])
                }
                this.$dispatch('ok', this.value)
                this.show = false
            },// 多选的时候提交
            cancel() {
                this.show = false
            },// 隐藏控件
            output(args) {
                if (this.type == 'time') {
                    return this.zero(args[3]) + ":" + this.zero(args[4]) + ":" + this.zero(args[5])
                }
                if (this.type == 'datetime') {
                    return args[0] + this.sep + this.zero(args[1] + 1) + this.sep + this.zero(args[2]) + " " + this.zero(args[3]) + ":" + this.zero(args[4]) + ":" + this.zero(args[5])
                }
                if (this.type == 'date') {
                    return args[0] + this.sep + this.zero(args[1] + 1) + this.sep + this.zero(args[2])
                }
            },// 格式化输出
            change(type, value) {
                if (type === 'hour') {
                    return this.hour = this.hour >= value ? value : this.hour
                }else if(type === 'minute'){
                    return this.minute = this.minute >= value ? value : this.minute
                }else if(type === 'second'){
                    return this.second = this.second >= value ? value : this.second
                }
            },//时间限制
            close() {
                this.show = false;
            }
        }
    }
</script>

