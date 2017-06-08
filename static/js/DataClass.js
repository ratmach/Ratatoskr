function DataClass(id,name,email,index,isActive) {
    this._public_list="id,name,email,index,isActive"
    this.id=id;this.name=name || "abcd";this.email=email;this.index=index;this.isActive=isActive;
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
    this.create = function (callback){
        var that = this;

        socket = new WebSocket("ws://" + window.location.host + "/chat/");

        socket.onmessage = function(e) {

            var tmp = JSON.parse(e.data);
             if(tmp.exception){
                console.log(tmp)
             }

            for(var i in tmp){
                that.set(i, tmp[i]);
            }
            that.set("changed", false);
            if(callback){
                callback(that);
            }
        };

        socket.onopen = function() {
        var params_split = that._public_list.split(',');
        var json_params = {};
        for (var i = 0 ; i < params_split.length; i ++){
            json_params[params_split[i]]=that[params_split[i]]
        }
            socket.send(JSON.stringify(
                {
                    "method": "CREATE",
                    "model": "example1.DataClass",
                    "data": json_params
                }
            ));
        };
        if (socket.readyState == WebSocket.OPEN) socket.onopen();
    };

    this.delete = undefined;
    this.get =     function (callback){
        var that = this;
        queueRequest({"id": that["id"]},"GET",  "example1.DataClass", callback);
    };
    this.checkSetRule = undefined;
}