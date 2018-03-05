#!/usr/bin/env python
# coding=utf-8

from kazoo.client import KazooClient
import os, json
import portalocker

root_dir = os.path.dirname(os.path.abspath(__file__))

APP_ALERT_MAIL_ZNODE_PATH = '/app_alert_mail'
file_path = os.path.join(root_dir, 'app_alert_mail.json')


def zookeeper_alert_mail():
    '''
    description: zookeeper 应用内报警邮件目标地址
                 zookeeper 上的配置信息如果有更新的话保存到本地JSON文件
    return: dict zookeeper /app_alert_mail/ 路径下叶子节点的数据
    '''
    app_alert_mail = APP_ALERT_MAIL_ZNODE_PATH
    alert_mails = {}
    print file_path

    with open(file_path, 'w+') as f:
        portalocker.lock(f, portalocker.LOCK_EX)
        znode_data = f.readline().strip()
        if znode_data:
            try:
                alert_mails = json.loads(znode_data)
            except Exception:
                alert_mails = {}
        zk = KazooClient(hosts='192.168.1.84:2181,192.168.1.85:2181,192.168.1.86:2181')
        zk.start()
        if zk.exists(app_alert_mail):
            leaf_node_datas(zk, app_alert_mail, alert_mails)
        zk.stop()
        f.seek(0)
        f.write(json.dumps(alert_mails))
        f.flush()
        portalocker.unlock(f)
    return alert_mails


def leaf_node_datas(zookeeper, znode_path, alert_mails):
    zk = zookeeper
    if zk.exists(znode_path):
        data, stat = zk.get(znode_path)
        if stat.children_count == 0:
            if data:
                key_values = data.strip().split(";")
                for item in key_values:
                    value = item.split('=')
                    if len(value) > 1:
                        vs = value[1]
                        alert_mails[znode_path] = vs.replace("\"", "").split(",")
        else:
            znodes = zk.get_children(znode_path)
            for znode in znodes:
                leaf_node_datas(zk, os.path.join(znode_path, znode), alert_mails)


if __name__ == '__main__':
    alert_mails= zookeeper_alert_mail()
    to_people = alert_mails.get('/app_alert_mail/database/postgresql/sync/dev2his/to')
    cc_people_success = alert_mails.get('/app_alert_mail/database/postgresql/sync/dev2his/cc')
    cc_people_fail = alert_mails.get('/app_alert_mail/database/postgresql/sync/dev2his/fcc')