(function ($) {

    function xml2json(Xml) {
        var tempvalue, tempJson = {};
        $(Xml).each(function () {
            var tagName = ($(this).attr('id') || this.tagName);
            tempvalue = (this.childElementCount == 0) ? this.textContent : xml2json($(this).children());
            switch ($.type(tempJson[tagName])) {
                case 'undefined':
                    tempJson[tagName] = tempvalue;
                    break;
                case 'object':
                    tempJson[tagName] = Array(tempJson[tagName]);
                case 'array':
                    tempJson[tagName].push(tempvalue);
            }
        });
        return tempJson;
    }

    function setCookie(c_name, value, expiredays) {
        var exdate = new Date();
        exdate.setDate(exdate.getDate() + expiredays);
        document.cookie = c_name + '=' + escape(value) + ((expiredays == null) ? '' : ';expires=' + exdate.toGMTString()) + '; path=' + window.nps.web_base_url + '/;';
    }

    function getCookie(c_name) {
        if (document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + '=');
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(';', c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start, c_end));
            }
        }
        return null;
    }


    $.fn.setLang = function (dom) {
        languages['current'] = $('#languagemenu').attr('lang');
        if (dom == '') {
            $('#languagemenu span').text(' ' + languages['menu'][languages['current']]);
            if (languages['current'] != getCookie('lang')) setCookie('lang', languages['current']);
            if ($("#table").length > 0) $('#table').bootstrapTable('refreshOptions', {'locale': languages['current']});
        }
        $.each($(dom + ' [langtag]'), function (i, item) {
            var index = $(item).attr('langtag');
            string = languages['content'][index.toLowerCase()];
            switch ($.type(string)) {
                case 'string':
                    break;
                case 'array':
                    string = string[Math.floor((Math.random() * string.length))];
                case 'object':
                    string = (string[languages['current']] || string[languages['default']] || null);
                    break;
                default:
                    string = 'Missing language string "' + index + '"';
                    $(item).css('background-color', '#ffeeba');
            }
            if ($.type($(item).attr('placeholder')) == 'undefined') {
                $(item).text(string);
            } else {
                $(item).attr('placeholder', string);
            }
        });

        if (!$.isEmptyObject(chartdatas)) {
            setchartlang(languages['content']['charts'], chartdatas);
            for (var key in chartdatas) {
                if ($('#' + key).length == 0) continue;
                if ($.type(chartdatas[key]) == 'object')
                    charts[key] = echarts.init(document.getElementById(key));
                charts[key].setOption(chartdatas[key], true);
            }
        }
    }

})(jQuery);

var languages = {};
var charts = {};
var chartdatas = {};
var postsubmit;

function langreply(langstr) {
    var langobj = languages['content']['reply'][langstr.replace(/[\s,\.\?]*/g, "").toLowerCase()];
    if ($.type(langobj) == 'undefined') return langstr
    langobj = (langobj[languages['current']] || langobj[languages['default']] || langstr);
    return langobj
}

function submitform(action, url, postdata, filedata) {
    console.log(postdata)
    postsubmit = false;
    var fromData = new FormData();
    $.each(postdata, function (i, field) {
        fromData.append(field.name, field.value)
        fromData.append(i, postdata[i])
    })
    fromData.append("host_key_file", filedata[0])
    var data = fromData;
    switch (action) {
        case 'start':
        case 'stop':
        case 'delete':
            action = ('您确认要删除它吗？')
            if (!confirm(action)) return;
            postsubmit = true;

        case 'add':
        case 'edit':
            $.ajax({
                type: "POST",
                url: url,
                data: data,
                processData: false,
                contentType: false,
                success: function (res) {
                    alert(res.msg);
                    if (res.status) {
                        if (postsubmit) {
                            document.location.reload();
                        } else {
                            history.back(-1);
                        }
                    }
                }
            });
        case 'test':
            $.ajax({
                type: "POST",
                url: url,
                data: data,
                processData: false,
                contentType: false,
                success: function (res) {
                    $('#info').text(res.msg);
                }
            });
    }
}

function changeunit(limit) {
    var size = "";
    if (limit < 0.1 * 1024) {
        size = limit.toFixed(2) + "B";
    } else if (limit < 0.1 * 1024 * 1024) {
        size = (limit / 1024).toFixed(2) + "KB";
    } else if (limit < 0.1 * 1024 * 1024 * 1024) {
        size = (limit / (1024 * 1024)).toFixed(2) + "MB";
    } else {
        size = (limit / (1024 * 1024 * 1024)).toFixed(2) + "GB";
    }

    var sizeStr = size + "";
    var index = sizeStr.indexOf(".");
    var dou = sizeStr.substr(index + 1, 2);
    if (dou == "00") {
        return sizeStr.substring(0, index) + sizeStr.substr(index + 3, 2);
    }
    return size;
}