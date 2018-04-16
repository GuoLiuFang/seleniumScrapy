date +"%F %T"
echo "职位详情开始执行"
                rm -rf jobDetailsDir;mkdir jobDetailsDir
		scrapy crawl jobDetails -astartid="${1}" -astopid="${2}" -ahost="${3}" -s JOBDIR="`pwd`/jobDetailsDir" -o "job51-${1}-${2}".jl
		cat "job51-${1}-${2}".jl >> result.jl
date +"%F %T"
echo "职位详情执行结束"
