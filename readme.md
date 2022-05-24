# iHome每月镜像备份脚本

> 由于iHome每月初即“清空”上个月的诉求显示，因此可以通过该脚本将每月诉求列表及详细信息进行镜像备份
>
> 2022年5月24日

## 程序说明

修改`main.py`文件中的`cookie`信息，随后运行即可。脚本获得的数据保存在当前文件夹下面的以时间命名的文件夹中。

使用的非原生库为`requests`和`lxml`，用过`pip install`即可快速安装。

欢迎其他开发人员参与开发、更新或优化。

# 每月镜像查看

本人会尽量每月底执行脚本获取数据，用户于`发行界面`下载最新的压缩包。

解压并双击`index.html`即可查看列表，点击诉求链接即可查看详情。