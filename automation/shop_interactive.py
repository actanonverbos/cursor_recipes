#!/usr/bin/env python3
"""
Interactive Asda Shopping List Generator
Navigate through your recipes and generate shopping URLs with ease!

Uses arrow keys for navigation and space bar for selection.
"""

import os
import sys
import webbrowser
import time
import datetime
from pathlib import Path
from typing import List

try:
    import questionary
    from questionary import Choice, Separator
    from rich.console import Console
    from rich.panel import Panel
    from rich.columns import Columns
    from rich.text import Text
    from rich.table import Table
    from rich import box
except ImportError as e:
    print("❌ Missing required libraries")
    print("\nPlease install them by running:")
    print("  pip3 install -r requirements.txt")
    missing = getattr(e, 'name', str(e))
    print(f"\nMissing: {missing}\n")
    sys.exit(1)

console = Console()

# Import the existing shopping URL functions
from recipe_to_shopping_urls import (
    extract_ingredients_from_recipe,
    consolidate_ingredients,
    generate_asda_url,
    simplify_ingredient_for_search
)


def clear_screen():
    """Clear the terminal screen."""
    console.clear()


def print_simple_header(title: str):
    """Print a simple header for sub-pages."""
    console.print()
    console.rule(f"[bold]{title}[/bold]", style="cyan")
    console.print()


def print_welcome_panel(selected_count: int, recipes_path: Path):
    """Print a Claude Code-style split panel welcome screen using Rich."""
    
    # Get recent recipes
    recent_recipes = []
    try:
        all_recipes = []
        for cat in get_recipe_directories(recipes_path):
            all_recipes.extend(get_recipes_in_directory(cat))
        all_recipes.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        recent_recipes = all_recipes[:3]
    except:
        pass
    
    # Left panel - Welcome
    left_content = Text()
    left_content.append("\n")
    left_content.append("Welcome back!\n\n", style="bold")
    left_content.append("        🛒\n\n", style="yellow")
    left_content.append(f"Recipes: ", style="white")
    left_content.append(f"{selected_count}", style="magenta bold")
    left_content.append(" selected\n", style="white")
    left_content.append("Ready to shop!\n", style="cyan")
    
    # Right panel - Quick Actions & Recent
    right_content = Text()
    right_content.append("Quick Actions\n\n", style="bold")
    right_content.append("• Browse by category\n", style="green")
    right_content.append("• Add recipe by path\n", style="green")
    if selected_count > 0:
        right_content.append("• Generate shopping list\n", style="green")
    else:
        right_content.append("• Open your trolley\n", style="green")
    
    right_content.append("\nRecent Recipes\n", style="bold")
    
    if recent_recipes:
        for recipe in recent_recipes:
            recipe_name = recipe.stem.replace('-', ' ').title()
            mtime = datetime.datetime.fromtimestamp(recipe.stat().st_mtime)
            now = datetime.datetime.now()
            delta = now - mtime
            if delta.days == 0:
                time_ago = "today"
            elif delta.days == 1:
                time_ago = "yesterday"
            else:
                time_ago = f"{delta.days}d ago"
            
            right_content.append(f"• {recipe_name} ", style="yellow")
            right_content.append(f"({time_ago})\n", style="cyan dim")
    else:
        right_content.append("No recent activity\n", style="cyan dim")
    
    # Create columns
    columns = Columns([
        Panel(left_content, expand=True, border_style="cyan"),
        Panel(right_content, expand=True, border_style="cyan")
    ], equal=True, expand=True)
    
    # Print the panel
    console.print()
    console.print(Panel(
        columns,
        title="[cyan]Asda Shopping List Generator[/cyan]",
        border_style="cyan",
        box=box.ROUNDED
    ))
    console.print()


