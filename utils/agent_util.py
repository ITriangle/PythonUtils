#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import
from __future__ import division

import hashlib
import sys
import logging
import traceback

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause
from sqlalchemy.exc import IntegrityError

from pyhive import hive

import requests


reload(sys)
sys.setdefaultencoding("utf-8")


#logger = logging.getLogger("sync_pg2hive")


def make_md5(x):
    return hashlib.md5(str(x).strip()).hexdigest()





class NeedSqlAlchemyTextObject(Exception):
    def __init__(self, message):
        super(NeedSqlAlchemyTextObject, self).__init__("{!s} is not a valid SQLAlchemy text object!".format(message))


class PGAgent(object):
    def __init__(self, db_uri):
        self.eng = create_engine(db_uri, pool_size=20, pool_recycle=300)


    def execute_raw_query(self, sql_text, params=None, use_eng=None):
        if not isinstance(sql_text, TextClause):
            raise NeedSqlAlchemyTextObject(sql_text)

        use_eng = self.eng if use_eng is None else use_eng

        with use_eng.connect() as conn:
            try:
                if params is not None and isinstance(params, dict):
                    qrs = conn.execute(sql_text, params)
                else:
                    qrs = conn.execute(sql_text)
                return qrs
            except:
                rootLogger.error("SQL: {}".format(sql_text))
                rootLogger.error(traceback.format_exc())
                raise
                sys.exit(1)


    def get_table_column_define(self, schemaname, tablename):
        rootLogger.debug("PG get define of columns in table: {}.{}".format(schemaname, tablename))
        rspxy = self.execute_raw_query(text("""SELECT ordinal_position
                                                    , column_name
                                                    , CASE WHEN data_type in ('character varying', 'text')
                                                           THEN 'varchar'
                                                           WHEN data_type = 'double precision'
                                                           THEN 'double'
                                                           ELSE LOWER(data_type)
                                                      END                AS column_type
                                                    , CASE WHEN data_type = 'ARRAY'
                                                            AND udt_name = '_int4'
                                                           THEN 'integer'
                                                           WHEN data_type = 'ARRAY'
                                                            AND udt_name in ('_varchar', '_text')
                                                           THEN 'varchar'
                                                           WHEN data_type = 'ARRAY'
                                                            AND udt_name = '_float8'
                                                           THEN 'double'
                                                           ELSE ''
                                                      END                AS  element_type
                                                    , col_description('{v_fulltablename}'::regclass,
                                                                      ordinal_position)  AS desc
                                                    , obj_description('{v_fulltablename}'::regclass,
                                                                      'pg_class')        AS table_comment
                                                    , (SELECT data_type = 'ARRAY'
                                                         FROM information_schema.columns
                                                        WHERE table_schema = :v_schemaname
                                                          AND table_name = :v_tablename
                                                          AND data_type = 'ARRAY'
                                                        LIMIT 1
                                                      )                  AS if_contain_array_column
                                                 FROM information_schema.columns
                                                WHERE table_schema = :v_schemaname
                                                  AND table_name = :v_tablename
                                             ORDER BY ordinal_position ASC """.format(v_fulltablename="{}.{}".format(schemaname.strip(),
                                                                               tablename.strip()))),
                                            {"v_schemaname": schemaname.strip(),
                                             "v_tablename": tablename.strip()})

        rs = rspxy.fetchall()
        rs_list = []
        if rs is not None:
            for each_row in rs:
                rs_list.append((int(each_row[0]),
                                each_row[1],
                                each_row[2],
                                each_row[3],
                                each_row[4],
                                each_row[5],
                                True if each_row[6] is not None else False))

        return rs_list


    def get_all_vals_of_partkey(self, schemaname, tablename, part_cond):
        rootLogger.debug("PG get all values of table {}.{}".format(schemaname, tablename))
        rspxy = self.execute_raw_query(text("""SELECT DISTINCT {col_cond}
                                                 FROM {schemaname}.{tablename}
                                            """.format(col_cond=part_cond,
                                                       schemaname=schemaname,
                                                       tablename=tablename)))
        return rspxy.fetchall()


    def get_table_query_sql(self, schemaname, tablename, part_key=None, part_val=None):
        rootLogger.debug("PG get query sql for table: {}.{}".format(schemaname, tablename))
        if part_key is None or (isinstance(part_key, str) and part_key == ''):
            rspxy = self.execute_raw_query(text(""" SELECT 'SELECT '|| tmp.col_str ||' FROM {v_fulltablename} '
                                                      FROM (SELECT ordinal_position       AS idx
                                                                 , string_agg(column_name, ',')
                                                                   OVER(ORDER BY ordinal_position ASC) AS col_str
                                                                 , max(ordinal_position)
                                                                   OVER()                 AS max_idx
                                                              FROM information_schema.columns
                                                             WHERE table_schema = :v_schemaname
                                                               AND table_name = :v_tablename
                                                           ) tmp
                                                     WHERE tmp.idx = tmp.max_idx """.format(v_fulltablename="{}.{}".format(schemaname.strip(),
                                                                                                                           tablename.strip()))),
                                                {"v_schemaname": schemaname.strip(),
                                                 "v_tablename": tablename.strip()})
        else:
            if part_val is None or (isinstance(part_val, str) and part_val.strip() == ''):
                raise ValueError("part_val cannot be None when part_key is not None!!")

            rootLogger.debug("PG query sql get data for partition key [{}] in value [{!s}]".format(part_key, part_val))
            if isinstance(part_val, str) or isinstance(part_val, unicode):
                fillup_part_val = "''{}''".format(part_val)
            else:
                fillup_part_val = part_val
            rspxy = self.execute_raw_query(text(""" SELECT 'SELECT '||tmp.col_str||' FROM {v_fulltablename} '
                                                        || ' WHERE {part_key} = {v_part_value} '
                                                      FROM (SELECT ordinal_position       AS idx
                                                                 , string_agg(column_name, ',')
                                                                   OVER(ORDER BY ordinal_position ASC) AS col_str
                                                                 , max(ordinal_position)
                                                                   OVER()                 AS max_idx
                                                              FROM information_schema.columns
                                                             WHERE table_schema = :v_schemaname
                                                               AND table_name = :v_tablename
                                                               AND column_name != :v_part_key
                                                           ) tmp
                                                     WHERE tmp.idx = tmp.max_idx """.format(part_key=part_key.strip(),
                                                                                            v_fulltablename="{}.{}".format(schemaname.strip(),
                                                                                                                           tablename.strip()),
                                                                                            v_part_value=fillup_part_val)),
                                                {"v_schemaname": schemaname.strip(),
                                                 "v_tablename": tablename.strip(),
                                                 "v_part_key": part_key.strip()})

        rs = rspxy.fetchone()
        if rs is not None:
            return rs[0]
        else:
            return None


