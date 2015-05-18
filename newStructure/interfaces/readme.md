1. createGroup
    - add group infomation to providerConf(key $groupName) and groupMConf(key gmIP, currentTid) in redis
2. addDeviceToGroup
    - startProvider
        + export storage at storageProvider(storageProvider.exportStorage)
        + update providerConf in redis(key $groupName{key $deviceID})
    - extendGroup
        + extend group at groupManager(groupManager.integrateStorageInit or groupManager.extendIntegrateStorage)
        + update groupMConf in redis(key devicesLoaded)
3. addStorageConsumer
    - startConsumer
        + add consumer configuration to consumerConf in redis
4. requestExtraStorage
    - requsetStorage
        + storageConsumer.requestStorage
5. releaseStorage
    - releaseStorage
        + storageConsumer.releaseStorage
6. getInfo
    - get info configuration from redis
7. getUsageInfo
    - calculate usage info based on getInfo result