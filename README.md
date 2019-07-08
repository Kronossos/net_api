# net_scrapper

An application for downloading text and images from the website.
    
    Commands:
        -test: run test
            example: > test
            
        -help: show help
            example: > help
        
        -update url: download html code of given site. url in format PROTOCOL://HOST/PATH.
            example: > url https://en.wikipedia.org/wiki/Main_Page
        
        -img [save_path]: save all the images for given site. Default path is site name.
            example: > img my/path/
        
        -text [save_path]: save the text of the page for given site. Default path is site name.
            example: > text my/path/
            
        -exit: close app
            example: > exit
