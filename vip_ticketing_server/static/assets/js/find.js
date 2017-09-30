$(document).ready(function () {
    $('div.comment').data('list', [])
    $('#comment_button').on('click', function () {
        if ($('#explore_input').val() == "") {
            $('.am-input-group').addClass('shake');
            setTimeout(function () {
                $('.am-input-group').removeClass('shake');
            }, 200);
        } else {
            explore_comment_post();
        }
    });//po评论
    ask_from_where();//隐藏收藏
    explore_detail();//内容
    explore_comments_list();//评论列表
    words_number();

    $('div#heart').on('click', function (e) {
        var self = $(this)
        if (self.data('working'))
            return
        self.data('working', true)
        $.ajax({
            url: API_host.path_join('/explore/posts/{0}/like'.format(detail_query_str.id)),
            type: 'get',
            success: function (data) {
                console.log(data)
                self.data('working', false)
                toggle_like_display()
            },
            error: function (xhr) {
                console.log(xhr.responseText)
                self.data('working', false)
                call_native_login()
            }
        })
    })
});

var toggle_like_display = function (set) {
    var $self = $('div#heart')

    if (set === undefined) {
        $self.toggleClass('heart-right-active')
        return
    }

    if (set === true)
        $self.addClass('heart-right-active')
    else
        $self.removeClass('heart-right-active')
}

function ask_from_where() {
    if (not_app) {
        $('#heart').css('display', 'none');
        $('.comment').css('display', 'none');
        $('.c-detail-footer').css('display', 'none');
        $('.find-main').css('height','100%')
    }
}

//explore content
function share_description() {
    var share_tit = window.content_object.caption_title,
        share_img = host.path_join(String(window.content_object.cover)),
        share_des = window.content_object.caption_description;

    var share_data = {
        "share_tit": share_tit,
        "share_img": share_img + '?size=tiny',
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
function explore_detail() {
    $.ajax({
        url: API_host.path_join('explore', 'posts', detail_query_str.id),
        type: 'get',
        success: function (content_object) {
            window.content_object = content_object;
            // $('.explore-video > video').attr('src', content_object.video)
            // $('.explore-video > video').attr('type', 'video/m4v')
            var video_html = content_object.video
            $('.explore-video').html(video_html)
            $('.explore-video > *').css({
                width: '100%',
                height: 'auto'
            })
            $('.explore-tit').text(content_object.title);
            $('.explore-time').text(content_object.date);
            $('.explore-text').html(content_object.raw_content);
            render_rich_text('.explore-text');//处理图片
            toggle_like_display(content_object.liked === undefined ? false : content_object.liked)
        },
        error: function (error_message, err) {
            console.log(error_message);
            console.log(err)
        }
    })
}

//get comments list
function comment_show(comment) {
    var $container = $('.comment');
    var $template = $('script#explore_comments_template');
    var $elem = $($template.html());

    user_data = comment.user;
    if (user_data.name == "") {
        $elem.find('.comment-name').text('匿名');
    } else {
        $elem.find('.comment-name').text(user_data.name);
    } //姓名
    if (user_data.avatar == "") {
        $elem.find('.comment-avatar>img').attr('src', '/static/assets/i/app-icon72x72@2x.png');
    }
    else {
        var user_photo = host.path_join(user_data.avatar);
        $elem.find('.comment-avatar>img').attr('src', user_photo + '?size=middle');
    }//头像

    $elem.find('.comment-text > p').text(comment.text);//内容
    $elem.find('.comment-date').text(comment.date);//时间

    var $head = $container.find('div.comment-tit')
    $head.after($elem)
}

var comment_exist = function (object, list) {
    for (var i = 0; i < list.length; i++) {
        if (object.id === list[i].id)
            return true
    }
    return false
}

function explore_comments_list() {
    var $container = $('.comment');

    $.ajax({
        url: API_host.path_join('explore', 'posts', detail_query_str.id, 'comments/'),
        type: 'get',
        success: function (comments_object) {
            $('.comment-count').text(comments_object.count);//条数
            comments = comments_object.data;//提数据

            var current_list = $container.data('list')
            for (var i = comments.length - 1; i > -1; i--) {
                if (comment_exist(comments[i], current_list)) {
                    continue
                }
                comment_show(comments[i]);
            }
            $container.data('list', comments)

            $('.comment-con:last').removeClass('comment-border');
        },
        error: function (error_message, err) {
            console.log(error_message);
            console.log(err);
        }
    })
}

//post comment
function explore_comment_post() {
    var str = '#explore_input';

    var post_comment_content = {
        'text': $(str).val(),
        'id': detail_query_str.id
    };
    $.ajax({
        url: API_host.path_join('explore', 'posts', detail_query_str.id, 'comment/'),
        type: 'post',
        data: post_comment_content,
        success: function () {
            $('#explore_input').val('');
            explore_comments_list();//刷新列表
            $('html, body').animate({
                scrollTop: parseInt($('#anchor').offset().top)
            })
        },
        error: function (error_message, err) {
            console.log(error_message);
            console.log(err);
            $('.am-input-group').addClass('shake');
            setTimeout(function () {
                $('.am-input-group').removeClass('shake');
            }, 200);
            call_native_login();
        }
    })
}

//字数控制
function words_number() {
    $("#explore_input").keydown(function () {
        var curLength = $("#explore_input").val().length;
        if (curLength >= 140) {
            var num = $("#explore_input").val().substr(0, 139);
            $("#explore_input").val(num);
            $('.am-input-group').addClass('shake');
            setTimeout(function () {
                $('.am-input-group').removeClass('shake');
            }, 200);
        }
    });
}

function onKeyboardOpen() {
    max_scroll = 99999;
    window.scrollTo(0, max_scroll);
}
