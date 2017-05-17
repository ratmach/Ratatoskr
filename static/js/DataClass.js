function DataClass(index,isActive,id,name,email) {
    this.index=index;this.isActive=isActive;this.id=id;this.name=name || "abcd";this.email=email;
    this.changed=false;
    this.observers = {};

    this.set = function (key, value) {
        var prevVal = this[key];
        this[key] = value;
        if (this.observers[key]) {
            for (var i = 0; i < this.observers[key].length; ++i) {
                this.observers[key][i](this);
            }
        }
        if (key == "changed")
            return 1;
        var tmp = this.changed;
        this.changed = prevVal != value || this.changed;
        if (this.changed != tmp) {
            key = "changed";
            value = this.changed;
            if (this.observers[key]) {
                for (i = 0; i < this.observers[key].length; ++i) {
                    this.observers[key][i](this);
                }
            }
        }
    };
    this.setObserver = function (key, observer) {
        if (this.observers[key] == undefined) {
            this.observers[key] = [];
        }
        this.observers[key].push(observer);
    };
    this.update = undefined;
    this.create = undefined;
    this.delete = undefined;
    this.get = function (callback){
        var that = this;
        socket = new WebSocket("ws://" + window.location.host + "/chat/");
        socket.onmessage = function(e) {
            var tmp = JSON.parse(e.data);
            for(var i in tmp){
                that.set(i, tmp[i]);
            }
            that.set("changed", false);
            if(callback){
                callback(that);
            }
        };
        socket.onopen = function() {
            socket.send(JSON.stringify(
                {
                    "method": "GET",
                    "model": "example1.DataClass",
                    "data": {
                        "id": that["id"]
                    }
                }
            ));
        };
        if (socket.readyState == WebSocket.OPEN) socket.onopen();
    };
    this.checkSetRule = undefined;
}