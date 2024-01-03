class AdditionalParameters:
    def add_parameters(self, window_creator, loader, saver):
        window_creator.add_tab_creator(self.create_tab)
        self.add_applyers(loader)
        self.add_savers(saver)
    
    @classmethod
    def is_active(cls, config):
        return True
    
    def create_tab(self):
        raise NotImplementedError()
    
    def add_applyers(self, loader):
        raise NotImplementedError()

    def add_savers(self, saver):
        raise NotImplementedError()