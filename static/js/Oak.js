/**
 * Created by RageNaRock on 6/7/2017.
 */
var oakTree = undefined; //მიმღები socket subscribe ფუნქციისვის
var oakTreeSend = undefined; //გამგზავნი socket update ფუნქციისთვის
var oakQueue = []; //update socket ის რიგი

/**
 * ახდენს სოკეტების ინიციალიზაციას
 * @param callback
 */
function initOak(callback, callbackOakm) {
    oakTree = new WebSocket("ws://" + window.location.host + "/chat/");
    oakTreeSend = new WebSocket("ws://" + window.location.host + "/chat/");
    oakTree.onmessage = function (e) {
        var tmp = JSON.parse(e.data);
        console.log("tree init");
        oakTree.onmessage = oakmessage;
        if(callbackOakm !== undefined){
            callbackOakm();
        }
    };
    oakTreeSend.onopen = function () {
        if (callback) {
            callback();
        }
    };
    oakTree.onopen = function () {
        oakTree.send(
            JSON.stringify({
                "method": "PING",
                "model": "None",
                "data": {}
            })
        );
    };
}
/***
 * სვამს მოთხოვნას რიგში
 * @param data გასაგზავნი ინფორმაციის ტიპი
 * @param method მეთოდის სახელი
 * @param model ბაზაში მოდელის სახელი
 * @param callback callback შესრულების შემდეგ
 */
function queueRequest(data, method, model, callback) {
    var tmp = {};
    tmp["data"] = data;
    tmp["method"] = method;
    tmp["model"] = model;
    oakQueue.push({
        "data": tmp,
        "callback": callback
    });
    if (oakQueue.length === 1) {
        startRatatoskr();
    }
}
/**
 * სინქრონიზირებული გამოძახება, რომელიც აგვარებს რიგით გამოძახებას
 */
function startRatatoskr() {
    var tmp = oakQueue.pop();
    oakTreeSend.onmessage = function (e) {
        if ("callback" in tmp) {
            tmp["callback"](JSON.parse(e.data));
        }
        if (oakQueue.length > 0)
            startRatatoskr();
    };
    oakTreeSend.send(JSON.stringify(
        tmp.data
    ));
}

oak_subscription = {};
/**
 * უსმენს სერვერზე კონკრეტული ცვლადის განახლებას
 * @param dataType ცვლადის ტიპი
 * @param objpk ობიექტის უნიკალური გასაღები
 * @param callback თუ ეს ცვლილება შემოვიდა რა უნდა მოხდეს
 */
function subscribeSocket(dataType, objpk, callback) {
    if (!(dataType in oak_subscription)) {
        oak_subscription[dataType] = {};
    }
    oak_subscription[dataType][objpk] = callback;
    oakTree.send(
        JSON.stringify({
            "data": {},
            "method": "SUBSCRIBE",
            "model": dataType
        })
    );
}
/**
 * აუქმებს ცვლადის მოსმენას
 * @param dataType ცვლადის ტიპი
 * @param objpk ობიექტის უნიკალური გასაღები
 */
function cancelsubscription(dataType, objpk) {
    delete oak_subscription[dataType][objpk]
}
/**
 * აგვარებს subscribe/cancelsubscribe ლოგიკის მუშაობას
 * თუ სოკეტზე რამე მოვიდა იძახებს შესაბამის callback ებს
 * @param e
 */
function oakmessage(e) {
    var tmp = JSON.parse(e.data);
    if (!("datatype" in tmp))
        return;
    console.log(tmp);
    var datatype = tmp["datatype"];
    var pk = tmp["pk"];
    if (datatype in oak_subscription) {
        func = oak_subscription[datatype][pk];
        if (func !== undefined) {
            func(tmp);
        }
    }
}