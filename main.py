import os

# name="test"
# zhname="测试"
# ver="0.01"
# author="小葱"
# authorurl="http://www.mrcong.cn"

print('''
宝塔开发助手
一键生成开发包免去修改麻烦
作者：小葱 QQ：809468582
''')

name=input('请输入唯一标识   : ')
zhname=input('请输入插件中文名称   : ')
ver=input('请输入版本号   : ')
author=input('请输入作者   : ')
authorurl=input('请输入作者主页   : ')

def write(path,strs):
    s='/'.join(path.split('/')[:-1])
    if not os.path.exists(s):
        os.makedirs(s)
    with open(path, 'w',encoding='utf-8') as f:

        f.write(strs)
        f.close()


path='data/{}/info.json'.format(name)
strs='''
  "title": "{}",
  "name": "{}",
  "ps": "{}",
  "versions": "{}",
  "checks": "/www/server/panel/plugin/{}",
  "author": "{}",
  "home": "{}"
'''.format(zhname,name,zhname,ver,name,author,authorurl)
print('生成 {}'.format(path))
write(path,'{'+strs+'}')

path='data/{}/install.sh'.format(name)
strs='''#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

#配置插件安装目录
install_path=/www/server/panel/plugin/'''+name+'''

#安装
Install()
{
	
	echo '正在安装...'
	#==================================================================
	#依赖安装开始


	#依赖安装结束
	#==================================================================

	echo '================================================'
	echo '安装完成'
}

#卸载
Uninstall()
{
	rm -rf $install_path
}

#操作判断
if [ "${1}" == 'install' ];then
	Install
elif [ "${1}" == 'uninstall' ];then
	Uninstall
else
	echo 'Error!';
fi


'''
print('生成 {}'.format(path))
write(path,strs)



path='data/{}/index.html'.format(name)
strs='''<style>
    /*样式写这里*/
    .demo-table table tbody tr td span{
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        width:580px;
        display:block;
    }

</style>
<div class="bt-form">
    <div class="bt-w-main">
        <!--菜单部分-->
        <div class="bt-w-menu">
            <p class="bgw" onclick="demo.get_index()">概览</p>
            <p onclick="demo.get_logs()">操作日志</p>
        </div>
        <!--内容部分-->
        <div class="bt-w-con pd15">
            <div class="plugin_body"></div>
        </div>
    </div>
</div>

<!--JS脚本部分，不要将JS脚本写在其它地方-->
<script type="text/javascript" src="/demo/static/js/test.js"></script> <!--引用插件目录下的static/js/test.js-->
<script type="text/javascript">

    //定义窗口尺寸
    $('.layui-layer-page').css({ 'width': '900px' });

    //左测菜单切换效果
    $(".bt-w-menu p").click(function () {
        $(this).addClass('bgw').siblings().removeClass('bgw')
    });

    /**
     * 插件交互对象
     * 您的所有JS代码可以写在里面
     * 若不习惯JS的面向对象编程，可删除此对象，使用传统函数化的方式编写
     * */
    var demo = {
        //构造概览内容
        get_index: function () {
            $('.plugin_body').html("<h1 style='text-align:center;margin-top:30%;'>这是一个示例插件!</h1>");
        },

        /**
         * 获取面板日志
         * @param p 被获取的分页
         */
        get_logs : function (p) {
            if (p == undefined) p = 1;
            request_plugin('demo', 'get_logs', { p: p, callback: 'demo.get_logs' }, function (rdata) {
                var log_body = '';
                for (var i = 0; i < rdata.data.length; i++) {
                    log_body += '<tr><td>' + rdata.data[i].addtime + '</td><td><span title="' + rdata.data[i].log + '">' + rdata.data[i].log + '</span></td></tr>'
                }

                var my_body = '<div class="demo-table"><div class="divtable">'
                            +'<table class="table table-hover">'
                                +'<thead>'
                                    +'<tr><th width="150">时间</th><th>详情</th></tr>'
                                +'</thead>'
                                +'<tbody>'+ log_body + '</tbody>'
                            +'</table>'
                    + '</div><div class="page" style="margin-top:15px">' + rdata.page + '</div</div>';

                $('.plugin_body').html(my_body);
            });
        }

    }

    /**
     * 发送请求到插件
     * 注意：除非你知道如何自己构造正确访问插件的ajax，否则建议您使用此方法与后端进行通信
     * @param plugin_name    插件名称 如：demo
     * @param function_name  要访问的方法名，如：get_logs
     * @param args           传到插件方法中的参数 请传入数组，示例：{p:1,rows:10,callback:"demo.get_logs"}
     * @param callback       请传入处理函数，响应内容将传入到第一个参数中
     */
    function request_plugin(plugin_name, function_name, args, callback, timeout) {
        if (!timeout) timeout = 3600;
        $.ajax({
            type:'POST',
            url: '/plugin?action=a&s=' + function_name + '&name=' + plugin_name,
            data: args,
            timeout:timeout,
            success: function(rdata) {
                if (!callback) {
                    layer.msg(rdata.msg, { icon: rdata.status ? 1 : 2 });
                    return;
                }
                return callback(rdata);
            },
            error: function(ex) {
                if (!callback) {
                    layer.msg('请求过程发现错误!', { icon: 2 });
                    return;
                }
                return callback(ex);
            }
        });
    }

    //第一次打开窗口时调用
    demo.get_index();

</script>
'''.replace('demo',name)
print('生成 {}'.format(path))
write(path,strs)



