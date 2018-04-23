date +"%F %T"
echo "网址程序开始执行"
for major in  "建筑设计" "规划设计" "房地产/物业" "市政工程" "水利工程" "智能建筑/楼宇自控" "造价/预算/评估/招投标" "环境工程" "高层管理" "综合管理" "土木/工程" "现场专业人员" "园林景观" "铁路工程" "钢结构" "灯光照明" "安装" "安全/消防" "销售/市场" "工程/项目管理" "装饰装修/室内设计" "建筑表现" "城市轨道交通" "给排水/暖通/空调/电气" "展览展示" "检测/质检" "技工" "财务/会计/审计"; do
	#statements
	# echo "${major}"
	for city in  "北京" "上海" "天津" "重庆" "广东" "安徽" "山西" "贵州" "青海" "海南" "河北" "黑龙江" "甘肃" "福建" "河南" "辽宁" "内蒙古" "山东" "湖北" "吉林" "宁夏" "江苏" "江西" "湖南" "广西" "西藏" "浙江" "四川" "陕西" "云南" "新疆"; do
		#statements
		echo "前网址程序----${major}-----${city}"
		scrapy crawl scrapebuildhr -atag="${major}" -aplace="${city}"
		echo "后网址程序----${major}-----${city}"
		#scrapy crawl scrape51jobDetails -atag="${major}" -aplace="${city}" -o "job51-${major}-${city}".jl
		cat "buildhr-${major}-${city}".jl >> result.jl
	done
done
date +"%F %T"
echo "网址程序执行结束"
echo "====================================================================================================="

#date +"%F %T"
#echo "网址程序开始执行"
#for major in '安装' '装饰' '市政' '材料管理' '园林' '下料' '土建' '给排水' '建筑室内设计' '工程测试' '轨道交通' '工程造价' '建筑信息化' '水利水电' '道路与桥梁' '园林艺术' '电力' '工程管理' '石油石化' '建筑设计' '土木工程' '建筑设备工程技术'; do
#	#statements
#	# echo "${major}"
#	for city in '广东省' '江苏省' '浙江省' '四川省' '海南省' '福建省' '山东省' '江西省' '广西' '安徽省' '河北省' '河南省' '湖北省' '湖南省' '陕西省' '山西省' '黑龙江省' '辽宁省' '吉林省' '云南省' '贵州省' '甘肃省' '内蒙古' '宁夏' '西藏' '新疆' '青海省' '香港' '澳门' '台湾' '北京' '上海' '广州' '深圳' '武汉' '西安' '杭州' '南京' '成都' '重庆' '东莞' '大连' '沈阳' '苏州' '昆明' '长沙' '合肥' '宁波' '郑州' '天津' '青岛' '济南' '哈尔滨' '长春' '福州'; do
#		#statements
#		echo "前网址程序----${major}-----${city}"
#                rm -rf currentJobDir;mkdir currentJobDir
#		scrapy crawl scrape51job -atag="${major}" -aplace="${city}" -s JOBDIR="`pwd`/currentJobDir"
#		echo "后网址程序----${major}-----${city}"
#		#scrapy crawl scrape51jobDetails -atag="${major}" -aplace="${city}" -o "job51-${major}-${city}".jl
#		cat "job51-${major}-${city}".jl >> result.jl
#	done
#done
#date +"%F %T"
#echo "网址程序执行结束"
#echo "====================================================================================================="
#
#date +"%F %T"
#echo "解析公司网址程序开始执行"
#for major in '安装' '装饰' '市政' '材料管理' '园林' '下料' '土建' '给排水' '建筑室内设计' '工程测试' '轨道交通' '工程造价' '建筑信息化' '水利水电' '道路与桥梁' '园林艺术' '电力' '工程管理' '石油石化' '建筑设计' '土木工程' '建筑设备工程技术'; do
#	#statements
#	# echo "${major}"
#	for city in '广东省' '江苏省' '浙江省' '四川省' '海南省' '福建省' '山东省' '江西省' '广西' '安徽省' '河北省' '河南省' '湖北省' '湖南省' '陕西省' '山西省' '黑龙江省' '辽宁省' '吉林省' '云南省' '贵州省' '甘肃省' '内蒙古' '宁夏' '西藏' '新疆' '青海省' '香港' '澳门' '台湾' '北京' '上海' '广州' '深圳' '武汉' '西安' '杭州' '南京' '成都' '重庆' '东莞' '大连' '沈阳' '苏州' '昆明' '长沙' '合肥' '宁波' '郑州' '天津' '青岛' '济南' '哈尔滨' '长春' '福州'; do
#		#statements
#		echo "前解析公司内容-------${major}-----${city}"
#		#scrapy crawl scrape51job -atag="${major}" -aplace="${city}"
#                rm -rf currentJobDir;mkdir currentJobDir
#		scrapy crawl scrape51jobDetails -atag="${major}" -aplace="${city}" -s JOBDIR=currentJobDir -o "job51-${major}-${city}".jl
#		echo "后解析公司内容-------${major}-----${city}"
#		cat "job51-${major}-${city}".jl >> result.jl
#	done
#done
#date +"%F %T"
#echo "解析公司网址程序执行结束"
#
