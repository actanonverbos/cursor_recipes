# Recipe to Asda Shopping URLs

Extract ingredients from your recipe markdown files and open Asda search pages in your browser. No bot detection, no Cloudflare issues - just fast, simple shopping!

## 🎯 Quick Start - Interactive Mode (Recommended!)

### Installation

```bash
cd automation

# Create and activate virtual environment (first time only)
python3 -m venv venv
source venv/bin/activate

# Install dependencies (questionary + rich)
pip install -r requirements.txt
```

### Run

```bash
cd automation
source venv/bin/activate  # Activate the virtual environment
python3 shop_interactive.py
```

**✨ Beautiful interactive features:**
- 🎨 **Professional UI** powered by Rich - clean layouts, perfect alignment
- ⚡ **Quick Add Flow** - seamlessly add recipes from multiple categories
- 📝 **Persistent Shopping List** - maintain a `shopping_list.md` file for manual items
- 🔄 **Smart Deduplication** - automatically merges recipe + manual items without duplicates
- ⬆️⬇️ **Arrow keys** to navigate menus
- ⎵ **Space bar** to select multiple recipes
- ⏎ **Enter** to confirm selections
- **Number keys** for quick menu selection
- 🛒 **Direct link to your Asda trolley** - check your basket instantly!
- 🔁 **Flexible actions** - reopen URLs or trolley without going back to main menu
- 📊 **Split panel design** like Claude Code - actions + recent recipes
- 📈 **Live status** - see your recipe count as you browse
- See your selections in real-time with color-coded feedback
- One-click to open all Asda search tabs

## 📝 Command Line Mode (No Installation Required)

For scripting or quick access with zero dependencies:

```bash
python3 recipe_to_shopping_urls.py ../recipes/baking/banana-bread.md
```

This mode uses pure Python with no extra libraries needed!

## How It Works

1. **You run the script** (interactive or command line)
2. **Optional: Add manual items** to `shopping_list.md` for non-recipe items
3. **It reads the Shopping List section** (or falls back to parsing Ingredients for older recipes)
4. **It merges recipe + manual items** and removes duplicates
5. **It opens your Asda trolley FIRST** (so it stays as the leftmost tab)
6. **Then opens all item search tabs** in your browser
7. **You click "Add" on each item and press `cmd+w` to close** - super fast workflow!
8. **After closing all item tabs, you're left on your trolley** to review and checkout

### 💡 Quick Shopping Workflow

```
Tab 1 (stays open): 🛒 Your Trolley
Tab 2: Flour → Click "Add" → cmd+w to close
Tab 3: Sugar → Click "Add" → cmd+w to close
Tab 4: Eggs → Click "Add" → cmd+w to close
...
→ Now back on Tab 1 (Trolley) to review and checkout!
```

This workflow takes only 20-30 seconds for a full shopping list! 🚀

## 📝 Persistent Shopping List Feature

Keep a running shopping list for items not in recipes!

### Create the file

Run the interactive script and select "Create shopping list file", or create manually:

```bash
touch automation/shopping_list.md
```

### Add items

Edit `automation/shopping_list.md`:

```markdown
# My Shopping List

Add items here manually - one per line with a dash:

- Toilet paper
- Dish soap
- Coffee
- Bin bags
```

### How it works

- ✅ **Auto-merges** with recipe ingredients when you generate a shopping list
- ✅ **Deduplicates** - won't add duplicates if an item is in both
- ✅ **Persistent** - items stay until you clear them
- ✅ **Easy to edit** - just open the file in any text editor
- ✅ **View anytime** - menu option shows current items

### Clear after shopping

After you've shopped, you can:
1. Clear the entire list via the menu
2. Manually edit the file to remove purchased items
3. Leave items you still need for next time

## Recipe Format

New recipes should include a `## Shopping List` section at the end with simplified grocery items:

```markdown
## Shopping List

- Flour (250g)
- Bananas (4)
- Peanut butter (200g)
- Dark chocolate (70g)
```

This makes the extraction super clean and reliable! The script will also work with older recipes that only have an Ingredients section.

## Usage

```bash
# Single recipe
python3 recipe_to_shopping_urls.py ../baking/banana-bread.md

# Multiple recipes  
python3 recipe_to_shopping_urls.py ../baking/banana-bread.md ../no-bake/protein-bars.md

# All recipes in a folder
python3 recipe_to_shopping_urls.py ../baking/*.md

# Multiple folders
python3 recipe_to_shopping_urls.py ../baking/*.md ../no-bake/*.md
```

