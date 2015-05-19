调用方式：

```python
opCodes = ["createGroup", "addDeviceToGroup", "addStorageConsumer", "requestExtraStorage", "releaseExtraStorage", "getInfo", "getUsageInfo"]
```

```sh
python main.py opCode argument(s)
```

存储服务器包括：

```json
{
    "192.168.3.192":"/dev/loop0",
    "192.168.3.192":"/dev/loop1",
    "192.168.3.167":"/dev/loop0",
    "192.168.3.167":"/dev/loop1"
}
```

应用服务器包括：

```json
["192.168.3.62","192.168.3.161"]
```

测试方式：

测试中包括5步，可以通过设定stepCode，指定测试程序执行的起始点。

```sh
python main.py testAll 1
```

自动部署：

```sh
# 打通各个节点(无密码ssh执行命令)
python main.py breakAll
# 初始部署
python main.py deployALL 192.168.3.162
# 全部更新
python main.py updateAll
```