import argparse
import gtts
from xml.dom import minidom
import xml.etree.cElementTree as et
import io # log whats used

def main(community):
    more = True
    doc = minidom.parse(community + ".xml")
    root = doc.firstChild
    tts = """"""
    
    
    r = open("YoutubeShorts/xml/titles.txt", "r")
    titles = """"""
    for x in r.readlines():
        titles = titles + x
    r.close()
    
    f = open("YoutubeShorts/xml/titles.txt", "w") 
    
    while more:  
        try:
            title = root.firstChild.getAttribute("title")
            if(title in titles ):
                print("poo")
                
                root.removeChild(root.firstChild)
                continue
            
            if(root.firstChild == None):
                break
            
            tts += root.firstChild.getAttribute("title")
            f.write(root.firstChild.getAttribute("title"))
            tts += ("\n -" + root.firstChild.firstChild.getAttribute("text"))
            print(root.removeChild(root.firstChild))
            tts += ("\n\n\n")
            
        except Exception as e:
            print(tts)
            print(e)
            print("fail")
            more = False
    f.close()

    
    
    
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = et.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help='xml file to parse and tts', required=True)
    args = parser.parse_args()

    main(args.file)