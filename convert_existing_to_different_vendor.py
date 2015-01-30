#!/usr/bin/env python
import getopt
import sys

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_utils import functions as sqlalclhemy_util_functions

def make_session(connection_string):
    engine = create_engine(connection_string, echo=False, convert_unicode=True)
    Session = sessionmaker(bind=engine)
    return Session(), engine

def pull_data(from_db, to_db, tables='*'):

    source, sengine = make_session(from_db)
    smeta = MetaData(bind=sengine)
    destination, dengine = make_session(to_db)
    
    if not sqlalclhemy_util_functions.database_exists(to_db):
        sqlalclhemy_util_functions.create_database(dengine.url)

    # handle tall tables
    if len(tables) == 1 and tables[0] == '*':
        smeta.reflect()
        tables = smeta.sorted_tables
        tables = [table.name for table in tables]

    for table_name in tables:
        print 'Processing', table_name
        print 'Pulling schema from source server'
        table = Table(table_name, smeta, autoload=True)
        #Ugly hack for varchar field without
        #for c in table.columns:
        #    if 'VARCHAR' in str(c.type) and c.type.length is None:
        #        c.type.lengty = 50
        print 'Creating table on destination server'
        table.metadata.create_all(dengine)
        if table_name == 'alembic_version':
            # This table doesn't have primary key, so
            # you can't get a mapper on that. Also you can 
            # just use the stamp command to get it
            # populated.
            pass
        else:
            NewRecord = quick_mapper(table)
            columns = table.columns.keys()
            print 'Transferring records'
            for record in source.query(table).all():
                data = dict(
                    [(str(column), getattr(record, column)) for column in columns]
                )
                destination.merge(NewRecord(**data))
    print 'Committing changes'
    destination.commit()

def print_usage():
    print """
Usage: %s -f source_server -t destination_server table [table ...]
    -f, -t = driver://user[:password]@host[:port]/database

Example: %s -f oracle://someuser:PaSsWd@db1/TSH1 \\
    -t mysql://root@db2:3307/reporting table_one table_two
    
Note: To convert all tables over, use '*' as table_one argument
    """ % (sys.argv[0], sys.argv[0])

def quick_mapper(table):
    Base = declarative_base()
    class GenericMapper(Base):
        __table__ = table
    return GenericMapper

if __name__ == '__main__':
    optlist, tables = getopt.getopt(sys.argv[1:], 'f:t:')

    options = dict(optlist)
    if '-f' not in options or '-t' not in options or not tables:
        print_usage()
        raise SystemExit, 1
    
    print tables

    pull_data(
        options['-f'],
        options['-t'],
        tables,
    )