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
    this.update =     function (callback){
        var that = this;
        queueRequest(that,"UPDATE",  "example1.DataClass", function(e){
            for(var tmp in e){
                that.set(tmp, e[tmp]);
            }
            if(callback)
                callback(that);
        });
    };
    this.create =     function (callback){
        var that = this;
        queueRequest(that,"CREATE",  "example1.DataClass", function(e){
            for(var tmp in e){
                that.set(tmp, e[tmp]);
            }
            if(callback)
                callback(that);
        });
    };

    this.delete =     function (callback){
        var that = this;
        queueRequest(that,"DELETE",  "example1.DataClass", callback);
    };
    this.get =     function (callback){
        var that = this;
        queueRequest({"id": that["id"]},"GET",  "example1.DataClass", function(e){
            for(var tmp in e){
                that.set(tmp, e[tmp]);
            }
            if(callback)
                callback(that);
        }
        );
    };
    this.checkSetRule = undefined;
    this.model = "example1.DataClass";
}