import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_wikipedia_current_events():
    """
    Fetches current events from Wikipedia and formats them for email.
    """
    url = "https://en.wikipedia.org/wiki/Portal:Current_events"
    
    try:
        # Fetch the page
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the current events section
        events_div = soup.find('div', {'id': 'mw-content-text'})
        
        # Get today's date for the email header
        today = datetime.now().strftime("%B %d, %Y")
        
        # Build email text
        email_text = f"Current Events - {today}\n"
        email_text += "=" * 50 + "\n\n"
        email_text += "Source: Wikipedia Portal:Current Events\n\n"
        
        # Find all event entries (typically in ul/li elements)
        event_sections = events_div.find_all('div', class_='current-events-content')
        
        if event_sections:
            for section in event_sections[:1]:  # Get most recent
                # Find category headers
                categories = section.find_all(['h2', 'h3', 'h4'])
                lists = section.find_all('ul')
                
                for i, ul in enumerate(lists):
                    # Try to find associated header
                    header = None
                    for cat in categories:
                        if cat.find_next('ul') == ul:
                            header = cat.get_text().strip()
                            break
                    
                    if header:
                        email_text += f"\n{header}\n"
                        email_text += "-" * len(header) + "\n"
                    
                    # Get list items
                    items = ul.find_all('li', recursive=False)
                    for item in items:
                        # Clean text (remove references, extra whitespace)
                        text = item.get_text()
                        text = ' '.join(text.split())  # Normalize whitespace
                        email_text += f"• {text}\n"
        
        email_text += "\n" + "=" * 50 + "\n"
        email_text += f"Retrieved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        return email_text
    
    except Exception as e:
        return f"Error fetching current events: {str(e)}"

if __name__ == "__main__":
    # Get and print the events
    events_text = get_wikipedia_current_events()
    print(events_text)
    
    # Optionally save to file
    with open("current_events.txt", "w", encoding="utf-8") as f:
        f.write(events_text)
    print("\n✓ Events saved to 'current_events.txt'")