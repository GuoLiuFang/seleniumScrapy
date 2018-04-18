start=1
for end in `seq 100000 100000 500000`; do
    echo "start=${start}========end=${end}"
    echo "开始使用参数"
    echo "变更参数"
    start=$((1+${end}))
done
