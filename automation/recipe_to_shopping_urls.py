#!/usr/bin/env python3
"""
Recipe to Shopping URLs
Extract ingredients from recipe markdown files and generate Asda shopping URLs.
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Set
import webbrowser
from urllib.parse import quote_plus


def extract_ingredients_from_recipe(recipe_path: Path) -> List[Dict[str, str]]:
    """Extract ingredients from a recipe markdown file."""
    try:
        content = recipe_path.read_text()
        
        # First, try to find the Shopping List section (preferred)
        shopping_list_match = re.search(
            r'## Shopping List\s*\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )
        
        if shopping_list_match:
            # Use the shopping list - it's already simplified!
            ingredients_text = shopping_list_match.group(1)
            ingredient_lines = re.findall(r'-\s+(.+)', ingredients_text)
            
            ingredients = []
            for line in ingredient_lines:
                # Shopping list format: "Flour (250g)" or just "Bananas"
                # Remove quantity in parentheses for search
                searchable = re.sub(r'\s*\([^)]*\)', '', line).strip()
                
                if len(searchable) > 2:
                    ingredients.append({
                        'original': line,
                        'searchable': searchable
                    })
            
            return ingredients
        
        # Fall back to parsing Ingredients section (for older recipes)
        ingredients_match = re.search(
            r'## Ingredients.*?\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )
        
        if not ingredients_match:
            print(f"⚠️  No ingredients or shopping list section found in {recipe_path.name}")
            return []
        
        ingredients_text = ingredients_match.group(1)
        
        # Extract each ingredient line (starting with -)
        ingredient_lines = re.findall(r'-\s+(.+)', ingredients_text)
        
        ingredients = []
        for line in ingredient_lines:
            # Skip Optional ingredients
            if line.lower().startswith('optional'):
                continue
                
            # Remove leading measurements: numbers + optional units
            # "250g all-purpose flour" -> "all-purpose flour"
            # "2 large eggs" -> "large eggs"
            # "5ml vanilla" -> "vanilla"
            clean_line = re.sub(r'^\d+\.?\d*\s*(g|kg|ml|l|oz|lb|cup|tbsp|tsp|teaspoon|tablespoon|mg)?\s*', '', line, flags=re.IGNORECASE)
            
            if not clean_line:
                continue
            
            # Remove parenthetical info
            clean_line = re.sub(r'\([^)]*\)', '', clean_line)
            
            # Remove common size/quality/prep descriptors at the start
            clean_line = re.sub(r'^(large|medium|small|fresh|frozen|ripe|raw|cooked|mashed|packed|chopped|diced)\s+', '', clean_line, flags=re.IGNORECASE)
            
            # Special case: "packed light or dark brown sugar" -> just get "brown sugar"
            if "brown sugar" in clean_line.lower():
                clean_line = "brown sugar"
            
            # Remove preparation instructions at end (after comma)
            # "unsalted butter, softened to room temperature" -> "unsalted butter"
            main_ingredient = clean_line.split(',')[0].strip()
            
            # Also split on " at " to remove "at room temperature" type phrases
            main_ingredient = main_ingredient.split(' at ')[0].strip()
            
            # Also split on " or " to get just the first option  
            main_ingredient = main_ingredient.split(' or ')[0].strip()
            
            # Clean up extra whitespace
            main_ingredient = ' '.join(main_ingredient.split())
            
            # Skip very short entries, single words like "light", "or" etc.
            if len(main_ingredient) <= 4 or main_ingredient.lower() in ['light', 'dark', 'or', 'and']:
                continue
                
            ingredients.append({
                'original': line,
                'searchable': main_ingredient
            })
        
        return ingredients
        
    except Exception as e:
        print(f"❌ Error reading {recipe_path.name}: {e}")
        return []


def simplify_ingredient_for_search(ingredient: str) -> str:
    """Simplify ingredient name to common grocery search terms."""
    
    # Mapping of recipe terms to grocery search terms
    simplifications = {
        'all-purpose flour': 'plain flour',
        'all purpose flour': 'plain flour',
        'whole wheat flour': 'wholemeal flour',
        'confectioners sugar': 'icing sugar',
        'powdered sugar': 'icing sugar',
        'granulated sugar': 'sugar',
        'caster sugar': 'caster sugar',
        'baking soda': 'bicarbonate of soda',
        'baking powder': 'baking powder',
        'unsalted butter': 'butter',
        'salted butter': 'butter',
        'greek yogurt': 'greek yoghurt',
        'plain yogurt': 'natural yoghurt',
        'sour cream': 'soured cream',
        'heavy cream': 'double cream',
        'whipping cream': 'double cream',
        'vanilla extract': 'vanilla extract',
        'chocolate chips': 'chocolate chips',
        'semi-sweet chocolate': 'dark chocolate',
        'cocoa powder': 'cocoa powder',
        'natural peanut butter': 'peanut butter',
        'creamy peanut butter': 'peanut butter',
        'brown sugar': 'brown sugar',
        'light brown sugar': 'brown sugar',
        'dark brown sugar': 'brown sugar',
        'ground flaxseed meal': 'flaxseed',
        'flaxseed meal': 'flaxseed',
        'protein powder': 'protein powder',
    }
    
    ingredient_lower = ingredient.lower()
    
    # Check if we have a simplification
    for key, value in simplifications.items():
        if key in ingredient_lower:
            return value
    
    # Default: return the ingredient as-is
    return ingredient


def generate_asda_url(ingredient: str) -> str:
    """Generate an Asda search URL for an ingredient."""
    search_term = simplify_ingredient_for_search(ingredient)
    encoded = quote_plus(search_term)
    return f"https://www.asda.com/groceries/search/{encoded}"


def consolidate_ingredients(all_ingredients: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Remove duplicate ingredients and consolidate similar ones."""
    seen = {}
    consolidated = []
    
    for ing in all_ingredients:
        searchable = ing['searchable'].lower().strip()
        
        # Normalize similar ingredients
        # e.g., "vanilla extract" and "pure vanilla extract" -> "vanilla extract"
        if 'vanilla extract' in searchable:
            searchable = 'vanilla extract'
        elif 'peanut butter' in searchable:
            searchable = 'peanut butter'
        elif 'brown sugar' in searchable:
            searchable = 'brown sugar'
        elif 'chocolate bar' in searchable:
            searchable = 'dark chocolate'
        elif searchable.endswith(' salt'):
            searchable = 'salt'
        
        # Skip if we've seen this ingredient
        if searchable in seen:
            continue
        
        seen[searchable] = True
        # Update the searchable term
        ing['searchable'] = searchable
        consolidated.append(ing)
    
    return consolidated


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("📋 Recipe to Shopping URLs")
        print("=" * 60)
        print("\nUsage:")
        print("  python recipe_to_shopping_urls.py <recipe_files...>")
        print("\nExamples:")
        print("  # Single recipe")
        print("  python recipe_to_shopping_urls.py ../baking/banana-bread.md")
        print("")
        print("  # Multiple recipes")
        print("  python recipe_to_shopping_urls.py ../baking/*.md")
        print("")
        print("  # All no-bake recipes")
        print("  python recipe_to_shopping_urls.py ../no-bake/*.md")
        print("=" * 60)
        sys.exit(1)
    
    recipe_paths = [Path(arg) for arg in sys.argv[1:]]
    
    # Validate files exist
    valid_paths = []
    for path in recipe_paths:
        if path.exists() and path.suffix == '.md':
            valid_paths.append(path)
        else:
            print(f"⚠️  Skipping {path} (not found or not a .md file)")
    
    if not valid_paths:
        print("❌ No valid recipe files found!")
        sys.exit(1)
    
    print(f"\n🍳 Processing {len(valid_paths)} recipe(s)...\n")
    
    # Extract all ingredients
    all_ingredients = []
    for path in valid_paths:
        print(f"📖 Reading: {path.name}")
        ingredients = extract_ingredients_from_recipe(path)
        print(f"   Found {len(ingredients)} ingredients")
        all_ingredients.extend(ingredients)
    
    # Consolidate duplicates
    print(f"\n🔄 Consolidating ingredients...")
    unique_ingredients = consolidate_ingredients(all_ingredients)
    print(f"   {len(unique_ingredients)} unique ingredients")
    
    # Generate URLs
    print(f"\n🛒 Generating Asda shopping URLs...\n")
    print("=" * 60)
    
    urls = []
    for i, ing in enumerate(unique_ingredients, 1):
        searchable = ing['searchable']
        url = generate_asda_url(searchable)
        urls.append(url)
        print(f"{i}. {searchable}")
        print(f"   {url}")
    
    print("=" * 60)
    
    # Ask user what to do (or auto-open if running non-interactively)
    print(f"\n✨ Generated {len(urls)} shopping URLs!")
    
    try:
        print("\nOptions:")
        print("  1. Open all URLs in browser tabs")
        print("  2. Save URLs to a file")
        print("  3. Both")
        print("  4. Exit")
        
        choice = input("\nYour choice (1-4): ").strip()
    except (EOFError, KeyboardInterrupt):
        # Non-interactive mode - default to opening in browser
        print("\n(Non-interactive mode detected - opening in browser)")
        choice = '1'
    
    if choice in ['1', '3']:
        print(f"\n🌐 Opening {len(urls)} tabs in your browser...")
        print("   (You may need to allow pop-ups)")
        
        import time
        # Open first few immediately, then pause
        for i, url in enumerate(urls):
            webbrowser.open(url)
            # Add a small delay to avoid overwhelming the browser
            if i > 0 and i % 5 == 0:
                print(f"   Opened {i+1}/{len(urls)}...")
                time.sleep(1)
        
        print("✅ All tabs opened! You can now click 'Add' on each one.")
    
    if choice in ['2', '3']:
        output_file = Path(__file__).parent / "shopping_urls.txt"
        with open(output_file, 'w') as f:
            f.write("# Asda Shopping URLs\n")
            f.write(f"# Generated from {len(valid_paths)} recipe(s)\n\n")
            for i, (ing, url) in enumerate(zip(unique_ingredients, urls), 1):
                f.write(f"{i}. {ing['searchable']}\n")
                f.write(f"   {url}\n\n")
        
        print(f"\n💾 URLs saved to: {output_file}")
        print("   You can open this file and click the links")
    
    if choice == '4':
        print("\n👋 Goodbye!")
    
    print("")


if __name__ == "__main__":
    main()

