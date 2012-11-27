from pyactiveresource.activeresource import ActiveResource


class Issue(ActiveResource):
    pass
    
class Project(ActiveResource):
    pass

class Query(ActiveResource):
    pass

class User(ActiveResource):
    pass

class Group(ActiveResource):
    pass

class Tracker(ActiveResource):
    pass

class IssueStatus(ActiveResource):
    pass

class Redmine:
    
    def __init__(self,url,api_key):
    
        self.__site = "http://%(api_key)s@%(url)s" % locals()

    def Issue(self):
        i=Issue
        i.site=self.__site
        return i
        
    def Project(self):
        p=Project
        p.site=self.__site
        return p
        
    def User(self):
        u=User
        u.site=self.__site
        return u
        
    def Group(self):
        g=Group
        g.site=self.__site
        return g
    
    def Query(self):
        q=Query
        q.site=self.__site
        return q
        
    def Tracker(self):
        t=Tracker
        t.site=self.__site
        return t
        
    def IssueStatus(self):
        s=IssueStatus
        s.site=self.__site
        return s
        
        