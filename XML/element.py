
import time
import AXUI.logger as AXUI_logger
import AXUI.driver as driver

class TimeOutError(Exception):
    pass

class FakeUIElement(object):
    '''
    use to replace UIElement in Element without identifier
    ''' 
    def __repr__(self):
        return "Fake element, Use when there is no identifier for this element"
    
    def verify(self):
        return self

class Element(object):
    '''wrapper for UIElement
    hold infomations from app map, and provide UIElement inferface for app map
    
    Attributes:
        name:
        parent_string:
        identifier_string:
        timeout:
        children:
        parent:
        start_func:
        stop_func:
        identifier:
        
        UIElement:
        
        find:
        start:
        stop:

    '''
    #fake UI element is for elements without identifier 
    fake_UI_element = FakeUIElement()
    
    def __init__(self):
        self.LOGGER = AXUI_logger.get_logger()
        #Need init by app map
        self.name = ""
        self.parent_string = ""
        self.identifier_string = ""
        self.timeout = 0
        self.children = {}
        self.parent = None
        self.start_func = None
        self.stop_func = None
        self.identifier = None
        
        #UIElement is assigned automatically during runtime
        self.UIElement = None
        
    def __repr__(self):
        docstring = "Element for: %s\n" % self.name
        if self.UIElement is None:
            docstring += "  UIElement not init for this Element\n"
        else:
            docstring += self.UIElement.__repr__()
            
        return docstring
        
    def _verify(self):
        '''verify UIElement is valid or not
        return None if not valid
        '''
        if self.UIElement:
            self.UIElement = self.UIElement.verify()

        return self.UIElement
        
    def find(self, identifier):
        '''find element by identifier
        identifier should already be parsed
        '''
        result = self._verify()
        if result is self.fake_UI_element:
            return self.parent.find(identifier)
        elif result is None:
            self.start()
        return self.UIElement.find(identifier)
        
    def _start(self):
        if not self.start_func is None:
            self.start_func.run()

    def start(self):
        '''start and find this UIElement
        '''
        if self._verify() is None:
            #UIElement is None
            if self.start_func:
                self._start()
            else:
                if self.parent:
                    self.parent.start()
                else:
                    #root element
                    self.LOGGER.debug("Root element found: %s" % self.name)
                    self.UIElement = driver.get_UIElement().get_root()
                    
            #keep finding the element by identifier, until found or timeout
            start_time = time.time()
            while True:
                if self.identifier:
                    self.LOGGER.debug("Normal UIElement found: %s" % self.name)
                    self.UIElement = self.parent.find(self.identifier)
                else:
                    self.LOGGER.debug("Fake UI element found: %s" % self.name)
                    #if identifier is not specified, use a fake UIElement to replace UIElement
                    self.UIElement = self.fake_UI_element
                    
                if not self.UIElement is None:
                    break
                
                time.sleep(0.1)
                current_time = time.time()
                if current_time - start_time > self.timeout:
                    raise TimeOutError("time out encounter, during element:%s start" % self.name)
            
    def _stop(self):
        if not self.stop_func is None:
            self.stop_func.run()
    
    def stop(self):
        '''stop and verify this UIElement
        '''
        if not self._verify() is None:
            if self.stop_func:
                self._stop()
                
            #keep verify the element, until not found or timeout
            start_time = time.time()
            while True:
                if self.identifier:
                    self.LOGGER.debug("Normal UIElement stop: %s" % self.name)
                    self.UIElement = self._verify()
                else:
                    self.LOGGER.debug("Fake UI element stop: %s" % self.name)
                    #if identifier is not specified, use a fake UIElement to replace UIElement
                    self.UIElement = None
                
                if self.UIElement is None:
                    break 

                time.sleep(0.1)
                current_time = time.time()
                if current_time - start_time > self.timeout:
                    raise TimeOutError("time out encounter, during element:%s stop" % self.name)

    def get_child_by_name(self, name):
        '''
        get child UIElement
        '''
        return self.children[name]
            
    def __getattr__(self, name):
        if self.children.has_key(name):
            return self.get_child_by_name(name)
        else:
            self.start()
            return getattr(self.UIElement, name)


