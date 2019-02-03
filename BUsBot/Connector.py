class Connector():
    """decided which module to call based on mode input"""
    
    def __init__(self, mode, station=None):
        self.mode = mode

    
    def mode_catcher(self):
        
        if self.mode == "next":
            return self.get_next()
        
        elif self.mode == "schedule":
            return self.get_schedule()
        
        else:
            return self.get_news()

    def get_next(self):
        # call next_bus module
        return "next"

    def get_schedule(self):
        # call schedule module
        ret = "sch"
        return ret
    
    def get_news(self):
        #call news module
        return "news"

if __name__ == '__main__':
    # x = ""
    result = Connector("schedule")
    print(result.mode_catcher())
    