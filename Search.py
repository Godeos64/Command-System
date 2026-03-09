import webbrowser

# config
PREFIX = "search"

# main execution function
def execute(args):
    # args is a list of words after the prefix
    # e.g. if input was "search hello world", args is ['hello', 'world']
    
    if not args:
        print("Please provide a search term.")
        return

    query = " ".join(args)
    search_url = f"https://duckduckgo.com/?t=ffab&q={query}&atb=v512-1&ia=web"
    
    webbrowser.open(search_url)
    print("search executed")
    return search_url