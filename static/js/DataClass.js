function DataClass(name,email,isActive) {
    this.name=name || "abcd";this.email=email;this.isActive=isActive;
    this.changed=false;
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
    this.get = undefined;
    this.checkSetRule = undefined;
}