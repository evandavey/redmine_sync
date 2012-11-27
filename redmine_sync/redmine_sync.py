#!/usr/bin/env python


__title__="REDMINE SYNC"
gap=int(len(__title__))
spacer=60
__description__="""

%s %s %s
A script to sync redmine issues to a csv.

Column help

* ID
    A - for new entry
    <id>E - to edit
    <id>D - to delete

* Project - use the identifier

* Status - use the status name

* Tracker - use the tracker name

* Priority - use the priority id (have not worked out enumerations API)

* Assigned_to - use login for users, name for groups

%s
""" % (spacer/2*"*",__title__,spacer/2*"*",(spacer+gap+2)*"*")


from redmine import Redmine
import os,csv,sys
from datetime import *
import logging
import argparse
from argparse import RawTextHelpFormatter

# Importing pyactiveresource
from pyactiveresource.activeresource import ActiveResource

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter
formatter = logging.Formatter('%(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

headers = ['id','subject','project','status','assigned_to','tracker','priority','last_sync']

global r



def find_user_or_group_login(uid):
    global r
    
    try: 
        return r.User().find(uid).login
    except:
        return r.Group().find(uid).name

def find_user_id(login):
    global r
    
    users=r.User().find()
    
    for u in users:
        if u.login.lower() == login.lower():
            return int(u.id)
            
    groups=r.Group().find()
    
    for g in groups:
        if g.name.lower() == login.lower():
            return int(g.id)
            
    return None

def find_status_id(status):
    global r
    states=r.IssueStatus().find()

    for s in states:
        if s.name.lower() == status.lower():
            return int(s.id)

    return None

def find_priority_id(priority):
    global r
    priorities=r.IssueStatus().find()

    for p in priorities:
        if p.name.lower() == priority.lower():
            return int(p.id)

    return None

def find_project_id(identifier):
    global r
    projs=r.Project().find()

    for p in projs:
        if p.identifier.lower() == identifier.lower():
            return int(p.id)

    return None

def find_tracker_id(name):
    global r
    trackers=r.Tracker().find()

    for t in trackers:
        if t.name.lower() == name.lower():
            return int(t.id)

    return None

def read_data(filename):
    data=[]
    try:
        with open(filename, 'rb') as f:
    
            reader = csv.DictReader(f,headers,dialect='excel')
            reader.next()
            for row in reader:
                data.append(row)
    except:
        pass
    return data

def write_data(filename, data):
    with open(filename, 'wb') as f:
        writer = csv.DictWriter(f,headers,dialect='excel')
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def main(argv=None):
    
    global r
    
    if argv is None:
           argv = sys.argv

   
    parser = argparse.ArgumentParser(
       description=__description__,formatter_class=RawTextHelpFormatter)

    parser.add_argument('url',metavar='URL',help="redmine url (excluding http)")
    parser.add_argument('api_key',metavar='KEY',help="user api key")

    parser.add_argument('--filename',metavar='FILE',default='tasks.csv',help="name of the csv file to sync")

    try:
       args = parser.parse_args()
    except:
       sys.exit(1)
    
    filename=args.filename
    url=args.url
    api_key=args.api_key
    
    r = Redmine(url,api_key)
    
    data=read_data(filename)

    newdata=[]
    id_hash={}
    for i in data:
    
        project_id=find_project_id(i['project'])
        assigned_to_id=find_user_id(i['assigned_to'])
        status_id=find_status_id(i['status'])
        tracker_id=find_tracker_id(i['tracker'])
    
        logger.debug("%(project_id)s,%(assigned_to_id)s,%(status_id)s,%(tracker_id)s" % locals())
    
        if i['id'][-1].upper()=='D':
            i['id']=i['id'][0:-1]
            r.Issue().delete(i['id'])
            logger.info('Deleted %s %s' % (i['id'],i['subject']))
        elif i['id'][-1].upper()=='E' or i['id'].upper()=='A':
            i_id=i['id'][0:-1]
            if project_id and tracker_id and status_id and assigned_to_id:
    
                if i['id']=='A':
                    ni=r.Issue()
                    action = "Added"
                else:
                    action ="Updated"
                    ni = r.Issue().find(i_id)

                ni.subject=i['subject']
                ni.tracker_id=tracker_id
                ni.project_id=project_id
                ni.assigned_to_id=assigned_to_id
                ni.status_id = status_id
                ni.priority_id = i['priority']
    
                ni.save()
            
        
                newdata.append({
                    'id':ni.id,
                    'subject':ni.subject,
                    'project': r.Project().find(ni.project.id).identifier,
                    'assigned_to': find_user_or_group_login(ni.assigned_to.id),
                    'status': i['status'],
                    'tracker': ni.tracker.name,
                    'priority': i['priority'],
                    'last_sync': date.today()
                })
        
                id_hash[ni.id]=True
            
                logger.info('%s %s,%s' % (action,ni.id,ni.subject))
        
            else:
                i['last_sync']=None
                newdata.append(i)
                logger.warning('Data error with record %s,%s' % (i['id'],i['subject']))

    issues=r.Issue().find()

    for ni in issues:
        try:
            i_id=id_hash[ni.id]
        except:
            
                
            newdata.append({
                    'id':ni.id,
                    'subject':ni.subject,
                    'project': r.Project().find(ni.project.id).identifier,
                    'assigned_to': find_user_or_group_login(ni.assigned_to.id),
                    'status': ni.status.name,
                    'tracker': ni.tracker.name,
                    'priority': ni.priority.id,
                    'last_sync': date.today(),
            })
            action='Syncing'
            logger.info('%s %s,%s' % (action,ni.id,ni.subject))
        
    write_data(filename,newdata)

if __name__ == "__main__":
 
    
    sys.exit(main())
