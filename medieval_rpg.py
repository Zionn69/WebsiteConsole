import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

class Character:
    def __init__(self, name, character_class):
        self.name = name
        self.character_class = character_class
        self.level = 1
        self.exp = 0
        self.gold = 100
        
        # Base stats based on class
        if character_class == "Knight":
            self.max_hp = 120
            self.hp = 120
            self.strength = 15
            self.defense = 12
            self.agility = 8
        elif character_class == "Archer":
            self.max_hp = 90
            self.hp = 90
            self.strength = 10
            self.defense = 8
            self.agility = 15
        elif character_class == "Mage":
            self.max_hp = 80
            self.hp = 80
            self.strength = 8
            self.defense = 6
            self.agility = 10
            self.mana = 100
            self.max_mana = 100
        
        # Inventory
        self.inventory = {
            "Health Potion": 3,
            "Mana Potion": 2 if character_class == "Mage" else 0,
            "Equipment": []
        }

class Enemy:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.hp = 50 + (level * 10)
        self.max_hp = self.hp
        self.strength = 8 + (level * 2)
        self.defense = 5 + (level * 1)
        self.gold = 20 + (level * 10)
        self.exp = 15 + (level * 5)

class MedievalRPG:
    def __init__(self, parent, player_name):
        self.window = tk.Toplevel(parent)
        self.window.title("Fantasy RPG")
        self.window.geometry("1200x800")
        self.window.configure(bg="#2d4a22")
        
        # Game state
        self.player_name = player_name
        self.character = None
        self.current_enemy = None
        self.in_combat = False
        self.combat_log = []
        
        # Create UI
        self.create_ui()
        
        # Load game if exists, otherwise show character creation
        if self.load_game():
            self.show_game_screen()
        else:
            self.show_character_creation()
    
    def create_ui(self):
        # Main container
        self.main_container = tk.Frame(self.window, bg="#2d4a22")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Character info and stats
        self.left_panel = tk.Frame(self.main_container, bg="#3d5a32", width=300)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Center panel - Main game area/combat
        self.center_panel = tk.Frame(self.main_container, bg="#2d4a22")
        self.center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right panel - Inventory and skills
        self.right_panel = tk.Frame(self.main_container, bg="#3d5a32", width=300)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Title
        self.title_label = tk.Label(
            self.center_panel,
            text="Medieval RPG Adventure",
            font=("Luminari", 32, "bold"),
            bg="#2d4a22",
            fg="#f1c40f"
        )
        self.title_label.pack(pady=20)
    
    def show_character_creation(self):
        # Clear main frame
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Character creation frame
        creation_frame = tk.Frame(self.main_container, bg="#2d4a22")
        creation_frame.pack(pady=50)
        
        # Title
        tk.Label(
            creation_frame,
            text="Create Your Character",
            font=("Luminari", 24),
            bg="#2d4a22",
            fg="#f1c40f"
        ).pack(pady=20)
        
        # Class selection
        tk.Label(
            creation_frame,
            text="Choose Your Class:",
            font=("Luminari", 16),
            bg="#2d4a22",
            fg="#f1c40f"
        ).pack(pady=10)
        
        # Class buttons frame
        class_frame = tk.Frame(creation_frame, bg="#2d4a22")
        class_frame.pack(pady=20)
        
        classes = ["Knight", "Archer", "Mage"]
        class_descriptions = {
            "Knight": "Strong warrior with high HP and defense",
            "Archer": "Agile fighter specializing in ranged combat",
            "Mage": "Powerful spellcaster with magical abilities"
        }
        
        for c in classes:
            btn = tk.Button(
                class_frame,
                text=f"{c}\n{class_descriptions[c]}",
                command=lambda c=c: self.create_character(c),
                font=("Luminari", 12),
                bg="#3d5a32",
                fg="#f1c40f",
                width=30,
                height=3
            )
            btn.pack(pady=5)
    
    def create_character(self, character_class):
        self.character = Character(self.player_name, character_class)
        self.save_game()
        self.show_game_screen()
    
    def show_game_screen(self):
        # Clear panels
        for widget in self.left_panel.winfo_children():
            widget.destroy()
        for widget in self.center_panel.winfo_children():
            widget.destroy()
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        # Left Panel - Character Stats
        self.update_character_stats()
        
        # Center Panel - Game Area
        self.create_game_area()
        
        # Right Panel - Inventory and Skills
        self.update_inventory_and_skills()
    
    def update_character_stats(self):
        # Clear existing widgets in left panel first
        for widget in self.left_panel.winfo_children():
            widget.destroy()
        
        # Character info frame
        char_info = tk.LabelFrame(self.left_panel, text="Character Info", bg="#3d5a32", fg="#f1c40f", font=("Luminari", 12, "bold"))
        char_info.pack(fill=tk.X, padx=5, pady=5)
        
        # Character name and class
        tk.Label(
            char_info,
            text=f"{self.character.name}\nLevel {self.character.level} {self.character.character_class}",
            font=("Luminari", 14, "bold"),
            bg="#3d5a32",
            fg="#f1c40f"
        ).pack(pady=5)
        
        # HP Bar
        hp_frame = tk.Frame(char_info, bg="#3d5a32")
        hp_frame.pack(fill=tk.X, padx=5, pady=2)
        tk.Label(hp_frame, text="HP:", bg="#3d5a32", fg="#f1c40f", font=("Luminari", 10)).pack(side=tk.LEFT)
        hp_bar = ttk.Progressbar(hp_frame, length=150, maximum=self.character.max_hp, value=self.character.hp)
        hp_bar.pack(side=tk.LEFT, padx=5)
        tk.Label(hp_frame, text=f"{self.character.hp}/{self.character.max_hp}", bg="#3d5a32", fg="#f1c40f", font=("Luminari", 10)).pack(side=tk.LEFT)
        
        # Mana Bar (if applicable)
        if hasattr(self.character, 'mana'):
            mana_frame = tk.Frame(char_info, bg="#3d5a32")
            mana_frame.pack(fill=tk.X, padx=5, pady=2)
            tk.Label(mana_frame, text="MP:", bg="#3d5a32", fg="#f1c40f", font=("Luminari", 10)).pack(side=tk.LEFT)
            mana_bar = ttk.Progressbar(mana_frame, length=150, maximum=self.character.max_mana, value=self.character.mana)
            mana_bar.pack(side=tk.LEFT, padx=5)
            tk.Label(mana_frame, text=f"{self.character.mana}/{self.character.max_mana}", bg="#3d5a32", fg="#f1c40f", font=("Luminari", 10)).pack(side=tk.LEFT)
        
        # Stats frame
        stats_frame = tk.LabelFrame(self.left_panel, text="Stats", bg="#3d5a32", fg="#f1c40f", font=("Luminari", 12, "bold"))
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        stats = [
            ("Strength", self.character.strength),
            ("Defense", self.character.defense),
            ("Agility", self.character.agility),
            ("Gold", self.character.gold),
            ("EXP", f"{self.character.exp}/{self.character.level * 100}")
        ]
        
        for stat_name, stat_value in stats:
            stat_frame = tk.Frame(stats_frame, bg="#3d5a32")
            stat_frame.pack(fill=tk.X, padx=5, pady=2)
            tk.Label(stat_frame, text=f"{stat_name}:", bg="#3d5a32", fg="#f1c40f", font=("Luminari", 10)).pack(side=tk.LEFT)
            tk.Label(stat_frame, text=str(stat_value), bg="#3d5a32", fg="#f1c40f", font=("Luminari", 10, "bold")).pack(side=tk.RIGHT)

    def create_game_area(self):
        # Game area frame
        game_area = tk.Frame(self.center_panel, bg="#2d4a22")
        game_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Combat log
        self.combat_log_text = tk.Text(game_area, height=15, width=50, bg="#1a2915", fg="#f1c40f", font=("Luminari", 10))
        self.combat_log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.combat_log_text.insert(tk.END, "Welcome to the Medieval RPG!\n")
        self.combat_log_text.config(state=tk.DISABLED)
        
        # Action buttons
        action_frame = tk.Frame(game_area, bg="#2d4a22")
        action_frame.pack(fill=tk.X, pady=10)
        
        actions = [
            ("Start Combat", self.start_combat),
            ("Visit Shop", self.show_shop),
            ("Save Game", self.save_game)
        ]
        
        for text, command in actions:
            tk.Button(
                action_frame,
                text=text,
                command=command,
                font=("Luminari", 12),
                bg="#4a6a42",
                fg="#f1c40f",
                width=15
            ).pack(side=tk.LEFT, padx=5)

    def update_inventory_and_skills(self):
        # Clear existing widgets in right panel first
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        # Inventory frame
        inventory_frame = tk.LabelFrame(self.right_panel, text="Inventory", bg="#3d5a32", fg="#f1c40f", font=("Luminari", 12, "bold"))
        inventory_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Show potions
        for item, count in self.character.inventory.items():
            if item != "Equipment":  # Skip equipment list
                item_frame = tk.Frame(inventory_frame, bg="#3d5a32")
                item_frame.pack(fill=tk.X, padx=5, pady=2)
                tk.Label(item_frame, text=f"{item}:", bg="#3d5a32", fg="#f1c40f", font=("Luminari", 10)).pack(side=tk.LEFT)
                tk.Label(item_frame, text=str(count), bg="#3d5a32", fg="#f1c40f", font=("Luminari", 10, "bold")).pack(side=tk.RIGHT)
        
        # Skills frame
        skills_frame = tk.LabelFrame(self.right_panel, text="Skills", bg="#3d5a32", fg="#f1c40f", font=("Luminari", 12, "bold"))
        skills_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Class-specific skills
        skills = []
        if self.character.character_class == "Knight":
            skills = ["Shield Bash", "Power Strike", "Defensive Stance"]
        elif self.character.character_class == "Archer":
            skills = ["Quick Shot", "Aimed Shot", "Evasive Maneuver"]
        elif self.character.character_class == "Mage":
            skills = ["Fireball", "Ice Shard", "Arcane Blast"]
        
        for skill in skills:
            skill_button = tk.Button(
                skills_frame,
                text=skill,
                command=lambda s=skill: self.use_skill(s),
                font=("Luminari", 10),
                bg="#4a6a42",
                fg="#f1c40f",
                width=15
            )
            skill_button.pack(pady=2)
            
            # Disable skill buttons if not in combat
            if not self.in_combat:
                skill_button.config(state=tk.DISABLED)

    def use_skill(self, skill_name):
        """Use a character skill in combat."""
        if not self.in_combat:
            self.add_combat_log("You must be in combat to use skills!")
            return
        
        # Check if mage has enough mana
        if self.character.character_class == "Mage" and hasattr(self.character, 'mana'):
            if self.character.mana < 15:
                self.add_combat_log("Not enough mana to use skills!")
                return
            self.character.mana -= 15
        
        # Calculate damage based on skill and class
        damage_multiplier = 1.5  # Base multiplier
        
        if self.character.character_class == "Knight":
            if skill_name == "Shield Bash":
                damage_multiplier = 1.2
                self.add_combat_log("Shield Bash stuns the enemy!")
            elif skill_name == "Power Strike":
                damage_multiplier = 1.8
            elif skill_name == "Defensive Stance":
                self.character.defense += 5
                damage_multiplier = 0.8
                self.add_combat_log("Defensive Stance increases your defense!")
        
        elif self.character.character_class == "Archer":
            if skill_name == "Quick Shot":
                damage_multiplier = 1.3
                self.add_combat_log("Quick Shot hits twice!")
            elif skill_name == "Aimed Shot":
                damage_multiplier = 2.0
            elif skill_name == "Evasive Maneuver":
                self.character.agility += 5
                damage_multiplier = 0.7
                self.add_combat_log("Evasive Maneuver increases your agility!")
        
        elif self.character.character_class == "Mage":
            if skill_name == "Fireball":
                damage_multiplier = 2.2
            elif skill_name == "Ice Shard":
                damage_multiplier = 1.7
                self.add_combat_log("Ice Shard slows the enemy!")
            elif skill_name == "Arcane Blast":
                damage_multiplier = 1.9
        
        # Calculate and apply damage
        base_damage = self.character.strength
        damage = max(1, int(base_damage * damage_multiplier) - self.current_enemy.defense)
        self.current_enemy.hp -= damage
        
        self.add_combat_log(f"You used {skill_name} and dealt {damage} damage!")
        
        # Update enemy HP display
        self.update_enemy_hp()
        
        # Update character stats
        self.update_character_stats()
        
        # Check if enemy is defeated
        if self.current_enemy.hp <= 0:
            self.handle_enemy_defeat()
        else:
            self.enemy_attack()

    def start_combat(self):
        """Start a combat encounter."""
        if self.in_combat:
            return
        
        self.in_combat = True
        
        # Create enemy
        enemy_types = [
            ("Goblin", 1), ("Bandit", 2), ("Wolf", 3),
            ("Skeleton", 4), ("Dark Knight", 5), ("Evil Mage", 6),
            ("Dragon", 7)
        ]
        enemy_type, level = random.choice(enemy_types[:min(self.character.level + 2, len(enemy_types))])
        self.current_enemy = Enemy(enemy_type, level)
        
        # Clear existing combat widgets if any
        for widget in self.center_panel.winfo_children():
            widget.destroy()
        
        # Show combat screen
        self.show_combat_screen()

    def show_combat_screen(self):
        """Display the combat interface."""
        # Combat frame
        combat_frame = tk.Frame(self.center_panel, bg="#2d4a22")
        combat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Enemy info
        self.enemy_frame = tk.LabelFrame(combat_frame, text="Enemy", bg="#3d5a32", fg="#f1c40f", font=("Luminari", 12, "bold"))
        self.enemy_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.enemy_name_label = tk.Label(
            self.enemy_frame,
            text=f"{self.current_enemy.name} (Level {self.current_enemy.level})",
            font=("Luminari", 14, "bold"),
            bg="#3d5a32",
            fg="#f1c40f"
        )
        self.enemy_name_label.pack(pady=5)
        
        # Enemy HP bar
        self.enemy_hp_frame = tk.Frame(self.enemy_frame, bg="#3d5a32")
        self.enemy_hp_frame.pack(fill=tk.X, padx=5, pady=2)
        tk.Label(self.enemy_hp_frame, text="HP:", bg="#3d5a32", fg="#f1c40f", font=("Luminari", 10)).pack(side=tk.LEFT)
        self.enemy_hp_bar = ttk.Progressbar(self.enemy_hp_frame, length=200, maximum=self.current_enemy.max_hp, value=self.current_enemy.hp)
        self.enemy_hp_bar.pack(side=tk.LEFT, padx=5)
        self.enemy_hp_label = tk.Label(self.enemy_hp_frame, text=f"{self.current_enemy.hp}/{self.current_enemy.max_hp}", bg="#3d5a32", fg="#f1c40f", font=("Luminari", 10))
        self.enemy_hp_label.pack(side=tk.LEFT)
        
        # Combat log
        log_frame = tk.Frame(combat_frame, bg="#2d4a22")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.combat_log_text = tk.Text(log_frame, height=10, width=50, bg="#1a2915", fg="#f1c40f", font=("Luminari", 10))
        self.combat_log_text.pack(fill=tk.BOTH, expand=True)
        self.combat_log_text.insert(tk.END, f"A {self.current_enemy.name} appears!\n")
        self.combat_log_text.see(tk.END)
        
        # Action buttons
        button_frame = tk.Frame(combat_frame, bg="#2d4a22")
        button_frame.pack(fill=tk.X, pady=10)
        
        # Attack button
        tk.Button(
            button_frame,
            text="Attack",
            command=self.attack_enemy,
            font=("Luminari", 12),
            bg="#3d5a32",
            fg="#f1c40f",
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Use potion button
        tk.Button(
            button_frame,
            text="Use Potion",
            command=self.use_potion,
            font=("Luminari", 12),
            bg="#3d5a32",
            fg="#f1c40f",
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Flee button
        tk.Button(
            button_frame,
            text="Flee",
            command=self.flee_combat,
            font=("Luminari", 12),
            bg="#3d5a32",
            fg="#f1c40f",
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Update character stats and inventory/skills
        self.update_character_stats()
        self.update_inventory_and_skills()

    def update_enemy_hp(self):
        """Update the enemy HP display."""
        if hasattr(self, 'enemy_hp_bar') and self.enemy_hp_bar.winfo_exists():
            self.enemy_hp_bar['value'] = self.current_enemy.hp
            self.enemy_hp_label.config(text=f"{self.current_enemy.hp}/{self.current_enemy.max_hp}")
            self.enemy_hp_bar.update()

    def add_combat_log(self, message):
        """Add a message to the combat log."""
        if hasattr(self, 'combat_log_text') and self.combat_log_text.winfo_exists():
            self.combat_log_text.config(state=tk.NORMAL)
            self.combat_log_text.insert(tk.END, message + "\n")
            self.combat_log_text.see(tk.END)
            self.combat_log_text.config(state=tk.DISABLED)
            self.combat_log_text.update()

    def attack_enemy(self):
        """Handle player's attack."""
        if not self.in_combat:
            return
            
        # Calculate damage
        damage = max(1, self.character.strength - self.current_enemy.defense)
        self.current_enemy.hp -= damage
        
        # Log the attack
        self.add_combat_log(f"You attack the {self.current_enemy.name} for {damage} damage!")
        
        # Update enemy HP display
        self.update_enemy_hp()
        
        # Check if enemy is defeated
        if self.current_enemy.hp <= 0:
            self.handle_enemy_defeat()
        else:
            self.enemy_attack()

    def magic_attack(self):
        """Handle mage's magic attack."""
        if not self.in_combat or self.character.character_class != "Mage":
            return
        
        if self.character.mana < 20:
            self.add_combat_log("Not enough mana!")
            return
        
        # Use mana and calculate damage
        self.character.mana -= 20
        damage = max(1, int(self.character.strength * 2) - self.current_enemy.defense)
        self.current_enemy.hp -= damage
        
        # Log the attack
        self.add_combat_log(f"You cast a spell at the {self.current_enemy.name} for {damage} damage!")
        
        # Update enemy HP display
        self.update_enemy_hp()
        
        # Update character stats
        self.update_character_stats()
        
        # Check if enemy is defeated
        if self.current_enemy.hp <= 0:
            self.handle_enemy_defeat()
        else:
            self.enemy_attack()

    def enemy_attack(self):
        """Handle enemy's attack."""
        damage = max(1, self.current_enemy.strength - self.character.defense)
        self.character.hp -= damage
        
        # Log the attack
        self.add_combat_log(f"The {self.current_enemy.name} attacks you for {damage} damage!")
        
        # Update character stats
        self.update_character_stats()
        
        # Check if player is defeated
        if self.character.hp <= 0:
            self.handle_player_defeat()

    def handle_enemy_defeat(self):
        """Handle enemy defeat and rewards."""
        self.add_combat_log(f"You defeated the {self.current_enemy.name}!")
        
        # Award gold and experience
        self.character.gold += self.current_enemy.gold
        self.character.exp += self.current_enemy.exp
        
        self.add_combat_log(f"You gained {self.current_enemy.gold} gold and {self.current_enemy.exp} experience!")
        
        # Check for level up
        if self.character.exp >= self.character.level * 100:
            self.level_up()
        
        # End combat
        self.in_combat = False
        self.current_enemy = None
        
        # Save game
        self.save_game()
        
        # Return to game screen after a short delay
        self.window.after(2000, self.show_game_screen)

    def handle_player_defeat(self):
        """Handle player defeat."""
        self.add_combat_log("You have been defeated!")
        
        # Lose some gold
        gold_loss = min(self.character.gold, int(self.character.gold * 0.1))
        self.character.gold -= gold_loss
        
        # Restore some HP
        self.character.hp = max(1, int(self.character.max_hp * 0.5))
        
        if gold_loss > 0:
            self.add_combat_log(f"You lost {gold_loss} gold...")
        
        # End combat
        self.in_combat = False
        self.current_enemy = None
        
        # Save game
        self.save_game()
        
        # Return to game screen after a short delay
        self.window.after(2000, self.show_game_screen)

    def use_potion(self):
        if self.character.inventory["Health Potion"] <= 0:
            self.add_combat_log("No Health Potions left!")
            return
        
        self.character.inventory["Health Potion"] -= 1
        
        heal_amount = 50
        self.character.hp = min(self.character.max_hp, self.character.hp + heal_amount)
        self.add_combat_log(f"You used a Health Potion and recovered {heal_amount} HP!")
        
        self.update_character_stats()
    
    def flee_combat(self):
        """Attempt to flee from combat."""
        if not self.in_combat:
            return
        
        # 50% chance to flee successfully
        if random.random() < 0.5:
            self.add_combat_log("You successfully fled from combat!")
            self.in_combat = False
            self.current_enemy = None
            self.window.after(1500, self.show_game_screen)
        else:
            self.add_combat_log("Failed to flee!")
            self.enemy_attack()
    
    def level_up(self):
        """Handle character level up."""
        self.character.level += 1
        self.character.exp = 0
        
        # Increase stats
        self.character.max_hp += 10
        self.character.hp = self.character.max_hp
        self.character.strength += 2
        self.character.defense += 2
        self.character.agility += 2
        
        if hasattr(self.character, 'mana'):
            self.character.max_mana += 10
            self.character.mana = self.character.max_mana
        
        self.add_combat_log(f"Level Up! You are now level {self.character.level}!")
        self.add_combat_log("Your stats have increased!")
        
        # Update display
        self.update_character_stats()

    def show_shop(self):
        shop_window = tk.Toplevel(self.window)
        shop_window.title("Shop")
        shop_window.geometry("400x500")
        shop_window.configure(bg="#2d4a22")
        
        tk.Label(
            shop_window,
            text="Shop",
            font=("Luminari", 24, "bold"),
            bg="#2d4a22",
            fg="#f1c40f"
        ).pack(pady=20)
        
        items = {
            "Health Potion": 50,
            "Mana Potion": 75
        }
        
        for item, price in items.items():
            if item == "Mana Potion" and self.character.character_class != "Mage":
                continue
                
            frame = tk.Frame(shop_window, bg="#3d5a32", relief=tk.RIDGE, bd=2)
            frame.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(
                frame,
                text=f"{item} - {price} gold",
                font=("Luminari", 12),
                bg="#3d5a32",
                fg="#f1c40f"
            ).pack(side=tk.LEFT, padx=10)
            
            tk.Button(
                frame,
                text="Buy",
                command=lambda i=item, p=price: self.buy_item(i, p),
                font=("Luminari", 12),
                bg="#4a6a42",
                fg="#f1c40f"
            ).pack(side=tk.RIGHT, padx=10)
    
    def buy_item(self, item, price):
        if self.character.gold >= price:
            self.character.gold -= price
            self.character.inventory[item] += 1
            messagebox.showinfo("Shop", f"You bought 1 {item}!")
            self.save_game()
            self.show_game_screen()
        else:
            messagebox.showinfo("Shop", "Not enough gold!")
    
    def save_game(self):
        save_data = {
            "name": self.character.name,
            "class": self.character.character_class,
            "level": self.character.level,
            "exp": self.character.exp,
            "hp": self.character.hp,
            "max_hp": self.character.max_hp,
            "strength": self.character.strength,
            "defense": self.character.defense,
            "agility": self.character.agility,
            "gold": self.character.gold,
            "inventory": self.character.inventory
        }
        
        if hasattr(self.character, 'mana'):
            save_data["mana"] = self.character.mana
            save_data["max_mana"] = self.character.max_mana
        
        save_file = f"medieval_rpg_{self.player_name.lower()}.json"
        with open(save_file, "w") as f:
            json.dump(save_data, f)
        
        messagebox.showinfo("Save", "Game saved successfully!")
    
    def load_game(self):
        save_file = f"medieval_rpg_{self.player_name.lower()}.json"
        if not os.path.exists(save_file):
            return False
        
        try:
            with open(save_file, "r") as f:
                save_data = json.load(f)
            
            self.character = Character(save_data["name"], save_data["class"])
            self.character.level = save_data["level"]
            self.character.exp = save_data["exp"]
            self.character.hp = save_data["hp"]
            self.character.max_hp = save_data["max_hp"]
            self.character.strength = save_data["strength"]
            self.character.defense = save_data["defense"]
            self.character.agility = save_data["agility"]
            self.character.gold = save_data["gold"]
            self.character.inventory = save_data["inventory"]
            
            if "mana" in save_data:
                self.character.mana = save_data["mana"]
                self.character.max_mana = save_data["max_mana"]
            
            return True
        except:
            return False 