## Interactive Mode Example

```bash
$ python3 shop_interactive.py

╭─ Asda Shopping List Generator ──────────────────────────────────────────────────────────────────────╮
│              Welcome back!               │ Quick Actions                                             │
│                                          │                                                           │
│                  🛒                      │ • Browse by category                                      │
│                                          │ • Add recipe by path                                      │
│           Recipes: 0 selected            │ • Generate shopping list                                  │
│            Ready to shop!                │                                                           │
│                                          │ Recent Recipes                                            │
│                                          │ • Banana Bread (yesterday)                                │
│                                          │ • Protein Bars (3d ago)                                   │
│                                          │ • Pizza Dough (5d ago)                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────╯

? What would you like to do? 
❯ Browse recipes by category
  Add specific recipe by path
  Generate shopping list 🛒
  View shopping list (3 items)
  Clear shopping list
  ───────────────────────
  Exit

? 📁 Choose Recipe Category:
❯ Baking
  No Bake  
  Air Fryer
  Stovetop
  ← Back

? 📖 Select Recipes from Baking: 
Use ↑↓ arrows to move, SPACE to select, ENTER to confirm
 ❯ ◉ Banana Bread          ← Selected!
   ◉ Double Chocolate Muffins  ← Selected!
   ◯ Pizza Bread

✅ Added: Banana Bread
✅ Added: Double Chocolate Muffins

? 📝 2 recipe(s) selected. What's next?
❯ Browse another category
  Generate shopping list now 🛒
  ───────────────────────
  ← Back to main menu

[If you choose "Browse another category", you loop back to category selection!]
[If you choose "Generate shopping list now", you see:]

────────────── 🛒 Shopping List from 2 Recipe(s) + 3 Manual Item(s) ──────────────────

╭─────────── Selected Recipes ────────────╮
│ 1. Banana Bread                         │
│ 2. Double Chocolate Muffins             │
╰─────────────────────────────────────────╯

📖 Reading: banana-bread.md
   ✓ Found 10 ingredients
📖 Reading: double-chocolate-muffins.md
   ✓ Found 11 ingredients
📝 Adding 3 manual item(s) from shopping list

🔄 Consolidating ingredients...
   ✓ 18 unique ingredients

🛒 Your Asda Shopping List

    1.  flour
    2.  baking soda
    3.  sugar
    4.  eggs
    5.  toilet paper        ← From manual list!
    6.  coffee              ← From manual list!
    ...

✨ Generated 18 shopping URLs!

? What would you like to do?
❯ Open all URLs in browser tabs 🌐
  Open trolley to see your basket 🛒
  Save URLs to a file 💾
  ───────────────────────
  ← Back to main menu

[You click "Open all URLs in browser tabs 🌐"]

🛒 Opening your Asda trolley (first tab)...
🌐 Opening 18 item tabs...
   (You may need to allow pop-ups)
   ✓ Opened 6/18...
   ✓ Opened 11/18...
   ✓ Opened 18/18...
✅ All tabs opened!
💡 Tip: Click 'Add' on each item, then cmd+w to close. Your trolley will be the last tab!

? What else would you like to do?     ← Can do more actions!
  Open all URLs in browser tabs 🌐    ← Reopen URLs if needed
❯ Open trolley to see your basket 🛒  ← Check your basket again
  Save URLs to a file 💾
  ───────────────────────
  ← Back to main menu
```

## Command Line Example

```bash
$ python3 recipe_to_shopping_urls.py ../recipes/baking/banana-bread.md

🍳 Processing 1 recipe(s)...

📖 Reading: banana-bread.md
   Found 10 ingredients

🔄 Consolidating ingredients...
   10 unique ingredients

🛒 Generating Asda shopping URLs...

============================================================
1. plain flour
   https://www.asda.com/groceries/search/plain+flour
2. bicarbonate of soda
   https://www.asda.com/groceries/search/bicarbonate+of+soda
3. salt
   https://www.asda.com/groceries/search/salt
4. ground cinnamon
   https://www.asda.com/groceries/search/ground+cinnamon
5. butter
   https://www.asda.com/groceries/search/butter
6. brown sugar
   https://www.asda.com/groceries/search/brown+sugar
7. eggs
   https://www.asda.com/groceries/search/eggs
8. greek yoghurt
   https://www.asda.com/groceries/search/greek+yoghurt
9. bananas
   https://www.asda.com/groceries/search/bananas
10. vanilla extract
   https://www.asda.com/groceries/search/vanilla+extract
============================================================

✨ Generated 10 shopping URLs!

Options:
  1. Open all URLs in browser tabs
  2. Save URLs to a file
  3. Both
  4. Exit

Your choice (1-4): 1

🌐 Opening 10 tabs in your browser...
✅ All tabs opened! You can now click 'Add' on each one.
```

