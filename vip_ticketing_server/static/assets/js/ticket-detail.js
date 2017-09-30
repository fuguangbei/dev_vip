$(document).ready(function () {
    detail_id = get_query_parameters().id;
    ajax_content();

})

function ajax_content() {

    $.ajax({
        url: API_host.path_join('/tickets/scenery/{0}'.format(detail_id)),
        type: 'get',
        success: function (content_object) {
            window.content_object = content_object;

            content_fill(content_object);
            tickets_like();//收藏
            toggle_like(content_object.liked);
            ask_from_where();//判断访问入口是否显示收藏

        },
        error: function (error_message, err) {
            console.log(error_message);
            console.log(err)
        }
    })
}
function content_fill(content_object) {

    document.title = content_object.title;

    var detail_cover_url = host.path_join(content_object.detail_cover);
    $('.disney-cover').find('img').attr({src: detail_cover_url + '?size=medium', alt: content_object.caption_title});

    $('.d-cover-tit').text(content_object.title);//title

    $('.tk-num i').text(content_object.price);//price

    $('.package-intro').html(content_object.package_introduction);//套餐介绍

    $('.purchase-notes').html(content_object.purchase_notes);//购买须知

    render_rich_text('.package-intro');//处理图

    if (content_object.remaining == 0) {
        $('.am-btn-primary').addClass('am-disabled');
    } else {
        go_to_native_pay();//支付
    }

    render_rich_text('.purchase-notes', '.package-intro');//处理图片


}

//tickets_like
function tickets_like() {
    var heart = $('.footer-heart-icon')
    heart.on('click', function () {
        var cookie_sessionid = getCookie('sessionid')

        var self = $(this)
        if (self.data('working'))
            return;
        self.data('working', true)

        $.ajax({
            url: API_host.path_join('/tickets/scenery/{0}/like'.format(detail_id)),
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

//收藏样式
function toggle_like(s) {
    var heart = $('.footer-heart-icon')
    if (s === true)
        heart.addClass('heart-right-active')
    else if (s === false)
        heart.removeClass('heart-right-active')
    else
        heart.toggleClass('heart-right-active')
}

// 传给原生like状态
function like_status() {
    var data = {
        "type": detail_type,
        "id": detail_id,
        "like_status": $('.footer-heart-icon').hasClass('heart-right-active')
    };
    var param = {
        'method': 'refresh_like_list',
        'title': document.title,
        'data': data
    };
    param = JSON.stringify(param);//变成字符串
    console.log(param);
    call_native('refresh_like_list', param)
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

//pay
function go_to_native_pay() {
    var pay_data = window.content_object;
    console.log(pay_data);
    $('.pay-btn').click(function () {
        var param = {
            'method': 'go_to_pay',
            'title': document.title,
            'data': pay_data
        };
        param = JSON.stringify(param);//变成字符串
        call_native('go_to_pay', param);
    })
}

//ask_ entrance
function ask_from_where() {
    if (not_app) {
        $('.icon-footer').css('display', 'none').removeClass('am-u-sm-4');
        $('.button_footer').removeClass('am-u-sm-8').addClass('am-u-sm-12');
    }
}