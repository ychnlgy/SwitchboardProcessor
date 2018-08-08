from project.mainmethod import mainmethod

def test_main():

    f = "foo"
    
    @mainmethod(f)
    def main1(DIR, args):
        return
    
    try:
        @mainmethod(f)
        def main2(DIR, args):
            raise Exception
    except Exception:
        pass
