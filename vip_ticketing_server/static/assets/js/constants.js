host = "http://139.196.83.122:8000/";
// host = "http://120.76.126.214:8000/"; //公司阿里云测试服务器
// host = "http://10.10.10.28:8000/"; //汉章的个人电脑
// host = "http://localhost:8000/"
API_root = "api/v1/";
API_host = host + API_root;

//app agent
ios_str = /shanghaivip.ios/;
android_str = /shanghaivip.android/;
sUserAgent = navigator.userAgent.toLowerCase();
blsIphoneOs = sUserAgent.match(/iphone os/i) == 'iphone os';
blsAndroid = sUserAgent.match(/android/i) == 'android';
not_app = !(ios_str.test(sUserAgent) || android_str.test(sUserAgent));

//版本
version_str = /ver2.0.0/;
new_version = version_str.test(sUserAgent);//是不是新版本
if (!new_version) {
    $('.old-version-hidden').css('display','none');
}
//detail
arr = ['disney', 'concert', 'aerospace'];
str1 = new RegExp(arr[0]);
str2 = new RegExp(arr[1]);
str3 = new RegExp(arr[2]);
explorer_href = window.location.href;
type_str = '';//有斜杠

//拼地址
String.prototype.path_join = function () {
    var current = this,
        args = Array.prototype.slice.call(arguments);

    args.forEach(function (elem, i) {
        var ending = current[current.length - 1],
            starting = elem[0];

        if (ending !== '/')
            current = current + '/';

        if (starting === '/')
            current += elem.substring(1);
        else
            current += elem
    });

    return current
};

//什么鬼
String.prototype.format = function () {
    var formatted = this;
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{' + i + '\\}', 'gi');
        formatted = formatted.replace(regexp, arguments[i])
    }
    return formatted
};

//query_url_str
var get_query_parameters = function () {
    var query_str = window.location.search.substr(1);
    var query_list = query_str.split('&');
    var str_object = {};//dictionary
    query_list.forEach(function (elem, i) {
        var elemArray = elem.split('=');//等号拆分两个值
        if (elemArray[1]) {
            str_object[elemArray[0]] = elemArray[1];
        }
    });
    return str_object;
};

detail_query_str = get_query_parameters();

//图片显示
var display_image = function (dom_image) {
    var $image = $(dom_image);
    var src_url = $image.attr('src');
    src_url = host.path_join(src_url);
    $image.attr('src', src_url)
};

//图片按比例缩放
var resize_image = function (dom_image) {
    var $image = $(dom_image);

    var width, height, ratio;
    width = $image.width();
    height = $image.height();
    ratio = (width + 0.0) / height;//变浮点

    $image.width('100%');
    width = $image.width();
    $image.height(width / ratio)
};

//该函数接收任意个数的参数  富文本取图片
var render_rich_text = function () {
    var selectors = Array.prototype.slice.call(arguments);
    selectors.forEach(function (selector, i) {
        var $object = $(selector);
        var $images = $object.find('input[type=image]');
        for (var i = 0; i < $images.length; i++) {
            display_image($images[i]);
            resize_image($images[i])
        }
    })
};

//日期换格式
function concert_time(time) {
    var date = new Date(time);
    var year = date.getFullYear();
    var month = date.getMonth() + 1; //js从0开始取
    var date1 = date.getDate();
    var hour = date.getHours();
    var minutes = date.getMinutes();

    if (month < 10) {
        month = "0" + month;
    }
    if (date1 < 10) {
        date1 = "0" + date1;
    }
    if (hour < 10) {
        hour = "0" + hour;
    }
    if (minutes < 10) {
        minutes = "0" + minutes;
    }
    new_date = year + "-" + month + "-" + date1 + " " + hour + ":" + minutes;
    return (new_date);
}

// is_landscape: boolean类型变量, 为true时表示横图, 反之表示竖图
var set_image_placeholder = function ($img, is_landscape) {
    if (is_landscape === undefined) {
        is_landscape = true
    }
    placeholder = is_landscape ? '/static/assets/i/cover.png' : '/static/assets/i/cover_portrait.png'
    var path = host.path_join(placeholder)
    $img.attr('src', path)
}

function img2dataURI(dom_img) {
    var canvas = document.createElement('canvas'),
        context = canvas.getContext('2d')

    canvas.height = dom_img.height
    canvas.width = dom_img.width
    context.drawImage(dom_img, 0, 0, dom_img.width, dom_img.height)
    return canvas.toDataURL('image/jpeg')
}

var get_arguments = function (args) {
    var ret = []
    for (var i = 0; i < args.length; i++)
        ret.push(args[i])
    return ret
}

var call_native = function (func_name) {
    var args = get_arguments(arguments)
    args = args.slice(1)

    if (blsAndroid) {
        callAndroid[func_name](args[0])
    }
    else if (blsIphoneOs) {
        window[func_name].apply(this, args)
    }
}

var call_native_login = function () {
    var params = {
        'method': 'trigger_login',
        'title': document.title
    }
    call_native('trigger_login', JSON.stringify(params))
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function index_call_native(function_name, param) {
    console.log(param)
    if (blsAndroid)
        callAndroid[function_name](param)
    else if (blsIphoneOs) {
        window.webkit.messageHandlers[function_name].postMessage(param)
    }
}


