//index

$(document).ready(function () {
    if (blsAndroid) {
        $('.top-nav').css('padding-top', '5px');
        $('.am-main-con').css('margin-bottom','0')
    }
    ad();//获取门票广告
    swiper_create();//swiper
    // city();//城市
    go_to_native_search();//搜索
    go_to_native_list();//menu跳转列表
    // getLocation();//定位信息
    get_feature_list();//猜你喜欢
});

//swiper
function swiper_create() {
    var mySwiper = new Swiper('.swiper-container', {
        //autoplay: 6000,
        pagination: '.swiper-pagination', //分页器
        observer: true,//修改swiper自己或子元素时，自动初始化swiper
        observeParents: true,//修改swiper的父元素时，自动初始化swiper
        lazyLoading: true,//延迟加载
        lazyLoadingOnTransitionStart: true,//切换一开始就加载
        lazyLoadingInPrevNext: true//加载到最近一张图
    });
    var mySwiper2 = new Swiper('.swiper-container2', {
        slidesPerView: 2.3, //一屏显示多少图
        paginationClickable: true,
        spaceBetween: 12, //图间距
        freeMode: true //自由模式
    });
}

//go_to_native_search
function go_to_native_search() {
    $('.nav-right img').on('click', function () {
        var param = {
            'method': 'go_to_search',
            'title': 'index_search'
        };
        index_call_native('go_to_search', JSON.stringify(param))

    })
}

//头部广告
function commercial_show(commercial_object) {
    var $container = $('.commercial-con');//放入的容器
    var $template = $('script#commercial_template'); //定义的模版
    var cover_url = host.path_join(commercial_object.cover); //拼接cover地址
    var $elem = $($template.html());
    var cached_img = localStorage.getItem(commercial_object.cover)

    $container.append($elem); //添加请求回的内容到容器

    $elem.find('img').attr('data-src', cover_url + '?size=large'); //更换commercial图片地址

    $elem.find('img').on('load', function () {
        var data = img2dataURI(this)
        localStorage.setItem(commercial_object.cover, data)
    })

    if (cached_img !== null) {
        $elem.find('img').attr('src', cached_img)
    }

    $elem.on('click',function () {
        var data = {
            'type' : commercial_object.type,
            'id' : commercial_object.id
        }
        var c_param = {
            'method' : 'go_to_detail',
            'title' : document.title,
            'data' :data
        }
        index_call_native('go_to_detail',JSON.stringify(c_param))
    })
}

function ad() {

    var cached_list = $.parseJSON(localStorage.getItem('cached_commercial_list'))
    if (cached_list !== null) {
        $('.commercial-con div.swiper-slide').remove()
        for (var i = 0; i < cached_list.length; i++) {
            commercial_show(cached_list[i])
        }
    }

    $.ajax({
        url: API_host.path_join('commercials'),
        type: 'get',
        success: function (commercial_list) {
            //for 循环处理commacials列表每一项
            $('.commercial-con div.swiper-slide').remove()
            for (var i = 0; i < commercial_list.length; i++) {
                commercial_show(commercial_list[i]);
            }
            localStorage.setItem('cached_commercial_list', JSON.stringify(commercial_list))
        },
        error: function (error_message, err) {
            console.log(error_message);
            console.log(err)
        }
    });
}

//menu to native_list
function go_to_native_list() {
    $('.menu img').each(function () {
        $(this).on('click',function(){
            var post_id = $(this).attr("id");
            var param = {
                'method': 'go_to_list',
                'title': 'index',
                'data': post_id
            };
            index_call_native('go_to_list', JSON.stringify(param))
        })
    })
}

