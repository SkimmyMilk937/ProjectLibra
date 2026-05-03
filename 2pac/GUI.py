
from pathlib import Path
import PySimpleGUI as sg
from RedditData import reddit_data
from Reddit import reddit_interface as reddit

sg.theme("DarkGrey16")



libra_logo = reddit_data.resolve_path("Libra_logof.ico")
reddit_logo = reddit_data.resolve_path("reddit_logoF.png")
youtube_logo = reddit_data.resolve_path("youtube_logo.png")
scrape_logo = reddit_data.resolve_path("scrape_logof.png")
send_logo = reddit_data.resolve_path("send_logof.png")

Scrapeframe_numPosts = sg.Frame("Number of posts to find per subreddit (current conditions: \'new\'[to be editable] + only unique \'unstickied\' posts )", layout=[[sg.Input(default_text = 3, key="-numPostsToFind-", font=("Bebas Neue", 12), expand_x = True, expand_y=True, tooltip="[be conscious of potential rate limits]")]])
scrapeFrame = sg.Frame("Scrape", layout=[[Scrapeframe_numPosts]])
scrape_tab_layout = [   
                        [scrapeFrame], [sg.Output(key="-scrape_output-", font=("Bebas Neue", 12), expand_x = True, expand_y=True, size=(100, 3))],
                        [sg.Button("Scrape", key="-scrape_button-", font=("Bebas Neue", 25), expand_x = True, expand_y=True, pad=(100, 20))]
                    ]
responseSpin = sg.Spin(values="", key="-post_options-", font=("Bebas Neue", 12), expand_x = True, expand_y=True, enable_events=True)
response_tab_layout = [[sg.Text("Response", font=("Bebas Neue", 25), expand_x = True, expand_y=True), responseSpin],
                       [sg.Multiline("", key="-responses_interactive-", font=("Bebas Neue", 12), expand_x = True, expand_y=True, size=(100, 3)), sg.Output(key="-post_output-", font=("Bebas Neue", 12), expand_x = True, expand_y=True, size=(100, 3))],
                       [sg.Button("Save to default", key="-update_response-", font=("Bebas Neue", 25), expand_x = True, expand_y=True, pad=(100, 20)), sg.Button("Send", key="-send_response-", font=("Bebas Neue", 25), expand_x = True, expand_y=True, pad=(100, 20))]
                       ]

subreddits_tab_layout = [[sg.Text("Subreddits", font=("Bebas Neue", 25), expand_x = True, expand_y=True)],
                         [sg.Multiline("", key="-subreddits_interactive-", font=("Bebas Neue", 12), expand_x = True, expand_y=True, size=(100, 3))],
                         [sg.Button("Update", key="-update_subreddits-", font=("Bebas Neue", 25), expand_x = True, expand_y=True, pad=(100, 20))]
                        ]

scrape_tab = sg.Tab( title="Scrape", layout=scrape_tab_layout, background_color="red", key="-reddit_scrape_tab-",
                    image_source=scrape_logo, font=("Bebas Neue"), expand_x=True, expand_y=True, tooltip="Scrape posts from subreddits",)
response_tab = sg.Tab(title="Response", layout=response_tab_layout, background_color="red", key="-reddit_response_tab-",
                      image_source=send_logo, font=("Bebas Neue"), expand_x=True, expand_y=True, tooltip="Modify and send responses")
subreddits_tab = sg.Tab(title="Subreddits", layout=subreddits_tab_layout, background_color="red", key="-reddit_subreddits_tab-",
                        image_source=send_logo, font=("Bebas Neue"), expand_x=True, expand_y=True, tooltip="Modify subreddits to parse/interact with")

reddit_tabs_group = sg.TabGroup(layout=[[subreddits_tab], 
                                  [scrape_tab],
                                  [response_tab]], 
                          key="-reddit_tabs-", tab_location="left", selected_title_color="yellow", selected_background_color="black", 
                          title_color="white", background_color="black", expand_x=True, expand_y=True
                          )


Reddit_layout = [[sg.Text("Reddit Actions", font=("Bebas Neue", 25))], [reddit_tabs_group]]
Youtube_layout = [[sg.Text("Youtube")]]

reddit_bar_tab = sg.Tab(title="Reddit", layout=Reddit_layout, background_color="red", key="-Reddit_layoutTab-",
                        image_source=reddit_logo, font=("Bebas Neue"), expand_x=True, expand_y=True)
youtube_bar_tab = sg.Tab(title="Youtube", layout=Youtube_layout, background_color="blue", key="-Youtube_layoutTab-",
                         image_source=youtube_logo, font=("Bebas Neue"), expand_x=True, expand_y=True)

platform_tabs_group = sg.TabGroup(layout=[[reddit_bar_tab, youtube_bar_tab]], key="-platform_tabs-", selected_title_color="yellow",
                                  selected_background_color="black", title_color="white", expand_x=True, expand_y=True)

layout = [[sg.Text("Platform")], 
          [platform_tabs_group], 
          [sg.Text("Done")]
]

# '''size=(800, 600),'''
window = sg.Window(title="Libra", layout=layout, resizable=True, use_custom_titlebar=False, finalize=True, auto_size_text=True,auto_size_buttons=
True, margins=(0,0), element_padding=(0,0), icon=libra_logo)
#sg.SystemTray(menu=['UNUSED', ['My', 'Simple', '---', 'Menu', 'Exit']], filename=libra_logo)













reddit = reddit(window)

for x in reddit.myRedditData.subs:
    window["-subreddits_interactive-"].print(x)

window["-responses_interactive-"].update(reddit.myRedditData.message)

currentPostIdx = 0
try:
    while True:
        
        event, values = window.read()
        if(event == "Exit" or event == sg.WIN_CLOSED):
            break
        if(event == "-Exit-"):
            break
        
        if(event == "-scrape_button-"):
            reddit.scrape(window["-numPostsToFind-"].get())
            out = []
            for x in reddit.newlyScraped:
                window["-scrape_output-"].print(x.title)
                out.append(x.title)
            window["-post_options-"].update(value = out[0], values=out)
            window["-post_output-"].update(reddit.newlyScraped[0].selftext)
            
            #window["-scrape_output-"].update(reddit.getTitles())
            #window.add_row(sg.Text("Scraping..."))
            
        if(event == "-update_subreddits-"):
            reddit.updateSubreddits(window["-subreddits_interactive-"].get().splitlines())
            out_sub = ""

            for x in (window["-subreddits_interactive-"].get()):
                if(x != "\'" or x != "\"" or x != "[" or x != "]" or x != "\n" or x != "\\"):
                    out_sub += x
                if(x == ","):
                    window["-subreddits_interactive-"].print(out_sub)
                    out_sub = ""
        
        if(event == "-post_options-"):
            idx = 0
            for x in reddit.newlyScraped:
                if(x.title == window["-post_options-"].get()):
                    break
                idx += 1
            print(idx) 
            window["-post_output-"].update(reddit.newlyScraped[idx].selftext)
            currentPostIdx = idx
            
        if(event == "-update_response-"):
            reddit.updateMessage(window["-responses_interactive-"])
        
        if(event == "-send_response-"):
            reddit.newlyScraped[currentPostIdx].reply(reddit.myRedditData.message)
except Exception as e:
    print(e)
        



    
    
window.close()