def get_recipe_directories(recipes_path: Path) -> List[Path]:
    """Get all recipe category directories."""
    if not recipes_path.exists():
        return []
    
    dirs = [d for d in recipes_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
    return sorted(dirs)


def get_recipes_in_directory(directory: Path) -> List[Path]:
    """Get all markdown recipe files in a directory."""
    if not directory.exists():
        return []
    
    recipes = [f for f in directory.iterdir() if f.suffix == '.md']
    return sorted(recipes)


def load_shopping_list(script_dir: Path) -> List[str]:
    """Load items from shopping_list.md if it exists."""
    shopping_list_file = script_dir / "shopping_list.md"
    items = []
    
    if shopping_list_file.exists():
        with open(shopping_list_file, 'r') as f:
            for line in f:
                line = line.strip()
                # Parse markdown bullet points
                if line.startswith('- ') or line.startswith('* '):
                    item = line[2:].strip()
                    if item:
                        items.append(item)
    
    return items


def save_shopping_list(script_dir: Path, items: List[str]):
    """Save items to shopping_list.md."""
    shopping_list_file = script_dir / "shopping_list.md"
    
    with open(shopping_list_file, 'w') as f:
        f.write("# My Shopping List\n\n")
        f.write("Add items here manually - one per line with a dash:\n\n")
        for item in items:
            f.write(f"- {item}\n")


def select_single(items: List[str], title: str, back_option: str = "← Back") -> int:
    """Show a single-selection menu with arrow keys."""
    choices = items + [Separator(), back_option]
    
    result = questionary.select(
        title,
        choices=choices,
        use_shortcuts=True,
        use_arrow_keys=True,
    ).ask()
    
    if result == back_option or result is None:
        return -1
    
    return items.index(result)


def select_multiple(items: List[str], title: str, instruction: str = None) -> List[int]:
    """Show a multiple-selection menu with arrow keys and space bar."""
    if instruction is None:
        instruction = "Use ↑↓ arrows to move, SPACE to select, ENTER to confirm"
    
    result = questionary.checkbox(
        title,
        choices=items,
        instruction=instruction,
    ).ask()
    
    if result is None:  # User cancelled (Ctrl+C)
        return []
    
    # Return indices of selected items
    return [items.index(item) for item in result]


def main():
    """Main interactive loop."""
    # Find the recipes directory
    script_dir = Path(__file__).parent
    recipes_path = script_dir.parent / "recipes"
    
    if not recipes_path.exists():
        console.print(f"[red]❌ Could not find recipes directory at: {recipes_path}[/red]")
        console.print("[yellow]   Make sure this script is in the automation/ folder[/yellow]")
        sys.exit(1)
    
    selected_recipes = []
    
    while True:
        clear_screen()
        print_welcome_panel(len(selected_recipes), recipes_path)
        
        if selected_recipes:
            console.print("📝 [yellow]Selected Recipes:[/yellow]")
            for recipe in selected_recipes:
                console.print(f"   [green]✓ {recipe.stem.replace('-', ' ').title()}[/green]")
            console.print()
        
        # Check if there's a manual shopping list
        manual_items = load_shopping_list(script_dir)
        
        # Build main menu options
        menu_options = [
            "Browse recipes by category",
            "Add specific recipe by path",
        ]
        
        if selected_recipes or manual_items:
            menu_options.append("Generate shopping list 🛒")
        
        if selected_recipes:
            menu_options.append("Clear selected recipes")
        
        # Shopping list management
        if manual_items:
            menu_options.append(f"View shopping list ({len(manual_items)} items)")
            menu_options.append("Clear shopping list")
        else:
            menu_options.append("Create shopping list file")
        
        menu_options.append(Separator())
        menu_options.append("Exit")
        
        choice = questionary.select(
            "What would you like to do?",
            choices=menu_options,
            use_shortcuts=True,
            use_arrow_keys=True,
        ).ask()
        
        if choice is None or choice == "Exit":
            console.print("\n[cyan bold]👋 Happy Shopping! See you next time![/cyan bold]\n")
            sys.exit(0)
        
        elif choice == "Browse recipes by category":
            # Browse by category - with quick add flow
            keep_browsing = True
            while keep_browsing:
                categories = get_recipe_directories(recipes_path)
                if not categories:
                    console.print("\n[red]❌ No recipe categories found![/red]")
                    time.sleep(2)
                    break
                
                category_names = [d.name.replace('-', ' ').title() for d in categories]
                
                clear_screen()
                
                # Show current selection status if any recipes selected
                if selected_recipes:
                    status_panel = Panel(
                        Text.from_markup(f"[green]✓[/green] {len(selected_recipes)} recipe(s) selected"),
                        border_style="green",
                        box=box.ROUNDED
                    )
                    console.print(status_panel)
                    console.print()
                
                selected_cat_idx = select_single(
                    category_names,
                    "📁 Choose Recipe Category:"
                )
                
                if selected_cat_idx == -1:
                    keep_browsing = False
                    continue
                
                category = categories[selected_cat_idx]
                recipes = get_recipes_in_directory(category)
                
                if not recipes:
                    console.print(f"\n[red]❌ No recipes found in {category.name}[/red]")
                    time.sleep(2)
                    continue
                
                recipe_names = [r.stem.replace('-', ' ').title() for r in recipes]
                
                clear_screen()
                selected_recipe_indices = select_multiple(
                    recipe_names,
                    f"📖 Select Recipes from {category.name.title()}:"
                )
                
                if selected_recipe_indices:
                    console.print()
                    for idx in selected_recipe_indices:
                        recipe = recipes[idx]
                        if recipe not in selected_recipes:
                            selected_recipes.append(recipe)
                            console.print(f"[green]✅ Added: [bold]{recipe.stem.replace('-', ' ').title()}[/bold][/green]")
                        else:
                            console.print(f"[yellow]⚠️  Already selected: {recipe.stem.replace('-', ' ').title()}[/yellow]")
                    
                    console.print()
                    
                    # Quick add flow - ask what's next with Rich styling
                    next_action = questionary.select(
                        f"📝 {len(selected_recipes)} recipe(s) selected. What's next?",
                        choices=[
                            "Browse another category",
                            "Generate shopping list now 🛒",
                            Separator(),
                            "← Back to main menu"
                        ],
                        use_shortcuts=True,
                    ).ask()
                    
                    if next_action == "Browse another category":
                        # Loop back to category selection
                        continue
                    elif next_action == "Generate shopping list now 🛒":
                        # Jump to generation
                        keep_browsing = False
                        choice = "Generate shopping list 🛒"
                    else:
                        # Back to main menu
                        keep_browsing = False
        
        elif choice == "Add specific recipe by path":
            # Add by path
            clear_screen()
            print_simple_header("📝 Add Recipe by Path")
            
            path_input = questionary.text(
                "Enter recipe path (relative to recipes/):",
                instruction="Example: baking/banana-bread.md"
            ).ask()
            
            if not path_input:
                continue
            
            recipe_path = recipes_path / path_input
            
            if recipe_path.exists() and recipe_path.suffix == '.md':
                if recipe_path not in selected_recipes:
                    selected_recipes.append(recipe_path)
                    console.print(f"\n[green]✅ Added: [bold]{recipe_path.stem.replace('-', ' ').title()}[/bold][/green]")
                else:
                    console.print(f"\n[yellow]⚠️  Already selected: {recipe_path.stem.replace('-', ' ').title()}[/yellow]")
            else:
                console.print(f"\n[red]❌ Recipe not found: {path_input}[/red]")
            
            time.sleep(1.5)
        
        if choice == "Generate shopping list 🛒":
            # Generate shopping list
            clear_screen()
            
            # Load manual shopping list
            manual_items = load_shopping_list(script_dir)
            
            # Build title
            title_parts = []
            if selected_recipes:
                title_parts.append(f"{len(selected_recipes)} Recipe(s)")
            if manual_items:
                title_parts.append(f"{len(manual_items)} Manual Item(s)")
            title = f"🛒 Shopping List from {' + '.join(title_parts)}"
            
            print_simple_header(title)
            
            # Show selected recipes in a nice panel if any
            if selected_recipes:
                recipes_list = []
                for i, recipe_path in enumerate(selected_recipes, 1):
                    recipes_list.append(f"[dim]{i}.[/dim] [cyan]{recipe_path.stem.replace('-', ' ').title()}[/cyan]")
                
                recipes_text = "\n".join(recipes_list)
                
                console.print(Panel(
                    recipes_text,
                    title="[bold]Selected Recipes[/bold]",
                    border_style="cyan",
                    box=box.ROUNDED
                ))
                console.print()
            
            # Extract ingredients from recipes
            all_ingredients = []
            if selected_recipes:
                for recipe_path in selected_recipes:
                    console.print(f"[blue]📖 Reading: [bold]{recipe_path.name}[/bold][/blue]")
                    ingredients = extract_ingredients_from_recipe(recipe_path)
                    console.print(f"[green]   ✓ Found {len(ingredients)} ingredients[/green]")
                    all_ingredients.extend(ingredients)
            
            # Add manual shopping list items
            if manual_items:
                console.print(f"[blue]📝 Adding {len(manual_items)} manual item(s) from shopping list[/blue]")
                for item in manual_items:
                    # Convert to same format as recipe ingredients
                    all_ingredients.append({
                        'original': item,
                        'searchable': simplify_ingredient_for_search(item)
                    })
            
            # Consolidate
            console.print("\n[yellow]🔄 Consolidating ingredients...[/yellow]")
            unique_ingredients = consolidate_ingredients(all_ingredients)
            console.print(f"[green]   ✓ {len(unique_ingredients)} unique ingredients[/green]")
            
            # Generate URLs
            console.print("\n[magenta bold]🛒 Your Asda Shopping List[/magenta bold]\n")
            
            # Create a nice table for ingredients
            table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
            table.add_column("No", style="dim", width=4)
            table.add_column("Item", style="cyan")
            
            urls = []
            for i, ing in enumerate(unique_ingredients, 1):
                searchable = ing['searchable']
                url = generate_asda_url(searchable)
                urls.append(url)
                table.add_row(f"{i}.", searchable)
            
            console.print(table)
            console.print(f"\n[green bold]✨ Generated {len(urls)} shopping URLs![/green bold]\n")
            
            # Options menu with arrow keys
            action = questionary.select(
                "What would you like to do?",
                choices=[
                    "Open all URLs in browser tabs 🌐",
                    "Open trolley to see your basket 🛒",
                    "Save URLs to a file 💾",
                    "Both URLs + Trolley",
                    Separator(),
                    "← Back to main menu"
                ],
                use_shortcuts=True,
            ).ask()
            
            if action is None or action == "← Back to main menu":
                continue
            
            # Action loop - keep showing options until user goes back
            while action and action != "← Back to main menu":
                if action in ["Open all URLs in browser tabs 🌐", "Both URLs + Trolley"]:
                    # Open trolley FIRST so it's the first tab
                    trolley_url = "https://www.asda.com/groceries/trolley"
                    console.print("\n[magenta]🛒 Opening your Asda trolley (first tab)...[/magenta]")
                    webbrowser.open(trolley_url)
                    time.sleep(1)  # Give it a moment before opening others
                    
                    console.print(f"[cyan]🌐 Opening {len(urls)} item tabs...[/cyan]")
                    console.print("[yellow]   (You may need to allow pop-ups)[/yellow]")
                    
                    for i, url in enumerate(urls):
                        webbrowser.open(url)
                        if i > 0 and i % 5 == 0:
                            console.print(f"[green]   ✓ Opened {i+1}/{len(urls)}...[/green]")
                            time.sleep(1)
                    
                    console.print("[green bold]✅ All tabs opened![/green bold]")
                    console.print("[cyan]💡 Tip: Click 'Add' on each item, then cmd+w to close. Your trolley will be the last tab![/cyan]")
                
                elif action == "Open trolley to see your basket 🛒":
                    trolley_url = "https://www.asda.com/groceries/trolley"
                    console.print("\n[magenta]🛒 Opening your Asda trolley...[/magenta]")
                    time.sleep(0.5)
                    webbrowser.open(trolley_url)
                    console.print("[green]✅ Trolley opened![/green]")
                
                if action in ["Save URLs to a file 💾", "Both URLs + Trolley"]:
                    output_file = script_dir / "shopping_urls.txt"
                    with open(output_file, 'w') as f:
                        f.write("# Asda Shopping URLs\n")
                        f.write(f"# Generated from {len(selected_recipes)} recipe(s)\n\n")
                        f.write("# Trolley: https://www.asda.com/groceries/trolley\n\n")
                        for i, (ing, url) in enumerate(zip(unique_ingredients, urls), 1):
                            f.write(f"{i}. {ing['searchable']}\n")
                            f.write(f"   {url}\n\n")
                    
                    console.print(f"\n[blue]💾 URLs saved to: [bold]{output_file}[/bold][/blue]")
                    console.print("[yellow]   You can open this file and click the links[/yellow]")
                
                # Show options again
                console.print()
                action = questionary.select(
                    "What else would you like to do?",
                    choices=[
                        "Open all URLs in browser tabs 🌐",
                        "Open trolley to see your basket 🛒",
                        "Save URLs to a file 💾",
                        Separator(),
                        "← Back to main menu"
                    ],
                    use_shortcuts=True,
                ).ask()
                
                if action is None:
                    break
        
        elif choice == "Clear selected recipes":
            # Clear selections
            confirm = questionary.confirm(
                f"Clear all {len(selected_recipes)} selected recipes?"
            ).ask()
            
            if confirm:
                selected_recipes.clear()
                console.print("\n[magenta]🗑️  Cleared all selected recipes[/magenta]")
                time.sleep(1)
        
        elif choice and "View shopping list" in choice:
            # View manual shopping list
            clear_screen()
            print_simple_header("📝 Your Shopping List")
            
            items = load_shopping_list(script_dir)
            if items:
                for i, item in enumerate(items, 1):
                    console.print(f"[cyan]{i}. {item}[/cyan]")
                console.print(f"\n[dim]Edit {script_dir / 'shopping_list.md'} to modify[/dim]")
            
            console.print("\n[yellow]Press ENTER to continue...[/yellow]")
            input()
        
        elif choice == "Clear shopping list":
            # Clear manual shopping list
            confirm = questionary.confirm(
                "Clear your shopping list file?"
            ).ask()
            
            if confirm:
                save_shopping_list(script_dir, [])
                console.print("\n[magenta]🗑️  Shopping list cleared[/magenta]")
                time.sleep(1)
        
        elif choice == "Create shopping list file":
            # Create empty shopping list
            shopping_list_file = script_dir / "shopping_list.md"
            if not shopping_list_file.exists():
                save_shopping_list(script_dir, [])
                console.print(f"\n[green]✅ Created {shopping_list_file}[/green]")
                console.print(f"[yellow]Add items to this file - one per line with a dash (-).[/yellow]")
                time.sleep(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[cyan bold]👋 Happy Shopping! See you next time![/cyan bold]\n")
        sys.exit(0)

