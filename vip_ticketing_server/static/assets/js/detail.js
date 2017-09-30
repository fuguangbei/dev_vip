$(document).ready(function () {
    get_detail_content();
});

function get_detail_content() {
    if (str1.test(explorer_href)) { //迪士尼详情页
        type_str = arr[0];
        ajax_detail()
    } else if (str2.test(explorer_href)) { //演唱会详情页
        type_str = arr[1];
        ajax_detail()
    } else if (str3.test(explorer_href)) { //宇航套餐详情页
        type_str = arr[2];
        ajax_detail();
        $('#aerospace_button').click(function () {
            $('#my_alert').modal({
                relatedTarget: this
            });
            $('.am-modal-href').click(function () {
                setTimeout(function () {
                    $('body').removeClass('am-dimmer-active')
                    $('.am-modal').css('display', 'none').removeClass('am-modal-active').addClass('am-modal-out');
                    $('.am-dimmer').css('display', 'none').removeClass('am-active');

                }, 10)

            })
        })
    }
}

//ajax
function ajax_detail() {
    $.ajax({
        url: API_host.path_join('tickets', type_str, detail_query_str.id),
        type: 'get',
        success: function (content_object) {
            window.content_object = content_object;
            detail_fill(content_object);//详情页内容
            tickets_like();//收藏
            toggle_like(content_object.liked);
            ask_from_where();//判断访问入口是否显示收藏
        },
        error: function (error_message, err) {
            console.log(error_message);
            console.log(err)
        }
    });
}

//content
function detail_fill(content_object) {
    var detail_cover_url = host.path_join(content_object.detail_cover);

    $('.disney-cover').find('img').attr({
        src: detail_cover_url + '?size=middle', alt: function () {
            return this.src
        }
    });

    $('.d-cover-tit').text(content_object.title);//title
    $('.tk-num i').text(content_object.price);//price

    $('.tk-time i').text(content_object.validity);//有效期
    $('.purchase-notes').html(content_object.purchase_notes);//购买须知
    $('.seat-num').text(content_object.remaining);//concert剩余票数

    if (content_object.remaining == 0) {
        $('.am-btn-primary').addClass('am-disabled');
    } else {
        go_to_native_pay();//支付
    }

    function concert_location() {
        var source = content_object.location;
        var rt = /(.+)?(?:\(|（)(.+)(?=\)|）)/.exec(source);
        $('.concert-building').text(rt[1]);
        $('.concert-address span').text(rt[2]);
    }//concert地点

    if (content_object.type == arr[1]) {
        $('.concert-time').text(concert_time(content_object.time));
        concert_location();
    }

    $('.vip-seating').html(content_object.vip_seating);//concertvip专座
    $('.performance-intro').html(content_object.performance_introduction);//concert演出介绍
    $('.package-intro').html(content_object.package_introduction);//套餐介绍 disney aerospace
    $('.vip-channel').html(content_object.vip_channel);//vip通道 disney
    render_rich_text('.vip-seating', '.performance-intro', '.vip-channel', '.package-intro');//处理图片
}

//pay
function go_to_native_pay() {
    if (!(type_str == arr[2])) {
        var pay_data = window.content_object;
        $('.button_footer button').click(function () {
            var button_id = $(this).attr('id');
            var param = {
                'method': 'go_to_pay',
                'title': document.title,
                'button_name': button_id,
                'data': pay_data
            };
            param = JSON.stringify(param);//变成字符串
            call_native('go_to_pay', param);
        })
    }
}

//ask_ entrance
function ask_from_where() {
    if (not_app) {
        $('.icon-footer').css('display', 'none').removeClass('am-u-sm-4');
        $('.button_footer').removeClass('am-u-sm-8').addClass('am-u-sm-12');
    }
}

//tickets_like
function tickets_like() {
    var heart = $('.footer-heart-icon')
    heart.on('click', function () {
        var cookie_sessionid = getCookie('sessionid')
        // alert(cookie_sessionid)
        // alert("[JAVASCRIPT] PRINTING COOKIE FROM HTML: {0}".format(document.cookie))

        var self = $(this)
        if (self.data('working'))
            return;
        self.data('working', true)
        $.ajax({
            url: API_host.path_join('tickets', type_str, detail_query_str.id, 'like/'),
            type: 'get',
            success: function (data) {
                console.log(data)
                self.data('working', false)
                toggle_like()
            },
            error: function (xhr) {
                console.log(xhr.responseText)
                self.data('working', false)
                call_native_login()
            }
        })
    })
}

function toggle_like(s) {
    var heart = $('.footer-heart-icon')
    if (s === true)
        heart.addClass('heart-right-active')
    else if (s === false)
        heart.removeClass('heart-right-active')
    else
        heart.toggleClass('heart-right-active')
}

//share
function share_description() {
    var share_tit = window.content_object.caption_title,
        share_img = host.path_join(window.content_object.detail_cover),
        share_des = window.content_object.caption_description;

    var share_data = {
        "share_tit": share_tit,
        "share_img": share_img + '?size=small',
        "share_des": share_des
    };
    var share_param = {
        'method': 'go_to_share',
        'title': document.title,
        'data': share_data
    };
    share_param = JSON.stringify(share_param);//变成字符串
    return share_param
}

function like_status() {
    var data = {
        "type": window.content_object.type,
        "id": window.content_object.id,
        "like_status": $('.footer-heart-icon').hasClass('heart-right-active')
    };
    var param = {
        'method': 'refresh_like_list',
        'title': document.title,
        'data': data
    };
    param = JSON.stringify(param);//变成字符串
    call_native('refresh_like_list', param)
}