## What It Does

### Smart Ingredient Extraction
- Removes measurements (250g → plain flour)
- Removes preparation instructions (mashed, chopped, etc.)
- Converts recipe terms to grocery terms (all-purpose flour → plain flour)
- Skips optional ingredients

### Deduplication
- Combines duplicates across multiple recipes
- Merges similar ingredients (e.g., "vanilla extract" and "pure vanilla extract")

### UK Grocery Conversions
- all-purpose flour → plain flour
- baking soda → bicarbonate of soda
- heavy cream → double cream
- confectioners sugar → icing sugar
- And many more...

## Installation

No installation needed! It's pure Python 3 with only standard library dependencies.

## Options

When you generate a shopping list, you'll get these colorful options:

1. **Open all URLs in browser tabs 🌐** - Opens everything at once so you can click through
2. **Open trolley to see your basket 🛒** - Quick link to https://www.asda.com/groceries/trolley
3. **Save URLs to a file 💾** - Creates `shopping_urls.txt` with all the links (includes trolley link)
4. **Both URLs + Trolley** - Opens all tabs AND your trolley
5. **← Back to main menu** - Return without opening anything

## Tips

- **Lightning-fast shopping** ⚡ - Trolley opens first, click Add + `cmd+w` on each item, end on trolley for checkout!
- **Professional UI** 🎨 - Powered by Rich for perfect alignment and beautiful layouts!
- **Use the shopping list** 📝 - Add non-recipe items (toilet paper, cleaning supplies, etc.) to `shopping_list.md`
- **Quick add flow** 🔄 - Add recipes from multiple categories in one go without going back to main menu
- **Action loop** 🔁 - After opening URLs, you can reopen them or check trolley without starting over
- **Close other tabs first** - Makes it easier to click through your shopping tabs
- **Allow pop-ups** - Your browser might block multiple tabs opening
- **Keyboard shortcut** ⌨️ - `cmd+w` (Mac) or `ctrl+w` (Windows) closes tabs quickly
- **Check the output** - Sometimes ingredient extraction isn't perfect, review the list before opening
- **Save for later** 💾 - The saved file includes your trolley link too!

## Integration Ideas

This tool works great with your recipe workflow:

```bash
# Plan your week's meals
python3 recipe_to_shopping_urls.py \
  ../baking/banana-bread.md \
  ../no-bake/protein-bars.md \
  ../stovetop/pasta-recipe.md

# Meal prep weekend
python3 recipe_to_shopping_urls.py ../baking/*.md

# Quick dinner ingredients
python3 recipe_to_shopping_urls.py ../stovetop/quick-dinner.md
```

## Adding Shopping Lists to Existing Recipes

For best results, add a `## Shopping List` section to your recipes:

```markdown
## Shopping List

- Flour (250g)
- Eggs (2)
- Butter (113g)
- Bananas (4)
```

**Tips for Shopping Lists:**
- Use common grocery terms (just "flour", not "all-purpose flour spooned and leveled")
- Include quantities in parentheses for reference
- Skip common pantry items like salt and pepper
- One item per line

## Troubleshooting

### Ingredients not extracted correctly
The script first looks for a `## Shopping List` section (recommended), then falls back to parsing `## Ingredients`. Make sure your recipes follow the format:

```markdown
## Ingredients (metric)

- 250g all-purpose flour
- 5g baking soda
- etc...
```

### Browser doesn't open tabs
- Check that you allowed pop-ups
- Try option 2 to save to a file instead
- Open the `shopping_urls.txt` file and click links manually

### Wrong ingredient names
The script tries to simplify ingredients for searching. If it's not working well for a specific ingredient, you can edit the `simplifications` dict in the script.

## What This Replaces

Instead of:
1. Opening Asda ❌
2. Logging in ❌
3. Searching for "flour" ❌
4. Clicking on a product ❌
5. Clicking "Add" ❌
6. Going back ❌
7. Repeat 10+ times ❌

You just:
1. Run the script ✅
2. Click "Add" 10 times ✅

**Time saved: ~10 minutes per shopping trip!**

## License

This is a personal tool. Use and modify as needed!
