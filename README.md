# Recipe Library 🍳

A smart recipe management system powered by AI that converts web recipes to markdown and generates instant shopping links. Built to work seamlessly with Cursor AI agent.

## 🎯 What This Does

This project solves two common cooking problems:

1. **Recipe Collection** - Convert any recipe URL into a beautifully formatted markdown file with metric measurements
2. **Smart Shopping** - Generate instant shopping links for all ingredients (no more bot blocks or Cloudflare issues!)

### Why This Exists

I got tired of:
- Copying recipes from websites cluttered with ads and life stories
- Converting cups to grams manually
- Typing ingredients one-by-one into grocery websites
- Getting blocked by Cloudflare on automation tools like Automato

This workflow takes **just a few minutes** from finding a recipe online to having a shopping list ready!

## 🚀 Quick Start

### 1. Save a Recipe

In Cursor, just paste a recipe URL and the AI agent will automatically:
- Fetch the recipe using Firecrawl
- Convert all measurements to metric (grams)
- Format it beautifully in markdown
- Categorize it by cooking method
- Add a shopping list section

**Example:**
```
"Convert this recipe: https://example.com/banana-bread"
```

The agent follows the rules defined in `.cursor/rules/recipe-url-to-markdown.mdc` to create a standardized format.

### 2. Generate Shopping Links

Use the automation tool to create instant shopping links:

```bash
cd automation
source venv/bin/activate
python3 shop_interactive.py
```

- Browse recipes by category
- Select multiple recipes
- Add manual items (toilet paper, coffee, etc.)
- Generate Asda shopping URLs
- Click through in seconds!

**Time saved: ~10 minutes per shopping trip** ⚡

## 📁 Project Structure

```
recipes_library/
├── recipes/               # All your saved recipes
│   ├── baking/           # Oven-baked goods
│   ├── no-bake/          # No cooking required
│   ├── stovetop/         # Stove-cooked meals
│   ├── air-fryer/        # Air fryer recipes
│   ├── slow-cooker/      # Slow cooker recipes
│   ├── instant-pot/      # Pressure cooker recipes
│   └── drinks/           # Beverages
│
├── automation/           # Shopping automation tools
│   ├── shop_interactive.py      # Interactive shopping list generator
│   ├── recipe_to_shopping_urls.py  # Command-line tool
│   ├── shopping_list.md         # Persistent manual items
│   └── README.md               # Detailed automation docs
│
└── .cursor/rules/        # AI agent workflow rules
    └── recipe-url-to-markdown.mdc
```

## 🤖 How the Cursor Agent Works

### The @rules Workflow

The `.cursor/rules/recipe-url-to-markdown.mdc` file defines the automated workflow:

1. **Fetch with Firecrawl** - Always uses the Firecrawl MCP tool (never skips this!)
2. **Extract Information** - Grabs title, yield, times, ingredients, instructions, notes
3. **Normalize Format** - Converts to our standard markdown structure
4. **Convert to Metric** - All ingredients become grams-first
5. **Auto-categorize** - Files go into the correct cooking method folder
6. **Add Shopping List** - Creates a simplified list for automation

### Recipe Format

Every recipe follows this structure:

```markdown
# Recipe Title

- Source: https://original-url.com
- Yield: 12 bars
- Prep Time: 10 minutes
- Total Time: 1 hour

## Ingredients (metric)

- 250g plain flour
- 200g brown sugar
- 2 large eggs

## Instructions

1) Mix dry ingredients
2) Add wet ingredients
3) Bake at 180°C for 25 minutes

## Notes

- Can substitute honey for maple syrup

## Storage

- Fridge: up to 1 week in an airtight container
- Freezer: up to 3 months

## Shopping List

- Flour (250g)
- Brown sugar (200g)
- Eggs (2)
```

The **Shopping List** section is key for the automation tool!

## 🛒 Shopping Automation

The automation tool is **way better than Automato** because:
- ✅ No bot detection or Cloudflare blocks
- ✅ No API rate limits
- ✅ Works every time
- ✅ Takes just a few minutes
- ✅ No manual clicking through grocery site menus

### Features