path='data/{}/{}_main.py'.format(name,name)
strs='''#!/usr/bin/python
# coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2099 宝塔软件(http://bt.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: xxx <xxxx@qq.com>
# +-------------------------------------------------------------------

#+--------------------------------------------------------------------
#|   宝塔第三方应用开发DEMO
#+--------------------------------------------------------------------
import sys,os,json

#设置运行目录
os.chdir("/www/server/panel")

#添加包引用位置并引用公共包
sys.path.append("class/")
import public

#from common import dict_obj
#get = dict_obj();


#在非命令行模式下引用面板缓存和session对象
if __name__ != '__main__':
    from BTPanel import cache,session,redirect

    #设置缓存(超时10秒) cache.set('key',value,10)
    #获取缓存 cache.get('key')
    #删除缓存 cache.delete('key')

    #设置session:  session['key'] = value
    #获取session:  value = session['key']
    #删除session:  del(session['key'])


class demo_main:
    __plugin_path = "/www/server/panel/plugin/demo/"
    __config = None

    #构造方法
    def  __init__(self):
        pass

    #自定义访问权限检查
    #一但声明此方法，这意味着可以不登录面板的情况下，直接访问此插件，由_check方法来检测是否有访问权限
    #如果您的插件必需登录后才能访问的话，请不要声明此方法，这可能导致严重的安全漏洞
    #如果权限验证通过，请返回True,否则返回 False 或 public.returnMsg(False,'失败原因')
    #示例未登录面板的情况下访问get_logs方法： /demo/get_logs.json  或 /demo/get_logs.html (使用模板)
    #可通过args.fun获取被请求的方法名称
    #可通过args.client_ip获取客户IP
    def _check(self,args):
        #token = '123456'
        #limit_addr = ['192.168.1.2','192.168.1.3']
        #if args.token != token: return public.returnMsg(False,'Token验证失败!')
        #if not args.client_ip in limit_addr: return public.returnMsg(False,'IP访问受限!')
        #return redirect('/login')
        return True

    #访问/demo/index.html时调用的默认方法，需要在templates中有index.html，否则无法正确响应模板
    def index(self,args):
        return self.get_logs(args)


    #获取面板日志列表
    #传统方式访问get_logs方法：/plugin?action=a&name=demo&s=get_logs
    #使用动态路由模板输出： /demo/get_logs.html
    #使用动态路由输出JSON： /demo/get_logs.json
    def get_logs(self,args):
        #处理前端传过来的参数
        if not 'p' in args: args.p = 1
        if not 'rows' in args: args.rows = 12
        if not 'callback' in args: args.callback = ''
        args.p = int(args.p)
        args.rows = int(args.rows)

        #取日志总行数
        count = public.M('logs').count()

        #获取分页数据
        page_data = public.get_page(count,args.p,args.rows,args.callback)

        #获取当前页的数据列表
        log_list = public.M('logs').order('id desc').limit(page_data['shift'] + ',' + page_data['row']).field('id,type,log,addtime').select()
        
        #返回数据到前端
        return {'data': log_list,'page':page_data['page'] }
        
    #读取配置项(插件自身的配置文件)
    #@param key 取指定配置项，若不传则取所有配置[可选]
    #@param force 强制从文件重新读取配置项[可选]
    def __get_config(self,key=None,force=False):
        #判断是否从文件读取配置
        if not self.__config or force:
            config_file = self.__plugin_path + 'config.json'
            if not os.path.exists(config_file): return None
            f_body = public.ReadFile(config_file)
            if not f_body: return None
            self.__config = json.loads(f_body)

        #取指定配置项
        if key:
            if key in self.__config: return self.__config[key]
            return None
        return self.__config

    #设置配置项(插件自身的配置文件)
    #@param key 要被修改或添加的配置项[可选]
    #@param value 配置值[可选]
    def __set_config(self,key=None,value=None):
        #是否需要初始化配置项
        if not self.__config: self.__config = {}

        #是否需要设置配置值
        if key:
            self.__config[key] = value

        #写入到配置文件
        config_file = self.__plugin_path + 'config.json'
        public.WriteFile(config_file,json.dumps(self.__config))
        return True


'''.replace('demo',name)
print('生成 {}'.format(path))
write(path,strs)



path='data/{}/templates/get_logs.html'.format(name)
strs='''<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8" />
    <title></title>
</head>
<body>
    the is test!
    <table>
        <thead>
            <tr>
                <th>时间</th>
                <th>详情</th>
            </tr>
        </thead>
        <tbody>
            {% for value in data['data'] %}
            <tr>
                <td>{{value['addtime']}}</td>
                <td>{{value['log']}}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <p>{{data['page']|safe}}</p>
</body>
<script type="text/javascript" src="/demo/static/js/test.js"></script>
</html>
'''
print('生成 {}'.format(path))
write(path, strs )


path='data/{}/templates/index.html'.format(name)
strs='''<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8" />
    <title></title>
</head>
<body>
    the is test!
    <table>
        <thead>
            <tr>
                <th>时间</th>
                <th>详情</th>
            </tr>
        </thead>
        <tbody>
            {% for value in data['data'] %}
            <tr>
                <td>{{value['addtime']}}</td>
                <td>{{value['log']}}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <p>{{data['page']|safe}}</p>
</body>
<script type="text/javascript" src="/demo/static/js/test.js"></script>
</html>

'''
print('生成 {}'.format(path))
write(path, strs )




path='data/{}/static/js/test.js'.format(name)
strs='''alert('这是静态资源引用测试!');
'''
print('生成 {}'.format(path))
write(path, strs )

path='data/{}/icon.png'.format(name)
print('生成 {}'.format(path))
write(path, '' )