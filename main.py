import functools


class lazy_attribute:
    """A property that caches itself to the class object

    Returns:
        _type_: _description_
    """
    def __init__(self,func):
        functools.update_wrapper(self.func,updated=[])
        self.generic=func

    def __get__(self,obj,cls):
        value=self.getter(cls)
        setattr(cls,self.__name__,value)
        return value

class Glass:

    @lazy_attribute
    def _global_config(cls):
        cfg = ConfigDict()
        cfg.meta_set("catchall","validate",bool)
        return cfg
    
    def __init__(self,**kwargs):
        self.config =self._global_config._make_overlay()