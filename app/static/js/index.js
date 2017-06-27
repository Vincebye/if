$(function () {
    var oExports = {
        initialize: fInitialize,
        // 渲染更多数据
        renderMore: fRenderMore,
        // 请求数据
        requestData: fRequestData,
        // 简单的模板替换
        tpl: fTpl
    };
    // 初始化页面脚本
    oExports.initialize();

    function detail_index() {
    var oExports = {
        initialize: fInitialize,
        encode: fEncode
    };
    oExports.initialize();

    function fInitialize() {
        var that = this;

        var num = $('ul.discuss-list');
        for (i = 1; i <= num.length; i++){
            //var sImageId = $('#js-image-id-' + i);
            //console.log(sImageId.val())
            //var oCmtIpt = $('#jsCmt-' + i);
            //var oListDv = $('#js-discuss-list-' + i);

            // 点击添加评论
            var bSubmit = false;
            $('#jsSubmit-' + i).unbind();
            $('#jsSubmit-' + i).on('click', function () {
                var control_id = $(this).attr('id')
                var id = control_id.substring(9)
                console.log(id)
                var sImageId = $('#js-image-id-' + id).val();
                console.log(sImageId)
                var oCmtIpt = $('#jsCmt-' + id);
                console.log(oCmtIpt.val())
                var oListDv = $('.js-discuss-list-' + id);

                //var sCmt = $.trim(oCmtIpt.val());
                //alert(sCmt)
                sCmt = oCmtIpt.val()
                console.log(sCmt)
                // 评论为空不能提交
                if (!sCmt) {
                    console.log('pinglun: ' + id + oCmtIpt.attr('id'))
                    return alert('评论不能为空');
                    //continue;
                }
                // 上一个提交没结束之前，不再提交新的评论
                if (bSubmit) {
                    return;
                }
                bSubmit = true;
                $.ajax({
                    url: '/addcomment/',
                    type: 'post',
                    dataType: 'json',
                    data: {image_id: sImageId, content: sCmt}
                }).done(function (oResult) {
                    if (oResult.code !== 0) {
                        return alert(oResult.msg || '提交失败，请重试');
                    }
                    // 清空输入框
                    oCmtIpt.val('');
                    // 渲染新的评论
                    var sHtml = [
                        '<li>',
                            '<a class="_4zhc5 _iqaka" title="', that.encode(oResult.username), '" href="/profile/', oResult.user_id, '">', that.encode(oResult.username), '</a> ',
                            '<span><span>', that.encode(sCmt), '</span></span>',
                        '</li>'].join('');
                    oListDv.prepend(sHtml);

                    // 修改评论数
                    var counts = $(".length-" + id).text()
                    $(".length-" + id).text(parseInt(counts, 10) + 1);

                }).fail(function (oResult) {
                    alert(oResult.msg || '提交失败，请重试');
                }).always(function () {
                    bSubmit = false;
                });
            });
        }
    }

    function fEncode(sStr, bDecode) {
        var aReplace =["&#39;", "'", "&quot;", '"', "&nbsp;", " ", "&gt;", ">", "&lt;", "<", "&amp;", "&", "&yen;", "¥"];
        !bDecode && aReplace.reverse();
        for (var i = 0, l = aReplace.length; i < l; i += 2) {
             sStr = sStr.replace(new RegExp(aReplace[i],'g'), aReplace[i+1]);
        }
        return sStr;
    };

}

    function fInitialize() {
        var that = this;
        // 常用元素
        that.listEl = $('div.js-image-list');
        // 初始化数据
        //that.uid = window.uid;
        that.page = 1;
        that.pageSize = 5;
        that.listHasNext = true;
        // 绑定事件
        $('.js-load-more').on('click', function (oEvent) {
            var oEl = $(oEvent.currentTarget);
            var sAttName = 'data-load';
            // 正在请求数据中，忽略点击事件
            if (oEl.attr(sAttName) === '1') {
                return;
            }
            // 增加标记，避免请求过程中的频繁点击
            oEl.attr(sAttName, '1');
            that.renderMore(function () {
                // 取消点击标记位，可以进行下一次加载
                oEl.removeAttr(sAttName);
                // 没有数据隐藏加载更多按钮
                !that.listHasNext && oEl.hide();
            });
        });
    }

    function fRenderMore(fCb) {
        var that = this;
        // 没有更多数据，不处理
        if (!that.listHasNext) {
            return;
        }
        that.requestData({
            uid: that.uid,
            page: that.page + 1,
            pageSize: that.pageSize,
            call: function (oResult) {
                // 是否有更多数据
                that.listHasNext = !!oResult.has_next && (oResult.images || []).length > 0;
                // 更新当前页面
                that.page++;
                // 渲染数据
                var sHtml = '';
                $.each(oResult.images, function (nIndex, oImage) {
                    sHtml_part1_1 = that.tpl([
                         '<article class="mod">',
            '<header class="mod-hd">',
                '<time class="time">#{ image.create_date }</time>',
                '<a href="/profile/#{image_user_id}" class="avatar">',
                 '   <img src="#{image_user_head_url}">',
                '</a>',
                '<div class="profile-info">',
                    '<a title="#{image_user_username}" href="/profile/#{image_user_id}">#{image_user_username}</a>',
                '</div>',
            '</header>',
            '<div class="mod-bd">',
                '<div class="img-box">',
                    '<a href = "/image/#{image_id}">',
                    '<img src="#{image_url}">',
               ' </div>',
           ' </div>',
           ' <div class="mod-ft">',
              '  <ul class="discuss-list">',
                   ' <li class="more-discuss">',
                       ' <a>',
                           ' <span>全部 </span><span class="length-'].join(''), oImage);

                    sHtml_part1_2 = that.tpl([
                        '">#{image_comments_length}</span>',
                            '<span> 条评论</span></a>',
                    '</li>',
                    '<div class = "js-discuss-list-',
            ].join(''), oImage);

                    sHtml_part1_3 = that.tpl(['"></div>',
                    ].join(''), oImage);

                    //var cur_page_id = page * pageSize + nIndex;
                    console.log((that.page - 1) * that.pageSize + nIndex);
                    var cur_page_id = (that.page - 1) * that.pageSize + nIndex + 1;
                    sHtml_part1 = sHtml_part1_1 + cur_page_id.toString() +  sHtml_part1_2 +
                        cur_page_id.toString() +  sHtml_part1_3;


                    sHtml_part2 = ' ';

                    for (var ni = 0; ni < oImage.image_comments_length; ni++){
                        dict = {'comment_user_username':oImage.comment_user_username[ni], 'comment_user_id':oImage.comment_user_id[ni],
                            'comment_content':oImage.comment_content[ni] };

                        sHtml_part2 += that.tpl([
                        '    <li>',
                            '    <a class="_4zhc5 _iqaka" title="#{comment_user_username}" href="/profile/#{comment_user_id}" data-reactid=".0.1.0.0.0.2.1.2:$comment-17856951190001917.1">#{comment_user_username}</a>',
                            '    <span>',
                            '        <span>#{comment_content}</span>',
                           '     </span>',
                         '   </li>',
                             ].join(''), dict);
                    }

                    sHtml_part3_1 =    that.tpl([
              '  </ul>',
                '<section class="discuss-edit">',
                    '<a class="icon-heart"></a>',
                    '<form>',
                        '<input placeholder="添加评论..." id = "jsCmt-',
                    ].join(''), oImage);

                    sHtml_part3_2 = that.tpl([
                        '" type="text">',
                        '<input id = "js-image-id-',
                         ].join(''), oImage);

                    sHtml_part3_3 = that.tpl([
                        '" type = "text" style="display: none" value="#{image_id}">',
                    '</form>',
                    '<button class="more-info" id = "jsSubmit-'
                        ].join(''), oImage);

                    sHtml_part3_4 = that.tpl([
                        '">更多选项</button>',
                '</section>',
           ' </div>',
       ' </article>  '
                    ].join(''), oImage);

                    sHtml_part3 = sHtml_part3_1 + cur_page_id.toString() +  sHtml_part3_2 +
                        cur_page_id.toString() +  sHtml_part3_3 +
                        cur_page_id.toString() +  sHtml_part3_4;


                    sHtml += sHtml_part1 + sHtml_part2 + sHtml_part3;
                });
                sHtml && that.listEl.append(sHtml);
            },
            error: function () {
                alert('出现错误，请稍后重试');
            },
            always: fCb
        });

        setTimeout(detail_index, 1000);
    }

    function fRequestData(oConf) {
        var that = this;
        var sUrl = '/images/' + oConf.page + '/' + oConf.pageSize + '/';
        $.ajax({url: sUrl, dataType: 'json'}).done(oConf.call).fail(oConf.error).always(oConf.always);
    }

    function fTpl(sTpl, oData) {
        var that = this;
        sTpl = $.trim(sTpl);
        return sTpl.replace(/#{(.*?)}/g, function (sStr, sName) {
            return oData[sName] === undefined || oData[sName] === null ? '' : oData[sName];
        });
    }
});