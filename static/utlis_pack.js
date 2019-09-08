var get = function (str) {
    return document.querySelector(str)
}

var get_all = function (str) {
    return document.querySelectorAll(str)
}

var log = function() {
    console.log.apply(console, arguments)
}
var ensure = function(condition, message) {
    // 在条件不成立的时候, 输出 message
    if(!condition) {
        log('*** 测试失败:', message)
    }
}

var switch_of_class = function (ele, class_name) {
    if (ele.classList.contains(class_name)){
        ele.classList.remove(class_name)
    }
    else{
        ele.classList.add(class_name)
    }
}

var bind_all = function (class_str, event, callback) {
    var eles = get_all(class_str)
    for (var ele of eles){
        ele.addEventListener(event, callback)
    }
}

var ajax = function(method, path, data, reseponseCallback) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    // 这个不是必须的
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
            reseponseCallback(r.response)
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}