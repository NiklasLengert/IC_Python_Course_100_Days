import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
import os
from typing import List, Dict
import schedule
import time
from dotenv import load_dotenv
import feedparser
import re

class NewsDigest:
    def __init__(self, config_file="config.json"):
        load_dotenv()
        
        self.config = self.load_config(config_file)
        
        self.email_config = {
            "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
            "smtp_port": int(os.getenv("SMTP_PORT", "587")),
            "sender_email": os.getenv("SENDER_EMAIL"),
            "sender_password": os.getenv("SENDER_PASSWORD"),
            "recipient_email": os.getenv("RECIPIENT_EMAIL")
        }
        
        if not self.email_config["sender_email"]:
            self.email_config = self.config.get("email", {})
            
        self.preferences = self.config.get("preferences", {})
        
    def load_config(self, config_file: str) -> Dict:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            return self.create_default_config(config_file)
    
    def create_default_config(self, config_file: str) -> Dict:
        default_config = {
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "your_email@gmail.com",
                "sender_password": "your_app_password",
                "recipient_email": "your_email@gmail.com"
            },
            "preferences": {
                "max_articles": 15,
                "exclude_sources": [],
                "keywords": ["Deutschland", "Berlin", "KI", "Technologie", "Startup", "Klima"]
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=4)
        
        print(f"Created {config_file}")
        return default_config

    def fetch_rss_feeds(self) -> List[Dict]:
        articles = []
        
        german_rss_feeds = {
            "SPIEGEL Online": "https://www.spiegel.de/schlagzeilen/tops/index.rss",
            "ZEIT Online": "https://newsfeed.zeit.de/index",
            "FOCUS Online": "https://rss.focus.de/fol/XML/rss_folnews.xml",
            "Handelsblatt": "https://www.handelsblatt.com/contentexport/feed/schlagzeilen",
            "WELT": "https://www.welt.de/feeds/latest.rss",
            "FAZ": "https://www.faz.net/rss/aktuell/",
            "Süddeutsche": "https://www.sueddeutsche.de/news/rss"
        }
        
        rss_feeds = os.getenv("RSS_FEEDS", "").split(",") if os.getenv("RSS_FEEDS") else []
        if not rss_feeds or not rss_feeds[0]:
            feeds_to_use = german_rss_feeds
        else:
            feeds_to_use = {name: url for name, url in german_rss_feeds.items() 
                          if any(feed.strip().lower() in name.lower() for feed in rss_feeds)}
        
        for source_name, rss_url in feeds_to_use.items():
            try:
                feed = feedparser.parse(rss_url)
                
                for entry in feed.entries[:5]:
                    published_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published_date = datetime(*entry.published_parsed[:6]).isoformat() + 'Z'
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        published_date = datetime(*entry.updated_parsed[:6]).isoformat() + 'Z'
                    else:
                        published_date = datetime.now().isoformat() + 'Z'
                    
                    description = ""
                    if hasattr(entry, 'summary'):
                        description = entry.summary
                    elif hasattr(entry, 'description'):
                        description = entry.description
                    
                    description = re.sub(r'<[^>]+>', '', description)
                    description = re.sub(r'&[^;]+;', ' ', description)
                    description = ' '.join(description.split())
                    description = description.strip()
                    
                    article = {
                        "title": entry.title,
                        "description": description,
                        "url": entry.link,
                        "source": {"name": source_name},
                        "publishedAt": published_date,
                        "category": source_name
                    }
                    articles.append(article)
                
            except Exception as e:
                print(f"Error fetching RSS from {source_name}: {e}")
        
        return articles

    def filter_articles(self, articles: List[Dict]) -> List[Dict]:
        filtered = []
        exclude_sources = [s.lower() for s in self.preferences.get("exclude_sources", [])]
        max_articles = self.preferences.get("max_articles", 15)
        seen_titles = set()
        
        for article in articles:
            if not article.get("title") or not article.get("description"):
                continue
                
            if article["title"] in seen_titles:
                continue
                
            if article["source"]["name"].lower() in exclude_sources:
                continue
                
            filtered.append(article)
            seen_titles.add(article["title"])
            
            if len(filtered) >= max_articles:
                break
        
        return filtered

    def generate_html_digest(self, articles: List[Dict]) -> str:
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px; margin-bottom: 30px; }}
                .header h1 {{ margin: 0; font-size: 2.5em; }}
                .header p {{ margin: 5px 0 0 0; font-size: 1.1em; opacity: 0.9; }}
                .category {{ background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #007bff; }}
                .category h2 {{ color: #007bff; margin-top: 0; font-size: 1.4em; }}
                .article {{ background: white; border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .article h3 {{ margin-top: 0; color: #2c3e50; }}
                .article h3 a {{ color: #2c3e50; text-decoration: none; }}
                .article h3 a:hover {{ color: #007bff; }}
                .article .meta {{ color: #666; font-size: 0.9em; margin: 10px 0; }}
                .article .description {{ margin: 15px 0; }}
                .keyword-tag {{ background: #e9ecef; color: #495057; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; margin-right: 5px; }}
                .footer {{ text-align: center; margin-top: 40px; padding: 20px; color: #666; border-top: 1px solid #ddd; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Daily News Digest</h1>
                <p>{datetime.now().strftime('%A, %B %d, %Y')}</p>
            </div>
        """
        
        categories = {}
        for article in articles:
            keyword = article.get("keyword", "")
            if keyword:
                category_name = keyword.title()
            else:
                category_name = article.get("category", "News")
            
            if category_name not in categories:
                categories[category_name] = []
            categories[category_name].append(article)
        
        for category_name, cat_articles in categories.items():
            html_content += f"""
            <div class="category">
                <h2>{category_name}</h2>
            """
            
            for article in cat_articles:
                published_time = datetime.fromisoformat(article["publishedAt"].replace('Z', '+00:00'))
                time_str = published_time.strftime("%I:%M %p")
                
                keyword_tag = ""
                if article.get("keyword"):
                    keyword_tag = f'<span class="keyword-tag">{article["keyword"]}</span>'
                
                html_content += f"""
                <div class="article">
                    <h3><a href="{article['url']}" target="_blank">{article['title']}</a></h3>
                    <div class="meta">
                        {keyword_tag}
                        <strong>{article['source']['name']}</strong> • {time_str}
                    </div>
                    <div class="description">{article.get('description', '')}</div>
                </div>
                """
            
            html_content += "</div>"
        
        html_content += """
            <div class="footer">
                <p>Powered by RSS Feeds from German News Sources</p>
            </div>
        </body>
        </html>
        """
        
        return html_content

    def send_email(self, html_content: str, subject: str = None):
        if not subject:
            subject = f"Daily News Digest - {datetime.now().strftime('%B %d, %Y')}"
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.email_config["sender_email"]
        msg['To'] = self.email_config["recipient_email"]
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        try:
            with smtplib.SMTP(self.email_config["smtp_server"], self.email_config["smtp_port"]) as server:
                server.starttls()
                server.login(self.email_config["sender_email"], self.email_config["sender_password"])
                server.send_message(msg)
            return True
            
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

    def save_digest_to_file(self, html_content: str, filename: str = None):
        if not filename:
            filename = f"digest_{datetime.now().strftime('%Y%m%d')}.html"
        
        with open(filename, "w", encoding='utf-8') as f:
            f.write(html_content)

    def generate_and_send_digest(self):
        articles = self.fetch_rss_feeds()
        filtered_articles = self.filter_articles(articles)
        
        if not filtered_articles:
            print("No articles found")
            return False
        
        html_content = self.generate_html_digest(filtered_articles)
        
        self.save_digest_to_file(html_content)
        
        if self.email_config.get("sender_email") and self.email_config.get("sender_password"):
            return self.send_email(html_content)
        else:
            return True

    def schedule_daily_digest(self, time_str: str = "07:00"):
        schedule.every().day.at(time_str).do(self.generate_and_send_digest)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("Scheduler stopped")

def main():
    digest = NewsDigest()
    
    if len(os.sys.argv) > 1 and os.sys.argv[1] == "--schedule":
        schedule_time = os.getenv("SCHEDULE_TIME", "07:00")
        digest.schedule_daily_digest(schedule_time)
    else:
        digest.generate_and_send_digest()

if __name__ == "__main__":
    main()
