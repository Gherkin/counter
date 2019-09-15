
Vue.use(new VueSocketIO({
    debug: true,
    connection: 'http://127.0.0.1:5000'
}));
var app = new Vue({
    data: {
    num: 0,
    prevs: []
  },
  sockets: {
    connect: function () {
      console.log('socket connected')
    },
    data: function(data) {
      this.num = data.num;
      this.prevs = data.laps;
    },
    num: function (data) {
      this.num = data.num;
    }
  },
  el: '#main',
  methods: {
    lap: function() {
      if(this.num === 0) {
        return;
      }
      this.prevs.push({num: this.num})
      this.num = 0;
      this.$socket.emit('lap')
    },
    reset: function() {
      this.num = 0;
      this.$socket.emit('reset')
    },
    clear: function() {
      this.prevs = [];
      this.num = 0;
      this.$socket.emit('clear')
    }
  }
})