//Geolocation
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        $('.position-tips').show();
        $('.position-tips-text').html('您当前的浏览器不支持定位');
    }
}
function showPosition(position) {
    // 百度地图API功能
    var map = new BMap.Map("allmap");

    function myFun(result) {
        var cityName = result.name;
        var newstr = cityName.substring(0, cityName.length - 1);

        var temp = $('ul.am-dropdown-content > li.city:not(.city-maker)')
        var found = false
        var i = null
        for (var i = 0; i < temp.length; i++) {
            if (newstr === $(temp[i]).text()) {
                found = true
                index_found = i
                break
            }
        }
        if (found) {
            $(temp[i]).click()
        }
        $('.city-maker').html(newstr);
    }

    var myCity = new BMap.LocalCity();
    myCity.get(myFun);

}
function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            $('.position-tips').show();
            $('.position-tips-text').html('定位失败,用户拒绝请求地理定位');
            setTimeout(function () {
                $('.position-tips').hide();
            }, 2000);
            break;
        case error.POSITION_UNAVAILABLE:
            $('.position-tips').show();
            $('.position-tips-text').html('定位失败,位置信息是不可用');
            setTimeout(function () {
                $('.position-tips').hide();
            }, 2000);
            break;
        case error.TIMEOUT:
            $('.position-tips').show();
            $('.position-tips-text').html('定位失败,请求获取用户位置超时');
            setTimeout(function () {
                $('.position-tips').hide();
            }, 2000);
            break;
        case error.UNKNOWN_ERROR:
            $('.position-tips').show();
            $('.position-tips-text').html('定位失败,定位系统失效');
            setTimeout(function () {
                $('.position-tips').hide();
            }, 2000);
            break;
    }
    $($('ul.am-dropdown-content > li.city:not(.city-maker)')[0]).click()
}

//city_list
function city_show(city_object) {
    var $container = $('.am-dropdown-content');
    var $template = $('script#city-template');
    var name = city_object.name;
    var $elem = $($template.html());
    $elem.text(name);
    $container.append($elem);
    $elem.click(function () {
        var city_name = $(this).html();
        $('.position-text').html(city_name);
        $('.am-dropdown').dropdown('close');
        $.ajax({
            url: API_host.path_join('city', city_object.id),
            type: 'post',
            success: function (msg) {
                // console.log(msg)
            },
            error: function (msg) {
                console.log(msg.responseText)
            }
        })
    })
}
function city() {
    $.ajax({
        url: API_host.path_join('cities'),
        type: 'get',
        success: function (city_list) {
            for (var i = 0; i < city_list.length; i++) {
                city_show(city_list[i]);
            }
            $('.city-maker').click(function () {
                var city_name = $(this).html();
                $('.position-text').html(city_name);
                $('.am-dropdown').dropdown('close');
            })
            getLocation()
        },
        error: function (error_message, err) {
            console.log(error_message);
            console.log(err)
        }
    });
    $('.am-dropdown-content li').click(function () {

    });
}

//get_feature_list
function get_feature_list() {
    $.ajax({
        url: API_host.path_join('features'),
        type: 'get',
        success: function (feature_list) {
            for (var i = 0; i < feature_list.length; i++) {
                feature_list_show(feature_list[i]);
            }
            var $list_odd =  $('.am-main-con li:odd')
            $list_odd.find('.am-list-main').addClass('float-right');
            $list_odd.find('.am-list-thumb').addClass('float-left');
            $('.am-main-con li:last').removeClass('ui-border-b');
        },
        error: function (error_message, err) {
            console.log(error_message);
            console.log(err)
        }
    });

}
function feature_list_show(feature_object) {
    var $container = $('.feature-con');
    var $template = $('script#feature_template');
    var cover_url = host.path_join(feature_object.cover);
    var $elem = $($template.html());
    $elem.find('h2').text(feature_object.title);
    $elem.find('.am-intro-default').text(feature_object.content);

    $.ajax({
        url: cover_url + '?size=tiny',
        type: 'get',
        success: function () {
            $elem.find('.feature-img').attr('src', cover_url + '?size=medium');
        },
        error: function () {
            set_image_placeholder($elem.find('.feature-img'), true)
        }
    })

    if (!(feature_object.price == null)) {
        $elem.find('.price .now-price').css('display', 'inline-block');
        $elem.find('.now-price .price-num').text(feature_object.price);
    }
    $container.append($elem);
    $elem.on('click',function(){
        var data = {
            'type' : feature_object.type,
            'id' : feature_object.id
        }
        var c_param = {
            'method' : 'go_to_detail',
            'title' : document.title,
            'data' :data
        }
        index_call_native('go_to_detail',JSON.stringify(c_param))
    })

}

$.ajax({
    url: 'signin',
    type: 'post',
    data: {
        phone_number: XXXX,
    },
    success: function() {}
})