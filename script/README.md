
以kvm虚拟机centos6.8为模板批量克隆虚拟机（自行设定ip、主机名、hosts文件）

脚本用法:

	usage: scprit -n start_number -f kvm_old_file -s kvm_cp_number -h hostname -i ip -g gateway --name kvm_start_name

	其中: 
		-n 指定虚拟机起始序号
		-s 指定克隆虚拟机的数量
		-f 指定模板虚拟机的配置文件
		-h 指定虚拟机的主机名前缀(例如:BJ-TEST-)最终会以 前缀+IP形势组成主机名
		-i 指定虚拟机的起始ip地址
		-g 指定虚拟机的网关
		--name 指定虚拟机域名字的默认前缀(例如newtest)最终以前缀+序列号的形势组成域名称

注意:

	宿主机需要安装工具libguestfs-tools
    #yum install libguestfs-tools -y
	   
	python版本要求2.7  
