/**
 * @ name : citySelect 省市区三级选择模块
 * @ Author: aggerChen
 * @ version: 1.0
 */

layui.define(['layer','form','element','laytpl'], function(exports){
	var $ = layui.$;
	var form = layui.form;
	var laytpl = layui.laytpl;
	var element = layui.emelemt;
	
	//外部接口
	var citySelect = {
		    config: {} //全局配置项
		    ,cache: {} //数据缓存
		    ,index: layui.laypage ? (layui.laypage.index + 10000) : 0
	};
	
	//操作当前实例
	var thisSelect = function(){
	    var that = this,
	    options = that.config,
	    id = options.id;
	    id && (thisSelect.config[id] = options);
	    
	    return {
	      reload: function(options){
	    	  that.reload.call(that, options);
	      },
	      config: options
	    }
	};
	
	//字符常量
	var MOD_NAME = 'citySelect';
	
	//主模板
	var TPL_MAIN = ['<div class="layui-form-item" >',
						'<label class="layui-form-label">{{ d.data.lableName }}</label>',
						'<div class="layui-input-inline" style="width:160px">',
							'<select name="{{ d.data.filed.provinceName }}" class="{{ d.data.id }}_selectCity" id="citySelect_{{ d.data.filed.provinceName }}{{ d.index }}" lay-filter="province{{ d.index }}" {{#if(d.data.search){ }}  lay-search {{# } }} {{#if(d.data.required){ }} lay-verify="required" {{# } }} {{#if(d.data.disabled){ }} disabled {{# } }} >',
								'<option value="000000">-- 全部 --</option>',
							'</select>',
						'</div>',
						'<div class="layui-input-inline" style="width:161px">',
							'<select name="{{ d.data.filed.cityName }}" class="{{ d.data.id }}_selectCity" id="citySelect_{{ d.data.filed.cityName }}{{ d.index }}" lay-filter="city{{ d.index }}" {{#if(d.data.search){ }}  lay-search {{# } }} {{#if(d.data.required){ }} lay-verify="required" {{# } }} {{#if(d.data.disabled){ }} disabled {{# } }} >',
								'<option value="">-- 全部 --</option>',
							'</select>',
						'</div>',
						'{{# if(d.data.filed.area){ }}',
						'<div class="layui-input-inline" style="width:161px">',
							'<select name="{{ d.data.filed.areaName }}" class="{{ d.data.id }}_selectCity" id="citySelect_{{ d.data.filed.areaName }}{{ d.index }}" lay-filter="area{{ d.index }}" {{#if(d.data.search){ }}  lay-search {{# } }} {{#if(d.data.required){ }} lay-verify="required" {{# } }} {{#if(d.data.disabled){ }} disabled {{# } }} >',
								'<option value="">-- 全部 --</option>',
							'</select>',
						'</div>',
						'{{# } }}',
						
						'{{# if(d.data.msg){ }}',
						 '<div class="layui-form-mid layui-word-aux">{{ d.data.msg }}</div>',
						 '{{# } }}',
					'</div>'
				].join("");
	//选项模板
	var TPL_OPTION = [
	                '<option value="">-- 全部 --</option>',
	                '{{# layui.each(d.data,function(index,item){ }}',
	                	'<option class="ajaxOption" value="{{ item[d.options.filed.regionId] }}" {{#if(d.options.selectedArr.length>0 && ($.inArray(item[d.options.filed.regionId], d.options.selectedArr)!=-1)){ }} selected {{# } }} >{{ item[d.options.filed.regionName] }}</option>',
	                '{{# }) }}'
	                ].join("");
	
	
	//构造器
	var Class = function(options){
		var that = this;
	    that.index = ++citySelect.index;
	    that.config = $.extend(true,{}, that.config, citySelect.config, options);
	    that.render();
	};
	
	//核心入口
	citySelect.render = function(options){
	    var inst = new Class(options);
	    return thisSelect.call(inst);
	};
    //获取选中值
	citySelect.values = function(id){
		return citySelect.cache[id]["values"];		//返回缓存中的选中值
    };
    //设置禁用/启用
    citySelect.disabled = function(id,flag){
    	$("."+id+"_selectCity").attr("disabled",flag);
    };
    //重载
    thisSelect.config = {};
    citySelect.reload = function(id,options){
    	var config = thisSelect.config[id];
        if(!config) return hint.error('The ID option was not found in the citySelect instance');
        return citySelect.render($.extend(true, {}, config, options));
    };
	
	//默认配置
	Class.prototype.config = {
		lableName : "行政区域",
		required : false,		//是否必选
		search : true,			//是否搜索
		msg:null,				//默认附加信息
		selectedArr : [],		//默认选中数组
		disabled:false,			//禁用 默认不禁用
		filed:{
	    	area:true,				//默认启用区
	    	regionId:'regionId',	//默认字段id名
	    	regionName:'regionName',//默认字段name名
	    	provinceName: "province",	//默认省份名称
			cityName : "city",			//默认城市名称
			areaName : "area",			//默认区县名称
	    },
		
	};
	
	//加载容器
	Class.prototype.render = function(){
		 var that = this;
		 var options = that.config;	
		 options.elem = $(options.elem);
		 var othis = options.elem; 
		 if(!options.elem[0]) return that;		//如果元素不存在
	     
		 //请求参数的自定义格式
	     options.request = $.extend({
	    	 //pageName: 'page',
	    	 //limitName: 'limit'
	     }, options.request);
	    
	    //响应数据的自定义格式
	    options.response = $.extend({
	    	statusName: 'code',
	    	statusCode: 0,
	    	msgName: 'msg',
	    	dataName: 'data',
	    }, options.response);
		 
		 //主容器
		 var reElem = that.elem = $(laytpl(TPL_MAIN).render({
		      //VIEW_CLASS: ELEM_VIEW,
		      data: options,
		      index: that.index //索引
		 }));
		 othis.html(reElem);			//生成主元素
		 that.pullData();				//渲染初始
		 that.formFilter();				//监听选择
		 
	};
	
	//监听表单
	Class.prototype.formFilter = function(){
		var that = this;
		var options = that.config;
		that.key = options.id || options.index;
		
		//监听省
		form.on('select(province'+that.index+')', function(data){
			var cityDom = $("#citySelect_"+ options.filed.cityName + that.index);	//市
			var areaDom = $("#citySelect_"+ options.filed.areaName + that.index);	//区
			that.chearDom(cityDom);								//清理市
			that.chearDom(areaDom);								//清理区
			citySelect.cache[that.key]["values"][0] = data.value;	//存入缓存
			citySelect.cache[that.key]["values"][1] = "";			//清理市级缓存
			citySelect.cache[that.key]["values"][2] = "";			//清理区级缓存
			if(data.value!=""){
				if(options.data){
					that.localData(cityDom, data.value);				//本地渲染市级			
				}else{
					that.ajaxData(cityDom,data.value);					//ajax渲染市
				}
			}
		}); 
		//监听市
		form.on('select(city'+that.index+')', function(data){
			var areaDom = $("#citySelect_"+ options.filed.areaName + that.index);	//区
			that.chearDom(areaDom);									//清理区
			citySelect.cache[that.key]["values"][1] = data.value;
			citySelect.cache[that.key]["values"][2] = "";
			if(data.value!=""){
				if(options.data){
					that.localData(areaDom, data.value);				//本地渲染市级			
				}else{
					that.ajaxData(areaDom,data.value);					//加载区
				}
			}
		}); 
		//监听区
		form.on('select(area'+that.index+')', function(data){
			citySelect.cache[that.key]["values"][2] = data.value;
			console.log("选择区"); //得到select原始DOM对象
		}); 
		
	};
	
	//渲染数据
	Class.prototype.pullData = function(){
		var that = this;
		var options = that.config;
		var dom = $("#citySelect_"+ options.filed.provinceName + that.index);	//默认先渲染省
		that.key = options.id || options.index;
		citySelect.cache[that.key] = {values:["","",""]}; 	//记录values缓存标记
		
		if(options.data){ 		//data存在
			that.localData(dom,"000000");
		}else if(options.url){	//url存在
			that.ajaxData(dom);
		}
		
	};
	
	//data渲染数据
	Class.prototype.localData = function(dom,regionId){ 
		var that = this;
		var options = that.config;
		var regs = /^\d{2}0000$/;	//验证省id 
		var regc = /^\d{4}00$/; 	//验证市ID
		if(regionId=="000000"){
			//渲染省级
			that.renderData(options.data,dom);
		}else if(regs.test(regionId)){
			//渲染市级
			$.each(options.data,function(index,item){
				if(regionId==item[options.filed.regionId]){
					that.renderData(item.children,dom);
				}
			});
		}else if(regc.test(regionId)){
			//渲染区级
			var sId = regionId.substr(0, 2)+"0000";		//获取省级Id
			$.each(options.data,function(index,item){
				if(sId==item[options.filed.regionId]){
					$.each(item.children,function(i,it){
						if(regionId==it[options.filed.regionId]){
							that.renderData(it.children,dom);
						}
					});
				}
			});
		}
	}
	
	
	//ajax获取数据
	Class.prototype.ajaxData = function(dom,regionId){
		var that = this;
		var options = that.config;
	    var response = options.response;
	    var params = {};
	    params[options.filed.regionId] = regionId==undefined?"000000":regionId;
	    
	    //先查看缓存有没有
	    if(citySelect.cache[that.key][regionId]!=undefined ){
	    	 that.renderData(citySelect.cache[that.key][regionId],dom);
	    }else{
	    	$.ajax({
	    		type: options.method || 'get',
	    		url: options.url,
	    		data: $.extend(params, options.where),
	    		dataType: 'json',
	    		success: function(res){
	    			if(res[response.statusName] != response.statusCode){
	    				that.renderForm();
	    				typeof options.error === 'function' && options.error(res);
	    				return ;
	    			}
	    			var data = res[options.response.dataName] || [];
	    			that.renderData(data,dom);
	    			if(data.length>0){
	    				citySelect.cache[that.key][regionId] = data;			//将已经获取的数据保存缓存
	    			}
	    			options.time = (new Date().getTime() - that.startTime) + ' ms'; //耗时（接口请求+视图渲染）
	    			typeof options.done === 'function' && options.done(res);
	    		}
	    	,error: function(e, m){
	    		that.renderData('<option value="">数据接口请求异常</option>',dom);
	    		typeof options.error === 'function' && options.error(res, e,m);
	    	}
	    	});
	    }
	    
	};
	
	//数据渲染
	Class.prototype.renderData = function(data,dom){
		var that = this,
		options = that.config;
		var selectedArr = options.selectedArr;		//获取默认选中数组
		
		if(typeof data === 'string'){
			$(dom).html(data);
		}else{
			//渲染选择项
			$(dom).html( $(laytpl(TPL_OPTION).render({
				data: data,
				options:options,
				index: that.index //索引
			})));
			that.renderForm('select');
		}
		//设置默认选中
		var v = $(dom).val();
		if(v!=""&&selectedArr.length>0){
			for (var i = 0; i < selectedArr.length; i++) {
				if(v == selectedArr[i] && i<3){
					citySelect.cache[that.key]["values"][i] = v;		//保存到选中缓存
					that.config.selectedArr[i] = "";					//清除默认选择数组
					if(i==0){
						var dom = $("#citySelect_"+ options.filed.cityName + that.index);
						if(options.data){
							that.localData(dom, v);		//本地渲染市级			
						}else{
							that.ajaxData(dom, v);		//ajax渲染市级
						}
					}else if(i==1&&options.filed.area){
						var dom = $("#citySelect_"+ options.filed.areaName + that.index);
						if(options.data){
							that.localData(dom, v);		//本地渲染区级			
						}else{
							that.ajaxData(dom, v);		//ajax渲染区级
						}
					}
				}
			}
		}
	};

	
	//渲染表单
	Class.prototype.renderForm = function(type){
		form.render(type);
	};
	
	//清空select
	Class.prototype.chearDom = function(dom){
		var that = this;
		$(dom).html('');
		$(dom).append('<option value="">-- 全部 --</option>');
		that.renderForm('select');
	};
	
	//暴露模块
	exports(MOD_NAME, citySelect);
});



