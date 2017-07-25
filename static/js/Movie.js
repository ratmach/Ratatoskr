function Movie(name,year,image) {
    this._public_list="name,year,image";
    this.name=name;this.year=year;this.image=image;
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
        queueRequest(that,"UPDATE",  "movies.Movie", function(e){
            for(var tmp in e){
                that.set(tmp, e[tmp]);
            }
            that.set("changed", false);
            if(callback)
                callback(that);
        });
    };
    this.create =     function (callback){
        var that = this;
        queueRequest(that,"CREATE",  "movies.Movie", function(e){
            for(var tmp in e){
                that.set(tmp, e[tmp]);
            }
            that.set("changed", false);
            if(callback)
                callback(that);
        });
    };

    this.delete =     function (callback){
        var that = this;
        queueRequest(that,"DELETE",  "movies.Movie", function(e){
            that.set("changed", false);
            if(callback)
                callback(that);
        });
    };
    this.get =     function (callback){
        var that = this;
        queueRequest({"pk": that["pk"]},"GET",  "movies.Movie", function(e){
            for(var tmp in e){
                that.set(tmp, e[tmp]);
            }
            that.set("changed", false);
            if(callback)
                callback(that);
        }
        );
    };
    this.checkSetRule = undefined;
    this.model = "movies.Movie";
    this.sync = function(data){
        for(var d in data){
            this.set(d, data[d]);
        }
    }
}