class HiveAgent(object):
    def __init__(self,auth,username,password, hive_database, hive_host, hive_port=10000):
        self.host=hive_host
        self.port=hive_port
        self.database=hive_database

        self.auth=auth
        self.username=username
        self.password=password


    def execute(self, hql):
        rootLogger.debug("Hive execute hql: {}".format(hql))
        conn = hive.connect(host=self.host,
                            port=self.port,
                            database=self.database,
                            auth=self.auth,
                            username=self.username,
                            password=self.password)
        cur = conn.cursor()
        try:
            cur.execute(hql.strip())
        except:
            rootLogger.error(traceback.format_exc())
        finally:
            cur.close()
            conn.close()


class HDFSAgent(object):
    def __init__(self, nm_host, nm_port=50070, hdfsuser="hdfs"):
        self.host = nm_host
        self.port = nm_port
        self.user = hdfsuser

    def _make_full_url(self, hdfs_path, operation, options=None):
        options = '' if options is None else options.strip()
        return "http://{host}:{port}/webhdfs/v1{path}?user.name={as_user}&op={operation}{opts}".format(host=self.host,
                                                                                                 port=self.port,
                                                                                                 path=hdfs_path.strip(),
                                                                                                 as_user=self.user,
                                                                                                 operation=operation.strip().upper(),
                                                                                                 opts=options)

    def ensure_hdfs_directory(self, hdfs_abs_path):
        query_url = self._make_full_url(hdfs_abs_path, "GETFILESTATUS")
        query_resp = requests.get(query_url)

        if query_resp.status_code == 200:
            rootLogger.debug("hdfs directory [{}] already exists!".format(hdfs_abs_path))
        elif query_resp.status_code == 404:
            rootLogger.debug("hdfs directory [{}] not found, create it.".format(hdfs_abs_path))
            mkdir_url = self._make_full_url(hdfs_abs_path, "MKDIRS")
            mkdir_resp = requests.put(mkdir_url)

            if mkdir_resp.status_code == 200:
                rootLogger.debug("SUCCEE to create hdfs directory: {}".format(hdfs_abs_path))
            else:
                rootLogger.error("FAIL to create hdfs directory: {}".format(hdfs_abs_path))
                rootLogger.error(mkdir_resp.text)
                mkdir_resp.raise_for_status()
        else:
            rootLogger.error("Unexptected status: {!s}".format(query_resp.status_code))
            rootLogger.error(query_resp.text)
            query_resp.raise_for_status()