- **Interactive UI** - Beautiful terminal interface with arrow keys and selection
- **Multi-recipe** - Combine ingredients from multiple recipes
- **Persistent List** - Keep manual items (toilet paper, etc.) in `shopping_list.md`
- **Smart Deduplication** - Automatically merges and removes duplicates
- **UK Grocery Terms** - Converts US terms (all-purpose flour → plain flour)
- **Instant URLs** - Opens all search pages in tabs
- **Fast Workflow** - Click "Add" + `cmd+w` on each tab

### Installation

```bash
cd automation

# Create virtual environment (first time only)
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Interactive mode (recommended)
python3 shop_interactive.py

# Command line mode
python3 recipe_to_shopping_urls.py ../recipes/baking/banana-bread.md
```

See [automation/README.md](automation/README.md) for detailed documentation.

## 🎯 Complete Workflow Example

### Step 1: Find a Recipe Online

You're browsing and find an amazing recipe at `https://foodblog.com/banana-bread`

### Step 2: Save with Cursor Agent

In Cursor:
```
"Save this recipe: https://foodblog.com/banana-bread"
```

The AI agent:
- Fetches it with Firecrawl
- Converts to metric
- Saves to `recipes/baking/banana-bread.md`
- Takes ~30 seconds

### Step 3: Plan Your Week

Decide what to make this week:
- Banana bread
- Chocolate muffins
- Protein bars

### Step 4: Generate Shopping List

```bash
cd automation
source venv/bin/activate
python3 shop_interactive.py
```

1. Select "Browse recipes by category"
2. Choose "Baking"
3. Select: Banana bread, Chocolate muffins
4. Browse "No Bake"
5. Select: Protein bars
6. Choose "Generate shopping list"
7. Select "Open all URLs in browser tabs"

**Time: ~2 minutes**

### Step 5: Shop

Your browser opens:
- Tab 1: Your Asda trolley (stays open)
- Tabs 2-20: Each ingredient search

For each tab:
- Click "Add to trolley"
- Press `cmd+w` to close

You end up back on your trolley tab to review and checkout!

**Time: ~2 minutes for 20 items**

### Total Time: ~5 minutes from recipe URL to shopping cart! 🚀

## 🔧 Technical Details

### Technologies

- **Firecrawl MCP** - Web scraping without bot detection
- **Python 3** - Automation scripts
- **Questionary** - Interactive terminal UI
- **Rich** - Beautiful terminal formatting
- **Markdown** - Recipe storage format

### Requirements

- Python 3.13+ (or 3.10+)
- Cursor AI with Firecrawl MCP configured
- Internet connection
- A browser (for opening shopping links)

### No PII

This repository contains:
- ✅ Recipe files (public recipes from the web)
- ✅ Automation scripts
- ✅ Configuration files
- ❌ No personal information
- ❌ No API keys or credentials
- ❌ No private data

## 📝 Adding Your Own Recipes

### Method 1: From URL (Recommended)

Just tell Cursor:
```
"Add this recipe: https://example.com/recipe"
```

### Method 2: Manual Creation

Create a new `.md` file in the appropriate category folder following the format above. Make sure to include the `## Shopping List` section!

## 🤝 Contributing

This is a personal project, but feel free to:
- Fork it
- Adapt it for your needs
- Use your own grocery store URLs (just update the scripts)
- Add more conversion rules

## 💡 Tips & Tricks

1. **Keep shopping_list.md updated** - Add non-recipe items so you never forget them
2. **Close other tabs first** - Makes the shopping workflow smoother
3. **Allow pop-ups** - Browser might block multiple tabs
4. **Use keyboard shortcuts** - `cmd+w` makes closing tabs super fast
5. **Review the list** - Sometimes ingredient extraction needs manual tweaking

## 📄 License

MIT License - Use this however you want!

## 🙏 Credits

Built with:
- [Cursor AI](https://cursor.sh) - AI-powered code editor
- [Firecrawl](https://firecrawl.dev) - Web scraping that actually works
- [Asda](https://asda.com) - UK grocery delivery

---

**Made with ❤️ and a lot of hunger**

