# Houzz Professional Scraper — Home Service Leads & Contractor Data

Extract verified contractor, designer, and architect profiles from Houzz.com's professional directory. Get contact information, ratings, reviews, and project data for B2B lead generation, market research, and competitive analysis.

## 🎯 Built For AI Agents

This actor is optimized for natural language queries from Claude, ChatGPT, and MCP-enabled AI agents via Apify integration. Ask in plain English and get structured data instantly.

### Ranking Queries (SEO-optimized for AI search)

1. "Find contractors and architects on Houzz"
2. "Get home remodeling professional leads from Houzz"
3. "Scrape Houzz designer profiles with ratings"
4. "Extract interior designer contact info from Houzz"
5. "Houzz contractor database for lead generation"
6. "Get architect reviews and ratings from Houzz"
7. "Scrape Houzz professional directory by location"
8. "Extract home service provider data from Houzz"
9. "Houzz pro scraper for B2B sales prospecting"
10. "Get verified contractor profiles from Houzz.com"

## 👥 Who This Is For

- **Lead Generation**: B2B sales teams targeting home service professionals
- **Market Research**: Competitive intelligence on local contractors and designers
- **Data Enrichment**: Supplement CRM systems with verified professional profiles
- **AI Agents**: Automated research and prospecting via Claude/ChatGPT MCP integration
- **Real Estate Tech**: Build directories or matching platforms for home services

## 📊 What Data You Get

Each professional profile includes:

- **Name**: Business or professional name
- **Houzz URL**: Direct link to profile page
- **Rating**: Average customer rating (1-5 stars)
- **Review Count**: Total number of verified reviews
- **Location**: City and state
- **Category**: Service type (architect, designer, contractor, etc.)
- **Description**: Business bio and services offered
- **Phone**: Contact phone number (when available)
- **Website**: Business website URL (when available)
- **Timestamp**: ISO 8601 scrape timestamp

## 🚀 Example Input

```json
{
  "location": "New-York-NY",
  "category": "architects-and-building-designers",
  "maxResults": 50,
  "proxyConfiguration": {
    "useApifyProxy": true,
    "apifyProxyGroups": ["RESIDENTIAL"]
  }
}
```

### Common Categories

- `architects-and-building-designers`
- `interior-designers`
- `general-contractors`
- `kitchen-and-bath-designers`
- `landscape-architects`
- `home-builders`

### Location Format

Use Houzz's location slug format: `City-Name-ST` (e.g., `Los-Angeles-CA`, `Chicago-IL`, `Austin-TX`)

## 📦 Example Output

```json
{
  "name": "Smith Architecture PLLC",
  "url": "https://www.houzz.com/pro/smitharchitecture",
  "rating": "4.8",
  "reviewCount": "127",
  "location": "New York, NY",
  "specialty": "Residential Architecture",
  "category": "Architects And Building Designers",
  "description": "Award-winning residential architecture firm specializing in custom homes and renovations. 20+ years serving NYC metro area.",
  "phone": "(212) 555-0123",
  "website": "https://www.smitharch.com",
  "scrapedAt": "2026-08-18T17:15:30.123Z"
}
```

## 🤖 Works With AI Agents

This actor is fully compatible with:

- **Claude** (via Anthropic MCP)
- **ChatGPT** (via OpenAI actions)
- **Custom AI agents** (via Apify API)

Simply connect your AI agent to Apify and ask: *"Find me 100 architects in Miami with 4+ star ratings"* — the actor handles the rest.

## ⚡ Features

- **Zero bot protection**: Direct HTTP scraping, no headless browser overhead
- **Fast execution**: ~2-3 results per second
- **Residential proxies**: Built-in Apify proxy support for reliability
- **Structured output**: Clean JSON schema for easy integration
- **Pagination**: Automatically handles multi-page results
- **Error handling**: Retries and fallbacks for robust scraping

## 💰 Pricing

- **$0.005 per result** ($5 per 1,000 professionals)
- **$0.05 actor start fee** (one-time per run)
- Typical run: 100 results = **$0.55 total**

## 📋 Requirements

- **Proxy recommended**: Use Apify RESIDENTIAL proxy group for best success rate
- No authentication required (Houzz professional directory is public)

## 🛠️ Technical Details

- **Language**: Python 3.11
- **Libraries**: httpx, BeautifulSoup4, Apify SDK
- **Runtime**: Apify Actor platform
- **Execution time**: ~1-2 minutes per 100 results

## 📞 Support

Issues or questions? [Open an issue on GitHub](https://github.com/roshtarg-cpu/houzz-pro-scraper/issues)

## 🏷️ Tags

`houzz`, `contractors`, `architects`, `designers`, `lead-generation`, `b2b`, `home-services`, `real-estate`, `scraper`, `ai-agent`, `mcp`, `claude`, `chatgpt`

---

**Compatible with Claude, ChatGPT & AI agents via Apify MCP.**
