start=1
for end in `seq -f "%.0f" 100000 100000 3000000`;do
    echo "start========${start}========end=${end}"
    if [ `expr ${end} % 500000` == 0 ]
    then
        echo "这里执行阻塞任务"
		scrapy crawl zwDetails -astartid="${start}" -astopid="${end}" -ahost="localhost" -o "job51-${start}-${end}".jl
    else
        echo "这里执行后台任务。。通过后台实现并发"
		scrapy crawl zwDetails -astartid="${start}" -astopid="${end}" -ahost="localhost" -o "job51-${start}-${end}".jl &
    fi
    #最后执行更新操作
    start=$((1+${end}))
done
