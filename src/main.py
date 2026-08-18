"""Main actor entry point for Houzz Professional Scraper."""
import asyncio
from apify import Actor
from datetime import datetime, timezone
from .utils import fetch, create_proxy_config
from .parser import extract_professionals, extract_next_page_url


async def main():
    """Main actor function."""
    async with Actor:
        # Get input
        actor_input = await Actor.get_input() or {}
        
        # Input parameters
        location = actor_input.get('location', 'New-York-NY')
        category = actor_input.get('category', 'architects-and-building-designers')
        max_results = actor_input.get('maxResults', 50)
        proxy_config = actor_input.get('proxyConfiguration')
        
        # Get proxy URL from Apify environment
        proxy_url = None
        if proxy_config:
            proxy_password = Actor.get_env('APIFY_PROXY_PASSWORD')
            if proxy_password:
                groups = proxy_config.get('apifyProxyGroups', ['RESIDENTIAL'])
                proxy_url = f"http://auto:{proxy_password}@proxy.apify.com:8000"
                Actor.log.info(f"Using Apify proxy with groups: {groups}")
        
        # Build start URL
        start_url = f"https://www.houzz.com/professionals/{category}/c/{location}"
        Actor.log.info(f"Starting scrape: {start_url}")
        Actor.log.info(f"Target: {max_results} professionals")
        
        scraped_count = 0
        current_url = start_url
        page_num = 1
        
        while current_url and scraped_count < max_results:
            Actor.log.info(f"Fetching page {page_num}: {current_url}")
            
            try:
                # Fetch page
                html = await fetch(current_url, proxy_url=proxy_url)
                Actor.log.info(f"Page {page_num} fetched ({len(html)} bytes)")
                
                # Parse professionals
                professionals = extract_professionals(html)
                Actor.log.info(f"Found {len(professionals)} professionals on page {page_num}")
                
                # Push each professional to dataset
                for pro in professionals:
                    if scraped_count >= max_results:
                        break
                    
                    # Add metadata
                    pro['scrapedAt'] = datetime.now(timezone.utc).isoformat()
                    pro['location'] = pro.get('location') or location.replace('-', ' ')
                    pro['category'] = category.replace('-', ' ').title()
                    
                    # Push to dataset
                    await Actor.push_data(pro)
                    scraped_count += 1
                    
                    if scraped_count % 10 == 0:
                        Actor.log.info(f"Progress: {scraped_count}/{max_results} professionals scraped")
                
                # Check if we need more results
                if scraped_count >= max_results:
                    Actor.log.info(f"Reached target of {max_results} results")
                    break
                
                # Find next page
                next_url = extract_next_page_url(html, current_url)
                if not next_url:
                    Actor.log.info("No next page found, pagination complete")
                    break
                
                current_url = next_url
                page_num += 1
                
                # Rate limiting
                await asyncio.sleep(2)
                
            except Exception as e:
                Actor.log.error(f"Error fetching page {page_num}: {e}")
                # Continue to next page if pagination exists
                break
        
        Actor.log.info(f"Scraping complete: {scraped_count} professionals collected")
